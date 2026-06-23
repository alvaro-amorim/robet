from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


PROVIDER = "the_odds_api"


@dataclass
class OddsApiPayload:
    endpoint: str
    params: dict[str, Any]
    status_code: int | None
    data: list[dict[str, Any]] | dict[str, Any]
    raw_payload_id: str
    error_message: str | None = None


@dataclass
class OutcomeQuote:
    odds_event_id: str
    match_id: str | None
    bookmaker_id: str
    bookmaker_title: str
    market_id: str
    market_key: str
    selection_name: str
    odd_decimal: float
    point: float | None
    implied_probability: float
    captured_at: datetime
    source_last_update: datetime | None


@dataclass
class OddsSyncSummary:
    provider: str = PROVIDER
    sport_key: str = ""
    requests_used: int = 0
    events_received: int = 0
    odds_events_created: int = 0
    odds_events_updated: int = 0
    odds_snapshots_saved: int = 0
    market_summaries_created: int = 0
    linked_to_matches: int = 0
    unlinked_events: int = 0
    raw_payloads_saved: int = 0
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "provider": self.provider,
            "sport_key": self.sport_key,
            "requests_used": self.requests_used,
            "events_received": self.events_received,
            "odds_events_created": self.odds_events_created,
            "odds_events_updated": self.odds_events_updated,
            "odds_snapshots_saved": self.odds_snapshots_saved,
            "market_summaries_created": self.market_summaries_created,
            "linked_to_matches": self.linked_to_matches,
            "unlinked_events": self.unlinked_events,
            "raw_payloads_saved": self.raw_payloads_saved,
            "warnings": self.warnings,
        }
