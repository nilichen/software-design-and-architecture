"""Add-ons as mixins: each one adds its charge to daily_price and passes the call on."""

from vehicles import Car, Truck, Van

INSURANCE_PER_DAY = 1500  # cents
GPS_PER_DAY = 300
CHILD_SEAT_PER_DAY = 500


class InsuranceMixin:
    def daily_price(self) -> int:
        return super().daily_price() + INSURANCE_PER_DAY  # type: ignore[misc, no-any-return]


class GpsMixin:
    def daily_price(self) -> int:
        return super().daily_price() + GPS_PER_DAY  # type: ignore[misc, no-any-return]


class ChildSeatMixin:
    def daily_price(self) -> int:
        return super().daily_price() + CHILD_SEAT_PER_DAY  # type: ignore[misc, no-any-return]


# One class per vehicle and add-on combination.
class InsuredCar(InsuranceMixin, Car):
    pass


class InsuredGpsCar(InsuranceMixin, GpsMixin, Car):
    pass


class InsuredGpsChildSeatCar(InsuranceMixin, GpsMixin, ChildSeatMixin, Car):
    pass


class InsuredVan(Van, InsuranceMixin):
    pass


class InsuredTruck(InsuranceMixin, Truck):
    pass
