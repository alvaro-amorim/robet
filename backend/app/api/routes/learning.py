from fastapi import APIRouter

from app.api.routes.recommendations import get_recommendation_history
from app.domain.learning.engine import generate_learning_insights
from app.schemas.models import LearningInsight

router = APIRouter(prefix="/learning")


@router.get("/insights", response_model=list[LearningInsight])
def list_insights() -> list[LearningInsight]:
    return generate_learning_insights(get_recommendation_history())
