import pytest
from src.services.board_service import BoardService
from src.models.board import Board, Privacy
from src.models.user import User
from src.exceptions.custom_exceptions import ResourceNotFoundException
from src.utils.id_generator import IdGenerator


class TestBoardService:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        IdGenerator.reset()
        self.board_service = BoardService()
        
        # Create test users
        self.user1 = User(user_id="user1", name="Test User 1", email="user1@test.com")
        self.user2 = User(user_id="user2", name="Test User 2", email="user2@test.com")
        
        self.board_service.add_user(self.user1)
        self.board_service.add_user(self.user2)

    def test_create_board(self):
        """Test creating a new board"""
        board = self.board_service.create_board("Test Board", Privacy.PUBLIC, self.user1.user_id)
        
        assert board.name == "Test Board"
        assert board.privacy == Privacy.PUBLIC
        assert board.url == f"/boards/{board.id}"
        assert self.user1.user_id in board.members
        assert board.id == "board_1"

    def test_get_board(self):
        """Test getting a board by ID"""
        created_board = self.board_service.create_board("Test Board")
        retrieved_board = self.board_service.get_board(created_board.id)
        
        assert retrieved_board.id == created_board.id
        assert retrieved_board.name == created_board.name

    def test_get_board_not_found(self):
        """Test getting a non-existent board"""
        with pytest.raises(ResourceNotFoundException):
            self.board_service.get_board("non_existent_id")

    def test_delete_board(self):
        """Test deleting a board"""
        board = self.board_service.create_board("Test Board")
        board_id = board.id
        
        assert self.board_service.delete_board(board_id) == True
        
        with pytest.raises(ResourceNotFoundException):
            self.board_service.get_board(board_id)

    def test_add_member(self):
        """Test adding a member to a board"""
        board = self.board_service.create_board("Test Board")
        
        updated_board = self.board_service.add_member(board.id, self.user1.user_id)
        
        assert self.user1.user_id in updated_board.members
        assert self.board_service.is_member(board.id, self.user1.user_id)

    def test_remove_member(self):
        """Test removing a member from a board"""
        board = self.board_service.create_board("Test Board", creator_id=self.user1.user_id)
        self.board_service.add_member(board.id, self.user2.user_id)
        
        updated_board = self.board_service.remove_member(board.id, self.user2.user_id)
        
        assert self.user2.user_id not in updated_board.members
        assert not self.board_service.is_member(board.id, self.user2.user_id)

    def test_modify_board_attributes(self):
        """Test modifying board attributes"""
        board = self.board_service.create_board("Test Board", Privacy.PUBLIC)
        
        updated_board = self.board_service.update_board(
            board.id, 
            name="Updated Board", 
            privacy=Privacy.PRIVATE
        )
        
        assert updated_board.name == "Updated Board"
        assert updated_board.privacy == Privacy.PRIVATE