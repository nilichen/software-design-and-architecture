"""Book a car for Ana Silva and pay, from a scripted session: python3 main.py"""

from collections.abc import Callable

from authorizers import (
    authorize_fingerprint,
    authorize_google,
    authorize_robot,
    authorize_sms,
)
from booking import BookingService, SmtpMailer, SqliteBookings
from payments import (
    ApplePayProcessor,
    Authorizer,
    CardProcessor,
    Chargeable,
    DebitProcessor,
    PaymentProcessor,
    PayPalProcessor,
)
from pricing import daily_rate, fuel_charge
from questions import Read, ask_choice, ask_whole_number
from rental import DamageFee, RentalContract

CUSTOMER = "Ana Silva"
CUSTOMER_EMAIL = "ana.silva@example.com"
MEMBER_PERCENT_OFF = 10
VOUCHER = 1000
SCRATCHED_DOOR_FEE = 12000

SESSION = [
    "half",
    "prepaid",  # fuel plan: a wrong answer, then a right one
    "unlimited",  # mileage
    "0",
    "4",  # days: zero is refused
    "34",  # driver age
    "card",
    "sms",
    "123",  # pay the rental
    "paypal",
    "fingerprint",
    CUSTOMER_EMAIL,  # pay the damage fee
]


def scripted(answers: list[str]) -> Read:
    """Answer each prompt from the list, and echo it like a terminal would."""
    remaining = iter(answers)

    def read(prompt: str) -> str:
        answer = next(remaining)
        print(f"{prompt}{answer}")
        return answer

    return read


def create_card(read: Read) -> PaymentProcessor:
    return CardProcessor(read("Security code: "))


def create_paypal(read: Read) -> PaymentProcessor:
    return PayPalProcessor(read("PayPal email: "))


def create_debit(read: Read) -> PaymentProcessor:
    return DebitProcessor()


def create_apple_pay(read: Read) -> PaymentProcessor:
    return ApplePayProcessor()


PROCESSORS: dict[str, Callable[[Read], PaymentProcessor]] = {
    "card": create_card,
    "paypal": create_paypal,
    "debit": create_debit,
    "apple-pay": create_apple_pay,
}
AUTHORIZERS: dict[str, Authorizer] = {
    "sms": authorize_sms,
    "google": authorize_google,
    "robot": authorize_robot,
    "fingerprint": authorize_fingerprint,
}


def pay(chargeable: Chargeable, read: Read) -> None:
    create = PROCESSORS[ask_choice(list(PROCESSORS), "Pay by", read)]
    authorize = AUTHORIZERS[ask_choice(list(AUTHORIZERS), "Confirm by", read)]
    create(read).pay(chargeable, authorize)


def main(read: Read) -> None:
    fuel_plan = ask_choice(["full-to-full", "prepaid"], "Fuel plan", read)
    mileage = ask_choice(["limited", "unlimited"], "Mileage", read)
    days = ask_whole_number("Days", read)
    age = ask_whole_number("Driver age", read)
    rental = RentalContract(
        "AB-123",
        CUSTOMER,
        days,
        daily_rate(mileage, age),
        fuel_charge(fuel_plan),
        percent_off=MEMBER_PERCENT_OFF,
        fixed_off=VOUCHER,
    )
    booking = BookingService(
        SqliteBookings("rentals.db"), SmtpMailer("smtp.example.com")
    )
    booking.book(rental, CUSTOMER_EMAIL)
    pay(rental, read)

    # The car comes back with a scratched door.
    fee = DamageFee(rental.plate, "scratched door", SCRATCHED_DOOR_FEE)
    pay(fee, read)
    print(f"Rental {rental.status.name}, damage fee {fee.status.name}")


if __name__ == "__main__":
    main(scripted(SESSION))
