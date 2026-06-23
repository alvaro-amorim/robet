from datetime import datetime, timezone

from app.core.config import Settings
from app.db import repositories
from app.db.base import OddsEventModel, OddsMarketSummaryModel, OddsSnapshotModel, RawApiPayloadModel
from app.providers.odds_api.mapper import build_market_summaries, implied_probability
from app.providers.odds_api.schemas import OddsApiPayload
from app.providers.odds_api.service import OddsSyncService


class FakeOddsClient:
    def __init__(self):
        self.requests_used = 0

    def get_odds(self, sport_key: str):
        self.requests_used += 1
        return OddsApiPayload(
            endpoint=f"sports/{sport_key}/odds",
            params={"regions": "eu"},
            status_code=200,
            raw_payload_id="raw_odds_stub",
            data=[
                {
                    "id": "event_2026_001",
                    "sport_key": sport_key,
                    "sport_title": "FIFA World Cup",
                    "commence_time": "2026-06-12T20:00:00Z",
                    "home_team": "Brazil",
                    "away_team": "Scotland",
                    "bookmakers": [
                        {
                            "key": "book_a",
                            "title": "Book A",
                            "last_update": "2026-06-01T12:00:00Z",
                            "markets": [
                                {
                                    "key": "h2h",
                                    "outcomes": [
                                        {"name": "Brazil", "price": 1.80},
                                        {"name": "Draw", "price": 3.60},
                                        {"name": "Scotland", "price": 4.20},
                                    ],
                                },
                                {
                                    "key": "totals",
                                    "outcomes": [
                                        {"name": "Over", "price": 1.90, "point": 2.5},
                                        {"name": "Under", "price": 1.95, "point": 2.5},
                                        {"name": "Over", "price": 2.40, "point": 3.5},
                                    ],
                                },
                            ],
                        },
                        {
                            "key": "book_b",
                            "title": "Book B",
                            "last_update": "2026-06-01T12:01:00Z",
                            "markets": [
                                {
                                    "key": "h2h",
                                    "outcomes": [
                                        {"name": "Brazil", "price": 1.85},
                                        {"name": "Draw", "price": 3.50},
                                        {"name": "Scotland", "price": 4.00},
                                    ],
                                },
                                {
                                    "key": "totals",
                                    "outcomes": [
                                        {"name": "Over", "price": 1.91, "point": 2.5},
                                        {"name": "Under", "price": 1.92, "point": 2.5},
                                    ],
                                },
                            ],
                        },
                    ],
                }
            ],
        )


def test_sanitize_request_params_removes_odds_api_key():
    sanitized = repositories.sanitize_request_params({"apiKey": "secret", "regions": "eu"})
    assert sanitized["apiKey"] == "[REDACTED]"
    assert sanitized["regions"] == "eu"


def test_implied_probability():
    assert round(implied_probability(2.0), 4) == 0.5


def test_odds_provider_service_with_stub_saves_unlinked_data(db_session):
    client = FakeOddsClient()
    service = OddsSyncService(Settings(odds_primary_sport_key="soccer_fifa_world_cup"), db_session, client=client)
    result = service.sync_world_cup()

    assert result["events_received"] == 1
    assert result["odds_events_created"] == 1
    assert result["linked_to_matches"] == 0
    assert result["unlinked_events"] == 1
    assert result["odds_snapshots_saved"] == 11
    assert db_session.query(OddsEventModel).count() == 1
    assert db_session.query(OddsSnapshotModel).count() == 11
    assert db_session.query(OddsSnapshotModel).first().match_id is None
    assert db_session.query(OddsMarketSummaryModel).count() >= 6


def test_odds_event_upsert_without_match_id(db_session):
    event = repositories.upsert_odds_event(
        db_session,
        provider="the_odds_api",
        external_event_id="event_1",
        sport_key="soccer_fifa_world_cup",
        sport_title="FIFA World Cup",
        commence_time=datetime(2026, 6, 12, tzinfo=timezone.utc),
        home_team="Brazil",
        away_team="Scotland",
        normalized_home_team="brazil",
        normalized_away_team="scotland",
        raw_payload_id=None,
        linked_match_id=None,
        match_link_confidence=0,
    )
    db_session.commit()
    assert event.linked_match_id is None


