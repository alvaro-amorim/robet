from datetime import datetime, timezone
from statistics import mean, median
from typing import Any

from app.db.base import OddsEventModel
from app.providers.odds_api.schemas import OutcomeQuote


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def implied_probability(odd_decimal: float) -> float:
    return 1 / odd_decimal


def point_key(point: float | None) -> str:
    return "none" if point is None else str(point)


def market_display_name(key: str) -> str:
    names = {"h2h": "Resultado final", "totals": "Total de gols"}
    return names.get(key, key)


def event_response_items(data: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return data
    response = data.get("response")
    if isinstance(response, list):
        return response
    return []


def build_market_summaries(event: OddsEventModel, quotes: list[OutcomeQuote]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, str], list[OutcomeQuote]] = {}
    for quote in quotes:
        key = (quote.market_key, quote.selection_name, point_key(quote.point))
        groups.setdefault(key, []).append(quote)

    h2h_devig = _aggregate_h2h_devig(event, groups)
    for (market_key, selection_name, point_key_value), grouped_quotes in groups.items():
        odds = [quote.odd_decimal for quote in grouped_quotes]
        best_odd = max(odds)
        lowest_odd = min(odds)
        point = grouped_quotes[0].point
        devig_data = h2h_devig.get(selection_name) if market_key == "h2h" and point is None else None
        summaries.append(
            {
                "odds_event_id": event.id,
                "match_id": event.linked_match_id,
                "market_key": market_key,
                "selection_name": selection_name,
                "point": point,
                "best_odd": best_odd,
                "average_odd": mean(odds),
                "median_odd": median(odds),
                "lowest_odd": lowest_odd,
                "bookmaker_count": len({quote.bookmaker_id for quote in grouped_quotes}),
                "market_spread": best_odd - lowest_odd,
                "raw_implied_probability": implied_probability(best_odd),
                "devig_probability": devig_data["devig_probability"] if devig_data else None,
                "market_margin": devig_data["market_margin"] if devig_data else None,
                "captured_at": max(quote.captured_at for quote in grouped_quotes),
            }
        )
    return summaries


def _aggregate_h2h_devig(event: OddsEventModel, groups: dict[tuple[str, str, str], list[OutcomeQuote]]) -> dict[str, dict[str, float]]:
    required = [event.home_team, "Draw", event.away_team]
    best_by_selection: dict[str, float] = {}
    for selection in required:
        quotes = groups.get(("h2h", selection, "none"))
        if not quotes:
            return {}
        best_by_selection[selection] = max(quote.odd_decimal for quote in quotes)
    raw = {selection: implied_probability(odd) for selection, odd in best_by_selection.items()}
    raw_sum = sum(raw.values())
    if raw_sum <= 0:
        return {}
    margin = raw_sum - 1
    return {selection: {"devig_probability": probability / raw_sum, "market_margin": margin} for selection, probability in raw.items()}
