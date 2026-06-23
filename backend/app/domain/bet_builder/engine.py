from uuid import uuid4

from app.domain.bankroll.engine import calculate_expected_value
from app.domain.probability.engine import apply_correlation_penalty, calculate_implied_probability, calculate_joint_probability
from app.schemas.models import CombinedBet, CombinedBetRequest, RearrangementSuggestion


def evaluate_combined_bet(request: CombinedBetRequest, penalty: float = 0.15, stake: float = 10.0) -> CombinedBet:
    probabilities = [leg.estimated_probability for leg in request.legs]
    joint = calculate_joint_probability(probabilities)
    adjusted = apply_correlation_penalty(joint, penalty)
    fair_odd = round(1 / adjusted, 2) if adjusted > 0 else 0
    implied = calculate_implied_probability(request.offered_combined_odd)
    edge = adjusted - implied
    ev = calculate_expected_value(adjusted, request.offered_combined_odd, stake)
    score = max(1, min(100, round(50 + edge * 180 + ev * 1.5 - max(0, len(request.legs) - 3) * 8)))
    risk = "alto" if len(request.legs) >= 4 or adjusted < 0.25 else "medio" if adjusted < 0.45 else "baixo"
    recommendation = "GOOD_OPPORTUNITY" if score >= 70 and ev > 0 else "WATCH" if score >= 50 else "AVOID"
    suggestions = rearrange_combined_bet(request, score)
    return CombinedBet(
        id=f"combined_{uuid4().hex[:10]}",
        match_id=request.match_id,
        legs=request.legs,
        individual_odds=[leg.individual_odd for leg in request.legs],
        offered_combined_odd=request.offered_combined_odd,
        fair_combined_odd_estimate=fair_odd,
        estimated_joint_probability=round(joint, 4),
        adjusted_joint_probability=round(adjusted, 4),
        implied_probability=round(implied, 4),
        edge=round(edge, 4),
        expected_value=ev,
        correlation_penalty=penalty,
        quality_score=score,
        risk_label=risk,
        recommendation=recommendation,
        rearrangement_suggestions=suggestions,
    )


def rearrange_combined_bet(request: CombinedBetRequest, original_score: int | None = None) -> list[RearrangementSuggestion]:
    base_score = original_score or 55
    suggestions: list[RearrangementSuggestion] = []
    riskiest = min(request.legs, key=lambda leg: leg.estimated_probability)
    if riskiest.estimated_probability < 0.72:
        suggestions.append(
            RearrangementSuggestion(
                type="REMOVE_LEG",
                reason=f"A perna '{riskiest.selection}' tem a menor probabilidade estimada e aumenta a incerteza da combinada.",
                new_estimated_quality_score=min(100, base_score + 11),
            )
        )
    if len(request.legs) > 2:
        suggestions.append(
            RearrangementSuggestion(
                type="REDUCE_LEGS",
                reason="Reduzir o número de pernas diminui o impacto da correlação entre eventos do mesmo jogo.",
                new_estimated_quality_score=min(100, base_score + 8),
            )
        )
    aggressive = next((leg for leg in request.legs if "Over" in leg.selection or "Under" in leg.selection), None)
    if aggressive:
        suggestions.append(
            RearrangementSuggestion(
                type="MAKE_LINE_SAFER",
                reason=f"Trocar '{aggressive.selection}' por uma linha mais conservadora pode reduzir risco sem eliminar o racional da entrada.",
                new_estimated_quality_score=min(100, base_score + 6),
            )
        )
    if not suggestions:
        suggestions.append(
            RearrangementSuggestion(
                type="KEEP_AND_WATCH",
                reason="A combinada não tem uma perna claramente fraca, mas ainda deve ser tratada como simulação por causa da correlação.",
                new_estimated_quality_score=base_score,
            )
        )
    return suggestions
