"""Ana Silva's bookings and returns for one week.

Run: python3 main.py
"""

from desk import Customer, Handover, book, return_vehicle
from pricing import ChildSeat, DailyRate, Gps, Insurance, RoadToll
from rental import Rental
from vehicles import Bike, Car, Truck, Van


def euros(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def main() -> None:
    """The one place that knows the concrete classes and the prices."""
    ana = Customer("Ana Silva", {"B", "C"})
    car = Car("AB-123", 4500)
    van = Van("VN-321", 7000)
    truck = Truck("TR-789", 9000)
    bike = Bike("BK-1", 1000)
    insurance = Insurance(per_day=1500)

    car_rental = Rental(3, [DailyRate(car.rate), insurance, Gps(per_day=300)])
    car_rental.parts.append(ChildSeat(per_day=500))  # added at the counter

    bookings: list[tuple[Handover, Rental]] = [
        (car, car_rental),
        (van, Rental(2, [DailyRate(van.rate), insurance])),
        (truck, Rental(2, [DailyRate(truck.rate), RoadToll(per_day=2000)])),
        (bike, Rental(2, [DailyRate(bike.rate)])),
    ]

    for vehicle, rental in bookings:
        b = book(ana, vehicle, rental)
        print(
            f"{b.customer}  {b.plate:<6}  {b.days} days"
            f"  total {euros(b.total):>6}  deposit {euros(b.deposit):>6}"
        )

    for vehicle, litres in [(car, 30), (van, 25), (truck, 60)]:
        fuel = return_vehicle(vehicle, litres)
        print(f"{vehicle.plate:<6} returned  {litres} l  fuel {euros(fuel):>6}")


if __name__ == "__main__":
    main()
