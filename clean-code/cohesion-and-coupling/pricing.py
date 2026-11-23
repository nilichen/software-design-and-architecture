"""Price arithmetic in integer cents. Plain numbers in, plain numbers out."""

CENTS_PER_KM = 25


def rental_cost(rate: int, free_km_per_day: int, days: int, km: int) -> int:
    extra_km = max(0, km - free_km_per_day * days)
    return rate * days + extra_km * CENTS_PER_KM


def percent_off(cents: int, percent: int) -> int:
    return cents - cents * percent // 100


def euros(cents: int) -> str:
    return f"€{cents // 100}.{cents % 100:02d}"
