from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db import repositories
from app.db.base import OddsEventModel
from app.db.session import get_db
from app.providers.odds_api.client import OddsApiError
from app.providers.odds_api.service import OddsSyncService

router = APIRouter()


def assert_odds_sync_allowed(settings: Settings, confirm_real_sync: bool) -> None:
    if settings.app_env != "development":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sync real de odds disponivel apenas em APP_ENV=development neste ciclo.")
    if not confirm_real_sync:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sync real de odds bloqueado. Envie confirm_real_sync=true para confirmar consumo de quota.")
    if not settings.odds_api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ODDS_API_KEY nao configurada.")


def get_odds_sync_service(db: Session, settings: Settings) -> OddsSyncService:
    return OddsSyncService(settings=settings, db=db)


def run_odds_sync(action):
    try:
        return action()
    except OddsApiError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get("/sync/odds/status")
def odds_sync_status() -> dict:
    settings = get_settings()
    return {
        "provider": "the_odds_api",
        "app_env": settings.app_env,
        "api_key_configured": bool(settings.odds_api_key),
        "sport_key": settings.odds_primary_sport_key,
        "regions": settings.odds_api_regions,
        "markets": settings.odds_api_market_list,
        "odds_format": settings.odds_api_odds_format,
        "date_format": settings.odds_api_date_format,
    }


@router.post("/sync/odds/world-cup")
def sync_world_cup_odds(
    confirm_real_sync: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    assert_odds_sync_allowed(settings, confirm_real_sync)
    return run_odds_sync(lambda: get_odds_sync_service(db, settings).sync_world_cup())


@router.get("/odds/real/world-cup")
def list_real_world_cup_odds(db: Session = Depends(get_db)) -> list[dict]:
    settings = get_settings()
    return [_event_with_summaries(db, event) for event in repositories.list_odds_events(db, sport_key=settings.odds_primary_sport_key)]


@router.get("/market-intelligence/odds-events")
def list_market_intelligence_odds_events(db: Session = Depends(get_db)) -> list[dict]:
    settings = get_settings()
    return [_event_summary(event) for event in repositories.list_odds_events(db, sport_key=settings.odds_primary_sport_key)]


@router.get("/market-intelligence/odds-events/{odds_event_id}")
def get_market_intelligence_odds_event(odds_event_id: str, db: Session = Depends(get_db)) -> dict:
    event = db.get(OddsEventModel, odds_event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento de odds nao encontrado.")
    return _event_with_summaries(db, event)


def _event_summary(event) -> dict:
    return {
        "id": event.id,
        "external_provider": event.external_provider,
        "external_event_id": event.external_event_id,
        "sport_key": event.sport_key,
        "sport_title": event.sport_title,
        "commence_time": event.commence_time,
        "home_team": event.home_team,
        "away_team": event.away_team,
        "linked_match_id": event.linked_match_id,
        "match_link_confidence": event.match_link_confidence,
        "link_status": "vinculado" if event.linked_match_id else "nao_vinculado",
    }


def _event_with_summaries(db: Session, event) -> dict:
    data = _event_summary(event)
    data["markets"] = [
        {
            "market_key": summary.market_key,
            "selection_name": summary.selection_name,
            "point": summary.point,
            "best_odd": summary.best_odd,
            "average_odd": summary.average_odd,
            "median_odd": summary.median_odd,
            "lowest_odd": summary.lowest_odd,
            "bookmaker_count": summary.bookmaker_count,
            "market_spread": summary.market_spread,
            "raw_implied_probability": summary.raw_implied_probability,
            "devig_probability": summary.devig_probability,
            "market_margin": summary.market_margin,
            "captured_at": summary.captured_at,
        }
        for summary in repositories.list_odds_market_summaries(db, odds_event_id=event.id)
    ]
    return data
