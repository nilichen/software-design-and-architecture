"""Emails to the customer. Knows nothing about contracts or payments."""

from datetime import date

import events


def send_reminder(email: str, pickup: date) -> None:
    print(f"  reminder to {email}: pick-up on {pickup}")


def _confirmed(data: dict[str, str]) -> None:
    print(
        f"  email to {data['email']}: {data['booking_id']} confirmed, "
        f"{data['amount']} paid"
    )


def _cancelled(data: dict[str, str]) -> None:
    print(
        f"  email to {data['email']}: "
        f"{data['booking_id']} cancelled, {data['amount']} refunded"
    )


def register() -> None:
    events.subscribe("booking_confirmed", _confirmed)
    events.subscribe("booking_cancelled", _cancelled)
