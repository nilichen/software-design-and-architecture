"""Stand-in for the payment provider's client library (a web API in real life)."""

_next_id = 0


def _transaction_id() -> str:
    global _next_id
    _next_id += 1
    return f"T{_next_id}"


def charge(card_number: str, cents: int) -> str:
    txn = _transaction_id()
    print(f"  [provider] charged {cents} cents to card ...{card_number[-4:]} ({txn})")
    return txn


def refund(txn: str, cents: int) -> None:
    print(f"  [provider] refunded {cents} cents ({txn})")
