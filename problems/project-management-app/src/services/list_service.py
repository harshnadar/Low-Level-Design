from typing import List, Optional
from src.models.list import TaskList
from src.models.board import Board
from src.repositories.in_memory_repository import InMemoryRepository
from src.exceptions.custom_exceptions import ResourceNotFoundException, InvalidOperationException


class ListService:
    """Service for managing lists"""
    
    def __init__(self, board_repository: InMemoryRepository[Board]):
        self.list_repository = InMemoryRepository[TaskList]()
        self.board_repository = board_repository

    def create_list(self, board_id: str, name: str) -> TaskList:
        """Create a new list in a board"""
        # Verify board exists
        board = self.board_repository.find_by_id(board_id)
        if not board:
            raise ResourceNotFoundException(f"Board with ID {board_id} not found")
        
        # Create the list
        task_list = TaskList(name=name, board_id=board_id)
        saved_list = self.list_repository.save(task_list.id, task_list)
        
        # Add list to board
        board.add_list(task_list.id)
        self.board_repository.update(board_id, board)
        
        return saved_list

    def get_list(self, list_id: str) -> TaskList:
        """Get a list by ID"""
        task_list = self.list_repository.find_by_id(list_id)
        if not task_list:
            raise ResourceNotFoundException(f"List with ID {list_id} not found")
        return task_list

    def get_all_lists(self) -> List[TaskList]:
        """Get all lists"""
        return self.list_repository.find_all()

    def get_lists_by_board(self, board_id: str) -> List[TaskList]:
        """Get all lists in a board"""
        board = self.board_repository.find_by_id(board_id)
        if not board:
            raise ResourceNotFoundException(f"Board with ID {board_id} not found")
        
        lists = []
        for list_id in board.lists:
            task_list = self.list_repository.find_by_id(list_id)
            if task_list:
                lists.append(task_list)
        return lists

    def delete_list(self, list_id: str) -> bool:
        """Delete a list and all its cards"""
        task_list = self.get_list(list_id)
        
        # Remove list from board
        board = self.board_repository.find_by_id(task_list.board_id)
        if board:
            board.remove_list(list_id)
            self.board_repository.update(board.id, board)
        
        # In a real implementation, we would also delete all cards
        # For now, we'll just delete the list
        return self.list_repository.delete(list_id)

    def update_list(self, list_id: str, name: str) -> TaskList:
        """Update list attributes"""
        task_list = self.get_list(list_id)
        task_list.update_name(name)
        return self.list_repository.update(list_id, task_list)

    def add_card_to_list(self, list_id: str, card_id: str) -> TaskList:
        """Add a card to a list"""
        task_list = self.get_list(list_id)
        task_list.add_card(card_id)
        return self.list_repository.update(list_id, task_list)

    def remove_card_from_list(self, list_id: str, card_id: str) -> TaskList:
        """Remove a card from a list"""
        task_list = self.get_list(list_id)
        task_list.remove_card(card_id)
        return self.list_repository.update(list_id, task_list)