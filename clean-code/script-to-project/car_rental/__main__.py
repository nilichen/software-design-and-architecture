from .booking import book
from .errors import CarRentalError
from .fleet_db import count_bookings, open_fleet
from .pricing import format_eur

REQUESTS = [
    ("Ana Silva", "AB-123", 3),
    ("Ana Silva", "ZZ-999", 2),
    ("Ana Silva", "CD-456", 0),
    ("Ana Silva", "CD-456", 5),
]


def main(requests: list[tuple[str, str, int]]) -> None:
    with open_fleet() as con:
        for customer, plate, days in requests:
            try:
                booking = book(con, customer, plate, days)
            except CarRentalError as e:
                print(f"{customer}: {plate} for {days} days -> refused: {e}")
                continue
            price = format_eur(booking.price_cents)
            print(f"{customer}: {plate} for {days} days = {price}")
        print("bookings saved:", count_bookings(con))


if __name__ == "__main__":
    main(REQUESTS)
