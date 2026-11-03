# Payment System: Abstract Base Classes in Python

A command-line payment system that demonstrates **abstract base classes (ABCs)** in Python. An abstract `PaymentMethod` class defines the contract every payment type must follow. A `PaymentProcessor` works with any payment method through that contract, without checking which concrete class it has.

## The OOP concept

An abstract base class cannot be instantiated directly. It declares abstract methods that subclasses must implement. Python's `abc` module enforces this: if a subclass leaves out an abstract method, creating an object from it raises a `TypeError`.

This project uses ABCs for four things:

1. **A required interface.** Every payment method must implement `validate`, `pay`, `refund`, and `fee_rate`.
2. **Shared behavior.** `total_with_fee`, `_check_positive`, and the owner handling are written once in the base class and inherited.
3. **Polymorphism.** `PaymentProcessor` calls `pay` and `refund` on any `PaymentMethod` without checking its type. Adding a new method doesn't change the processor.
4. **Consistent errors.** Custom exceptions share a base class, `PaymentError`, so the processor can catch all payment failures in one place.

## Project structure

```
payment_system/
├── README.md
├── main.py                  # interactive command-line menu
├── payments/
│   ├── __init__.py
│   ├── base.py              # abstract PaymentMethod
│   ├── methods.py           # UPI, CreditCard, Wallet, NetBanking
│   ├── processor.py         # PaymentProcessor
│   └── exceptions.py        # PaymentError and subclasses
└── tests/
    ├── __init__.py
    └── test_payments.py
```

## Payment methods

| Method      | Fee rate | Rules                                                      |
|-------------|----------|------------------------------------------------------------|
| UPI         | 0%       | Maximum 100,000 per transaction                            |
| Credit card | 2%       | Running balance including fees cannot exceed the limit     |
| Wallet      | 1%       | Amount plus fee cannot exceed the balance                  |
| Net banking | 0.5%     | Maximum 50,000 per transaction                             |

Every method supports `refund`. A refund succeeds only if a matching payment is on record. Refunds use the amount including fees, so you refund what was charged.

## Requirements

- Python 3.10 or newer (the code uses `float | None` and `list[str]`)
- `pytest` for the tests

```bash
pip install pytest
```

## Running the program

From the project root:

```bash
python main.py
```

The menu lets you:

1. Pay with UPI, credit card, wallet, or net banking
2. Refund a payment by entering the account key shown in the menu
3. View the transaction history

Account keys have the form `owner:method-number`, for example `Asha:2`. Use the same key when you request a refund.

Sample session:

```
Choose an option: 2
Owner name: Asha
Credit limit: 5000
Amount: 800
Charged 816.00 to credit card of Asha

Choose an option: 5
Account key (owner:method-number): Asha:2
Refund amount: 800
Credited 816.00 back to credit card of Asha
```

## Running the tests

```bash
pytest -v
```

The tests cover:

- The base class cannot be instantiated
- A subclass missing an abstract method fails at creation
- Each method's limits and fee rules
- Refunds restore balances and reject unknown payments
- The processor returns failure receipts instead of crashing
- All custom exceptions share the `PaymentError` base class

## How the design works

```
                PaymentMethod (ABC)
                ├── validate()          [abstract]
                ├── pay()               [abstract]
                ├── refund()            [abstract]
                ├── fee_rate()          [abstract]
                ├── total_with_fee()    [shared]
                └── _check_positive()   [shared]
                       ▲       ▲       ▲       ▲
                       │       │       │       │
                     UPI  CreditCard  Wallet  NetBanking
                       ▲
                       │  uses only the interface
                PaymentProcessor
```

Adding a new method, such as `UPILite`, means writing one subclass. The processor and the menu code stay the same.

## Possible extensions

- Save transactions to a JSON file so history survives restarts
- Add a `PayLater` method that requires a monthly billing cycle
- Add a `top_up()` abstract method for wallets

## License

MIT
