from dataclasses import dataclass, field
from typing import List, Optional
from src.utils.id_generator import IdGenerator


@dataclass
class TaskList:
    """List model representing a list of cards in a board"""
    id: str = field(default_factory=lambda: IdGenerator.generate_id("list"))
    name: str = ""
    board_id: str = ""
    cards: List[str] = field(default_factory=list)  # List of card IDs

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validate list data"""
        if not self.name:
            raise ValueError("List name is required")
        if not self.board_id:
            raise ValueError("Board ID is required")

    def add_card(self, card_id: str):
        """Add a card to the list"""
        if card_id not in self.cards:
            self.cards.append(card_id)

    def remove_card(self, card_id: str):
        """Remove a card from the list"""
        if card_id in self.cards:
            self.cards.remove(card_id)

    def update_name(self, name: str):
        """Update list name"""
        if not name:
            raise ValueError("List name cannot be empty")
        self.name = name

    def get_card_position(self, card_id: str) -> int:
        """Get the position of a card in the list"""
        if card_id in self.cards:
            return self.cards.index(card_id)
        return -1

    def __eq__(self, other):
        if not isinstance(other, TaskList):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)