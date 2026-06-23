from datetime import datetime, time, timezone
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db import repositories
from app.providers.football_api.schemas import ApiFootballPayload, PROVIDER


class ApiFootballError(RuntimeError):
    pass


class RequestBudget:
    def __init__(self, max_requests: int):
        self.max_requests = max_requests
        self.used = 0

    def consume(self) -> None:
        if self.used >= self.max_requests:
            raise ApiFootballError(f"Limite de requests por execução atingido: {self.max_requests}.")
        self.used += 1


class ApiFootballClient:
    def __init__(self, settings: Settings, db: Session, budget: RequestBudget):
        self.settings = settings
        self.db = db
        self.budget = budget

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> ApiFootballPayload:
        if not self.settings.football_api_key:
            raise ApiFootballError("FOOTBALL_API_KEY não configurada.")

        start_of_day = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)
        used_today = repositories.count_raw_api_payloads_since(self.db, PROVIDER, start_of_day)
        if used_today >= self.settings.football_api_daily_request_limit:
            raise ApiFootballError(f"Limite diário da API-Football atingido: {self.settings.football_api_daily_request_limit}.")

        self.budget.consume()
        request_params = params or {}
        url = f"{self.settings.football_api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = httpx.get(
                url,
                params=request_params,
                headers={"x-apisports-key": self.settings.football_api_key},
                timeout=self.settings.football_api_timeout_seconds,
            )
            payload = response.json()
            raw = repositories.save_raw_api_payload(
                self.db,
                provider=PROVIDER,
                endpoint=endpoint,
                request_method="GET",
                request_params=request_params,
                response_status=response.status_code,
                raw_payload=payload,
                cost_estimate=1.0,
                error_message=None if response.is_success else f"HTTP {response.status_code}",
            )
            self.db.commit()
            if not response.is_success:
                raise ApiFootballError(f"API-Football retornou HTTP {response.status_code}.")
            return ApiFootballPayload(endpoint=endpoint, params=request_params, status_code=response.status_code, data=payload, raw_payload_id=raw.id)
        except httpx.HTTPError as exc:
            raw = repositories.save_raw_api_payload(
                self.db,
                provider=PROVIDER,
                endpoint=endpoint,
                request_method="GET",
                request_params=request_params,
                response_status=None,
                raw_payload={"error": exc.__class__.__name__},
                cost_estimate=1.0,
                error_message=str(exc),
            )
            self.db.commit()
            return ApiFootballPayload(endpoint=endpoint, params=request_params, status_code=None, data={"response": []}, raw_payload_id=raw.id, error_message=str(exc))
