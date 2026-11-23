# Clean Code | From Script to Project

This folder is the app after the fixes. **[See before vs after as one diff](https://github.com/nilichen/software-design-and-architecture/commit/85e24484360d55e78c31fd5c228a8f04ef4fbded)** (switch to *Split* for side by side), or [browse the before](https://github.com/nilichen/software-design-and-architecture/tree/277fd539a05a25a7845686edbef81bf4d00bd0d2/clean-code/script-to-project).

In the notes below, `before/x.py` means `x.py` in the before version and `after/x.py` the file as it is now. To run the before locally: `git switch --detach 277fd53`, then `git switch main` to come back.

## What changed

Run the before with `cd before && python3 rental.py` and the after with
`cd after && python3 -m car_rental`. The tests run with `cd after && uvx pytest`.

- **Project layout.** The single `before/rental.py` became `after/pyproject.toml`, a `car_rental/` package and a `tests/` folder. `pyproject.toml` names the project and holds the ruff and pytest settings, so everyone on the team runs the same tools with the same rules.
- **Formatting and linting.** `after/` passes `ruff check` and `ruff format --check`. On `before/rental.py`, ruff reports seven problems, among them the wildcard import, the bare `except` and a line that may use an undefined name. Running ruff in CI catches these before review, and nobody has to comment on layout.
- **Modules, one job each.** The script's database setup, prices and booking logic are now `fleet_db.py`, `pricing.py` and `booking.py`, and the run itself is in `__main__.py`. Each file can be read and tested alone, and there is no `utils` module where unrelated helpers pile up.
- **Imports.** `from sqlite3 import *` put 210 names into `rental.py`, among them `Warning`, which shadows the built-in, and `time` and `datetime`. Any of them can silently clash with a name of our own. It also hides the `custmer` typo from ruff: ruff can only say the name "may be defined from star imports". The after writes `import sqlite3`, uses relative imports inside the package (`from .errors import ...`) and absolute ones from the tests (`from car_rental.booking import book`).
- **A clear error, raised early.** In the before, an unknown plate becomes `{}` in `get_car` and fails two calls later in `daily_rate` as `KeyError('category')`, a message that never mentions the plate. In the after, `fleet_db.fetch_category` raises `VehicleNotFoundError` right after the query. The error carries `plate`, and its message is `no vehicle with plate ZZ-999`.
- **A small hierarchy, caught by its base.** `errors.py` defines `CarRentalError` with two subclasses, `VehicleNotFoundError` and `InvalidRentalPeriodError`. `__main__.py` has a single `except CarRentalError` and reports both kinds of refusal, and each error keeps its own type and data.
- **The connection is closed.** The before opens a module-level connection and never closes it. In the after, `fleet_db.open_fleet()` is a context manager with `try`/`finally`, so the connection closes when the `with` block ends, even if a booking raises. A test checks this.
- **Fail fast, with an error that fits.** The before books 0 days and charges €0.00. In the after, `booking.book` checks `days < 1` before it touches the database and raises `InvalidRentalPeriodError`, which names the rental period, not a database or arithmetic problem.
- **Catch only what you can handle.** In the before, `save` wraps the insert in a bare `except: pass`. The insert uses the misspelled `custmer`, the bare `except` swallows the `NameError`, and no booking is ever saved: the run ends with `bookings saved: 0`. The after has no `try` around the insert, and `__main__.py` catches only `CarRentalError`, so a typo like that would crash the run at once. A test checks that a `NameError` gets through `main`.

## Behaviour differences

| Request | before | after |
|---|---|---|
| Ana Silva, AB-123, 3 days | €135.00 | €135.00 |
| Ana Silva, ZZ-999, 2 days | `error: KeyError('category')` | `refused: no vehicle with plate ZZ-999` |
| Ana Silva, CD-456, 0 days | €0.00 (booked) | `refused: a rental must be at least 1 day, got 0` |
| Ana Silva, CD-456, 5 days | €300.00 | €300.00 |
| Last line | `bookings saved: 0` (typo hidden) | `bookings saved: 2` |
