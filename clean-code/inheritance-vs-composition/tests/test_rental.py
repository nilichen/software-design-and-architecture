from dataclasses import dataclass

from pricing import Insurance
from rental import Rental


@dataclass
class Fixed:
    """Stand-in part: always the same price, whatever the days."""

    cents: int

    def price(self, days: int) -> int:
        return self.cents


def test_total_adds_up_all_parts() -> None:
    assert Rental(3, [Fixed(700), Fixed(300)]).total() == 1000


def test_rental_without_parts_costs_nothing() -> None:
    assert Rental(3).total() == 0


def test_insurance_charges_per_day() -> None:
    assert Insurance(per_day=1500).price(2) == 3000
