from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.providers.football_api.client import ApiFootballError
from app.providers.football_api.service import FootballSyncService

router = APIRouter(prefix="/sync/football")


def assert_sync_allowed(settings: Settings, confirm_real_sync: bool) -> None:
    if settings.app_env != "development":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sync real disponível apenas em APP_ENV=development neste ciclo.")
    if not settings.football_real_sync_enabled and not confirm_real_sync:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sync real bloqueado. Defina FOOTBALL_REAL_SYNC_ENABLED=true ou envie confirm_real_sync=true.",
        )
    if not settings.football_api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="FOOTBALL_API_KEY não configurada.")


def get_sync_service(db: Session, settings: Settings) -> FootballSyncService:
    return FootballSyncService(settings=settings, db=db)


def run_sync_action(action):
    try:
        return action()
    except ApiFootballError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get("/status")
def sync_status() -> dict:
    settings = get_settings()
    return {
        "provider": settings.football_data_provider,
        "app_env": settings.app_env,
        "real_sync_enabled": settings.football_real_sync_enabled,
        "api_key_configured": bool(settings.football_api_key),
        "max_requests_per_run": settings.football_sync_max_requests_per_run,
        "daily_request_limit": settings.football_api_daily_request_limit,
        "default_season": settings.football_default_season,
        "search_terms": settings.football_world_cup_search_term_list,
    }


@router.post("/competitions")
def sync_competitions(
    confirm_real_sync: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    assert_sync_allowed(settings, confirm_real_sync)
    return run_sync_action(lambda: get_sync_service(db, settings).sync_competitions())


@router.post("/world-cup-fixtures")
def sync_world_cup_fixtures(
    confirm_real_sync: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    assert_sync_allowed(settings, confirm_real_sync)
    return run_sync_action(lambda: get_sync_service(db, settings).sync_world_cup_fixtures())


@router.post("/results")
def sync_results(
    confirm_real_sync: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    assert_sync_allowed(settings, confirm_real_sync)
    return run_sync_action(lambda: get_sync_service(db, settings).sync_results())
