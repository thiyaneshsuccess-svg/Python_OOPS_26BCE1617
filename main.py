from payments.methods import CreditCard, NetBanking, UPI, Wallet
from payments.processor import PaymentProcessor


METHOD_TYPES = {
    "1": ("UPI", UPI),
    "2": ("Credit card", CreditCard),
    "3": ("Wallet", Wallet),
    "4": ("Net banking", NetBanking),
}


def create_method(choice: str):
    name = input("Owner name: ").strip()
    if choice == "2":
        limit = float(input("Credit limit: "))
        return CreditCard(name, limit)
    if choice == "3":
        balance = float(input("Opening wallet balance: "))
        return Wallet(name, balance)
    return METHOD_TYPES[choice][1](name)


def show_menu():
    print("\n=== Payment System ===")
    print("1. Pay with UPI")
    print("2. Pay with credit card")
    print("3. Pay with wallet")
    print("4. Pay with net banking")
    print("5. Refund a payment")
    print("6. Show history")
    print("0. Exit")


def main():
    processor = PaymentProcessor()
    # Keep methods so refunds can reach the same account object.
    accounts: dict[str, object] = {}

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        if choice in METHOD_TYPES:
            try:
                method = create_method(choice)
                amount = float(input("Amount: "))
            except ValueError as err:
                print(f"Input error: {err}")
                continue
            accounts[f"{method.owner}:{choice}"] = method
            print(processor.process(method, amount))

        elif choice == "5":
            key = input("Account key (owner:method-number): ").strip()
            if key not in accounts:
                print("No account with that key. Make a payment first.")
                continue
            try:
                amount = float(input("Refund amount: "))
            except ValueError:
                print("Please enter a number.")
                continue
            print(processor.process_refund(accounts[key], amount))

        elif choice == "6":
            if not processor.history:
                print("No transactions yet.")
            for entry in processor.history:
                print(" -", entry)

        else:
            print("Unknown option, try again.")


if __name__ == "__main__":
    main()
