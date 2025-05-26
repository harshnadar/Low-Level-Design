from decimal import Decimal
from src.models.user import User
from src.models.expense import ExpenseType
from src.services.user_service import UserService
from src.services.balance_service import BalanceService
from src.services.expense_service import ExpenseService
from src.services.group_service import GroupService

class ExpenseSharingApp:
    def __init__(self):
        self.user_service = UserService()
        self.balance_service = BalanceService()
        self.expense_service = ExpenseService(self.user_service, self.balance_service)
        self.group_service = GroupService(self.user_service, self.balance_service)
    
    def add_user(self, user_id: str, name: str, email: str, mobile: str) -> User:
        user = User(user_id, name, email, mobile)
        self.user_service.add_user(user)
        return user
    
    def add_expense(self, amount: float, paid_by: str, expense_type: str,
                   participants: list, splits: list = None, description: str = "") -> None:
        amount_decimal = Decimal(str(amount))
        expense_type_enum = ExpenseType(expense_type)
        
        splits_decimal = None
        if splits:
            splits_decimal = [Decimal(str(s)) for s in splits]
        
        expense = self.expense_service.add_expense(
            amount_decimal, paid_by, expense_type_enum,
            participants, splits_decimal, description
        )
        print(f"Expense added: {expense}")
    
    def show_balances(self, user_id: str = None) -> None:
        if user_id:
            balances = self.balance_service.get_user_balances(user_id)
            print(f"\nBalances for {user_id}:")
        else:
            balances = self.balance_service.get_all_balances()
            print("\nAll balances:")
        
        if not balances:
            print("No balances")
        else:
            for balance in balances:
                print(balance)
    
    def show_user_expenses(self, user_id: str) -> None:
        expenses = self.expense_service.get_user_expenses(user_id)
        print(f"\nExpenses for {user_id}:")
        for expense in expenses:
            print(f"- {expense}")
            if expense.paid_by == user_id:
                print(f"  You paid {expense.amount}")
            else:
                if user_id in expense.individual_shares:
                    print(f"  Your share: {expense.individual_shares[user_id]}")
    
    def create_group(self, group_id: str, name: str, members: list) -> None:
        group = self.group_service.create_group(group_id, name, members)
        print(f"Group created: {group.name} with members: {members}")
    
    def show_group_balances(self, group_id: str) -> None:
        simplified_balances = self.group_service.get_simplified_group_balances(group_id)
        print(f"\nSimplified balances for group {group_id}:")
        if not simplified_balances:
            print("No balances in group")
        else:
            for balance in simplified_balances:
                print(balance)

def main():
    app = ExpenseSharingApp()
    
    # Add users
    app.add_user("u1", "User1", "user1@example.com", "1234567890")
    app.add_user("u2", "User2", "user2@example.com", "2345678901")
    app.add_user("u3", "User3", "user3@example.com", "3456789012")
    app.add_user("u4", "User4", "user4@example.com", "4567890123")
    
    # Example 1: Equal split
    print("\n=== Example 1: Equal Split ===")
    app.add_expense(1000, "u1", "EQUAL", ["u1", "u2", "u3", "u4"])
    app.show_balances()
    
    # Example 2: Exact split
    print("\n=== Example 2: Exact Split ===")
    app.add_expense(1250, "u1", "EXACT", ["u2", "u3"], [370, 880])
    app.show_balances("u1")
    
    # Example 3: Percent split
    print("\n=== Example 3: Percent Split ===")
    app.add_expense(1200, "u4", "PERCENT", ["u1", "u2", "u3", "u4"], [40, 20, 20, 20])
    app.show_balances()
    
    # Create a group and show simplified balances
    print("\n=== Group Settlement ===")
    app.create_group("g1", "Friends", ["u1", "u2", "u3", "u4"])
    app.show_group_balances("g1")

if __name__ == "__main__":
    main()