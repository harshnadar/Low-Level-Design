import pytest
from decimal import Decimal
from src.models.user import User
from src.models.group import Group
from src.services.user_service import UserService
from src.services.balance_service import BalanceService
from src.services.expense_service import ExpenseService
from src.models.expense import ExpenseType

class TestBalanceService:
    def setup_method(self):
        self.user_service = UserService()
        self.balance_service = BalanceService()
        self.expense_service = ExpenseService(self.user_service, self.balance_service)
        
        # Add test users
        self.user_service.add_user(User("u1", "User1", "user1@test.com", "1111111111"))
        self.user_service.add_user(User("u2", "User2", "user2@test.com", "2222222222"))
        self.user_service.add_user(User("u3", "User3", "user3@test.com", "3333333333"))
    
    def test_update_balance(self):
        self.balance_service.update_balance("u1", "u2", Decimal('100'))
        
        balances = self.balance_service.get_user_balances("u1")
        assert len(balances) == 1
        assert balances[0].from_user == "u1"
        assert balances[0].to_user == "u2"
        assert balances[0].amount == Decimal('100')
    
    def test_balance_cancellation(self):
        self.balance_service.update_balance("u1", "u2", Decimal('100'))
        self.balance_service.update_balance("u2", "u1", Decimal('100'))
        
        u1_balances = self.balance_service.get_user_balances("u1")
        u2_balances = self.balance_service.get_user_balances("u2")
        
        assert len(u1_balances) == 0
        assert len(u2_balances) == 0
    
    def test_net_balance(self):
        self.balance_service.update_balance("u1", "u2", Decimal('100'))
        self.balance_service.update_balance("u2", "u1", Decimal('30'))
        
        u1_balances = self.balance_service.get_user_balances("u1")
        assert len(u1_balances) == 1
        assert u1_balances[0].amount == Decimal('70')
    
    def test_group_simplification(self):
        # Create a scenario where A owes B 300 and B owes C 300
        self.balance_service.update_balance("u1", "u2", Decimal('300'))
        self.balance_service.update_balance("u2", "u3", Decimal('300'))
        
        group = Group("g1", "Test Group", ["u1", "u2", "u3"])
        simplified = self.balance_service.simplify_group_balances(group)
        
        assert len(simplified) == 1
        assert simplified[0].from_user == "u1"
        assert simplified[0].to_user == "u3"
        assert simplified[0].amount == Decimal('300')
    
    def test_complex_group_simplification(self):
        # More complex scenario
        self.balance_service.update_balance("u1", "u2", Decimal('100'))
        self.balance_service.update_balance("u1", "u3", Decimal('50'))
        self.balance_service.update_balance("u2", "u3", Decimal('80'))

        group = Group("g1", "Test Group", ["u1", "u2", "u3"])
        simplified = self.balance_service.simplify_group_balances(group)

        # Verify the simplified balances
        # u1 has net debt of 150 (100+50)
        # u2 has net credit of 20 (100-80)
        # u3 has net credit of 130 (50+80)
        # So u1 should owe 20 to u2 and 130 to u3

        assert len(simplified) == 2

        # Find the balances
        u1_to_u2 = next((b for b in simplified if b.from_user == "u1" and b.to_user == "u2"), None)
        u1_to_u3 = next((b for b in simplified if b.from_user == "u1" and b.to_user == "u3"), None)

        assert u1_to_u2 is not None
        assert u1_to_u3 is not None
        assert u1_to_u2.amount == Decimal('20')
        assert u1_to_u3.amount == Decimal('130')

        # The total simplified debt should equal the net debt of debtors
        total_simplified = sum(b.amount for b in simplified)
        assert total_simplified == Decimal('150')  # u1's total debt

    def test_group_simplification_verification(self):
        """Verify that group simplification preserves net positions"""
        # Create a complex scenario
        self.balance_service.update_balance("u1", "u2", Decimal('100'))
        self.balance_service.update_balance("u1", "u3", Decimal('50'))
        self.balance_service.update_balance("u2", "u3", Decimal('80'))
        
        # Calculate net positions before simplification
        net_positions_before = {}
        for user in ["u1", "u2", "u3"]:
            net_positions_before[user] = Decimal('0')
            
        # u1 owes 150 total
        net_positions_before["u1"] -= Decimal('150')
        # u2 receives 100, owes 80
        net_positions_before["u2"] += Decimal('20')
        # u3 receives 130 total
        net_positions_before["u3"] += Decimal('130')
        
        group = Group("g1", "Test Group", ["u1", "u2", "u3"])
        simplified = self.balance_service.simplify_group_balances(group)
        
        # Calculate net positions after simplification
        net_positions_after = {"u1": Decimal('0'), "u2": Decimal('0'), "u3": Decimal('0')}
        for balance in simplified:
            net_positions_after[balance.from_user] -= balance.amount
            net_positions_after[balance.to_user] += balance.amount
        
        # Verify net positions are preserved
        for user in ["u1", "u2", "u3"]:
            assert abs(net_positions_before[user] - net_positions_after[user]) < Decimal('0.01')