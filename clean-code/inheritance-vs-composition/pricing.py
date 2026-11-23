"""Price parts. Each one fits rental.PriceComponent without importing it."""

from dataclasses import dataclass


@dataclass
class DailyRate:
    cents: int

    def price(self, days: int) -> int:
        return self.cents * days


@dataclass
class Insurance:
    per_day: int  # cents

    def price(self, days: int) -> int:
        return self.per_day * days


@dataclass
class Gps:
    per_day: int  # cents

    def price(self, days: int) -> int:
        return self.per_day * days


@dataclass
class ChildSeat:
    per_day: int  # cents

    def price(self, days: int) -> int:
        return self.per_day * days


@dataclass
class RoadToll:
    per_day: int  # cents

    def price(self, days: int) -> int:
        return self.per_day * days
