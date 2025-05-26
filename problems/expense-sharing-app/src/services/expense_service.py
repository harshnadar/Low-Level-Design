from typing import List, Dict, Optional
from decimal import Decimal
import uuid
from src.models.expense import Expense, ExpenseType
from src.models.user import User
from src.strategies.split_strategy import SplitStrategy
from src.strategies.equal_split import EqualSplitStrategy
from src.strategies.exact_split import ExactSplitStrategy
from src.strategies.percent_split import PercentSplitStrategy
from src.services.balance_service import BalanceService
from src.services.user_service import UserService
from src.exceptions.custom_exceptions import InvalidExpenseException, UserNotFoundException

class ExpenseService:
    def __init__(self, user_service: UserService, balance_service: BalanceService):
        self.user_service = user_service
        self.balance_service = balance_service
        self.expenses: Dict[str, Expense] = {}
        self.strategies: Dict[ExpenseType, SplitStrategy] = {
            ExpenseType.EQUAL: EqualSplitStrategy(),
            ExpenseType.EXACT: ExactSplitStrategy(),
            ExpenseType.PERCENT: PercentSplitStrategy()
        }
    
    def add_expense(self, amount: Decimal, paid_by: str, expense_type: ExpenseType,
                   participants: List[str], splits: List[Decimal] = None,
                   description: str = "") -> Expense:
        # Validate users exist
        if not self.user_service.user_exists(paid_by):
            raise UserNotFoundException(f"Payer {paid_by} not found")
        
        for participant in participants:
            if not self.user_service.user_exists(participant):
                raise UserNotFoundException(f"Participant {participant} not found")
        
        # Create expense
        expense_id = str(uuid.uuid4())
        expense = Expense(expense_id, amount, paid_by, expense_type, 
                         participants, splits, description)
        
        # Calculate individual shares using strategy pattern
        strategy = self.strategies[expense_type]
        expense.individual_shares = strategy.calculate_splits(amount, participants, splits)
        
        # Update balances
        for participant, share in expense.individual_shares.items():
            if participant != paid_by:
                self.balance_service.update_balance(participant, paid_by, share)
        
        # Store expense
        self.expenses[expense_id] = expense
        
        return expense
    
    def get_user_expenses(self, user_id: str) -> List[Expense]:
        """Get all expenses where user is either payer or participant"""
        user_expenses = []
        for expense in self.expenses.values():
            if expense.paid_by == user_id or user_id in expense.participants:
                user_expenses.append(expense)
        return user_expenses
    
    def get_expense(self, expense_id: str) -> Optional[Expense]:
        return self.expenses.get(expense_id)
    
    def get_all_expenses(self) -> List[Expense]:
        return list(self.expenses.values())