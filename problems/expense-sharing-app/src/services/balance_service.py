from typing import Dict, List, Set, Tuple
from decimal import Decimal
from collections import defaultdict
from src.models.balance import Balance
from src.models.group import Group
from src.exceptions.custom_exceptions import UserNotFoundException

class BalanceService:
    def __init__(self):
        # Stores net balances: balances[from_user][to_user] = amount
        self.balances: Dict[str, Dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    
    def update_balance(self, from_user: str, to_user: str, amount: Decimal) -> None:
        """Update balance where from_user owes to_user the given amount"""
        if from_user == to_user:
            return
        
        # Simplify by maintaining net balances
        self.balances[from_user][to_user] += amount
        self.balances[to_user][from_user] -= amount
        
        # Clean up zero balances
        if abs(self.balances[from_user][to_user]) < Decimal('0.01'):
            del self.balances[from_user][to_user]
            if not self.balances[from_user]:
                del self.balances[from_user]
        
        if abs(self.balances[to_user][from_user]) < Decimal('0.01'):
            if from_user in self.balances[to_user]:
                del self.balances[to_user][from_user]
            if not self.balances[to_user]:
                del self.balances[to_user]
    
    def get_user_balances(self, user_id: str) -> List[Balance]:
        """Get all non-zero balances for a user"""
        balances = []
        
        # Check what this user owes to others
        if user_id in self.balances:
            for to_user, amount in self.balances[user_id].items():
                if amount > Decimal('0'):
                    balances.append(Balance(user_id, to_user, amount))
        
        # Check what others owe to this user
        for from_user, user_balances in self.balances.items():
            if from_user != user_id and user_id in user_balances:
                amount = user_balances[user_id]
                if amount > Decimal('0'):
                    balances.append(Balance(from_user, user_id, amount))
        
        return balances
    
    def get_all_balances(self) -> List[Balance]:
        """Get all non-zero balances in the system"""
        balances = []
        for from_user, user_balances in self.balances.items():
            for to_user, amount in user_balances.items():
                if amount > Decimal('0'):
                    balances.append(Balance(from_user, to_user, amount))
        return balances
    
    def simplify_group_balances(self, group: Group) -> List[Balance]:
        """Implement smart settlement for a group"""
        # Build net balance graph for group members only
        net_balance = defaultdict(Decimal)
        
        # Calculate net balance for each user in the group
        for member in group.members:
            if member in self.balances:
                for to_user, amount in self.balances[member].items():
                    if to_user in group.members and amount > Decimal('0'):
                        net_balance[member] -= amount
                        net_balance[to_user] += amount
        
        # Separate creditors and debtors
        creditors = []  # (user_id, amount)
        debtors = []    # (user_id, amount)
        
        for user_id, balance in net_balance.items():
            if balance > Decimal('0'):
                creditors.append((user_id, balance))
            elif balance < Decimal('0'):
                debtors.append((user_id, -balance))
        
        # Sort to optimize matching
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1], reverse=True)
        
        # Simplify debts
        simplified_balances = []
        i, j = 0, 0
        
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt_amount = debtors[i]
            creditor_id, credit_amount = creditors[j]
            
            settlement_amount = min(debt_amount, credit_amount)
            if settlement_amount > Decimal('0.01'):
                simplified_balances.append(Balance(debtor_id, creditor_id, settlement_amount))
            
            debtors[i] = (debtor_id, debt_amount - settlement_amount)
            creditors[j] = (creditor_id, credit_amount - settlement_amount)
            
            if debtors[i][1] < Decimal('0.01'):
                i += 1
            if creditors[j][1] < Decimal('0.01'):
                j += 1
        
        return simplified_balances