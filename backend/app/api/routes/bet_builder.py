from fastapi import APIRouter

from app.core.config import get_settings
from app.domain.bankroll.engine import calculate_stake
from app.domain.bet_builder.engine import evaluate_combined_bet, rearrange_combined_bet
from app.schemas.models import CombinedBet, CombinedBetRequest, RearrangementSuggestion

router = APIRouter(prefix="/bet-builder")


@router.post("/evaluate", response_model=CombinedBet)
def evaluate(request: CombinedBetRequest) -> CombinedBet:
    settings = get_settings()
    stake = calculate_stake(settings.bankroll_initial_balance, settings.max_stake_per_recommendation_percent)
    return evaluate_combined_bet(
        request,
        penalty=settings.combined_bet_default_correlation_penalty,
        stake=stake,
    )


@router.post("/rearrange")
def rearrange(request: CombinedBetRequest) -> dict[str, int | list[RearrangementSuggestion]]:
    settings = get_settings()
    stake = calculate_stake(settings.bankroll_initial_balance, settings.max_stake_per_recommendation_percent)
    evaluated = evaluate_combined_bet(
        request,
        penalty=settings.combined_bet_default_correlation_penalty,
        stake=stake,
    )
    return {
        "original_quality_score": evaluated.quality_score,
        "suggestions": rearrange_combined_bet(request, evaluated.quality_score),
    }
