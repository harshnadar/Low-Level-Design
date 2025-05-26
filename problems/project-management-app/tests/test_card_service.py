import pytest
from src.services.board_service import BoardService
from src.services.list_service import ListService
from src.services.card_service import CardService
from src.models.user import User
from src.models.card import Card
from src.exceptions.custom_exceptions import ResourceNotFoundException
from src.utils.id_generator import IdGenerator


class TestCardService:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        IdGenerator.reset()
        self.board_service = BoardService()
        self.list_service = ListService(self.board_service.board_repository)
        self.card_service = CardService(
            self.list_service.list_repository,
            self.board_service.user_repository
        )
        
        # Create test data
        self.board = self.board_service.create_board("Test Board")
        self.task_list = self.list_service.create_list(self.board.id, "Test List")
        self.user = User(user_id="user1", name="Test User", email="test@test.com")
        self.board_service.add_user(self.user)

    def test_create_card(self):
        """Test creating a new card"""
        card = self.card_service.create_card(
            self.task_list.id, 
            "Test Card", 
            "Test Description"
        )
        
        assert card.name == "Test Card"
        assert card.description == "Test Description"
        assert card.list_id == self.task_list.id
        assert card.assigned_user is None
        assert card.id == "card_1"
        
        # Verify card was added to list
        updated_list = self.list_service.get_list(self.task_list.id)
        assert card.id in updated_list.cards

    def test_get_card(self):
        """Test getting a card by ID"""
        created_card = self.card_service.create_card(self.task_list.id, "Test Card")
        retrieved_card = self.card_service.get_card(created_card.id)
        
        assert retrieved_card.id == created_card.id
        assert retrieved_card.name == created_card.name

    def test_delete_card(self):
        """Test deleting a card"""
        card = self.card_service.create_card(self.task_list.id, "Test Card")
        card_id = card.id
        
        assert self.card_service.delete_card(card_id) == True
        
        with pytest.raises(ResourceNotFoundException):
            self.card_service.get_card(card_id)
        
        # Verify card was removed from list
        updated_list = self.list_service.get_list(self.task_list.id)
        assert card_id not in updated_list.cards

    def test_modify_card(self):
        """Test modifying card attributes"""
        card = self.card_service.create_card(self.task_list.id, "Test Card", "Test Description")
        
        updated_card = self.card_service.update_card(
            card.id, 
            name="Updated Card", 
            description="Updated Description"
        )
        
        assert updated_card.name == "Updated Card"
        assert updated_card.description == "Updated Description"

    def test_assign_user(self):
        """Test assigning a user to a card"""
        card = self.card_service.create_card(self.task_list.id, "Test Card")
        
        updated_card = self.card_service.assign_user(card.id, self.user.user_id)
        
        assert updated_card.assigned_user == self.user.user_id
        assert updated_card.is_assigned()

    def test_unassign_user(self):
        """Test unassigning a user from a card"""
        card = self.card_service.create_card(self.task_list.id, "Test Card")
        self.card_service.assign_user(card.id, self.user.user_id)
        
        updated_card = self.card_service.unassign_user(card.id)
        
        assert updated_card.assigned_user is None
        assert not updated_card.is_assigned()

    def test_move_card_across_lists(self):
        """Test moving a card across lists"""
        # Create another list
        another_list = self.list_service.create_list(self.board.id, "Another List")
        
        # Create a card in the first list
        card = self.card_service.create_card(self.task_list.id, "Test Card")
        
        # Move the card to another list
        moved_card = self.card_service.move_card(card.id, another_list.id)
        
        assert moved_card.list_id == another_list.id
        
        # Verify card was removed from original list
        original_list = self.list_service.get_list(self.task_list.id)
        assert card.id not in original_list.cards
        
        # Verify card was added to target list
        target_list = self.list_service.get_list(another_list.id)
        assert card.id in target_list.cards