from fastapi import APIRouter

from app.providers.mock.world_cup import list_world_cup_matches
from app.schemas.models import Match

router = APIRouter()


@router.get("/matches", response_model=list[Match])
def get_matches() -> list[Match]:
    return list_world_cup_matches()


@router.get("/matches/world-cup", response_model=list[Match])
def get_world_cup_matches() -> list[Match]:
    return list_world_cup_matches()
