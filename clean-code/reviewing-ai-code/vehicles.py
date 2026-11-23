"""The vehicles we rent out."""

from datetime import date


class Car:
    def __init__(self, kind: str) -> None:
        self.kind = kind  # "economy", "compact", "suv" or "truck"

    def price(self, days: int) -> int:
        if self.kind == "suv":
            rate = 8000
        elif self.kind == "compact":
            rate = 6000
        else:
            rate = 4500
        return rate * days


class Van:
    def __init__(self, cost_per_day: int) -> None:
        self.cost_per_day = cost_per_day

    def cost(self, start: date, end: date) -> int:
        return self.cost_per_day * (end - start).days
