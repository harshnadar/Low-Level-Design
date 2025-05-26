from typing import Dict, List, Optional
from src.models.user import User
from src.exceptions.custom_exceptions import UserNotFoundException

class UserService:
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user
    
    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise UserNotFoundException(f"User {user_id} not found")
        return self.users[user_id]
    
    def get_all_users(self) -> List[User]:
        return list(self.users.values())
    
    def user_exists(self, user_id: str) -> bool:
        return user_id in self.users