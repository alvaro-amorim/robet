from app.providers.mock.world_cup import MODEL_PROBABILITY_OVERRIDES
from app.schemas.models import OddsSnapshot


def calculate_implied_probability(odd_decimal: float) -> float:
    if odd_decimal <= 1:
        raise ValueError("Odd decimal precisa ser maior que 1.")
    return 1 / odd_decimal


def estimate_model_probability(odd: OddsSnapshot) -> float:
    override = MODEL_PROBABILITY_OVERRIDES.get((odd.match_id, odd.selection))
    if override is not None:
        return override
    implied = calculate_implied_probability(odd.odd_decimal)
    return min(max(implied + 0.03, 0.05), 0.90)


def calculate_edge(model_probability: float, implied_probability: float) -> float:
    return model_probability - implied_probability


def calculate_joint_probability(probabilities: list[float]) -> float:
    joint = 1.0
    for probability in probabilities:
        if probability <= 0 or probability >= 1:
            raise ValueError("Probabilidades estimadas devem estar entre 0 e 1.")
        joint *= probability
    return joint


def apply_correlation_penalty(joint_probability: float, penalty: float) -> float:
    if penalty < 0 or penalty >= 1:
        raise ValueError("Penalidade de correlação deve ficar entre 0 e 1.")
    return joint_probability * (1 - penalty)
