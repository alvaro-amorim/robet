from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import repositories
from app.db.session import get_db
from app.domain.bankroll.engine import calculate_stake
from app.domain.bet_builder.engine import evaluate_combined_bet, rearrange_combined_bet
from app.services.persistence import ensure_seeded, persist_combined_bet
from app.schemas.models import CombinedBet, CombinedBetRequest, RearrangementSuggestion

router = APIRouter(prefix="/bet-builder")


@router.get("/history", response_model=list[CombinedBet])
def history(db: Session = Depends(get_db)) -> list[CombinedBet]:
    ensure_seeded(db, get_settings())
    return repositories.list_combined_bets(db)


@router.post("/evaluate", response_model=CombinedBet)
def evaluate(request: CombinedBetRequest, db: Session = Depends(get_db)) -> CombinedBet:
    settings = get_settings()
    ensure_seeded(db, settings)
    stake = calculate_stake(settings.bankroll_initial_balance, settings.max_stake_per_recommendation_percent)
    combined_bet = evaluate_combined_bet(
        request,
        penalty=settings.combined_bet_default_correlation_penalty,
        stake=stake,
    )
    return persist_combined_bet(db, combined_bet, stake=stake)


@router.post("/rearrange")
def rearrange(request: CombinedBetRequest, db: Session = Depends(get_db)) -> dict[str, int | list[RearrangementSuggestion]]:
    settings = get_settings()
    ensure_seeded(db, settings)
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
