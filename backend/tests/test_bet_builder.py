from app.domain.bet_builder.engine import evaluate_combined_bet, rearrange_combined_bet
from app.schemas.models import CombinedBetRequest


def sample_request() -> CombinedBetRequest:
    return CombinedBetRequest(
        match_id="worldcup_mock_001",
        offered_combined_odd=2.2,
        legs=[
            {"market": "corners", "selection": "Over 7.5 corners", "individual_odd": 1.2, "estimated_probability": 0.78},
            {"market": "h2h", "selection": "Brazil wins", "individual_odd": 1.1, "estimated_probability": 0.82},
            {"market": "cards", "selection": "Under 5.5 cards", "individual_odd": 1.3, "estimated_probability": 0.70},
        ],
    )


def test_evaluate_combined_bet():
    result = evaluate_combined_bet(sample_request(), penalty=0.15, stake=10)
    assert result.estimated_joint_probability == 0.4477
    assert result.adjusted_joint_probability == 0.3806
    assert result.fair_combined_odd_estimate == 2.63
    assert result.recommendation in {"GOOD_OPPORTUNITY", "WATCH", "AVOID"}


def test_rearrange_combined_bet():
    suggestions = rearrange_combined_bet(sample_request(), 61)
    assert any(item.type == "REMOVE_LEG" for item in suggestions)
    assert any(item.type == "REDUCE_LEGS" for item in suggestions)
