"""Payments: one plain class per method, and a dict to pick one."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from pricing import format_cents


class Payer(Protocol):
    def pay(self, cents: int) -> None: ...


class PaymentMethod(Enum):
    CARD = "card"
    PAYPAL = "paypal"


@dataclass(frozen=True)
class CardPayment:
    card_number: str

    def pay(self, cents: int) -> None:
        print(f"  Charged {format_cents(cents)} to card ending {self.card_number[-4:]}")


@dataclass(frozen=True)
class PayPalPayment:
    email: str

    def pay(self, cents: int) -> None:
        print(f"  Charged {format_cents(cents)} to PayPal {self.email}")


PAYERS: dict[PaymentMethod, Callable[[str], Payer]] = {
    PaymentMethod.CARD: CardPayment,
    PaymentMethod.PAYPAL: PayPalPayment,
}


def make_payer(method: PaymentMethod, account: str) -> Payer:
    return PAYERS[method](account)
