"""The rental data, with each piece of behaviour next to the data it needs."""

from dataclasses import dataclass, field
from datetime import date

import pricing


@dataclass(frozen=True)
class Customer:
    name: str
    email: str


@dataclass(frozen=True)
class Vehicle:
    name: str
    rate: int  # cents per day
    free_km: int  # per day

    def price(self, days: int, km: int) -> int:
        return pricing.rental_cost(self.rate, self.free_km, days, km)


@dataclass(frozen=True)
class Extra:
    name: str
    price: int  # cents


@dataclass
class RentalContract:
    booking_id: str
    customer: Customer
    vehicle: Vehicle
    days: int
    km: int
    pickup: date
    discount_percent: int = 0
    extras: list[Extra] = field(default_factory=list)

    def add_extra(self, extra: Extra) -> None:
        self.extras.append(extra)

    def remove_extra(self, name: str) -> None:
        self.extras = [extra for extra in self.extras if extra.name != name]

    def customer_name(self) -> str:
        return self.customer.name

    def customer_email(self) -> str:
        return self.customer.email

    def vehicle_name(self) -> str:
        return self.vehicle.name

    def rental_price(self) -> int:
        return self.vehicle.price(self.days, self.km)

    def total_price(self) -> int:
        return self.rental_price() + sum(extra.price for extra in self.extras)

    def discounted_price(self) -> int:
        """The price after the discount. Asking twice gives the same answer."""
        return pricing.percent_off(self.total_price(), self.discount_percent)
