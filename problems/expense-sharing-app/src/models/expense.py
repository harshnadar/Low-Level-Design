from enum import Enum
from typing import List, Dict
from decimal import Decimal
from datetime import datetime

class ExpenseType(Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENT = "PERCENT"

class Expense:
    def __init__(self, expense_id: str, amount: Decimal, paid_by: str, 
                 expense_type: ExpenseType, participants: List[str],
                 splits: List[Decimal] = None, description: str = ""):
        self.expense_id = expense_id
        self.amount = amount
        self.paid_by = paid_by
        self.expense_type = expense_type
        self.participants = participants
        self.splits = splits or []
        self.description = description
        self.created_at = datetime.now()
        self.individual_shares: Dict[str, Decimal] = {}
    
    def __str__(self):
        return f"Expense({self.expense_id}, {self.amount}, {self.expense_type.value})"