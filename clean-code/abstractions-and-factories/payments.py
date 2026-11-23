"""Taking the money for anything chargeable."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

Authorizer = Callable[[], bool]


class Chargeable(Protocol):
    def total_price(self) -> int: ...
    def mark_paid(self) -> None: ...


class PaymentProcessor(Protocol):
    def pay(self, chargeable: Chargeable, authorize: Authorizer) -> None: ...


def check(authorize: Authorizer) -> None:
    if not authorize():
        raise RuntimeError("payment not authorized")


@dataclass
class CardProcessor:
    security_code: str

    def pay(self, chargeable: Chargeable, authorize: Authorizer) -> None:
        check(authorize)
        print(f"  card payment of {chargeable.total_price()} cents")
        chargeable.mark_paid()


@dataclass
class PayPalProcessor:
    email: str

    def pay(self, chargeable: Chargeable, authorize: Authorizer) -> None:
        check(authorize)
        print(f"  PayPal payment of {chargeable.total_price()} cents from {self.email}")
        chargeable.mark_paid()


class DebitProcessor:
    def pay(self, chargeable: Chargeable, authorize: Authorizer) -> None:
        check(authorize)
        print(f"  debit payment of {chargeable.total_price()} cents")
        chargeable.mark_paid()


class ApplePayProcessor:
    def pay(self, chargeable: Chargeable, authorize: Authorizer) -> None:
        check(authorize)
        print(f"  Apple Pay payment of {chargeable.total_price()} cents")
        chargeable.mark_paid()
