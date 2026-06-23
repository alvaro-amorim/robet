from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db import repositories
from app.db.base import MatchModel, OddsEventModel
from app.domain.normalization.team import normalize_team_name
from app.providers.odds_api.client import OddsApiClient
from app.providers.odds_api.mapper import (
    build_market_summaries,
    event_response_items,
    implied_probability,
    market_display_name,
    parse_datetime,
)
from app.providers.odds_api.schemas import OutcomeQuote, OddsSyncSummary, PROVIDER


class OddsSyncService:
    def __init__(self, settings: Settings, db: Session, client: OddsApiClient | None = None):
        self.settings = settings
        self.db = db
        self.client = client or OddsApiClient(settings, db)

    def sync_world_cup(self) -> dict:
        summary = OddsSyncSummary(sport_key=self.settings.odds_primary_sport_key)
        payload = self.client.get_odds(self.settings.odds_primary_sport_key)
        summary.requests_used = self.client.requests_used
        summary.raw_payloads_saved = 1
        items = event_response_items(payload.data)
        summary.events_received = len(items)

        fallback_years = self._real_match_years()
        event_years: set[int] = set()
        for item in items:
            event, was_created = self._upsert_event(item, payload.raw_payload_id)
            event_years.add(event.commence_time.year)
            if was_created:
                summary.odds_events_created += 1
            else:
                summary.odds_events_updated += 1
            if event.linked_match_id:
                summary.linked_to_matches += 1
            else:
                summary.unlinked_events += 1
            quotes = self._save_quotes(event, item, payload.raw_payload_id)
            summary.odds_snapshots_saved += len(quotes)
            for market_summary in build_market_summaries(event, quotes):
                repositories.save_odds_market_summary(self.db, **market_summary)
                summary.market_summaries_created += 1
        if fallback_years and event_years and fallback_years.isdisjoint(event_years) and summary.unlinked_events:
            summary.warnings.append(
                "Odds events foram salvos sem vinculo com API-Football porque os dados reais de futebol persistidos sao de outra temporada."
            )
        self.db.commit()
        return summary.as_dict()

    def _upsert_event(self, item: dict, raw_payload_id: str):
        external_id = str(item.get("id"))
        sport_key = item.get("sport_key") or self.settings.odds_primary_sport_key
        existing = self.db.get(OddsEventModel, f"odds_event_{PROVIDER}_{sport_key}_{external_id}")
        commence_time = parse_datetime(item.get("commence_time"))
        linked_match_id, confidence = self._match_event(item.get("home_team") or "", item.get("away_team") or "", commence_time)
        event = repositories.upsert_odds_event(
            self.db,
            provider=PROVIDER,
            external_event_id=external_id,
            sport_key=sport_key,
            sport_title=item.get("sport_title"),
            commence_time=commence_time,
            home_team=item.get("home_team") or "Unknown home team",
            away_team=item.get("away_team") or "Unknown away team",
            normalized_home_team=normalize_team_name(item.get("home_team") or "Unknown home team"),
            normalized_away_team=normalize_team_name(item.get("away_team") or "Unknown away team"),
            raw_payload_id=raw_payload_id,
            linked_match_id=linked_match_id,
            match_link_confidence=confidence,
        )
        self.db.flush()
        return event, existing is None

    def _save_quotes(self, event, item: dict, raw_payload_id: str) -> list[OutcomeQuote]:
        quotes: list[OutcomeQuote] = []
        captured_at = repositories.utcnow()
        for bookmaker_item in item.get("bookmakers", []) or []:
            bookmaker = repositories.upsert_bookmaker(
                self.db,
                provider=PROVIDER,
                external_key=bookmaker_item.get("key") or "unknown",
                title=bookmaker_item.get("title") or bookmaker_item.get("key") or "Unknown bookmaker",
            )
            source_last_update = parse_datetime(bookmaker_item.get("last_update")) if bookmaker_item.get("last_update") else None
            for market_item in bookmaker_item.get("markets", []) or []:
                market_key = market_item.get("key") or "unknown"
                market = repositories.upsert_market(self.db, market_key, market_display_name(market_key))
                for outcome in market_item.get("outcomes", []) or []:
                    price = float(outcome.get("price"))
                    point = outcome.get("point")
                    point = float(point) if point is not None else None
                    probability = implied_probability(price)
                    repositories.save_real_odds_snapshot(
                        self.db,
                        odds_event_id=event.id,
                        match_id=event.linked_match_id,
                        raw_payload_id=raw_payload_id,
                        bookmaker_id=bookmaker.id,
                        bookmaker_title=bookmaker.title,
                        market_id=market.id,
                        market_key=market.key,
                        selection_name=outcome.get("name") or "Unknown selection",
                        odd_decimal=price,
                        point=point,
                        implied_probability=probability,
                        captured_at=captured_at,
                        source_last_update=source_last_update,
                    )
                    quotes.append(
                        OutcomeQuote(
                            odds_event_id=event.id,
                            match_id=event.linked_match_id,
                            bookmaker_id=bookmaker.id,
                            bookmaker_title=bookmaker.title,
                            market_id=market.id,
                            market_key=market.key,
                            selection_name=outcome.get("name") or "Unknown selection",
                            odd_decimal=price,
                            point=point,
                            implied_probability=probability,
                            captured_at=captured_at,
                            source_last_update=source_last_update,
                        )
                    )
        return quotes

    def _match_event(self, home_team: str, away_team: str, commence_time) -> tuple[str | None, float]:
        normalized_home = normalize_team_name(home_team)
        normalized_away = normalize_team_name(away_team)
        rows = self.db.query(MatchModel).filter(MatchModel.external_provider.is_not(None)).all()
        for row in rows:
            same_teams = normalize_team_name(row.home_team) == normalized_home and normalize_team_name(row.away_team) == normalized_away
            same_year = row.commence_time.year == commence_time.year
            time_delta_hours = abs((row.commence_time - commence_time).total_seconds()) / 3600
            if same_teams and same_year and time_delta_hours <= 4:
                return row.id, 0.95
        return None, 0.0

    def _real_match_years(self) -> set[int]:
        return {match.commence_time.year for match in repositories.list_matches(self.db, only_real=True)}
