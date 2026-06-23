import pytest

from app.domain.probability.engine import (
    apply_correlation_penalty,
    calculate_edge,
    calculate_implied_probability,
    calculate_joint_probability,
)


def test_calculate_implied_probability():
    assert calculate_implied_probability(2.0) == 0.5


def test_calculate_edge():
    assert calculate_edge(0.56, 0.50) == pytest.approx(0.06)


def test_calculate_joint_probability():
    assert calculate_joint_probability([0.78, 0.82, 0.70]) == pytest.approx(0.44772)


def test_apply_correlation_penalty():
    assert apply_correlation_penalty(0.44772, 0.15) == pytest.approx(0.380562)
