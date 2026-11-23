"""The vehicles we rent out. Every vehicle answers price(days) in cents."""

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Protocol

from partner import LeasedVan


class VehicleKind(Enum):
    ECONOMY = "economy"
    COMPACT = "compact"
    SUV = "suv"
    TRUCK = "truck"


DAILY_RATE_CENTS = {
    VehicleKind.ECONOMY: 4500,
    VehicleKind.COMPACT: 6000,
    VehicleKind.SUV: 8000,
}


class Priced(Protocol):
    def price(self, days: int) -> int: ...


@dataclass(frozen=True)
class Car:
    kind: VehicleKind

    @property
    def daily_rate_cents(self) -> int:
        return DAILY_RATE_CENTS[self.kind]

    def price(self, days: int) -> int:
        return self.daily_rate_cents * days


@dataclass(frozen=True)
class Van:
    daily_rate_cents: int

    def price(self, days: int) -> int:
        return self.daily_rate_cents * days


class LeasedVanAdapter:
    """Gives a partner's LeasedVan our price(days) interface."""

    def __init__(self, van: LeasedVan) -> None:
        self.van = van

    def price(self, days: int) -> int:
        start = date.today()
        euros = self.van.quote(start, start + timedelta(days=days))
        return round(euros * 100)
