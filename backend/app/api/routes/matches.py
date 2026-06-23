from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import repositories
from app.db.session import get_db
from app.services.persistence import ensure_seeded
from app.schemas.models import Match

router = APIRouter()


@router.get("/matches", response_model=list[Match])
def get_matches(db: Session = Depends(get_db)) -> list[Match]:
    ensure_seeded(db, get_settings())
    return repositories.list_matches(db)


@router.get("/matches/world-cup", response_model=list[Match])
def get_world_cup_matches(db: Session = Depends(get_db)) -> list[Match]:
    ensure_seeded(db, get_settings())
    return repositories.list_matches(db)
