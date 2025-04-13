class PaymentProcessor:
    def __init__(self, card_number, amount):
        self.__card_number = self.__mask_card_number(card_number)
        self.__amount = amount

    def __mask_card_number(self, card_number):
        return "****-****-****-" + card_number[-4:]

    def process_payment(self):
        print(f"Processing payment of {self.__amount} for card {self.__card_number}")

# Usage
payment = PaymentProcessor("1234567812345678", 250.00)
payment.process_payment()