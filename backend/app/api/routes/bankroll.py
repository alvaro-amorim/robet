from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.api.routes.recommendations import get_recommendation_history
from app.db import repositories
from app.db.session import get_db
from app.services.persistence import build_bankroll
from app.schemas.models import Bankroll

router = APIRouter()


@router.get("/bankroll", response_model=Bankroll)
def get_bankroll(db: Session = Depends(get_db)) -> Bankroll:
    settings = get_settings()
    recommendations = get_recommendation_history(db)
    bankroll = build_bankroll(settings, recommendations)
    repositories.save_bankroll_snapshot(db, bankroll)
    db.commit()
    return bankroll
