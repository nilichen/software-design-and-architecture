# Clean Code | Reviewing AI-Written Code

This folder is the app after the fixes. **[See before vs after as one diff](https://github.com/nilichen/software-design-and-architecture/commit/81abff80eee4233bcc50ae9266f653515429d129)** (switch to *Split* for side by side), or [browse the before](https://github.com/nilichen/software-design-and-architecture/tree/0b583eadeb7b3fb21e57b40879aa3573aeaae621/clean-code/reviewing-ai-code).

In the notes below, `before/x.py` means `x.py` in the before version and `after/x.py` the file as it is now. To run the before locally: `git switch --detach 0b583ea`, then `git switch main` to come back.

## What changed

`before/` is a checkout an AI assistant might write for the car-rental app. It runs and looks tidy, and it has every smell from the video. `after/` is the same app after the review. Read the diff between the two folders, or run both:

```
cd before && python3 main.py
cd after && python3 main.py
cd after && uvx pytest
```

Money is in integer cents everywhere. `partner.py` stands in for a partner agency's package that we can't change, so it is the same file in both folders.

## The fixes

- **Kind as an enum.** `vehicles.py` now has `VehicleKind`, and `main.py` turns each stored string into a member when it loads the fleet. Rule: don't use a type much wider than the values that are allowed. Before, the hand-typed `"SUV"` quietly got the economy rate (€140.00 instead of €245.00). Now `VehicleKind("SUV")` raises a `ValueError` where the record enters the program.
- **Built-ins instead of hand-written loops.** In `rental.py` the extras are added with `sum()` and `available()` is one list comprehension. In `main.py`, `enumerate()` numbers the list instead of `range(len(...))`. Rule: don't rebuild what Python already has. There are fewer moving parts to check, and a reader recognises the built-in at a glance.
- **Clear names with units.** `amount` became `days`, `rental` became `rental_cents`, `extras` became `extras_cents`, `BOOKING_FEE` became `BOOKING_FEE_CENTS`, and the payment's `account` became `card_number` or `email` (`rental.py`, `pricing.py`, `payments.py`). Rule: a name says what the value is and, for money, its unit. The signature now tells you what to pass.
- **Stale comment removed.** In `pricing.py` the comment on `loyalty()` said 10% off while the code took 5%. The percentages are now the named constants `WEEKEND_PERCENT_OFF` and `LOYALTY_PERCENT_OFF`. Rule: say it in code, not in a comment that can drift. The constant is the code, so it can't go out of date.
- **A Customer object instead of loose arguments.** `first`, `last` and `email` became one frozen `Customer` dataclass in `rental.py`, and `main.py` builds Ana once. Rule: group arguments that belong together. You can no longer swap the first and last names by mistake, and a `Booking` keeps only the customer's email as its id.
- **Two functions instead of a flag.** `checkout(..., returning, ...)` became `pick_up()` and `return_car()` in `rental.py`, and `pick_up()` no longer takes or charges the payment: `main.py` charges the total with the method the customer chose. Rule: a boolean that picks the branch means two jobs in one function. Returning a car is now `desk.return_car("AB-123")` instead of a call padded with blanks. Before, passing neither a card nor a PayPal address handed out the car with nothing charged and no error. Now each payment class requires its account, so there is no `None` to forget.
- **Guard clauses and a dict instead of nesting.** `pick_up()` in `rental.py` checks the plate and the days first and raises right next to each check, so the main path is flat. In `vehicles.py` the `if`/`elif` chain of rates became the `DAILY_RATE_CENTS` dict. Rule: keep the main path flat and use data for a value-to-value mapping. Adding a kind is one line, and the truck, which has no rate yet, now fails with a `KeyError` instead of quietly paying the economy rate (€50.00).
- **No self where it isn't needed.** `new_booking_id()` never used `self`, so it is a module function in `rental.py`. The receipt kept `self.subtotal` and `self.fee` on the desk after it returned. It is now a module function with no temporaries. Rule: use `self` only for state that describes the object. The desk's fields are now just its fleet and the plates that are out.
- **The booking computes its own total, and the receipt asks for only that.** `Booking.total_cents()` in `rental.py` adds rental, fee and extras, and `receipt()` takes any `HasTotal`, a one-method `Protocol`, instead of reaching into a `Booking`'s fields. Rules: tell, don't ask, and depend on the smallest interface you need. A change to pricing touches only `Booking`, and `tests/test_rental.py` prints a receipt for a stand-in quote.
- **A computed count instead of a stored counter.** `cars_out` in `rental.py` is a property that counts `rented`, and the counter that `pick_up` and `return_car` had to keep in step is gone. Rule: don't store what you can compute. Before, a record fixed by hand left the desk saying 4 cars were out when 3 were. The property can't go stale.
- **One vehicle interface, plus an adapter.** `Car` and `Van` in `vehicles.py` both have `daily_rate_cents` and `price(days)`, and a small `Priced` protocol names what they share. The partner's `LeasedVan` has `quote(start, end)` in euros, so `LeasedVanAdapter` gives it `price(days)` in cents. Rule: things in the same role get the same interface, and a class you can't change gets wrapped. The three-way `isinstance` switch and the `start` date argument are gone from the checkout.
- **Explicit imports.** `from pricing import *` in `rental.py` became `from pricing import BOOKING_FEE_CENTS, format_cents`. Rule: import the names you use. Each name's source is visible, and the module doesn't fill up with names nobody asked for.
- **Plain payment classes.** In `payments.py`, `Payment` no longer overrides `__new__` to return its own subclasses. `CardPayment` and `PayPalPayment` are separate dataclasses that satisfy a `Payer` protocol, and `make_payer()` looks the class up in a dict keyed by the `PaymentMethod` enum. Rule: don't redefine what a language concept means. The parent no longer knows its children, adding a method doesn't mean editing a parent class, and calling a class gives you an object of that class.
- **A composed discount instead of reassignments.** In `pricing.py`, `weekend_deal` is `compose(weekend, loyalty, partial(add_fee, fee_cents=BOOKING_FEE_CENTS))` instead of four lines that reassign `price`. Rule: name a pipeline instead of reusing one variable for four different values. Each step is a function you can test, and the pipeline has a name. It gives the same €210.20 for three days in the SUV.

## Output differences

Both versions print the same checkouts for AB-123, EF-789 and JK-345 (€255.00, €195.00 and €230.00), the same error for the unknown plate ZZ-999, and the same weekend deal. The rest differs because the after removes bugs:

| | before | after |
|---|---|---|
| CD-456, kind typed as `"SUV"` | checked out at the economy rate, €140.00 | rejected when the fleet loads, so its checkout fails |
| GH-012, a truck with no rate | checked out at the economy rate, €50.00 | checkout fails with `KeyError(<VehicleKind.TRUCK: 'truck'>)` |
| Cars out after a record is fixed by hand | `4 of 6`, while 3 are out | `1 of 5`, matching the available list |

## Lint

`uvx ruff check` is clean on `after/`. On `before/` it reports F403 (`from pricing import *`) and F405 (`BOOKING_FEE` and `format_cents` may come from the star import), both in `rental.py`. Both folders select the same rules in `pyproject.toml` (`E`, `F`, `B`, `SIM`, `UP`).
