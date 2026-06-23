from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db import repositories
from app.providers.odds_api.schemas import OddsApiPayload, PROVIDER


class OddsApiError(RuntimeError):
    pass


class OddsApiClient:
    def __init__(self, settings: Settings, db: Session):
        self.settings = settings
        self.db = db
        self.requests_used = 0

    def get_odds(self, sport_key: str) -> OddsApiPayload:
        if not self.settings.odds_api_key:
            raise OddsApiError("ODDS_API_KEY nao configurada.")
        endpoint = f"sports/{sport_key}/odds"
        params = {
            "apiKey": self.settings.odds_api_key,
            "regions": self.settings.odds_api_regions,
            "markets": self.settings.odds_api_markets,
            "oddsFormat": self.settings.odds_api_odds_format,
            "dateFormat": self.settings.odds_api_date_format,
        }
        url = f"{self.settings.odds_api_base_url.rstrip('/')}/{endpoint}"
        try:
            response = httpx.get(url, params=params, timeout=self.settings.odds_api_timeout_seconds)
            self.requests_used += 1
            try:
                data = response.json()
            except ValueError:
                data = {"raw_text": response.text}
            raw = repositories.save_raw_api_payload(
                self.db,
                provider=PROVIDER,
                endpoint=endpoint,
                request_method="GET",
                request_params=params,
                response_status=response.status_code,
                raw_payload=data if isinstance(data, dict) else {"response": data},
                source_timestamp=datetime.now(timezone.utc),
                cost_estimate=1.0,
                error_message=None if response.is_success else self._error_message(response.status_code, data),
            )
            self.db.commit()
            if not response.is_success:
                raise OddsApiError(self._error_message(response.status_code, data))
            return OddsApiPayload(endpoint=endpoint, params=params, status_code=response.status_code, data=data, raw_payload_id=raw.id)
        except httpx.HTTPError as exc:
            raw = repositories.save_raw_api_payload(
                self.db,
                provider=PROVIDER,
                endpoint=endpoint,
                request_method="GET",
                request_params=params,
                response_status=None,
                raw_payload={"error": exc.__class__.__name__},
                error_message=str(exc),
            )
            self.db.commit()
            raise OddsApiError(f"Falha ao chamar The Odds API: {exc.__class__.__name__}.") from exc

    @staticmethod
    def _error_message(status_code: int, data) -> str:
        if status_code == 401:
            return "The Odds API recusou a chave informada."
        if status_code == 429:
            return "Quota ou rate limit da The Odds API atingido."
        if isinstance(data, dict):
            message = data.get("message") or data.get("error") or data.get("details")
            if message:
                return str(message)
        return f"The Odds API retornou HTTP {status_code}."
