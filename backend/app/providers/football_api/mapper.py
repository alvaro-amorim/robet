from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.db import repositories
from app.db.base import CompetitionModel, MatchModel
from app.providers.football_api.schemas import PROVIDER


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def map_league_item(db: Session, item: dict[str, Any], season: int) -> CompetitionModel:
    league = item.get("league") or {}
    country = item.get("country") or {}
    seasons = item.get("seasons") or []
    season_data = next((entry for entry in seasons if entry.get("year") == season), seasons[0] if seasons else {})
    return repositories.upsert_competition(
        db,
        external_provider=PROVIDER,
        external_id=str(league.get("id")),
        name=league.get("name") or "Unknown competition",
        country=country.get("name"),
        season=int(season_data.get("year") or season),
        competition_type=league.get("type"),
        is_active=bool(season_data.get("current", True)),
    )


def map_fixture_item(db: Session, item: dict[str, Any], raw_payload_id: str) -> MatchModel:
    fixture = item.get("fixture") or {}
    league = item.get("league") or {}
    teams = item.get("teams") or {}
    goals = item.get("goals") or {}
    home = teams.get("home") or {}
    away = teams.get("away") or {}
    status = fixture.get("status") or {}

    season = int(league.get("season") or 0)
    fixture_id = fixture.get("id")
    if fixture_id is None:
        raise ValueError("Fixture da API-Football sem fixture.id.")
    competition = repositories.upsert_competition(
        db,
        external_provider=PROVIDER,
        external_id=str(league.get("id")),
        name=league.get("name") or "Unknown competition",
        country=league.get("country"),
        season=season,
        competition_type=None,
        is_active=True,
    )
    home_team = repositories.upsert_team(db, home.get("name") or "Unknown home team", home.get("country"))
    away_team = repositories.upsert_team(db, away.get("name") or "Unknown away team", away.get("country"))
    db.flush()
    if home.get("id") is not None:
        repositories.upsert_team_alias(db, home_team.id, PROVIDER, str(home["id"]), home.get("name") or home_team.name)
    if away.get("id") is not None:
        repositories.upsert_team_alias(db, away_team.id, PROVIDER, str(away["id"]), away.get("name") or away_team.name)

    return repositories.upsert_real_match(
        db,
        provider=PROVIDER,
        external_id=str(fixture_id),
        competition=competition,
        home_team=home_team,
        away_team=away_team,
        home_team_name_snapshot=home.get("name") or home_team.name,
        away_team_name_snapshot=away.get("name") or away_team.name,
        commence_time=parse_datetime(fixture.get("date")),
        status=status.get("short") or status.get("long") or "unknown",
        raw_payload_id=raw_payload_id,
        home_score=goals.get("home"),
        away_score=goals.get("away"),
    )
