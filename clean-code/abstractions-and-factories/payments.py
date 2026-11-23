"""Taking the money for a rental."""

from authorizers import (
    authorize_fingerprint,
    authorize_google,
    authorize_robot,
    authorize_sms,
)
from rental import PaymentStatus, RentalContract


class PaymentProcessor:
    def __init__(self, authorizer_type: str) -> None:
        if authorizer_type == "sms":
            self.authorize = authorize_sms
        elif authorizer_type == "google":
            self.authorize = authorize_google
        elif authorizer_type == "robot":
            self.authorize = authorize_robot
        elif authorizer_type == "fingerprint":
            self.authorize = authorize_fingerprint
        else:
            raise ValueError(f"unknown authorizer {authorizer_type!r}")

    def pay_by_card(self, rental: RentalContract, security_code: str) -> None:
        if not self.authorize():
            raise RuntimeError("payment not authorized")
        print(f"  card payment of {rental.total_price()} cents")
        rental.status = PaymentStatus.PAID

    def pay_by_paypal(self, rental: RentalContract, email: str) -> None:
        if not self.authorize():
            raise RuntimeError("payment not authorized")
        print(f"  PayPal payment of {rental.total_price()} cents from {email}")
        rental.status = PaymentStatus.PAID

    def pay_by_debit(self, rental: RentalContract) -> None:
        if not self.authorize():
            raise RuntimeError("payment not authorized")
        print(f"  debit payment of {rental.total_price()} cents")
        rental.status = PaymentStatus.PAID
