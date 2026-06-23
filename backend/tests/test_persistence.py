from sqlalchemy import func, select

from app.core.config import Settings
from app.db import repositories
from app.db.base import (
    BankrollSnapshotModel,
    CombinedBetLegModel,
    CombinedBetModel,
    LearningInsightModel,
    MatchModel,
    OddsSnapshotModel,
    RearrangementSuggestionModel,
    RecommendationModel,
    SimulationResultModel,
)
from app.domain.bet_builder.engine import evaluate_combined_bet
from app.domain.recommendation.engine import generate_mock_recommendations
from app.providers.mock.world_cup import list_mock_odds, list_world_cup_matches
from app.schemas.models import Bankroll, CombinedBetRequest
from app.services.persistence import reset_development_data, seed_mock_data


def count(db_session, model) -> int:
    return db_session.scalar(select(func.count()).select_from(model))


def test_create_match_and_odds_snapshot(db_session):
    match = list_world_cup_matches()[0]
    odds = list_mock_odds()[0]
    repositories.upsert_match(db_session, match)
    repositories.upsert_odds_snapshot(db_session, odds, "odds_test_001")
    db_session.commit()
    assert count(db_session, MatchModel) == 1
    assert count(db_session, OddsSnapshotModel) == 1


def test_create_recommendation(db_session):
    match = list_world_cup_matches()[0]
    repositories.upsert_match(db_session, match)
    recommendation = generate_mock_recommendations(Settings())[0]
    repositories.upsert_recommendation(db_session, recommendation)
    db_session.commit()
    assert count(db_session, RecommendationModel) == 1


def test_create_combined_bet_leg_and_rearrangement(db_session):
    repositories.upsert_match(db_session, list_world_cup_matches()[0])
    request = CombinedBetRequest(
        match_id="worldcup_mock_001",
        offered_combined_odd=2.2,
        legs=[
            {"market": "corners", "selection": "Over 7.5 corners", "individual_odd": 1.2, "estimated_probability": 0.78},
            {"market": "h2h", "selection": "Brazil wins", "individual_odd": 1.1, "estimated_probability": 0.82},
            {"market": "cards", "selection": "Under 5.5 cards", "individual_odd": 1.3, "estimated_probability": 0.70},
        ],
    )
    combined_bet = evaluate_combined_bet(request)
    repositories.save_combined_bet(db_session, combined_bet)
    db_session.commit()
    assert count(db_session, CombinedBetModel) == 1
    assert count(db_session, CombinedBetLegModel) == 3
    assert count(db_session, RearrangementSuggestionModel) >= 1


def test_create_bankroll_snapshot_simulation_result_and_learning_insight(db_session):
    match = list_world_cup_matches()[0]
    repositories.upsert_match(db_session, match)
    recommendation = generate_mock_recommendations(Settings())[0]
    repositories.upsert_recommendation(db_session, recommendation)
    repositories.save_bankroll_snapshot(
        db_session,
        Bankroll(
            initial_balance=1000,
            current_balance=1000,
            simulated_exposure=10,
            simulated_profit_loss=0,
            total_recommendations=1,
            won=0,
            lost=0,
            pending=1,
        ),
    )
    repositories.upsert_simulation_result(
        db_session,
        result_id="simulation_test",
        recommendation_id=recommendation.id,
        status="pending",
        stake=10,
        profit_loss=0,
        result_label="aguardando_resultado",
    )
    repositories.upsert_learning_insight(
        db_session,
        insight=__import__("app.domain.learning.engine", fromlist=["generate_learning_insights"]).generate_learning_insights([recommendation])[0],
    )
    db_session.commit()
    assert count(db_session, BankrollSnapshotModel) == 1
    assert count(db_session, SimulationResultModel) == 1
    assert count(db_session, LearningInsightModel) == 1


def test_seed_is_idempotent(db_session):
    settings = Settings()
    first = seed_mock_data(db_session, settings)
    second = seed_mock_data(db_session, settings)
    assert first == second
    assert count(db_session, MatchModel) == 5
    assert count(db_session, OddsSnapshotModel) == 14
    assert count(db_session, RecommendationModel) == 14


def test_reset_recreates_development_data(db_session):
    reset_development_data(db_session, Settings())
    assert count(db_session, MatchModel) == 5
    assert count(db_session, RecommendationModel) == 14


def test_dev_seed_and_reset_endpoints(client):
    seed = client.post("/dev/seed")
    assert seed.status_code == 200
    reset = client.post("/dev/reset")
    assert reset.status_code == 200
    assert reset.json()["matches"] == 5


def test_dev_seed_blocked_outside_development(client, monkeypatch):
    from app.api.routes import dev

    monkeypatch.setattr(dev, "get_settings", lambda: Settings(app_env="production"))
    response = client.post("/dev/seed")
    assert response.status_code == 403
