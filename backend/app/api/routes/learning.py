from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.recommendations import get_recommendation_history
from app.db import repositories
from app.db.session import get_db
from app.domain.learning.engine import generate_learning_insights
from app.schemas.models import LearningInsight

router = APIRouter(prefix="/learning")


@router.get("/insights", response_model=list[LearningInsight])
def list_insights(db: Session = Depends(get_db)) -> list[LearningInsight]:
    existing = repositories.list_learning_insights(db)
    if existing:
        return existing
    insights = generate_learning_insights(get_recommendation_history(db))
    for insight in insights:
        repositories.upsert_learning_insight(db, insight)
    db.commit()
    return repositories.list_learning_insights(db)
