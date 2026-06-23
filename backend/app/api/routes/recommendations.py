from fastapi import APIRouter

from app.core.config import get_settings
from app.domain.recommendation.engine import generate_mock_recommendations
from app.schemas.models import Recommendation

router = APIRouter()
_recommendation_history: list[Recommendation] = []


def get_recommendation_history() -> list[Recommendation]:
    global _recommendation_history
    if not _recommendation_history:
        _recommendation_history = generate_mock_recommendations(get_settings())
    return _recommendation_history


@router.get("/recommendations", response_model=list[Recommendation])
def list_recommendations() -> list[Recommendation]:
    return get_recommendation_history()


@router.post("/recommendations/run-mock", response_model=list[Recommendation])
def run_mock_recommendations() -> list[Recommendation]:
    global _recommendation_history
    _recommendation_history = generate_mock_recommendations(get_settings())
    return _recommendation_history
