DAILY_RATES_CENTS = {"compact": 4500, "suv": 6000}


def rental_price(category: str, days: int) -> int:
    return DAILY_RATES_CENTS[category] * days


def format_eur(cents: int) -> str:
    return f"€{cents // 100}.{cents % 100:02d}"
