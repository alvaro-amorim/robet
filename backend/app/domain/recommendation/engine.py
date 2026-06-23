from app.core.config import Settings
from app.domain.bankroll.engine import calculate_expected_value, calculate_stake
from app.domain.probability.engine import calculate_edge, calculate_implied_probability, estimate_model_probability
from app.providers.mock.world_cup import list_mock_odds
from app.schemas.models import Recommendation


def classify_recommendation(edge: float, expected_value: float, confidence: float, quality_score: int) -> tuple[str, str]:
    if confidence < 0.45:
        return "INSUFFICIENT_DATA", "alto"
    if quality_score >= 72 and expected_value > 0 and edge >= 0.04:
        return "GOOD_OPPORTUNITY", "baixo"
    if quality_score >= 55:
        return "WATCH", "medio"
    if expected_value < 0:
        return "AVOID", "medio"
    return "HIGH_RISK", "alto"


def quality_score(edge: float, expected_value: float, confidence: float) -> int:
    raw = 50 + (edge * 220) + (expected_value * 1.4) + ((confidence - 0.5) * 35)
    return max(1, min(100, round(raw)))


def confidence_for_market(market: str) -> float:
    return {
        "h2h": 0.66,
        "totals": 0.61,
        "corners": 0.54,
        "cards": 0.48,
    }.get(market, 0.45)


def generate_mock_recommendations(settings: Settings) -> list[Recommendation]:
    stake = calculate_stake(settings.bankroll_initial_balance, settings.max_stake_per_recommendation_percent)
    recommendations: list[Recommendation] = []
    for index, odd in enumerate(list_mock_odds(), start=1):
        implied = calculate_implied_probability(odd.odd_decimal)
        model_probability = estimate_model_probability(odd)
        edge = calculate_edge(model_probability, implied)
        ev = calculate_expected_value(model_probability, odd.odd_decimal, stake)
        confidence = confidence_for_market(odd.market)
        score = quality_score(edge, ev, confidence)
        rec_type, risk = classify_recommendation(edge, ev, confidence, score)
        explanation = (
            f"Odd implica {implied:.1%}; o modelo inicial estima {model_probability:.1%}. "
            f"Edge de {edge:.1%} e EV simulado de R$ {ev:.2f} com stake de R$ {stake:.2f}."
        )
        recommendations.append(
            Recommendation(
                id=f"rec_mock_{index:03d}",
                match_id=odd.match_id,
                market=odd.market,
                selection=odd.selection,
                odd_decimal=odd.odd_decimal,
                implied_probability=round(implied, 4),
                model_probability=round(model_probability, 4),
                edge=round(edge, 4),
                expected_value=ev,
                confidence=confidence,
                quality_score=score,
                risk_label=risk,
                recommendation_type=rec_type,
                explanation=explanation,
                simulated_stake=stake,
            )
        )
    return sorted(recommendations, key=lambda item: item.quality_score, reverse=True)
