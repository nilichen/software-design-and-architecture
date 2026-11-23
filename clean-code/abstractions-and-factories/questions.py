"""The questions the app asks while booking. `read` defaults to the keyboard."""

from collections.abc import Callable

Read = Callable[[str], str]


def ask_fuel_plan(read: Read = input) -> str:
    while True:
        answer = read("Fuel plan (full-to-full/prepaid): ")
        if answer in ("full-to-full", "prepaid"):
            return answer
        print("Please choose one of: full-to-full, prepaid")


def ask_mileage_plan(read: Read = input) -> str:
    while True:
        answer = read("Mileage (limited/unlimited): ")
        if answer in ("limited", "unlimited"):
            return answer
        print("Please choose one of: limited, unlimited")


def ask_days(
    read: Read = input,
    minimum: int = 1,
    maximum: int | None = None,
    forbidden: set[int] | None = None,
) -> int:
    while True:
        answer = read("Days: ")
        if not answer.lstrip("-").isdigit():
            print("Please enter a whole number")
            continue
        value = int(answer)
        if value < minimum:
            print(f"Please enter a whole number, {minimum} or more")
        elif maximum is not None and value > maximum:
            print(f"Please enter a whole number, {maximum} or less")
        elif forbidden is not None and value in forbidden:
            print(f"{value} is not allowed")
        else:
            return value


def ask_driver_age(read: Read = input) -> int:
    while True:
        answer = read("Driver age: ")
        if answer.isdigit() and int(answer) > 0:
            return int(answer)
        print("Please enter a whole number, 1 or more")
