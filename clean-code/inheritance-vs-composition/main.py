"""Ana Silva's bookings and returns for one week.

Run: python3 main.py
"""



from desk import Customer, book, return_vehicle
from pricing import InsuredGpsChildSeatCar, InsuredVan
from vehicles import Bike, Truck


def euros(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def main() -> None:
    ana = Customer("Ana Silva", {"B", "C"})
    car = InsuredGpsChildSeatCar("AB-123", 4500)
    van = InsuredVan("VN-321", 7000)
    truck = Truck("TR-789", 9000)
    bike = Bike("BK-1", 1000)

    for vehicle, days in [(car, 3), (van, 2), (truck, 2), (bike, 2)]:
        b = book(ana, vehicle, days)
        print(
            f"{b.customer}  {b.plate:<6}  {b.days} days"
            f"  total {euros(b.total):>6}  deposit {euros(b.deposit):>6}"
        )

    for vehicle, litres in [(car, 30), (van, 25), (truck, 60)]:
        fuel = return_vehicle(vehicle, litres)
        print(f"{vehicle.plate:<6} returned  {litres} l  fuel {euros(fuel):>6}")


if __name__ == "__main__":
    main()
