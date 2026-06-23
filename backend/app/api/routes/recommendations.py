from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import repositories
from app.db.session import get_db
from app.domain.recommendation.engine import generate_mock_recommendations
from app.services.persistence import ensure_seeded
from app.schemas.models import Recommendation

router = APIRouter()


def get_recommendation_history(db: Session) -> list[Recommendation]:
    ensure_seeded(db, get_settings())
    return repositories.list_recommendations(db)


@router.get("/recommendations", response_model=list[Recommendation])
def list_recommendations(db: Session = Depends(get_db)) -> list[Recommendation]:
    return get_recommendation_history(db)


@router.post("/recommendations/run-mock", response_model=list[Recommendation])
def run_mock_recommendations(db: Session = Depends(get_db)) -> list[Recommendation]:
    settings = get_settings()
    ensure_seeded(db, settings)
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
    db.commit()
    return repositories.list_recommendations(db)
