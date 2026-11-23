"""Saving a booking and confirming it by mail."""

from rental import RentalContract


class SqliteBookings:  # stands in for the real bookings database
    def __init__(self, path: str) -> None:
        self.path = path

    def save(self, rental: RentalContract) -> None:
        print(f"  saved booking {rental.plate} to {self.path}")


class SmtpMailer:  # stands in for the client of the company mail server
    def __init__(self, host: str) -> None:
        self.host = host

    def send(self, to: str, text: str) -> None:
        print(f"  mail to {to} via {self.host}: {text}")


class BookingService:
    def __init__(self) -> None:
        self.store = SqliteBookings("rentals.db")
        self.mailer = SmtpMailer("smtp.example.com")

    def book(self, rental: RentalContract, email: str) -> None:
        self.store.save(rental)
        self.mailer.send(
            email,
            f"{rental.customer}, {rental.plate} is booked for {rental.days} days"
            f" at {rental.total_price()} cents",
        )
