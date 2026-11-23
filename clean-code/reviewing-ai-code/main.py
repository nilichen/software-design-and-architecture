"""Run a few fixed checkouts and print what happens. Money is in cents."""

from partner import LeasedVan
from payments import PaymentMethod, make_payer
from pricing import format_cents, weekend_deal
from rental import Customer, RentalDesk, receipt
from vehicles import Car, LeasedVanAdapter, Priced, Van, VehicleKind

CARD = "4242424242424242"
ANA = Customer(first_name="Ana", last_name="Silva", email="ana@example.com")

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


def load_fleet() -> dict[str, Priced]:
    fleet: dict[str, Priced] = {}
    for plate, kind in CARS:
        try:
            fleet[plate] = Car(VehicleKind(kind))
        except ValueError as error:
            print(f"Rejected {plate}: {error}")
    fleet["EF-789"] = Van(daily_rate_cents=9500)
    fleet["JK-345"] = LeasedVanAdapter(LeasedVan("PARTNER-7", 110.0))
    return fleet


def main() -> None:
    fleet = load_fleet()
    desk = RentalDesk(fleet)

    for plate, days, extras_cents, method, account in BOOKINGS:
        try:
            booking = desk.pick_up(plate, ANA, days, extras_cents)
        except KeyError as error:
            print(f"Checkout failed for {plate}: {error!r}")
            continue
        make_payer(PaymentMethod(method), account).pay(booking.total_cents())
        print(f"  Booking {booking.booking_id}: {receipt(booking)}")

    desk.return_car("AB-123")
    desk.rented.discard("EF-789")  # a support script fixes a record by hand

    print(f"Cars out: {desk.cars_out} of {len(fleet)}")
    print("Available:")
    for number, plate in enumerate(desk.available(), start=1):
        print(f"  {number}. {plate}")

    deal = weekend_deal(fleet["AB-123"].price(3))
    print(f"Weekend deal, AB-123 for 3 days: {format_cents(deal)}")


if __name__ == "__main__":
    main()
