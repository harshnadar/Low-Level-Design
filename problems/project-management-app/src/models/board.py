from dataclasses import dataclass, field
from typing import List, Set, Optional
from enum import Enum
from src.utils.id_generator import IdGenerator


class Privacy(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


@dataclass
class Board:
    """Board model representing a project board"""
    id: str = field(default_factory=lambda: IdGenerator.generate_id("board"))
    name: str = ""
    privacy: Privacy = Privacy.PUBLIC
    url: str = field(default="")
    members: Set[str] = field(default_factory=set)  # Set of user IDs
    lists: List[str] = field(default_factory=list)  # List of list IDs

    def __post_init__(self):
        if not self.url:
            self.url = f"/boards/{self.id}"
        self._validate()

    def _validate(self):
        """Validate board data"""
        if not self.name:
            raise ValueError("Board name is required")

    def add_member(self, user_id: str):
        """Add a member to the board"""
        self.members.add(user_id)

    def remove_member(self, user_id: str):
        """Remove a member from the board"""
        if user_id in self.members:
            self.members.remove(user_id)

    def add_list(self, list_id: str):
        """Add a list to the board"""
        if list_id not in self.lists:
            self.lists.append(list_id)

    def remove_list(self, list_id: str):
        """Remove a list from the board"""
        if list_id in self.lists:
            self.lists.remove(list_id)

    def update_attributes(self, name: Optional[str] = None, privacy: Optional[Privacy] = None):
        """Update board attributes"""
        if name:
            self.name = name
        if privacy:
            self.privacy = privacy

    def is_member(self, user_id: str) -> bool:
        """Check if a user is a member of the board"""
        return user_id in self.members

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)