import pytest
from decimal import Decimal
from src.models.user import User
from src.models.expense import ExpenseType
from src.services.user_service import UserService
from src.services.balance_service import BalanceService
from src.services.expense_service import ExpenseService
from src.exceptions.custom_exceptions import UserNotFoundException

class TestExpenseService:
    def setup_method(self):
        self.user_service = UserService()
        self.balance_service = BalanceService()
        self.expense_service = ExpenseService(self.user_service, self.balance_service)
        
        # Add test users
        self.user_service.add_user(User("u1", "User1", "user1@test.com", "1111111111"))
        self.user_service.add_user(User("u2", "User2", "user2@test.com", "2222222222"))
        self.user_service.add_user(User("u3", "User3", "user3@test.com", "3333333333"))
        self.user_service.add_user(User("u4", "User4", "user4@test.com", "4444444444"))
    
    def test_add_equal_expense(self):
        amount = Decimal('1000')
        expense = self.expense_service.add_expense(
            amount, "u1", ExpenseType.EQUAL, 
            ["u1", "u2", "u3", "u4"]
        )
        
        assert expense.amount == amount
        assert expense.paid_by == "u1"
        assert len(expense.individual_shares) == 4
        assert expense.individual_shares["u2"] == Decimal('250.00')
    
    def test_add_exact_expense(self):
        amount = Decimal('1250')
        splits = [Decimal('370'), Decimal('880')]
        expense = self.expense_service.add_expense(
            amount, "u1", ExpenseType.EXACT,
            ["u2", "u3"], splits
        )
        
        assert expense.individual_shares["u2"] == Decimal('370.00')
        assert expense.individual_shares["u3"] == Decimal('880.00')
    
    def test_add_percent_expense(self):
        amount = Decimal('1200')
        splits = [Decimal('40'), Decimal('20'), Decimal('20'), Decimal('20')]
        expense = self.expense_service.add_expense(
            amount, "u4", ExpenseType.PERCENT,
            ["u1", "u2", "u3", "u4"], splits
        )
        
        assert expense.individual_shares["u1"] == Decimal('480.00')
        assert expense.individual_shares["u2"] == Decimal('240.00')
    
    def test_invalid_user_expense(self):
        with pytest.raises(UserNotFoundException):
            self.expense_service.add_expense(
                Decimal('100'), "invalid_user", ExpenseType.EQUAL,
                ["u1", "u2"]
            )
    
    def test_get_user_expenses(self):
        # Add multiple expenses
        self.expense_service.add_expense(
            Decimal('1000'), "u1", ExpenseType.EQUAL,
            ["u1", "u2", "u3"]
        )
        self.expense_service.add_expense(
            Decimal('500'), "u2", ExpenseType.EQUAL,
            ["u2", "u3", "u4"]
        )
        
        u1_expenses = self.expense_service.get_user_expenses("u1")
        u3_expenses = self.expense_service.get_user_expenses("u3")
        
        assert len(u1_expenses) == 1
        assert len(u3_expenses) == 2