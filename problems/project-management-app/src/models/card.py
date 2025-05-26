from dataclasses import dataclass, field
from typing import Optional
from ..utils.id_generator import IdGenerator


@dataclass
class Card:
    """Card model representing a task in a list"""
    id: str = field(default_factory=lambda: IdGenerator.generate_id("card"))
    name: str = ""
    description: str = ""
    list_id: str = ""
    assigned_user: Optional[str] = None  # User ID of assigned user

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validate card data"""
        if not self.name:
            raise ValueError("Card name is required")
        if not self.list_id:
            raise ValueError("List ID is required")

    def assign_user(self, user_id: str):
        """Assign a user to the card"""
        self.assigned_user = user_id

    def unassign_user(self):
        """Unassign the user from the card"""
        self.assigned_user = None

    def update_attributes(self, name: Optional[str] = None, description: Optional[str] = None):
        """Update card attributes"""
        if name is not None:
            if not name:
                raise ValueError("Card name cannot be empty")
            self.name = name
        if description is not None:
            self.description = description

    def is_assigned(self) -> bool:
        """Check if the card is assigned to a user"""
        return self.assigned_user is not None

    def move_to_list(self, new_list_id: str):
        """Move card to a different list"""
        self.list_id = new_list_id

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)