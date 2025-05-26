from src.expense_sharing_app import ExpenseSharingApp
from src.models.user import User
from src.models.expense import ExpenseType
from src.services.user_service import UserService
from src.services.balance_service import BalanceService
from src.services.expense_service import ExpenseService
from src.services.group_service import GroupService
from decimal import Decimal


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