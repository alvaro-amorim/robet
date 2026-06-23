from app.core.config import Settings
from app.domain.recommendation.engine import generate_mock_recommendations


def test_recommendations_are_ranked():
    recommendations = generate_mock_recommendations(Settings())
    scores = [item.quality_score for item in recommendations]
    assert len(recommendations) > 0
    assert scores == sorted(scores, reverse=True)
    assert all(item.implied_probability > 0 for item in recommendations)


def test_recommendations_include_ev_and_edge():
    recommendation = generate_mock_recommendations(Settings())[0]
    assert recommendation.edge != 0
    assert recommendation.expected_value != 0
