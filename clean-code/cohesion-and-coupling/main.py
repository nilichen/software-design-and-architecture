"""Car-rental desk: prices the day's bookings, takes payment, sends the emails.

Run: python3 main.py
"""

from dataclasses import dataclass
from datetime import date

import card_provider

try:
    import numpy as np
except ImportError:  # not installed on every machine
    np = None

CENTS_PER_KM = 25
CREDIT_FEE_PERCENT = 2
VEHICLES = {  # vehicle type -> (cents per day, free km per day)
    "compact": (3_000, 100),
    "suv": (4_500, 100),
    "van": (6_000, 50),
}

# The day's bookings, as they come out of the booking form.
BOOKINGS = [
    {
        "id": "B1", "name": "Ana Silva", "email": "ana.silva@example.com",
        "vehicle": "suv", "days": 3, "km": 450, "pickup": date(2026, 12, 1),
        "extras": [("gps", 1_000)], "dropped": [], "discount": 10,
        "method": "credit", "card": "4000000000001111", "cancelled": False,
    },
    {
        "id": "B2", "name": "Ana Silva", "email": "ana.silva@example.com",
        "vehicle": "van", "days": 2, "km": 180, "pickup": date(2026, 12, 8),
        "extras": [("gps", 1_000), ("child_seat", 500)], "dropped": ["gps"],
        "discount": 0, "method": "debit", "card": "5000000000002222",
        "cancelled": False,
    },
    {
        "id": "B3", "name": "Ana Silva", "email": "ana.silva@example.com",
        "vehicle": "compact", "days": 2, "km": 150, "pickup": date(2026, 12, 20),
        "extras": [], "dropped": [], "discount": 0,
        "method": "debit", "card": "5000000000002222", "cancelled": True,
    },
]


@dataclass
class Customer:
    name: str
    email: str


class Booking:
    def __init__(self, booking_id, customer, vehicle_type, days, km, pickup):
        self.booking_id = booking_id
        self.customer = customer
        self.vehicle_type = vehicle_type
        self.days = days
        self.km = km
        self.pickup = pickup
        self.extra_names: list[str] = []
        self.extra_prices: list[int] = []  # cents, same order as extra_names
        self.price = 0  # cents
        self.txn = ""

    def add_extra(self, name, price):
        self.extra_names.append(name)
        self.extra_prices.append(price)

    def pay(self, card_number, method):
        if method == "debit":
            self.txn = card_provider.charge(card_number, self.price)
            return self.price
        elif method == "credit":
            amount = self.price + self.price * CREDIT_FEE_PERCENT // 100
            self.txn = card_provider.charge(card_number, amount)
            return amount
        raise ValueError(f"unknown payment method {method}")


def compute_rental_cost(vehicle_type, days, km):
    rate, free_km = VEHICLES[vehicle_type]
    extra_km = max(0, km - free_km * days)
    return rate * days + extra_km * CENTS_PER_KM


def add_up(prices):
    if np is not None:
        return int(np.sum(prices))
    return sum(prices)


def apply_discount(booking, percent):
    booking.price -= booking.price * percent // 100
    return booking.price


def euros(cents):
    return f"€{cents // 100}.{cents % 100:02d}"


def send_confirmation(booking, amount):
    print(f"  email to {booking.customer.email}: {booking.booking_id} confirmed, "
          f"{euros(amount)} paid")


def write_invoice(booking, amount):
    print(f"  invoice for {booking.booking_id}: {euros(amount)}")


def send_reminder(booking):
    print(f"  reminder to {booking.customer.email}: pick-up on {booking.pickup}")


def main():
    for row in BOOKINGS:
        customer = Customer(row["name"], row["email"])
        booking = Booking(row["id"], customer, row["vehicle"], row["days"],
                          row["km"], row["pickup"])
        for name, price in row["extras"]:
            booking.add_extra(name, price)
        for name in row["dropped"]:  # changed their mind at the desk
            booking.extra_names.remove(name)

        rental = compute_rental_cost(booking.vehicle_type, booking.days, booking.km)
        booking.price = add_up([rental, *booking.extra_prices])
        print(f"{booking.booking_id} for {booking.customer.name}: "
              f"{booking.vehicle_type}, {booking.days} days, {booking.km} km")
        print(f"  rental {euros(rental)}")
        for name, price in zip(booking.extra_names, booking.extra_prices):
            print(f"  {name} {euros(price)}")
        if row["discount"]:
            quote = apply_discount(booking, row["discount"])
            print(f"  quote {euros(quote)} ({row['discount']}% off)")
        else:
            print(f"  quote {euros(booking.price)}")

        # checkout
        if row["discount"]:
            apply_discount(booking, row["discount"])
        amount = booking.pay(row["card"], row["method"])
        send_confirmation(booking, amount)
        write_invoice(booking, amount)
        send_reminder(booking)

        if row["cancelled"]:
            card_provider.refund(booking.txn, amount)
            print(f"  email to {booking.customer.email}: "
                  f"{booking.booking_id} cancelled, {euros(amount)} refunded")


if __name__ == "__main__":
    main()
