from datetime import datetime, timezone

import pytest

from app.core.config import Settings
from app.db import repositories
from app.db.base import CompetitionModel, MatchModel, RawApiPayloadModel, TeamAliasModel, TeamModel
from app.domain.normalization.team import normalize_team_name
from app.providers.football_api.client import ApiFootballError, RequestBudget
from app.providers.football_api.mapper import map_fixture_item
from app.providers.football_api.schemas import ApiFootballPayload
from app.providers.football_api.service import FootballSyncService


def test_sanitize_request_params_removes_api_key():
    sanitized = repositories.sanitize_request_params({"search": "world cup", "api_key": "secret", "token": "hidden"})
    assert sanitized["search"] == "world cup"
    assert sanitized["api_key"] == "[REDACTED]"
    assert sanitized["token"] == "[REDACTED]"


def test_payload_hash_is_stable():
    first = repositories.calculate_payload_hash({"b": 2, "a": 1})
    second = repositories.calculate_payload_hash({"a": 1, "b": 2})
    assert first == second


def test_raw_api_payload_repository(db_session):
    raw = repositories.save_raw_api_payload(
        db_session,
        provider="api_football",
        endpoint="leagues",
        request_method="GET",
        request_params={"search": "world cup", "x-apisports-key": "secret"},
        response_status=200,
        raw_payload={"response": []},
    )
    db_session.commit()
    saved = db_session.get(RawApiPayloadModel, raw.id)
    assert saved is not None
    assert saved.request_params_json["x-apisports-key"] == "[REDACTED]"
    assert saved.payload_hash


def test_team_normalization_simple_aliases():
    assert normalize_team_name("Brazil") == "brazil"
    assert normalize_team_name("Brasil") == "brazil"
    assert normalize_team_name("BRA") == "brazil"
    assert normalize_team_name("Brazil National Team") == "brazil"


def test_upsert_competition_team_and_alias(db_session):
    competition = repositories.upsert_competition(db_session, "api_football", "1", "World Cup", "World", 2026, "Cup", True)
    team = repositories.upsert_team(db_session, "Brasil", "Brazil")
    alias = repositories.upsert_team_alias(db_session, team.id, "api_football", "6", "Brazil")
    db_session.commit()
    assert db_session.get(CompetitionModel, competition.id) is not None
    assert db_session.get(TeamModel, team.id).normalized_name == "brazil"
    assert db_session.get(TeamAliasModel, alias.id).team_id == team.id


def test_upsert_real_match_from_fixture(db_session):
    raw = repositories.save_raw_api_payload(
        db_session,
        provider="api_football",
        endpoint="fixtures",
        request_method="GET",
        request_params={"league": 1, "season": 2026},
        response_status=200,
        raw_payload={"response": []},
    )
    fixture = {
        "fixture": {"id": 99, "date": "2026-06-14T16:00:00+00:00", "status": {"short": "FT"}},
        "league": {"id": 1, "name": "World Cup", "country": "World", "season": 2026},
        "teams": {"home": {"id": 6, "name": "Brazil"}, "away": {"id": 7, "name": "Scotland"}},
        "goals": {"home": 2, "away": 1},
    }
    match = map_fixture_item(db_session, fixture, raw.id)
    db_session.commit()
    saved = db_session.get(MatchModel, match.id)
    assert saved.external_provider == "api_football"
    assert saved.home_score == 2
    assert saved.away_score == 1
    assert saved.raw_payload_id == raw.id


class FakeFootballClient:
    def __init__(self):
        self.calls = []

    def get(self, endpoint, params=None):
        self.calls.append((endpoint, params or {}))
        if endpoint == "leagues":
            return ApiFootballPayload(
                endpoint=endpoint,
                params=params or {},
                status_code=200,
                raw_payload_id="raw_fake_leagues",
                data={
                    "response": [
                        {
                            "league": {"id": 1, "name": "World Cup", "type": "Cup"},
                            "country": {"name": "World"},
                            "seasons": [{"year": 2026, "current": True}],
                        }
                    ]
                },
            )
        return ApiFootballPayload(
            endpoint=endpoint,
            params=params or {},
            status_code=200,
            raw_payload_id="raw_fake_fixtures",
            data={
                "response": [
                    {
                        "fixture": {"id": 99, "date": "2026-06-14T16:00:00+00:00", "status": {"short": "NS"}},
                        "league": {"id": 1, "name": "World Cup", "country": "World", "season": 2026},
                        "teams": {"home": {"id": 6, "name": "Brazil"}, "away": {"id": 7, "name": "Scotland"}},
                        "goals": {"home": None, "away": None},
                    }
                ]
            },
        )


def test_provider_service_with_stub_does_not_call_internet(db_session):
    client = FakeFootballClient()
    service = FootballSyncService(Settings(football_sync_max_requests_per_run=10), db_session, client=client)
    competitions = service.sync_competitions()
    fixtures = service.sync_world_cup_fixtures()
    assert competitions["competitions_saved"] == 1
    assert fixtures["matches_created"] == 1
    assert client.calls[0][0] == "leagues"
    assert any(call[0] == "fixtures" for call in client.calls)


def test_request_budget_blocks_excess_requests():
    budget = RequestBudget(max_requests=1)
    budget.consume()
    with pytest.raises(ApiFootballError):
        budget.consume()


def test_daily_request_limit_blocks_client_before_internet(db_session):
    from app.providers.football_api.client import ApiFootballClient

    settings = Settings(football_api_key="key", football_api_daily_request_limit=0)
    client = ApiFootballClient(settings, db_session, RequestBudget(max_requests=10))
    with pytest.raises(ApiFootballError):
        client.get("leagues", {"search": "world cup"})


def test_sync_endpoints_blocked_when_not_development(client, monkeypatch):
    from app.api.routes import sync_football

    monkeypatch.setattr(sync_football, "get_settings", lambda: Settings(app_env="production", football_api_key="key", football_real_sync_enabled=True))
    response = client.post("/sync/football/competitions")
    assert response.status_code == 403


def test_sync_endpoints_blocked_when_real_sync_disabled(client, monkeypatch):
    from app.api.routes import sync_football

    monkeypatch.setattr(sync_football, "get_settings", lambda: Settings(app_env="development", football_api_key="key", football_real_sync_enabled=False))
    response = client.post("/sync/football/competitions")
    assert response.status_code == 403


def test_sync_endpoint_uses_stub_with_confirmation(client, monkeypatch):
    from app.api.routes import sync_football

    class FakeService:
        def sync_competitions(self):
            return {
                "provider": "api_football",
                "mode": "real_sync",
                "requests_used": 1,
                "competitions_found": 1,
                "competitions_saved": 1,
                "matches_created": 0,
                "matches_updated": 0,
                "raw_payloads_saved": 1,
                "warnings": [],
            }

    monkeypatch.setattr(sync_football, "get_settings", lambda: Settings(app_env="development", football_api_key="key", football_real_sync_enabled=False))
    monkeypatch.setattr(sync_football, "get_sync_service", lambda db, settings: FakeService())
    response = client.post("/sync/football/competitions?confirm_real_sync=true")
    assert response.status_code == 200
    assert response.json()["requests_used"] == 1


def test_real_matches_endpoint_empty_without_sync(client):
    response = client.get("/matches/real/world-cup")
    assert response.status_code == 200
    assert response.json() == []
