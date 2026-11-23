from dataclasses import dataclass

import pytest

from rental import Customer, RentalDesk, receipt
from vehicles import Van

ANA = Customer(first_name="Ana", last_name="Silva", email="ana@example.com")


def make_desk() -> RentalDesk:
    return RentalDesk({"EF-789": Van(9500), "XY-001": Van(9500)})


def test_booking_total_adds_rental_fee_and_extras():
    booking = make_desk().pick_up("EF-789", ANA, days=2, extras_cents=[1000, 500])
    assert booking.total_cents() == 19000 + 500 + 1500


@pytest.mark.parametrize(("plate", "days"), [("ZZ-999", 3), ("EF-789", 0)])
def test_bad_pick_up_raises_and_hands_out_nothing(plate, days):
    desk = make_desk()
    with pytest.raises((KeyError, ValueError)):
        desk.pick_up(plate, ANA, days, [])
    assert desk.cars_out == 0


def test_cars_out_follows_a_record_fixed_by_hand():
    desk = make_desk()
    desk.pick_up("EF-789", ANA, 1, [])
    desk.pick_up("XY-001", ANA, 1, [])
    desk.rented.discard("XY-001")
    assert desk.cars_out == 1
    assert desk.available() == ["XY-001"]


def test_receipt_prints_anything_with_a_total():
    @dataclass
    class Quote:
        cents: int

        def total_cents(self) -> int:
            return self.cents

    assert receipt(Quote(12000)) == "Total due: €120.00"