def test_real_odds_snapshot_without_match_id(db_session):
    event = repositories.upsert_odds_event(
        db_session,
        "the_odds_api",
        "event_1",
        "soccer_fifa_world_cup",
        "FIFA World Cup",
        datetime(2026, 6, 12, tzinfo=timezone.utc),
        "Brazil",
        "Scotland",
        "brazil",
        "scotland",
        None,
    )
    bookmaker = repositories.upsert_bookmaker(db_session, "the_odds_api", "book_a", "Book A")
    market = repositories.upsert_market(db_session, "h2h", "Resultado final")
    db_session.flush()
    snapshot = repositories.save_real_odds_snapshot(
        db_session,
        event.id,
        None,
        None,
        bookmaker.id,
        bookmaker.title,
        market.id,
        market.key,
        "Brazil",
        1.8,
        None,
        implied_probability(1.8),
        datetime.now(timezone.utc),
        None,
    )
    db_session.commit()
    assert snapshot.match_id is None


def test_market_summaries_best_average_median_totals_and_h2h_devig(db_session):
    client = FakeOddsClient()
    service = OddsSyncService(Settings(odds_primary_sport_key="soccer_fifa_world_cup"), db_session, client=client)
    service.sync_world_cup()
    event = db_session.query(OddsEventModel).first()
    summaries = db_session.query(OddsMarketSummaryModel).filter(OddsMarketSummaryModel.odds_event_id == event.id).all()

    brazil = next(item for item in summaries if item.market_key == "h2h" and item.selection_name == "Brazil")
    assert brazil.best_odd == 1.85
    assert round(brazil.average_odd, 3) == 1.825
    assert round(brazil.median_odd, 3) == 1.825
    assert brazil.devig_probability is not None
    assert brazil.market_margin is not None

    over_25 = next(item for item in summaries if item.market_key == "totals" and item.selection_name == "Over" and item.point == 2.5)
    over_35 = next(item for item in summaries if item.market_key == "totals" and item.selection_name == "Over" and item.point == 3.5)
    assert over_25.best_odd == 1.91
    assert over_35.best_odd == 2.40


def test_sync_odds_endpoint_blocks_without_confirmation(client, monkeypatch):
    from app.api.routes import odds

    monkeypatch.setattr(odds, "get_settings", lambda: Settings(app_env="development", odds_api_key="key"))
    response = client.post("/sync/odds/world-cup")
    assert response.status_code == 403


def test_sync_odds_endpoint_with_stub_does_not_require_match_link(client, monkeypatch):
    from app.api.routes import odds

    class FakeService:
        def sync_world_cup(self):
            return {
                "provider": "the_odds_api",
                "sport_key": "soccer_fifa_world_cup",
                "requests_used": 1,
                "events_received": 1,
                "odds_events_created": 1,
                "odds_events_updated": 0,
                "odds_snapshots_saved": 11,
                "market_summaries_created": 6,
                "linked_to_matches": 0,
                "unlinked_events": 1,
                "raw_payloads_saved": 1,
                "warnings": [],
            }

    monkeypatch.setattr(odds, "get_settings", lambda: Settings(app_env="development", odds_api_key="key"))
    monkeypatch.setattr(odds, "get_odds_sync_service", lambda db, settings: FakeService())
    response = client.post("/sync/odds/world-cup?confirm_real_sync=true")
    assert response.status_code == 200
    assert response.json()["unlinked_events"] == 1


def test_raw_payload_sanitizes_api_key(db_session):
    raw = repositories.save_raw_api_payload(
        db_session,
        provider="the_odds_api",
        endpoint="sports/soccer_fifa_world_cup/odds",
        request_method="GET",
        request_params={"apiKey": "secret"},
        response_status=200,
        raw_payload={"response": []},
    )
    db_session.commit()
    saved = db_session.get(RawApiPayloadModel, raw.id)
    assert saved.request_params_json["apiKey"] == "[REDACTED]"
