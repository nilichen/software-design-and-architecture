"""Every error the car_rental package raises on purpose."""


class CarRentalError(Exception):
    """Base class: catch this to handle anything the package raises."""


class VehicleNotFoundError(CarRentalError):
    def __init__(self, plate: str) -> None:
        super().__init__(f"no vehicle with plate {plate}")
        self.plate = plate


class InvalidRentalPeriodError(CarRentalError):
    def __init__(self, days: int) -> None:
        super().__init__(f"a rental must be at least 1 day, got {days}")
        self.days = days
