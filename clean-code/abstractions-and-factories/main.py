"""Book a car for Ana Silva and pay, from a scripted session: python3 main.py"""

from collections.abc import Callable


from booking import BookingService
from payments import PaymentProcessor
from pricing import FixedDiscount, PercentDiscount, daily_rate, fuel_charge
from questions import ask_days, ask_driver_age, ask_fuel_plan, ask_mileage_plan
from rental import RentalContract

CUSTOMER = "Ana Silva"
CUSTOMER_EMAIL = "ana.silva@example.com"
MEMBER_PERCENT_OFF = 10
VOUCHER = 1000
SCRATCHED_DOOR_FEE = 12000

SESSION = [
    "half", "prepaid",            # fuel plan: a wrong answer, then a right one
    "unlimited",                  # mileage
    "0", "4",                     # days: zero is refused
    "34",                         # driver age
    "card", "sms", "123",         # pay the rental
    "paypal", "fingerprint", CUSTOMER_EMAIL,  # pay the damage fee
]


def scripted(answers: list[str]) -> Callable[[str], str]:
    """Answer each prompt from the list, and echo it like a terminal would."""
    remaining = iter(answers)

    def read(prompt: str) -> str:
        answer = next(remaining)
        print(f"{prompt}{answer}")
        return answer

    return read


def pay(rental: RentalContract, read: Callable[[str], str]) -> None:
    method = read("Pay by (card/paypal/debit): ")
    processor = PaymentProcessor(read("Confirm by (sms/google/robot/fingerprint): "))
    if method == "card":
        processor.pay_by_card(rental, read("Security code: "))
    elif method == "paypal":
        processor.pay_by_paypal(rental, read("PayPal email: "))
    elif method == "debit":
        processor.pay_by_debit(rental)
    else:
        raise ValueError(f"unknown payment method {method!r}")


def main(read: Callable[[str], str]) -> None:
    fuel_plan = ask_fuel_plan(read)
    mileage = ask_mileage_plan(read)
    days = ask_days(read)
    age = ask_driver_age(read)
    rental = RentalContract(
        "AB-123",
        CUSTOMER,
        days,
        daily_rate(mileage, age),
        fuel_charge(fuel_plan),
        discounts=[PercentDiscount(MEMBER_PERCENT_OFF), FixedDiscount(VOUCHER)],
    )
    BookingService().book(rental, CUSTOMER_EMAIL)
    pay(rental, read)

    # The car comes back with a scratched door. The processor only takes
    # rentals, so the fee goes in as a one-day rental.
    fee = RentalContract(rental.plate, CUSTOMER, days=1, daily_rate=SCRATCHED_DOOR_FEE)
    pay(fee, read)
    print(f"Rental {rental.status.name}, damage fee {fee.status.name}")


if __name__ == "__main__":
    main(scripted(SESSION))
