from decimal import Decimal

class Balance:
    def __init__(self, from_user: str, to_user: str, amount: Decimal):
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount
    
    def __str__(self):
        return f"{self.from_user} owes {self.to_user}: {self.amount:.2f}"