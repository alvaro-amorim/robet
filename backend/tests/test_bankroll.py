from app.domain.bankroll.engine import calculate_expected_value, calculate_stake


def test_calculate_stake():
    assert calculate_stake(1000, 1) == 10


def test_calculate_expected_value():
    assert calculate_expected_value(0.55, 2.0, 10) == 1.0
