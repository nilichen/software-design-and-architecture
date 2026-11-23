"""The rental desk: licence check, deposit, booking and returns."""

from dataclasses import dataclass

from vehicles import Bike, Car, Truck, Van, Vehicle


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


def licence_ok(vehicle: Vehicle, licences: set[str]) -> bool:
    if isinstance(vehicle, (Car, Van)):
        return "B" in licences
    elif isinstance(vehicle, Truck):
        return "C" in licences
    else:  # bike
        return True


def deposit(vehicle: Vehicle) -> int:
    if isinstance(vehicle, Truck):
        return 50000
    elif isinstance(vehicle, Car):
        return 30000
    else:  # bike
        return 5000


def book(customer: Customer, vehicle: Vehicle, days: int) -> Booking:
    if not licence_ok(vehicle, customer.licences):
        raise ValueError(f"{customer.name} may not drive {vehicle.plate}")
    return Booking(
        customer.name, vehicle.plate, days, vehicle.reserve(days), deposit(vehicle)
    )


def return_vehicle(vehicle: Vehicle, litres: int) -> int:
    """Fuel charge in cents when the vehicle comes back."""
    if isinstance(vehicle, Bike):
        return 0  # Bike.refuel raises
    return vehicle.refuel(litres)
