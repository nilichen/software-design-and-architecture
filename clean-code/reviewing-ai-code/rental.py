"""Checkout for the car-rental app."""

import itertools
from dataclasses import dataclass
from datetime import date, timedelta

from partner import LeasedVan
from payments import Payment
from pricing import *
from vehicles import Car

_booking_numbers = itertools.count(1)


@dataclass
class Booking:
    booking_id: str
    plate: str
    customer_email: str
    days: int
    rental: int
    extras: list[int]


class RentalDesk:
    def __init__(self, fleet: dict) -> None:
        self.fleet = fleet
        self.rented: set[str] = set()
        self.cars_out = 0

    def new_booking_id(self) -> str:
        return f"BK-{next(_booking_numbers):03d}"

    def available(self) -> list[str]:
        result = []
        for plate in self.fleet:
            if plate not in self.rented:
                result.append(plate)
        return result

    def checkout(
        self,
        plate: str,
        first: str,
        last: str,
        email: str,
        amount: int,
        extras: list[int],
        card: str | None,
        paypal: str | None,
        returning: bool,
        start: date,
    ) -> Booking | None:
        if not returning:
            if plate in self.fleet:
                if amount > 0:
                    vehicle = self.fleet[plate]
                    end = start + timedelta(days=amount)
                    if isinstance(vehicle, Car):
                        rental = vehicle.price(amount)
                    elif isinstance(vehicle, LeasedVan):
                        rental = round(vehicle.quote(start, end) * 100)
                    else:
                        rental = vehicle.cost(start, end)
                    total = rental + BOOKING_FEE
                    for i in range(len(extras)):
                        total = total + extras[i]
                    self.rented.add(plate)
                    self.cars_out += 1
                    print(f"Hello {first} {last}, enjoy {plate}")
                    if card is not None:
                        Payment("card", card).pay(total)
                    else:
                        if paypal is not None:
                            Payment("paypal", paypal).pay(total)
                    return Booking(
                        self.new_booking_id(), plate, email, amount, rental, extras
                    )
                else:
                    raise ValueError("bad amount")
            else:
                raise KeyError(plate)
        else:
            self.rented.discard(plate)
            self.cars_out -= 1
            return None

    def receipt(self, booking: Booking) -> str:
        self.subtotal = booking.rental
        for extra in booking.extras:
            self.subtotal += extra
        self.fee = BOOKING_FEE
        return f"Total due: {format_cents(self.subtotal + self.fee)}"
