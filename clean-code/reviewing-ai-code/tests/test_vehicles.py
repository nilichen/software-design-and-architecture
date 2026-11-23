import pytest

from partner import LeasedVan
from vehicles import Car, LeasedVanAdapter, Van, VehicleKind


def test_kind_typed_in_capitals_is_rejected_at_the_edge():
    with pytest.raises(ValueError, match="'SUV' is not a valid VehicleKind"):
        VehicleKind("SUV")


def test_kind_without_a_rate_fails_instead_of_getting_the_economy_rate():
    with pytest.raises(KeyError):
        Car(VehicleKind.TRUCK).price(1)


def test_every_vehicle_prices_days_in_cents():
    fleet = [
        Car(VehicleKind.SUV),
        Van(daily_rate_cents=9500),
        LeasedVanAdapter(LeasedVan("PARTNER-7", 110.0)),
    ]
    assert [vehicle.price(2) for vehicle in fleet] == [16000, 19000, 22000]
