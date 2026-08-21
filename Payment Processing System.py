from abc import ABC, abstractmethod
import functools
import uuid
from datetime import datetime

# Decorator for transaction logging
def log_transaction(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        print(f"\n[LOG] Payment of Rs.{amount:.2f} via {self.strategy.name}")
        result = func(self, amount)
        print(f"[LOG] Transaction {result.txn_id} -> {result.status}")
        return result
    return wrapper

# Receipt class
class Receipt:
    def __init__(self, amount, method, status):
        self.txn_id = str(uuid.uuid4())[:8]
        self.amount = amount
        self.method = method
        self.status = status
        self.time = datetime.now()

    def __str__(self):
        return (f"----- PAYMENT RECEIPT -----\n"
                f"Txn ID : {self.txn_id}\n"
                f"Method : {self.method}\n"
                f"Amount : Rs.{self.amount:.2f}\n"
                f"Status : {self.status}\n"
                f"Time   : {self.time:%Y-%m-%d %H:%M:%S}\n"
                f"---------------------------")

# Strategy Interface
class PaymentStrategy(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

    def receipt(self, amount, status="SUCCESS"):
        return Receipt(amount, self.name, status)

# Credit Card Strategy
class CreditCardPayment(PaymentStrategy):
    name = "Credit Card"

    def __init__(self, card, cvv, expiry):
        self.card, self.cvv, self.expiry = card, cvv, expiry

    def validate(self):
        return self.card.isdigit() and len(self.card) == 16 and len(self.cvv) == 3

    def pay(self, amount):
        if not self.validate():
            return self.receipt(amount, "FAILED - Invalid Card Details")
        print(f"Charging Rs.{amount:.2f} to card ending {self.card[-4:]}")
        return self.receipt(amount)

# PayPal Strategy
class PayPalPayment(PaymentStrategy):
    name = "PayPal"

    def __init__(self, email, password):
        self.email, self.password = email, password

    def validate(self):
        return "@" in self.email and len(self.password) >= 6

    def pay(self, amount):
        if not self.validate():
            return self.receipt(amount, "FAILED - Invalid PayPal Credentials")
        print(f"Paying Rs.{amount:.2f} using PayPal")
        return self.receipt(amount)

# UPI Strategy
class UPIPayment(PaymentStrategy):
    name = "UPI"

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        return "@" in self.upi_id

    def pay(self, amount):
        if not self.validate():
            return self.receipt(amount, "FAILED - Invalid UPI ID")
        print(f"Requesting Rs.{amount:.2f} from UPI ID {self.upi_id}")
        return self.receipt(amount)

# Net Banking Strategy
class NetBankingPayment(PaymentStrategy):
    name = "Net Banking"

    def __init__(self, bank, account):
        self.bank, self.account = bank, account

    def validate(self):
        return self.account.isdigit() and len(self.account) >= 9

    def pay(self, amount):
        if not self.validate():
            return self.receipt(amount, "FAILED - Invalid Account Number")
        print(f"Debiting Rs.{amount:.2f} from {self.bank}")
        return self.receipt(amount)

# Context
class PaymentProcessor:
    _registry = {}

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy
        print(f"[CONFIG] Switched to {strategy.name}")

    @log_transaction
    def process_payment(self, amount):
        if not self.strategy:
            raise ValueError("No payment strategy configured")
        return self.strategy.pay(amount)

    @classmethod
    def register_strategy(cls, key, strategy):
        cls._registry[key] = strategy

    @classmethod
    def create(cls, key, **kwargs):
        return cls(cls._registry[key](**kwargs))

# Main Program
if __name__ == "__main__":
    PaymentProcessor.register_strategy("upi", UPIPayment)
    PaymentProcessor.register_strategy("card", CreditCardPayment)
    PaymentProcessor.register_strategy("paypal", PayPalPayment)
    PaymentProcessor.register_strategy("bank", NetBankingPayment)

    print("Available Methods:", list(PaymentProcessor._registry.keys()))

    p = PaymentProcessor.create("upi", upi_id="rahul@okhdfcbank")
    print(p.process_payment(1500))

    p.set_strategy(CreditCardPayment("1234567812345678", "123", "12/27"))
    print(p.process_payment(2500))

    p.set_strategy(PayPalPayment("bad-email", "123"))
    print(p.process_payment(500))

    p.set_strategy(NetBankingPayment("State Bank", "987654321"))
    print(p.process_payment(999.50))
