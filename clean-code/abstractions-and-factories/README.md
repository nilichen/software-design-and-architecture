# Clean Code | Abstractions, Factories, DRY, KISS, YAGNI

This folder is the app after the fixes. **[See before vs after as one diff](https://github.com/nilichen/software-design-and-architecture/commit/f1657c77da3d53ee3e101625a8776b37543650b4)** (switch to *Split* for side by side), or [browse the before](https://github.com/nilichen/software-design-and-architecture/tree/c5476663137c2892647bf64945fb2da40a001317/clean-code/abstractions-and-factories).

In the notes below, `before/x.py` means `x.py` in the before version and `after/x.py` the file as it is now. To run the before locally: `git switch --detach c547666`, then `git switch main` to come back.

## What changed

Run either version with `cd before && python3 main.py` (or `after`). Both play the same
scripted session for Ana Silva and print the same payments. The one difference in the
output is the "Pay by" prompt, which lists `apple-pay` in after/. Run the tests with
`cd after && uvx pytest`.

- **The authorizer is injected as a function.** In before/, `PaymentProcessor` in
  `payments.py` takes a string and turns it into one of the authorizers with an if/elif
  chain, so it imports every function in `authorizers.py`. In after/, `pay` receives an
  `Authorizer = Callable[[], bool]` and `payments.py` imports no authorizer at all. A
  misspelled name can no longer reach the processor, and a test passes `lambda: False`
  to see a payment refused without sending a text (`tests/test_payments.py`).
- **Processors depend on `Chargeable`, not `RentalContract`.** The processors in
  after/`payments.py` need only `total_price()` and `mark_paid()`, so that is all the
  protocol asks for. The processor no longer writes the status field itself. Before, the
  scratched-door fee in `main.py` had to be dressed up as a one-day rental, because the
  processor accepted only rentals. Now `DamageFee` in `rental.py` is a plain class that
  fits the protocol without mentioning it.
- **Processors and authorizers vary independently (the bridge idea).** The one class
  with a `pay_by_*` method per payment type became `CardProcessor`, `PayPalProcessor`,
  `DebitProcessor` and `ApplePayProcessor`, behind a `PaymentProcessor` protocol. Each
  holds only its own data (a security code, an email, nothing). Any processor works with
  any authorizer: 16 combinations from 8 pieces. The authorize check that was copied into
  every method is now one `check` function.
- **Creation is separated from use.** The if/elif chains in before/`main.py` that picked
  a payment method and an authorizer became creator functions (`create_card`,
  `create_paypal`, ...) in a `PROCESSORS` dict and the authorizer functions in an
  `AUTHORIZERS` dict. Each creator asks for its own extra input. `pay` only looks up and
  uses what the dicts hand over, and the prompts are built from the dict keys. An unknown
  answer is now asked again by `ask_choice` instead of raising `ValueError`.
- **The booking service gets its store and mailer passed in.** In before/`booking.py`,
  `BookingService` builds its own database and mail client, so any test of it writes to
  the database and sends mail. In after/, it takes a `BookingStore` and a `Mailer`
  (both protocols), and `main.py` passes the real ones. `tests/test_booking.py` passes a
  list-backed store and a fake mailer, and checks what would have been saved and sent.
- **A new payment method is new code plus one dict line (open-closed).** Apple Pay
  exists only in after/: the `ApplePayProcessor` class, `create_apple_pay`, and one line
  in `PROCESSORS`. No existing function changed. Compare the fingerprint check in
  before/, which needed a new import and a new branch in `PaymentProcessor` and an
  edited prompt in `main.py`. In after/ it is one function and one line in `AUTHORIZERS`.
- **The repeated questions became two helpers (DRY).** `ask_fuel_plan` and
  `ask_mileage_plan` were the same loop with different options, and `ask_days` and
  `ask_driver_age` the same loop with a different prompt. after/`questions.py` has
  `ask_choice(options, prompt)` and `ask_whole_number(prompt)`. A fix to a loop happens
  once, and a new question is one call.
- **Two discount fields replace a discount hierarchy (KISS).** before/`pricing.py` has a
  `Discount` protocol, `FixedDiscount` and `PercentDiscount`, and the rental applies a
  list of them in a loop. The business has one percentage and one fixed amount, so
  after/`rental.py` has `percent_off` and `fixed_off` and one line of arithmetic. The list
  also let the order change the total, and nothing said which order was right. Now the
  percentage always comes first (`tests/test_rental.py`).
- **Options nobody uses are gone (YAGNI).** `ask_days` had `maximum` and `forbidden`,
  and `PercentDiscount` had three rounding modes. The app never passed any of them, but
  each one would need tests and upkeep. All of them were deleted. A side effect: typing
  text that isn't a number for the days now gets the same message as typing 0.
