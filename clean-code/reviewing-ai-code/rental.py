"""Picking up and returning rental vehicles. Money is in cents."""

import itertools
from dataclasses import dataclass
from typing import Protocol

from pricing import BOOKING_FEE_CENTS, format_cents
from vehicles import Priced

_booking_numbers = itertools.count(1)


def new_booking_id() -> str:
    return f"BK-{next(_booking_numbers):03d}"


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    email: str


@dataclass
class Booking:
    booking_id: str
    plate: str
    customer_email: str
    days: int
    rental_cents: int
    extras_cents: list[int]

    def total_cents(self) -> int:
        return self.rental_cents + BOOKING_FEE_CENTS + sum(self.extras_cents)


class HasTotal(Protocol):
    def total_cents(self) -> int: ...


def receipt(item: HasTotal) -> str:
    return f"Total due: {format_cents(item.total_cents())}"


class RentalDesk:
    def __init__(self, fleet: dict[str, Priced]) -> None:
        self.fleet = fleet
        self.rented: set[str] = set()

    @property
    def cars_out(self) -> int:
        return len(self.rented)

    def available(self) -> list[str]:
        return [plate for plate in self.fleet if plate not in self.rented]

    def pick_up(
        self, plate: str, customer: Customer, days: int, extras_cents: list[int]
    ) -> Booking:
        if plate not in self.fleet:
            raise KeyError(plate)
        if days <= 0:
            raise ValueError(f"days must be positive, got {days}")
        rental_cents = self.fleet[plate].price(days)
        self.rented.add(plate)
        print(f"Hello {customer.first_name} {customer.last_name}, enjoy {plate}")
        return Booking(
            new_booking_id(), plate, customer.email, days, rental_cents, extras_cents
        )

    def return_car(self, plate: str) -> None:
        self.rented.discard(plate)
