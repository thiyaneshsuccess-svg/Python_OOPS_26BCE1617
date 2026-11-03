from .base import PaymentMethod
from .exceptions import PaymentError


class PaymentProcessor:
    """Works with any PaymentMethod through the abstract interface only."""

    def __init__(self):
        self._log: list[str] = []

    def process(self, method: PaymentMethod, amount: float) -> str:
        try:
            receipt = method.pay(amount)
        except PaymentError as err:
            receipt = f"FAILED: {err}"
        except ValueError as err:
            receipt = f"INVALID: {err}"
        self._log.append(receipt)
        return receipt

    def process_refund(self, method: PaymentMethod, amount: float) -> str:
        try:
            receipt = method.refund(amount)
        except PaymentError as err:
            receipt = f"REFUND FAILED: {err}"
        self._log.append(receipt)
        return receipt

    @property
    def history(self) -> list[str]:
        return list(self._log)
