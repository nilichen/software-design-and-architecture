"""The rental desk: booking and returns. Each function asks only for what it uses."""

from dataclasses import dataclass
from typing import Protocol

from rental import Rental


@dataclass
class Customer:
    name: str
    licences: set[str]


@dataclass
class Booking:
    customer: str
    plate: str
    days: int
    total: int  # cents
    deposit: int  # cents


class Handover(Protocol):
    plate: str

    def licence_ok(self, licences: set[str]) -> bool: ...

    def deposit(self) -> int: ...  # cents


class Fuelable(Protocol):
    def refuel(self, litres: int) -> int: ...  # cents


def book(customer: Customer, vehicle: Handover, rental: Rental) -> Booking:
    if not vehicle.licence_ok(customer.licences):
        raise ValueError(f"{customer.name} may not drive {vehicle.plate}")
    return Booking(
        customer.name, vehicle.plate, rental.days, rental.total(), vehicle.deposit()
    )


def return_vehicle(vehicle: Fuelable, litres: int) -> int:
    """Fuel charge in cents when the vehicle comes back."""
    return vehicle.refuel(litres)
