"""Prices for the car-rental app. All money is in cents."""

from collections.abc import Callable
from functools import partial, reduce

BOOKING_FEE_CENTS = 500
WEEKEND_PERCENT_OFF = 10
LOYALTY_PERCENT_OFF = 5

PriceFn = Callable[[int], int]


def format_cents(cents: int) -> str:
    return f"€{cents / 100:.2f}"


def weekend(cents: int) -> int:
    return cents * (100 - WEEKEND_PERCENT_OFF) // 100


def loyalty(cents: int) -> int:
    return cents * (100 - LOYALTY_PERCENT_OFF) // 100


def add_fee(cents: int, fee_cents: int) -> int:
    return cents + fee_cents


def compose(*functions: PriceFn) -> PriceFn:
    """Apply the functions left to right, each to the result of the one before."""

    def composed(cents: int) -> int:
        return reduce(lambda result, function: function(result), functions, cents)

    return composed


weekend_deal = compose(weekend, loyalty, partial(add_fee, fee_cents=BOOKING_FEE_CENTS))
