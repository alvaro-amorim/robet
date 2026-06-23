from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db import repositories
from app.providers.football_api.client import ApiFootballClient, RequestBudget
from app.providers.football_api.mapper import map_fixture_item, map_league_item
from app.providers.football_api.schemas import PROVIDER, SyncSummary


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
        competitions = repositories.list_competitions(self.db, provider=PROVIDER, name_contains="World Cup")
        if not competitions:
            summary.warnings.append("Nenhuma competição World Cup sincronizada ainda. Rode /sync/football/competitions primeiro.")
            return summary.as_dict()
        for competition in competitions:
            before_ids = {match.id for match in repositories.list_matches(self.db, only_real=True)}
            payload = self.client.get("fixtures", {"league": competition.external_id, "season": competition.season})
            summary.raw_payloads_saved += 1
            for item in payload.data.get("response", []):
                match = map_fixture_item(self.db, item, payload.raw_payload_id)
                if match.id in before_ids:
                    summary.matches_updated += 1
                else:
                    summary.matches_created += 1
            self.db.commit()
        summary.requests_used = self.requests_used
        return summary.as_dict()

    def sync_results(self) -> dict:
        summary = SyncSummary()
        competitions = repositories.list_competitions(self.db, provider=PROVIDER, name_contains="World Cup")
        if not competitions:
            summary.warnings.append("Nenhuma competição World Cup sincronizada ainda. Rode /sync/football/competitions primeiro.")
            return summary.as_dict()
        for competition in competitions:
            payload = self.client.get("fixtures", {"league": competition.external_id, "season": competition.season})
            summary.raw_payloads_saved += 1
            for item in payload.data.get("response", []):
                match = map_fixture_item(self.db, item, payload.raw_payload_id)
                summary.matches_updated += 1 if match.id else 0
            self.db.commit()
        summary.requests_used = self.requests_used
        return summary.as_dict()
