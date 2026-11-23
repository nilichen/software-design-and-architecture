from pricing import compose, weekend_deal


def test_weekend_deal_matches_the_three_steps():
    # 24000 -> 10% off -> 21600 -> 5% off -> 20520 -> + 500 fee
    assert weekend_deal(24000) == 21020


def test_compose_applies_left_to_right():
    add_one_then_double = compose(lambda cents: cents + 1, lambda cents: cents * 2)
    assert add_one_then_double(10) == 22
