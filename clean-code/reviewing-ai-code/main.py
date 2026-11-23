"""Run a few fixed checkouts and print what happens. Money is in cents."""

from datetime import date


from partner import LeasedVan
from pricing import format_cents, weekend_deal
from rental import RentalDesk
from vehicles import Car, Van

START = date(2026, 11, 20)
CARD = "4242424242424242"

CARS = [
    ("AB-123", "suv"),
    ("CD-456", "SUV"),  # typed in by hand
    ("GH-012", "truck"),
    ("LM-678", "economy"),
]

BOOKINGS = [
    # plate, days, extras in cents, payment method, account
    ("AB-123", 3, [1000], "card", CARD),
    ("EF-789", 2, [], "paypal", "ana@example.com"),
    ("JK-345", 2, [500], "card", CARD),
    ("CD-456", 3, [], "card", CARD),
    ("GH-012", 1, [], "card", CARD),
    ("ZZ-999", 3, [], "card", CARD),
]


def main() -> None:
    fleet = {plate: Car(kind) for plate, kind in CARS}
    fleet["EF-789"] = Van(9500)
    fleet["JK-345"] = LeasedVan("PARTNER-7", 110.0)
    desk = RentalDesk(fleet)

    for plate, amount, extras, method, account in BOOKINGS:
        card = account if method == "card" else None
        paypal = account if method == "paypal" else None
        try:
            booking = desk.checkout(
                plate, "Ana", "Silva", "ana@example.com", amount, extras,
                card, paypal, False, START,
            )
        except KeyError as error:
            print(f"Checkout failed for {plate}: {error!r}")
            continue
        print(f"  Booking {booking.booking_id}: {desk.receipt(booking)}")

    desk.checkout("AB-123", "", "", "", 0, [], None, None, True, START)
    desk.rented.discard("EF-789")  # a support script fixes a record by hand

    print(f"Cars out: {desk.cars_out} of {len(fleet)}")
    print("Available:")
    available = desk.available()
    for i in range(len(available)):
        print(f"  {i + 1}. {available[i]}")

    deal = weekend_deal(fleet["AB-123"].price(3))
    print(f"Weekend deal, AB-123 for 3 days: {format_cents(deal)}")


if __name__ == "__main__":
    main()
