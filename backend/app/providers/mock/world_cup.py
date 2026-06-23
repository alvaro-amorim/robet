from datetime import datetime, timezone

from app.schemas.models import Match, OddsSnapshot


MOCK_MATCHES = [
    Match(id="worldcup_mock_001", competition="Copa do Mundo", home_team="Scotland", away_team="Brazil", commence_time=datetime(2026, 6, 14, 16, 0, tzinfo=timezone.utc), status="scheduled"),
    Match(id="worldcup_mock_002", competition="Copa do Mundo", home_team="Morocco", away_team="Haiti", commence_time=datetime(2026, 6, 15, 13, 0, tzinfo=timezone.utc), status="scheduled"),
    Match(id="worldcup_mock_003", competition="Copa do Mundo", home_team="Czech Republic", away_team="Mexico", commence_time=datetime(2026, 6, 16, 19, 0, tzinfo=timezone.utc), status="scheduled"),
    Match(id="worldcup_mock_004", competition="Copa do Mundo", home_team="South Africa", away_team="South Korea", commence_time=datetime(2026, 6, 17, 15, 0, tzinfo=timezone.utc), status="scheduled"),
    Match(id="worldcup_mock_005", competition="Copa do Mundo", home_team="Canada", away_team="Switzerland", commence_time=datetime(2026, 6, 18, 21, 0, tzinfo=timezone.utc), status="scheduled"),
]


MOCK_ODDS = [
    OddsSnapshot(match_id="worldcup_mock_001", bookmaker="MockBook", market="h2h", selection="Brazil wins", odd_decimal=1.72),
    OddsSnapshot(match_id="worldcup_mock_001", bookmaker="MockBook", market="h2h", selection="Draw", odd_decimal=3.65),
    OddsSnapshot(match_id="worldcup_mock_001", bookmaker="MockBook", market="totals", selection="Over 2.5 goals", odd_decimal=1.95),
    OddsSnapshot(match_id="worldcup_mock_001", bookmaker="MockBook", market="corners", selection="Over 7.5 corners", odd_decimal=1.78, point=7.5),
    OddsSnapshot(match_id="worldcup_mock_001", bookmaker="MockBook", market="cards", selection="Under 5.5 cards", odd_decimal=1.84, point=5.5),
    OddsSnapshot(match_id="worldcup_mock_002", bookmaker="MockBook", market="h2h", selection="Morocco wins", odd_decimal=1.58),
    OddsSnapshot(match_id="worldcup_mock_002", bookmaker="MockBook", market="totals", selection="Under 3.5 goals", odd_decimal=1.52, point=3.5),
    OddsSnapshot(match_id="worldcup_mock_002", bookmaker="MockBook", market="corners", selection="Over 6.5 corners", odd_decimal=1.66, point=6.5),
    OddsSnapshot(match_id="worldcup_mock_003", bookmaker="MockBook", market="h2h", selection="Mexico wins", odd_decimal=2.05),
    OddsSnapshot(match_id="worldcup_mock_003", bookmaker="MockBook", market="totals", selection="Over 2.5 goals", odd_decimal=2.08, point=2.5),
    OddsSnapshot(match_id="worldcup_mock_004", bookmaker="MockBook", market="h2h", selection="South Korea wins", odd_decimal=2.34),
    OddsSnapshot(match_id="worldcup_mock_004", bookmaker="MockBook", market="cards", selection="Under 4.5 cards", odd_decimal=1.70, point=4.5),
    OddsSnapshot(match_id="worldcup_mock_005", bookmaker="MockBook", market="h2h", selection="Switzerland wins", odd_decimal=1.88),
    OddsSnapshot(match_id="worldcup_mock_005", bookmaker="MockBook", market="totals", selection="Under 2.5 goals", odd_decimal=1.82, point=2.5),
]

MODEL_PROBABILITY_OVERRIDES = {
    ("worldcup_mock_001", "Brazil wins"): 0.64,
    ("worldcup_mock_001", "Over 2.5 goals"): 0.55,
    ("worldcup_mock_001", "Over 7.5 corners"): 0.60,
    ("worldcup_mock_001", "Under 5.5 cards"): 0.57,
    ("worldcup_mock_002", "Morocco wins"): 0.65,
    ("worldcup_mock_002", "Under 3.5 goals"): 0.69,
    ("worldcup_mock_002", "Over 6.5 corners"): 0.59,
    ("worldcup_mock_003", "Mexico wins"): 0.51,
    ("worldcup_mock_003", "Over 2.5 goals"): 0.49,
    ("worldcup_mock_004", "South Korea wins"): 0.45,
    ("worldcup_mock_004", "Under 4.5 cards"): 0.55,
    ("worldcup_mock_005", "Switzerland wins"): 0.56,
    ("worldcup_mock_005", "Under 2.5 goals"): 0.54,
}


def list_world_cup_matches() -> list[Match]:
    return MOCK_MATCHES


def list_mock_odds() -> list[OddsSnapshot]:
    return MOCK_ODDS
