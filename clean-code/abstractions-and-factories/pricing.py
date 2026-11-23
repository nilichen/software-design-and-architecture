"""Daily rates and extras. Money is in integer cents."""

DAILY_RATES = {"limited": 4500, "unlimited": 5500}
YOUNG_DRIVER_SURCHARGE = 1000  # per day, for drivers under 25
PREPAID_FUEL = 6000


def daily_rate(mileage: str, driver_age: int) -> int:
    rate = DAILY_RATES[mileage]
    if driver_age < 25:
        rate += YOUNG_DRIVER_SURCHARGE
    return rate


def fuel_charge(fuel_plan: str) -> int:
    return PREPAID_FUEL if fuel_plan == "prepaid" else 0
