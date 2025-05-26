from typing import Dict, List
from decimal import Decimal

class User:
    def __init__(self, user_id: str, name: str, email: str, mobile: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.mobile = mobile
        self.balances: Dict[str, Decimal] = {}  # user_id -> amount owed
    
    def __str__(self):
        return f"User({self.user_id}, {self.name})"
    
    def __repr__(self):
        return self.__str__()