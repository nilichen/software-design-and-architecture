import sqlite3

import pytest

import car_rental.__main__ as app
from car_rental.booking import book
from car_rental.errors import InvalidRentalPeriodError, VehicleNotFoundError
from car_rental.fleet_db import count_bookings, open_fleet


def test_booking_is_priced_and_saved():
    with open_fleet() as con:
        booking = book(con, "Ana Silva", "AB-123", 3)
        assert booking.price_cents == 13_500
        assert count_bookings(con) == 1


def test_unknown_plate_raises_with_the_plate():
    with open_fleet() as con, pytest.raises(VehicleNotFoundError) as exc:
        book(con, "Ana Silva", "ZZ-999", 2)
    assert exc.value.plate == "ZZ-999"


def test_zero_days_fails_before_touching_the_database():
    # No connection at all: the check has to run before any query.
    with pytest.raises(InvalidRentalPeriodError):
        book(None, "Ana Silva", "AB-123", 0)


def test_connection_is_closed_even_when_booking_fails():
    with pytest.raises(VehicleNotFoundError), open_fleet() as con:
        book(con, "Ana Silva", "ZZ-999", 2)
    with pytest.raises(sqlite3.ProgrammingError):
        con.execute("SELECT 1")


def test_main_reports_package_errors_and_keeps_going(capsys):
    app.main([("Ana Silva", "ZZ-999", 2), ("Ana Silva", "AB-123", 3)])
    out = capsys.readouterr().out
    assert "refused: no vehicle with plate ZZ-999" in out
    assert "bookings saved: 1" in out


def test_main_lets_programming_errors_through(monkeypatch):
    # A typo inside book() raises NameError. main() must not swallow it.
    def broken_book(*args):
        raise NameError("name 'custmer' is not defined")

    monkeypatch.setattr(app, "book", broken_book)
    with pytest.raises(NameError):
        app.main([("Ana Silva", "AB-123", 3)])
