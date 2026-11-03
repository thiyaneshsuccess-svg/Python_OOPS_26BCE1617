class PaymentError(Exception):
    """Base class for all payment errors."""


class ValidationError(PaymentError):
    """Raised when a payment cannot be processed."""


class RefundError(PaymentError):
    """Raised when a refund cannot be processed."""
