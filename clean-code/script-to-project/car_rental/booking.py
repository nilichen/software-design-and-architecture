import sqlite3
from dataclasses import dataclass

from .errors import InvalidRentalPeriodError
from .fleet_db import fetch_category, save_booking
from .pricing import rental_price


@dataclass(frozen=True)
class Booking:
    customer: str
    plate: str
    days: int
    price_cents: int


def book(con: sqlite3.Connection, customer: str, plate: str, days: int) -> Booking:
    if days < 1:
        raise InvalidRentalPeriodError(days)
    price_cents = rental_price(fetch_category(con, plate), days)
    save_booking(con, customer, plate, days, price_cents)
    return Booking(customer, plate, days, price_cents)
