from typing import List, Optional
from src.models.card import Card
from src.models.list import TaskList
from src.models.user import User
from src.repositories.in_memory_repository import InMemoryRepository
from src.exceptions.custom_exceptions import ResourceNotFoundException, InvalidOperationException


class CardService:
    """Service for managing cards"""
    
    def __init__(self, list_repository: InMemoryRepository[TaskList], user_repository: InMemoryRepository[User]):
        self.card_repository = InMemoryRepository[Card]()
        self.list_repository = list_repository
        self.user_repository = user_repository

    def create_card(self, list_id: str, name: str, description: str = "") -> Card:
        """Create a new card in a list"""
        # Verify list exists
        task_list = self.list_repository.find_by_id(list_id)
        if not task_list:
            raise ResourceNotFoundException(f"List with ID {list_id} not found")
        
        # Create the card
        card = Card(name=name, description=description, list_id=list_id)
        saved_card = self.card_repository.save(card.id, card)
        
        # Add card to list
        task_list.add_card(card.id)
        self.list_repository.update(list_id, task_list)
        
        return saved_card

    def get_card(self, card_id: str) -> Card:
        """Get a card by ID"""
        card = self.card_repository.find_by_id(card_id)
        if not card:
            raise ResourceNotFoundException(f"Card with ID {card_id} not found")
        return card

    def get_all_cards(self) -> List[Card]:
        """Get all cards"""
        return self.card_repository.find_all()

    def get_cards_by_list(self, list_id: str) -> List[Card]:
        """Get all cards in a list"""
        task_list = self.list_repository.find_by_id(list_id)
        if not task_list:
            raise ResourceNotFoundException(f"List with ID {list_id} not found")
        
        cards = []
        for card_id in task_list.cards:
            card = self.card_repository.find_by_id(card_id)
            if card:
                cards.append(card)
        return cards

    def delete_card(self, card_id: str) -> bool:
        """Delete a card"""
        card = self.get_card(card_id)
        
        # Remove card from list
        task_list = self.list_repository.find_by_id(card.list_id)
        if task_list:
            task_list.remove_card(card_id)
            self.list_repository.update(task_list.id, task_list)
        
        return self.card_repository.delete(card_id)

    def update_card(self, card_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Card:
        """Update card attributes"""
        card = self.get_card(card_id)
        card.update_attributes(name=name, description=description)
        return self.card_repository.update(card_id, card)

    def assign_user(self, card_id: str, user_id: str) -> Card:
        """Assign a user to a card"""
        card = self.get_card(card_id)
        
        # Verify user exists
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        
        card.assign_user(user_id)
        return self.card_repository.update(card_id, card)

    def unassign_user(self, card_id: str) -> Card:
        """Unassign user from a card"""
        card = self.get_card(card_id)
        card.unassign_user()
        return self.card_repository.update(card_id, card)

    def move_card(self, card_id: str, target_list_id: str) -> Card:
        """Move a card to a different list"""
        card = self.get_card(card_id)
        
        # Verify target list exists
        target_list = self.list_repository.find_by_id(target_list_id)
        if not target_list:
            raise ResourceNotFoundException(f"Target list with ID {target_list_id} not found")
        
        # Remove card from current list
        current_list = self.list_repository.find_by_id(card.list_id)
        if current_list:
            current_list.remove_card(card_id)
            self.list_repository.update(current_list.id, current_list)
        
        # Add card to target list
        target_list.add_card(card_id)
        self.list_repository.update(target_list_id, target_list)
        
        # Update card's list reference
        card.move_to_list(target_list_id)
        return self.card_repository.update(card_id, card)