from dataclasses import dataclass, field

from booking import BookingService
from rental import RentalContract


@dataclass
class ListStore:
    saved: list[RentalContract] = field(default_factory=list)

    def save(self, rental: RentalContract) -> None:
        self.saved.append(rental)


@dataclass
class FakeMailer:
    sent: list[tuple[str, str]] = field(default_factory=list)

    def send(self, to: str, text: str) -> None:
        self.sent.append((to, text))


def test_booking_saves_and_mails_the_customer():
    store, mailer = ListStore(), FakeMailer()
    rental = RentalContract("AB-123", "Ana Silva", days=4, daily_rate=4500)

    BookingService(store, mailer).book(rental, "ana.silva@example.com")

    assert store.saved == [rental]
    assert mailer.sent == [
        (
            "ana.silva@example.com",
            "Ana Silva, AB-123 is booked for 4 days at 18000 cents",
        )
    ]
