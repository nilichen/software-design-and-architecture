"""The fleet. Every vehicle is a Vehicle, and the parent holds the shared code."""

from dataclasses import dataclass

FUEL_PER_LITRE = 190  # cents
ROAD_TOLL = 2000  # cents per day, trucks only


@dataclass
class Vehicle:
    plate: str
    rate: int  # cents per day

    def daily_price(self) -> int:
        return self.rate

    def reserve(self, days: int) -> int:
        # Was self.rate * days. Goes through daily_price now, so add-ons get charged.
        return self.daily_price() * days

    def refuel(self, litres: int) -> int:
        return FUEL_PER_LITRE * litres


class Car(Vehicle):
    pass


class Van(Vehicle):
    pass


class Truck(Vehicle):
    def daily_price(self) -> int:  # shown on the website's price list
        return self.rate + ROAD_TOLL

    def reserve(self, days: int) -> int:  # written when reserve used self.rate
        return super().reserve(days) + ROAD_TOLL * days


class Bike(Vehicle):
    def refuel(self, litres: int) -> int:
        raise NotImplementedError("a bike has no tank")
