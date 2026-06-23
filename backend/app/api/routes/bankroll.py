from fastapi import APIRouter

from app.core.config import get_settings
from app.api.routes.recommendations import get_recommendation_history
from app.schemas.models import Bankroll

router = APIRouter()


@router.get("/bankroll", response_model=Bankroll)
def get_bankroll() -> Bankroll:
    settings = get_settings()
    recommendations = get_recommendation_history()
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
