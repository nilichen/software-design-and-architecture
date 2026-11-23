import pytest

from payments import CardProcessor, DebitProcessor
from rental import DamageFee, PaymentStatus, RentalContract


def test_refused_authorizer_stops_the_payment():
    rental = RentalContract("AB-123", "Ana Silva", days=4, daily_rate=4500)

    with pytest.raises(RuntimeError, match="not authorized"):
        CardProcessor("123").pay(rental, lambda: False)

    assert rental.status is PaymentStatus.OPEN


def test_any_chargeable_can_be_paid():
    fee = DamageFee("AB-123", "scratched door", 12000)

    DebitProcessor().pay(fee, lambda: True)

    assert fee.status is PaymentStatus.PAID
