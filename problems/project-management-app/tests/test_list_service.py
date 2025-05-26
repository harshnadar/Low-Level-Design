import pytest
from src.services.board_service import BoardService
from src.services.list_service import ListService
from src.models.board import Board
from src.models.list import TaskList
from src.exceptions.custom_exceptions import ResourceNotFoundException
from src.utils.id_generator import IdGenerator


class TestListService:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        IdGenerator.reset()
        self.board_service = BoardService()
        self.list_service = ListService(self.board_service.board_repository)
        
        # Create a test board
        self.board = self.board_service.create_board("Test Board")

    def test_create_list(self):
        """Test creating a new list"""
        task_list = self.list_service.create_list(self.board.id, "Test List")
        
        assert task_list.name == "Test List"
        assert task_list.board_id == self.board.id
        assert task_list.id == "list_1"
        
        # Verify list was added to board
        updated_board = self.board_service.get_board(self.board.id)
        assert task_list.id in updated_board.lists

    def test_get_list(self):
        """Test getting a list by ID"""
        created_list = self.list_service.create_list(self.board.id, "Test List")
        retrieved_list = self.list_service.get_list(created_list.id)
        
        assert retrieved_list.id == created_list.id
        assert retrieved_list.name == created_list.name

    def test_delete_list(self):
        """Test deleting a list"""
        task_list = self.list_service.create_list(self.board.id, "Test List")
        list_id = task_list.id
        
        assert self.list_service.delete_list(list_id) == True
        
        with pytest.raises(ResourceNotFoundException):
            self.list_service.get_list(list_id)
        
        # Verify list was removed from board
        updated_board = self.board_service.get_board(self.board.id)
        assert list_id not in updated_board.lists

    def test_modify_list(self):
        """Test modifying list attributes"""
        task_list = self.list_service.create_list(self.board.id, "Test List")
        
        updated_list = self.list_service.update_list(task_list.id, "Updated List")
        
        assert updated_list.name == "Updated List"

    def test_add_card_to_list(self):
        """Test adding a card to a list"""
        task_list = self.list_service.create_list(self.board.id, "Test List")
        
        updated_list = self.list_service.add_card_to_list(task_list.id, "card_1")
        
        assert "card_1" in updated_list.cards

    def test_remove_card_from_list(self):
        """Test removing a card from a list"""
        task_list = self.list_service.create_list(self.board.id, "Test List")
        self.list_service.add_card_to_list(task_list.id, "card_1")
        
        updated_list = self.list_service.remove_card_from_list(task_list.id, "card_1")
        
        assert "card_1" not in updated_list.cards