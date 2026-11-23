"""A rental has price parts, and only knows them through PriceComponent."""

from dataclasses import dataclass, field
from typing import Protocol


class PriceComponent(Protocol):
    def price(self, days: int) -> int: ...  # cents


@dataclass
class Rental:
    days: int
    parts: list[PriceComponent] = field(default_factory=list)

    def total(self) -> int:
        return sum(part.price(self.days) for part in self.parts)
