def calculate_stake(current_balance: float, percent: float = 1.0) -> float:
    if current_balance <= 0:
        return 0.0
    return round(current_balance * (percent / 100), 2)


def calculate_expected_value(model_probability: float, odd_decimal: float, stake: float) -> float:
    if odd_decimal <= 1:
        raise ValueError("Odd decimal precisa ser maior que 1.")
    potential_profit = (odd_decimal - 1) * stake
    return round((model_probability * potential_profit) - ((1 - model_probability) * stake), 2)
