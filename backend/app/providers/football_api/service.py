from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db import repositories
from app.db.base import CompetitionModel
from app.providers.football_api.client import ApiFootballClient, RequestBudget
from app.providers.football_api.mapper import map_fixture_item, map_league_item
from app.providers.football_api.schemas import PROVIDER, SyncSummary


EXCLUDED_WORLD_CUP_TERMS = (
    "qualification",
    "qualifiers",
    "women",
    "u17",
    "u20",
    "u21",
    "club",
    "beach",
    "futsal",
)


class FootballSyncService:
    def __init__(self, settings: Settings, db: Session, client: ApiFootballClient | None = None):
        self.settings = settings
        self.db = db
        self.budget = RequestBudget(settings.football_sync_max_requests_per_run)
        self.client = client or ApiFootballClient(settings, db, self.budget)

    @property
    def requests_used(self) -> int:
        return self.budget.used

    def sync_competitions(self) -> dict:
        summary = SyncSummary()
        seen: set[tuple[str, int]] = set()
        for term in self.settings.football_world_cup_search_term_list:
            payload = self.client.get("leagues", {"search": term})
            summary.raw_payloads_saved += 1
            for item in payload.data.get("response", []):
                competition = map_league_item(self.db, item, self.settings.football_default_season)
                key = (competition.external_id, competition.season)
                if key not in seen:
                    summary.competitions_found += 1
                    summary.competitions_saved += 1
                    seen.add(key)
            self.db.commit()
        summary.requests_used = self.requests_used
        return summary.as_dict()

    def sync_world_cup_fixtures(self) -> dict:
        summary = SyncSummary()
        competition = self._select_world_cup_competition(summary)
        if competition is None:
            return summary.as_dict()

        before_ids = {match.id for match in repositories.list_matches(self.db, only_real=True)}
        payload = self._get_fixtures_payload(competition, summary)
        for item in payload.data.get("response", []):
            if not self._fixture_external_id(item):
                summary.warnings.append("Fixture ignorada porque veio sem fixture.id na API-Football.")
                continue
            match = map_fixture_item(self.db, item, payload.raw_payload_id)
            if match.id in before_ids:
                summary.matches_updated += 1
            else:
                summary.matches_created += 1
                before_ids.add(match.id)
        self.db.commit()
        summary.requests_used = self.requests_used
        return summary.as_dict()

    def sync_results(self) -> dict:
        summary = SyncSummary()
        existing_matches = repositories.list_matches(self.db, only_real=True)
        if not existing_matches:
            summary.warnings.append("Nenhuma fixture real persistida ainda. Rode /sync/football/world-cup-fixtures primeiro.")
            return summary.as_dict()

        competition = self._select_world_cup_competition(summary)
        if competition is None:
            return summary.as_dict()

        persisted_ids = {match.id for match in existing_matches}
        payload = self._get_fixtures_payload(competition, summary)
        for item in payload.data.get("response", []):
            if not self._fixture_external_id(item):
                summary.warnings.append("Resultado ignorado porque a fixture veio sem fixture.id na API-Football.")
                continue
            match = map_fixture_item(self.db, item, payload.raw_payload_id)
            if match.id in persisted_ids:
                summary.matches_updated += 1
        self.db.commit()
        summary.requests_used = self.requests_used
        return summary.as_dict()

    def _select_world_cup_competition(self, summary: SyncSummary) -> CompetitionModel | None:
        competitions = [
            competition
            for competition in repositories.list_competitions(self.db, provider=PROVIDER)
            if competition.season == self.settings.football_default_season and "world cup" in competition.name.lower()
        ]
        if not competitions:
            summary.warnings.append("Nenhuma competicao World Cup 2026 sincronizada ainda. Rode /sync/football/competitions primeiro.")
            return None

        ranked = sorted(
            ((self._world_cup_score(competition), competition) for competition in competitions),
            key=lambda item: (-item[0], self._stable_external_id(item[1]), item[1].name),
        )
        selected_score, selected = ranked[0]
        if selected_score <= 0:
            summary.warnings.append("Nao foi possivel identificar com seguranca a competicao World Cup 2026 para fixtures.")
            return None
        if len(competitions) > 1:
            summary.warnings.append(
                f"{len(competitions)} competicoes World Cup 2026 candidatas encontradas; usando {selected.name} "
                f"(external_id={selected.external_id}, country={selected.country or 'unknown'})."
            )
        return selected

    def _get_fixtures_payload(self, competition: CompetitionModel, summary: SyncSummary):
        last_payload = None
        for season in self._fixture_season_candidates(competition):
            payload = self.client.get("fixtures", {"league": competition.external_id, "season": season})
            summary.raw_payloads_saved += 1
            last_payload = payload
            response = payload.data.get("response", [])
            errors = payload.data.get("errors") or {}
            if response:
                if season != competition.season:
                    summary.warnings.append(
                        f"API-Football nao retornou fixtures para {competition.season}; usando temporada {season} como fallback real persistido."
                    )
                return payload
            if errors:
                summary.warnings.append(f"API-Football retornou erro para fixtures {competition.name} {season}: {errors}.")
                continue
            if season == competition.season:
                summary.warnings.append(f"API-Football retornou 0 fixtures para {competition.name} {season}.")
        return last_payload

    def _fixture_season_candidates(self, competition: CompetitionModel) -> list[int]:
        seasons = [competition.season]
        if competition.name.lower() == "world cup" and 2022 not in seasons:
            seasons.append(2022)
        return seasons

    @staticmethod
    def _world_cup_score(competition: CompetitionModel) -> int:
        name = competition.name.lower()
        score = 0
        if name == "world cup":
            score += 100
        elif "world cup" in name:
            score += 40
        if competition.country and competition.country.lower() == "world":
            score += 25
        if competition.type and competition.type.lower() == "cup":
            score += 15
        if competition.is_active:
            score += 5
        if any(term in name for term in EXCLUDED_WORLD_CUP_TERMS):
            score -= 100
        return score

    @staticmethod
    def _stable_external_id(competition: CompetitionModel) -> int:
        try:
            return int(competition.external_id)
        except (TypeError, ValueError):
            return 10**9

    @staticmethod
    def _fixture_external_id(item: dict) -> object | None:
        fixture = item.get("fixture") or {}
        return fixture.get("id")
