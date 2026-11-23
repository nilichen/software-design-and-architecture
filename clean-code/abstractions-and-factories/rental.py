"""A rental contract and what it costs. Money is in integer cents."""

from dataclasses import dataclass, field
from enum import Enum, auto

from pricing import Discount


class PaymentStatus(Enum):
    OPEN = auto()
    PAID = auto()


@dataclass
class RentalContract:
    plate: str
    customer: str
    days: int
    daily_rate: int
    fuel_charge: int = 0
    discounts: list[Discount] = field(default_factory=list)
    status: PaymentStatus = PaymentStatus.OPEN

    def total_price(self) -> int:
        price = self.days * self.daily_rate + self.fuel_charge
        for discount in self.discounts:
            price = discount.apply(price)
        return price
