from typing import List, Optional
from src.models.board import Board, Privacy
from src.models.user import User
from src.repositories.in_memory_repository import InMemoryRepository
from src.exceptions.custom_exceptions import ResourceNotFoundException, InvalidOperationException


class BoardService:
    """Service for managing boards"""
    
    def __init__(self):
        self.board_repository = InMemoryRepository[Board]()
        self.user_repository = InMemoryRepository[User]()

    def create_board(self, name: str, privacy: Privacy = Privacy.PUBLIC, creator_id: Optional[str] = None) -> Board:
        """Create a new board"""
        board = Board(name=name, privacy=privacy)
        
        # Add creator as a member if provided
        if creator_id:
            if self.user_repository.exists(creator_id):
                board.add_member(creator_id)
        
        return self.board_repository.save(board.id, board)

    def get_board(self, board_id: str) -> Board:
        """Get a board by ID"""
        board = self.board_repository.find_by_id(board_id)
        if not board:
            raise ResourceNotFoundException(f"Board with ID {board_id} not found")
        return board

    def get_all_boards(self) -> List[Board]:
        """Get all boards"""
        return self.board_repository.find_all()

    def delete_board(self, board_id: str) -> bool:
        """Delete a board and all its lists"""
        board = self.get_board(board_id)
        
        # In a real implementation, we would also delete all lists and cards
        # For now, we'll just delete the board
        return self.board_repository.delete(board_id)

    def add_member(self, board_id: str, user_id: str) -> Board:
        """Add a member to a board"""
        board = self.get_board(board_id)
        
        # Verify user exists
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        
        board.add_member(user_id)
        return self.board_repository.update(board_id, board)

    def remove_member(self, board_id: str, user_id: str) -> Board:
        """Remove a member from a board"""
        board = self.get_board(board_id)
        board.remove_member(user_id)
        return self.board_repository.update(board_id, board)

    def update_board(self, board_id: str, name: Optional[str] = None, privacy: Optional[Privacy] = None) -> Board:
        """Update board attributes"""
        board = self.get_board(board_id)
        board.update_attributes(name=name, privacy=privacy)
        return self.board_repository.update(board_id, board)

    def is_member(self, board_id: str, user_id: str) -> bool:
        """Check if a user is a member of a board"""
        board = self.get_board(board_id)
        return board.is_member(user_id)

    def add_user(self, user: User) -> User:
        """Add a user to the system"""
        return self.user_repository.save(user.user_id, user)

    def get_user(self, user_id: str) -> User:
        """Get a user by ID"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        return user