from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    """Abstract base class. Every payment method must implement these."""

    MAX_AMOUNT: float | None = None

    def __init__(self, owner: str):
        if not owner or not owner.strip():
            raise ValueError("Owner name cannot be empty")
        self._owner = owner.strip()
        self._transactions: list[float] = []

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def transactions(self) -> list[float]:
        return list(self._transactions)

    @abstractmethod
    def validate(self, amount: float) -> bool:
        """Return True if this method can pay the given amount."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process the payment and return a receipt string."""

    @abstractmethod
    def refund(self, amount: float) -> str:
        """Reverse a previous payment and return a receipt string."""

    @abstractmethod
    def fee_rate(self) -> float:
        """Processing fee as a fraction, e.g. 0.02 for 2%."""

    def total_with_fee(self, amount: float) -> float:
        # Shared logic: every subclass inherits this unchanged.
        return round(amount * (1 + self.fee_rate()), 2)

    def _check_positive(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(owner={self._owner!r})"
