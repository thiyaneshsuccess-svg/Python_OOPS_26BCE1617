import pytest

from payments.base import PaymentMethod
from payments.exceptions import PaymentError, RefundError, ValidationError
from payments.methods import CreditCard, NetBanking, UPI, Wallet
from payments.processor import PaymentProcessor


def test_base_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        PaymentMethod("someone")


def test_subclass_missing_abstract_method_fails():
    class Incomplete(PaymentMethod):
        def validate(self, amount):
            return True

    with pytest.raises(TypeError):
        Incomplete("someone")


def test_empty_owner_rejected():
    with pytest.raises(ValueError):
        UPI("   ")


def test_upi_rejects_amount_over_limit():
    with pytest.raises(ValidationError):
        UPI("Ravi").pay(200_000)


def test_upi_has_no_fee():
    assert UPI("Ravi").total_with_fee(500) == 500


def test_wallet_fee_is_applied():
    wallet = Wallet("Meera", balance=1_000)
    wallet.pay(100)
    assert wallet.balance == pytest.approx(1_000 - 101)


def test_wallet_insufficient_balance():
    with pytest.raises(ValidationError):
        Wallet("Meera", balance=50).pay(100)


def test_wallet_refund_restores_balance():
    wallet = Wallet("Meera", balance=1_000)
    wallet.pay(100)
    wallet.refund(100)
    assert wallet.balance == pytest.approx(1_000)


def test_credit_card_enforces_limit():
    card = CreditCard("Asha", limit=500)
    with pytest.raises(ValidationError):
        card.pay(1_000)


def test_credit_card_refund_reduces_balance():
    card = CreditCard("Asha", limit=5_000)
    card.pay(800)
    card.refund(800)
    assert card.balance == 0


def test_net_banking_limit():
    with pytest.raises(ValidationError):
        NetBanking("Kiran").pay(60_000)


def test_refund_without_payment_fails():
    with pytest.raises(RefundError):
        UPI("Ravi").refund(300)


def test_processor_returns_failure_receipt_instead_of_raising():
    processor = PaymentProcessor()
    receipt = processor.process(UPI("Ravi"), 200_000)
    assert receipt.startswith("FAILED")


def test_processor_works_with_any_method():
    processor = PaymentProcessor()
    methods = [UPI("A"), CreditCard("B", 5_000), Wallet("C", 1_000), NetBanking("D")]
    for method in methods:
        assert processor.process(method, 100).startswith(("Paid", "Charged", "Debited", "Transferred"))


def test_exceptions_share_base_class():
    assert issubclass(ValidationError, PaymentError)
    assert issubclass(RefundError, PaymentError)
