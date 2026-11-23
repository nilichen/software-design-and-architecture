"""Invoices. Listens for confirmed bookings, never imports the booking code."""

import events


def _confirmed(data: dict[str, str]) -> None:
    print(f"  invoice for {data['booking_id']}: {data['amount']}")


def register() -> None:
    events.subscribe("booking_confirmed", _confirmed)
