from dataclasses import dataclass, field
from typing import Any


PROVIDER = "api_football"


@dataclass
class ApiFootballPayload:
    endpoint: str
    params: dict[str, Any]
    status_code: int | None
    data: dict[str, Any]
    raw_payload_id: str
    error_message: str | None = None


@dataclass
class SyncSummary:
    provider: str = PROVIDER
    mode: str = "real_sync"
    requests_used: int = 0
    competitions_found: int = 0
    competitions_saved: int = 0
    matches_created: int = 0
    matches_updated: int = 0
    raw_payloads_saved: int = 0
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "provider": self.provider,
            "mode": self.mode,
            "requests_used": self.requests_used,
            "competitions_found": self.competitions_found,
            "competitions_saved": self.competitions_saved,
            "matches_created": self.matches_created,
            "matches_updated": self.matches_updated,
            "raw_payloads_saved": self.raw_payloads_saved,
            "warnings": self.warnings,
        }
