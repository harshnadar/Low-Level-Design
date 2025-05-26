from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User model representing a user in the system"""
    user_id: str
    name: str
    email: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validate user data"""
        if not self.user_id or not self.name or not self.email:
            raise ValueError("User ID, name, and email are required")
        
        if '@' not in self.email:
            raise ValueError("Invalid email format")

    def update_profile(self, name: Optional[str] = None, email: Optional[str] = None):
        """Update user profile information"""
        if name:
            self.name = name
        if email:
            if '@' not in email:
                raise ValueError("Invalid email format")
            self.email = email

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)