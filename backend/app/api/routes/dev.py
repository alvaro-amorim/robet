from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.services.persistence import reset_development_data, seed_mock_data

router = APIRouter(prefix="/dev")


def assert_development() -> None:
    if get_settings().app_env != "development":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Endpoint disponível apenas em APP_ENV=development.",
        )


@router.post("/seed")
def seed(db: Session = Depends(get_db)) -> dict[str, int | str]:
    assert_development()
    result = seed_mock_data(db, get_settings())
    return {"status": "seeded", **result}


@router.post("/reset")
def reset(db: Session = Depends(get_db)) -> dict[str, int | str]:
    assert_development()
    result = reset_development_data(db, get_settings())
    return {"status": "reset", **result}
