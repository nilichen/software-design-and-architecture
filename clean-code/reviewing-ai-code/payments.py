"""Payments. Payment("card", ...) gives you the right kind of payment."""

from pricing import format_cents


class Payment:
    def __new__(cls, method: str, account: str):
        if cls is Payment:
            if method == "card":
                return super().__new__(CardPayment)
            if method == "paypal":
                return super().__new__(PayPalPayment)
            raise ValueError(f"unknown payment method: {method}")
        return super().__new__(cls)

    def __init__(self, method: str, account: str) -> None:
        self.method = method
        self.account = account

    def pay(self, cents: int) -> None:
        raise NotImplementedError


class CardPayment(Payment):
    def pay(self, cents: int) -> None:
        print(f"  Charged {format_cents(cents)} to card ending {self.account[-4:]}")


class PayPalPayment(Payment):
    def pay(self, cents: int) -> None:
        print(f"  Charged {format_cents(cents)} to PayPal {self.account}")
