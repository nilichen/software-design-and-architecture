"""Prices for the car-rental app. All money is in cents."""

BOOKING_FEE = 500


def format_cents(cents: int) -> str:
    return f"€{cents / 100:.2f}"


def weekend(cents: int) -> int:
    # 10% off on weekends
    return cents * 90 // 100


def loyalty(cents: int) -> int:
    # 10% off for returning customers
    return cents * 95 // 100


def add_fee(cents: int, fee: int) -> int:
    return cents + fee


def weekend_deal(cents: int) -> int:
    price = cents
    price = weekend(price)
    price = loyalty(price)
    price = add_fee(price, BOOKING_FEE)
    return price
