"""Things a customer pays for: a rental contract and a damage fee. Money is in cents."""

from dataclasses import dataclass
from enum import Enum, auto


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
    percent_off: int = 0
    fixed_off: int = 0
    status: PaymentStatus = PaymentStatus.OPEN

    def total_price(self) -> int:
        price = self.days * self.daily_rate + self.fuel_charge
        price -= price * self.percent_off // 100
        return max(price - self.fixed_off, 0)

    def mark_paid(self) -> None:
        self.status = PaymentStatus.PAID


@dataclass
class DamageFee:
    plate: str
    description: str
    amount: int
    status: PaymentStatus = PaymentStatus.OPEN

    def total_price(self) -> int:
        return self.amount

    def mark_paid(self) -> None:
        self.status = PaymentStatus.PAID
