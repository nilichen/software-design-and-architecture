"""Car-rental desk: prices the day's bookings, takes payment, sends the emails.

Run: python3 main.py
"""

from datetime import date

import events
import invoices
import notifications
import payments
from pricing import euros
from rental import Customer, Extra, RentalContract, Vehicle

VEHICLES = {
    "compact": Vehicle("compact", rate=3_000, free_km=100),
    "suv": Vehicle("suv", rate=4_500, free_km=100),
    "van": Vehicle("van", rate=6_000, free_km=50),
}
PAY = {"debit": payments.pay_debit, "credit": payments.pay_credit}

# The day's bookings, as they come out of the booking form.
BOOKINGS = [
    {
        "id": "B1",
        "name": "Ana Silva",
        "email": "ana.silva@example.com",
        "vehicle": "suv",
        "days": 3,
        "km": 450,
        "pickup": date(2026, 12, 1),
        "extras": [("gps", 1_000)],
        "dropped": [],
        "discount": 10,
        "method": "credit",
        "card": "4000000000001111",
        "cancelled": False,
    },
    {
        "id": "B2",
        "name": "Ana Silva",
        "email": "ana.silva@example.com",
        "vehicle": "van",
        "days": 2,
        "km": 180,
        "pickup": date(2026, 12, 8),
        "extras": [("gps", 1_000), ("child_seat", 500)],
        "dropped": ["gps"],
        "discount": 0,
        "method": "debit",
        "card": "5000000000002222",
        "cancelled": False,
    },
    {
        "id": "B3",
        "name": "Ana Silva",
        "email": "ana.silva@example.com",
        "vehicle": "compact",
        "days": 2,
        "km": 150,
        "pickup": date(2026, 12, 20),
        "extras": [],
        "dropped": [],
        "discount": 0,
        "method": "debit",
        "card": "5000000000002222",
        "cancelled": True,
    },
]


def build_contract(row: dict, vehicles: dict[str, Vehicle]) -> RentalContract:
    contract = RentalContract(
        row["id"],
        Customer(row["name"], row["email"]),
        vehicles[row["vehicle"]],
        row["days"],
        row["km"],
        row["pickup"],
        discount_percent=row["discount"],
    )
    for name, price in row["extras"]:
        contract.add_extra(Extra(name, price))
    for name in row["dropped"]:  # changed their mind at the desk
        contract.remove_extra(name)
    return contract


def print_quote(contract: RentalContract) -> None:
    print(
        f"{contract.booking_id} for {contract.customer_name()}: "
        f"{contract.vehicle_name()}, {contract.days} days, {contract.km} km"
    )
    print(f"  rental {euros(contract.rental_price())}")
    for extra in contract.extras:
        print(f"  {extra.name} {euros(extra.price)}")
    off = f" ({contract.discount_percent}% off)" if contract.discount_percent else ""
    print(f"  quote {euros(contract.discounted_price())}{off}")


def check_out(contract: RentalContract, method: str, card: str) -> payments.Payment:
    payment = PAY[method](card, contract.discounted_price())
    events.publish(
        "booking_confirmed",
        {
            "booking_id": contract.booking_id,
            "email": contract.customer_email(),
            "amount": euros(payment.amount),
        },
    )
    notifications.send_reminder(contract.customer_email(), contract.pickup)
    return payment


def cancel(contract: RentalContract, payment: payments.Payment) -> None:
    payments.refund(payment)
    events.publish(
        "booking_cancelled",
        {
            "booking_id": contract.booking_id,
            "email": contract.customer_email(),
            "amount": euros(payment.amount),
        },
    )


def main() -> None:
    notifications.register()
    invoices.register()
    for row in BOOKINGS:
        contract = build_contract(row, VEHICLES)
        print_quote(contract)
        payment = check_out(contract, row["method"], row["card"])
        if row["cancelled"]:
            cancel(contract, payment)


if __name__ == "__main__":
    main()
