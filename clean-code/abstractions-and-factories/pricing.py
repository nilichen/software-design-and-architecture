"""Daily rates, extras and discounts. Money is in integer cents."""

from dataclasses import dataclass
from typing import Protocol

DAILY_RATES = {"limited": 4500, "unlimited": 5500}
YOUNG_DRIVER_SURCHARGE = 1000  # per day, for drivers under 25
PREPAID_FUEL = 6000


def daily_rate(mileage: str, driver_age: int) -> int:
    rate = DAILY_RATES[mileage]
    if driver_age < 25:
        rate += YOUNG_DRIVER_SURCHARGE
    return rate


def fuel_charge(fuel_plan: str) -> int:
    return PREPAID_FUEL if fuel_plan == "prepaid" else 0


class Discount(Protocol):
    def apply(self, price: int) -> int: ...


@dataclass
class FixedDiscount:
    amount: int

    def apply(self, price: int) -> int:
        return max(price - self.amount, 0)


@dataclass
class PercentDiscount:
    percent: int
    rounding: str = "down"  # "down", "up" or "nearest"

    def apply(self, price: int) -> int:
        cut = price * self.percent
        if self.rounding == "up":
            cut = -(-cut // 100)
        elif self.rounding == "nearest":
            cut = (cut + 50) // 100
        else:
            cut = cut // 100
        return price - cut
