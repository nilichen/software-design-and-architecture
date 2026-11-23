import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from .errors import VehicleNotFoundError

VEHICLES = [("AB-123", "compact"), ("CD-456", "suv")]


@contextmanager
def open_fleet() -> Iterator[sqlite3.Connection]:
    """An in-memory fleet database, closed when the with block ends."""
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE vehicles (plate TEXT PRIMARY KEY, category TEXT)")
        con.executemany("INSERT INTO vehicles VALUES (?, ?)", VEHICLES)
        con.execute(
            "CREATE TABLE bookings"
            " (customer TEXT, plate TEXT, days INTEGER, price_cents INTEGER)"
        )
        yield con
    finally:
        con.close()


def fetch_category(con: sqlite3.Connection, plate: str) -> str:
    row = con.execute(
        "SELECT category FROM vehicles WHERE plate = ?", (plate,)
    ).fetchone()
    if row is None:
        raise VehicleNotFoundError(plate)
    return row[0]


def save_booking(
    con: sqlite3.Connection, customer: str, plate: str, days: int, price_cents: int
) -> None:
    con.execute(
        "INSERT INTO bookings VALUES (?, ?, ?, ?)",
        (customer, plate, days, price_cents),
    )


def count_bookings(con: sqlite3.Connection) -> int:
    return con.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
