from .base import PaymentMethod
from .exceptions import RefundError, ValidationError


class UPI(PaymentMethod):
    MAX_AMOUNT = 100_000

    def validate(self, amount: float) -> bool:
        return 0 < amount <= self.MAX_AMOUNT

    def pay(self, amount: float) -> str:
        self._check_positive(amount)
        if not self.validate(amount):
            raise ValidationError(f"UPI limit is {self.MAX_AMOUNT} per transaction")
        self._transactions.append(amount)
        return f"Paid {amount:.2f} via UPI from {self.owner}"

    def refund(self, amount: float) -> str:
        if amount not in self._transactions:
            raise RefundError(f"No UPI payment of {amount:.2f} found for {self.owner}")
        self._transactions.remove(amount)
        return f"Refunded {amount:.2f} to UPI account of {self.owner}"

    def fee_rate(self) -> float:
        return 0.0


class CreditCard(PaymentMethod):
    MAX_AMOUNT = None

    def __init__(self, owner: str, limit: float):
        super().__init__(owner)
        if limit <= 0:
            raise ValueError("Credit limit must be greater than zero")
        self._limit = limit
        self._balance = 0.0

    @property
    def balance(self) -> float:
        return round(self._balance, 2)

    def validate(self, amount: float) -> bool:
        return self._balance + self.total_with_fee(amount) <= self._limit

    def pay(self, amount: float) -> str:
        self._check_positive(amount)
        if not self.validate(amount):
            raise ValidationError(f"{self.owner}: credit limit of {self._limit:.2f} exceeded")
        total = self.total_with_fee(amount)
        self._balance += total
        self._transactions.append(total)
        return f"Charged {total:.2f} to credit card of {self.owner}"

    def refund(self, amount: float) -> str:
        total = self.total_with_fee(amount)
        if total not in self._transactions:
            raise RefundError(f"No credit card charge of {total:.2f} found for {self.owner}")
        self._transactions.remove(total)
        self._balance -= total
        return f"Credited {total:.2f} back to credit card of {self.owner}"

    def fee_rate(self) -> float:
        return 0.02


class Wallet(PaymentMethod):
    MAX_AMOUNT = None

    def __init__(self, owner: str, balance: float):
        super().__init__(owner)
        if balance < 0:
            raise ValueError("Wallet balance cannot be negative")
        self._balance = balance

    @property
    def balance(self) -> float:
        return round(self._balance, 2)

    def validate(self, amount: float) -> bool:
        return self._balance >= self.total_with_fee(amount)

    def pay(self, amount: float) -> str:
        self._check_positive(amount)
        if not self.validate(amount):
            raise ValidationError(f"Insufficient wallet balance for {self.owner}")
        total = self.total_with_fee(amount)
        self._balance -= total
        self._transactions.append(total)
        return f"Debited {total:.2f} from wallet of {self.owner}, remaining {self.balance:.2f}"

    def refund(self, amount: float) -> str:
        total = self.total_with_fee(amount)
        if total not in self._transactions:
            raise RefundError(f"No wallet debit of {total:.2f} found for {self.owner}")
        self._transactions.remove(total)
        self._balance += total
        return f"Returned {total:.2f} to wallet of {self.owner}, balance {self.balance:.2f}"

    def fee_rate(self) -> float:
        return 0.01


class NetBanking(PaymentMethod):
    MAX_AMOUNT = 50_000

    def validate(self, amount: float) -> bool:
        return 0 < amount <= self.MAX_AMOUNT

    def pay(self, amount: float) -> str:
        self._check_positive(amount)
        if not self.validate(amount):
            raise ValidationError(f"Net banking limit is {self.MAX_AMOUNT} per transaction")
        total = self.total_with_fee(amount)
        self._transactions.append(total)
        return f"Transferred {total:.2f} via net banking from {self.owner}"

    def refund(self, amount: float) -> str:
        total = self.total_with_fee(amount)
        if total not in self._transactions:
            raise RefundError(f"No net banking transfer of {total:.2f} found for {self.owner}")
        self._transactions.remove(total)
        return f"Refund of {total:.2f} initiated to bank account of {self.owner}"

    def fee_rate(self) -> float:
        return 0.005
