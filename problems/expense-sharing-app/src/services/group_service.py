from typing import Dict, List, Optional
from src.models.group import Group
from src.models.balance import Balance
from src.services.balance_service import BalanceService
from src.services.user_service import UserService
from src.exceptions.custom_exceptions import GroupNotFoundException, UserNotFoundException

class GroupService:
    def __init__(self, user_service: UserService, balance_service: BalanceService):
        self.user_service = user_service
        self.balance_service = balance_service
        self.groups: Dict[str, Group] = {}
    
    def create_group(self, group_id: str, name: str, member_ids: List[str]) -> Group:
        # Validate all members exist
        for member_id in member_ids:
            if not self.user_service.user_exists(member_id):
                raise UserNotFoundException(f"User {member_id} not found")
        
        group = Group(group_id, name, member_ids)
        self.groups[group_id] = group
        return group
    
    def get_group(self, group_id: str) -> Group:
        if group_id not in self.groups:
            raise GroupNotFoundException(f"Group {group_id} not found")
        return self.groups[group_id]
    
    def add_member_to_group(self, group_id: str, user_id: str) -> None:
        group = self.get_group(group_id)
        if not self.user_service.user_exists(user_id):
            raise UserNotFoundException(f"User {user_id} not found")
        group.add_member(user_id)
    
    def remove_member_from_group(self, group_id: str, user_id: str) -> None:
        group = self.get_group(group_id)
        group.remove_member(user_id)
    
    def get_simplified_group_balances(self, group_id: str) -> List[Balance]:
        group = self.get_group(group_id)
        return self.balance_service.simplify_group_balances(group)
    
    def get_user_groups(self, user_id: str) -> List[Group]:
        user_groups = []
        for group in self.groups.values():
            if group.is_member(user_id):
                user_groups.append(group)
        return user_groups