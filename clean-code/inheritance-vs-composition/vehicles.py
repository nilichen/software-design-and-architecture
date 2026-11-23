"""The fleet. Each vehicle answers the desk's questions itself, so no code asks its kind."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

FUEL_PER_LITRE = 190  # cents


@dataclass
class MotorVehicle(ABC):
    """Shared state and code for vehicles with a tank. One level deep, no more."""

    plate: str
    rate: int  # cents per day

    def refuel(self, litres: int) -> int:
        return FUEL_PER_LITRE * litres

    @abstractmethod
    def licence_ok(self, licences: set[str]) -> bool: ...

    @abstractmethod
    def deposit(self) -> int: ...


class Car(MotorVehicle):
    def licence_ok(self, licences: set[str]) -> bool:
        return "B" in licences

    def deposit(self) -> int:
        return 30000


class Van(MotorVehicle):
    def licence_ok(self, licences: set[str]) -> bool:
        return "B" in licences

    def deposit(self) -> int:
        return 40000


class Truck(MotorVehicle):
    def licence_ok(self, licences: set[str]) -> bool:
        return "C" in licences

    def deposit(self) -> int:
        return 50000


@dataclass
class Bike:
    """No tank, so no refuel method to fake."""

    plate: str
    rate: int  # cents per day

    def licence_ok(self, licences: set[str]) -> bool:
        return True

    def deposit(self) -> int:
        return 5000
