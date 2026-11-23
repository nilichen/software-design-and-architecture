"""The only module that talks to the payment provider."""

from dataclasses import dataclass

import card_provider

CREDIT_FEE_PERCENT = 2


@dataclass(frozen=True)
class Payment:
    txn: str
    amount: int  # cents


def pay_debit(card_number: str, cents: int) -> Payment:
    return Payment(card_provider.charge(card_number, cents), cents)


def pay_credit(card_number: str, cents: int) -> Payment:
    amount = cents + cents * CREDIT_FEE_PERCENT // 100
    return Payment(card_provider.charge(card_number, amount), amount)


def refund(payment: Payment) -> None:
    card_provider.refund(payment.txn, payment.amount)
