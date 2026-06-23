from sqlalchemy.orm import Session
from threading import RLock

from app.core.config import Settings
from app.db import repositories
from app.domain.learning.engine import generate_learning_insights
from app.domain.recommendation.engine import generate_mock_recommendations
from app.providers.mock.world_cup import list_mock_odds, list_world_cup_matches
from app.schemas.models import Bankroll, CombinedBet

_seed_lock = RLock()


def seed_mock_data(db: Session, settings: Settings) -> dict[str, int]:
    with _seed_lock:
        return _seed_mock_data(db, settings)


def _seed_mock_data(db: Session, settings: Settings) -> dict[str, int]:
    matches = list_world_cup_matches()
    odds = list_mock_odds()
    for match in matches:
        repositories.upsert_match(db, match)
    for index, odd in enumerate(odds, start=1):
        repositories.upsert_odds_snapshot(db, odd, f"odds_mock_{index:03d}")

    recommendations = generate_mock_recommendations(settings)
    for recommendation in recommendations:
        repositories.upsert_recommendation(db, recommendation)
        repositories.upsert_simulation_result(
            db,
            result_id=f"simulation_{recommendation.id}",
            recommendation_id=recommendation.id,
            status="pending",
            stake=recommendation.simulated_stake,
            profit_loss=0.0,
            result_label="aguardando_resultado",
        )

    insights = generate_learning_insights(recommendations)
    for insight in insights:
        repositories.upsert_learning_insight(db, insight)

    bankroll = build_bankroll(settings, recommendations)
    repositories.save_bankroll_snapshot(db, bankroll, snapshot_id="bankroll_initial")
    db.commit()
    return {
        "matches": len(matches),
        "odds_snapshots": len(odds),
        "recommendations": len(recommendations),
        "learning_insights": len(insights),
    }


def reset_development_data(db: Session, settings: Settings) -> dict[str, int]:
    with _seed_lock:
        repositories.clear_development_data(db)
        db.commit()
        return _seed_mock_data(db, settings)


def ensure_seeded(db: Session, settings: Settings) -> None:
    if repositories.list_matches(db):
        return
    with _seed_lock:
        if not repositories.list_matches(db):
            _seed_mock_data(db, settings)


def build_bankroll(settings: Settings, recommendations=None) -> Bankroll:
    recommendations = recommendations if recommendations is not None else []
    pending = len([rec for rec in recommendations if rec.status == "simulada_pendente"])
    exposure = round(sum(rec.simulated_stake for rec in recommendations if rec.recommendation_type == "GOOD_OPPORTUNITY"), 2)
    return Bankroll(
        initial_balance=settings.bankroll_initial_balance,
        current_balance=settings.bankroll_initial_balance,
        simulated_exposure=exposure,
        simulated_profit_loss=0.0,
        total_recommendations=len(recommendations),
        won=0,
        lost=0,
        pending=pending,
    )


def persist_combined_bet(db: Session, combined_bet: CombinedBet, stake: float = 10.0) -> CombinedBet:
    repositories.save_combined_bet(db, combined_bet)
    repositories.upsert_simulation_result(
        db,
        result_id=f"simulation_{combined_bet.id}",
        combined_bet_id=combined_bet.id,
        status="pending",
        stake=stake,
        profit_loss=0.0,
        result_label="combinada_simulada",
    )
    db.commit()
    return combined_bet
