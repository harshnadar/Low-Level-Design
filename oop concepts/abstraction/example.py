from abc import ABC, abstractmethod

# Abstract class for Payment
class Payment(ABC):
    def __init__(self, amount):
        self.amount = amount
    
    @abstractmethod
    def pay(self):
        pass

# Implementing payment methods
class CreditCardPayment(Payment):
    def pay(self):
        print(f"Paid {self.amount} using Credit Card")

class PayPalPayment(Payment):
    def pay(self):
        print(f"Paid {self.amount} using PayPal")

if __name__ == "__main__":
    # Creating instances of different payment methods
    credit_card_payment = CreditCardPayment(100.50)
    credit_card_payment.pay()

    paypal_payment = PayPalPayment(200.75)
    paypal_payment.pay()
