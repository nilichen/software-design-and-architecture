from rental import RentalContract


def test_percent_comes_off_before_the_fixed_amount():
    rental = RentalContract(
        "AB-123", "Ana Silva", days=4, daily_rate=4500, percent_off=10, fixed_off=1000
    )

    assert rental.total_price() == 15200  # 18000 - 10% = 16200, minus 1000
