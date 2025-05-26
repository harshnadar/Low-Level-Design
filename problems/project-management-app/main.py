from src.services.board_service import BoardService
from src.services.list_service import ListService
from src.services.card_service import CardService
from src.models.user import User
from src.models.board import Privacy


def demonstrate_multiple_boards():
    """Demonstrate creating and managing multiple boards"""
    
    # Initialize services
    board_service = BoardService()
    list_service = ListService(board_service.board_repository)
    card_service = CardService(
        list_service.list_repository,
        board_service.user_repository
    )
    
    # Create users
    user1 = User(user_id="u1", name="John Doe", email="john@example.com")
    user2 = User(user_id="u2", name="Jane Smith", email="jane@example.com")
    user3 = User(user_id="u3", name="Bob Wilson", email="bob@example.com")
    
    board_service.add_user(user1)
    board_service.add_user(user2)
    board_service.add_user(user3)
    
    # Create multiple boards for different projects
    board1 = board_service.create_board("Web Development Project", Privacy.PRIVATE, user1.user_id)
    board2 = board_service.create_board("Mobile App Project", Privacy.PUBLIC, user2.user_id)
    board3 = board_service.create_board("Marketing Campaign", Privacy.PUBLIC, user3.user_id)
    
    print("=== Created Multiple Boards ===")
    print(f"Board 1: {board1.name} (ID: {board1.id}, Privacy: {board1.privacy.value})")
    print(f"Board 2: {board2.name} (ID: {board2.id}, Privacy: {board2.privacy.value})")
    print(f"Board 3: {board3.name} (ID: {board3.id}, Privacy: {board3.privacy.value})")
    
    # Add different members to different boards
    board_service.add_member(board1.id, user2.user_id)  # Add Jane to Web Dev project
    board_service.add_member(board2.id, user1.user_id)  # Add John to Mobile App project
    board_service.add_member(board2.id, user3.user_id)  # Add Bob to Mobile App project
    
    # Create lists for each board
    # Board 1 - Web Development
    web_todo = list_service.create_list(board1.id, "Backlog")
    web_progress = list_service.create_list(board1.id, "In Development")
    web_review = list_service.create_list(board1.id, "Code Review")
    web_done = list_service.create_list(board1.id, "Deployed")
    
    # Board 2 - Mobile App
    mobile_todo = list_service.create_list(board2.id, "To Do")
    mobile_design = list_service.create_list(board2.id, "Design")
    mobile_dev = list_service.create_list(board2.id, "Development")
    mobile_testing = list_service.create_list(board2.id, "Testing")
    
    # Board 3 - Marketing
    marketing_ideas = list_service.create_list(board3.id, "Ideas")
    marketing_active = list_service.create_list(board3.id, "Active Campaigns")
    marketing_complete = list_service.create_list(board3.id, "Completed")
    
    # Create cards in different boards
    # Web Development cards
    card1 = card_service.create_card(web_todo.id, "Setup CI/CD pipeline", "Configure GitHub Actions")
    card2 = card_service.create_card(web_todo.id, "Implement user authentication", "Add JWT tokens")
    card3 = card_service.create_card(web_progress.id, "Create REST API", "Build RESTful endpoints")
    
    # Mobile App cards
    card4 = card_service.create_card(mobile_design.id, "Design home screen", "Create mockups")
    card5 = card_service.create_card(mobile_dev.id, "Implement push notifications", "FCM integration")
    
    # Marketing cards
    card6 = card_service.create_card(marketing_ideas.id, "Social media campaign", "Plan Instagram strategy")
    card7 = card_service.create_card(marketing_active.id, "Email newsletter", "Monthly product updates")
    
    # Assign users to cards across different boards
    card_service.assign_user(card1.id, user1.user_id)
    card_service.assign_user(card3.id, user2.user_id)
    card_service.assign_user(card5.id, user1.user_id)
    card_service.assign_user(card7.id, user3.user_id)
    
    # Display all boards
    print("\n=== All Boards in the System ===")
    all_boards = board_service.get_all_boards()
    for board in all_boards:
        print(f"\nBoard: {board.name} (ID: {board.id})")
        print(f"  URL: {board.url}")
        print(f"  Privacy: {board.privacy.value}")
        print(f"  Members: {len(board.members)} users")
        
        # Show lists in each board
        lists = list_service.get_lists_by_board(board.id)
        print(f"  Lists ({len(lists)}):")
        for task_list in lists:
            cards = card_service.get_cards_by_list(task_list.id)
            print(f"    - {task_list.name}: {len(cards)} cards")
    
    # Demonstrate board isolation - cards can only move within the same board
    print("\n=== Moving Cards Within Same Board ===")
    # Move a card within the web development board
    card_service.move_card(card1.id, web_progress.id)
    print(f"Moved '{card1.name}' from '{web_todo.name}' to '{web_progress.name}'")
    
    # Show specific board details
    print("\n=== Detailed View: Web Development Project ===")
    web_board = board_service.get_board(board1.id)
    for list_id in web_board.lists:
        task_list = list_service.get_list(list_id)
        print(f"\n{task_list.name}:")
        cards = card_service.get_cards_by_list(list_id)
        if not cards:
            print("  (empty)")
        for card in cards:
            assigned = f" - Assigned to user {card.assigned_user}" if card.assigned_user else " - Unassigned"
            print(f"  • {card.name}{assigned}")


def main():
    """Main function demonstrating the project management application"""
    
    # Initialize services
    board_service = BoardService()
    list_service = ListService(board_service.board_repository)
    card_service = CardService(
        list_service.list_repository,
        board_service.user_repository
    )
    
    # Create users
    user1 = User(user_id="u1", name="John Doe", email="john@example.com")
    user2 = User(user_id="u2", name="Jane Smith", email="jane@example.com")
    
    board_service.add_user(user1)
    board_service.add_user(user2)
    
    # Create a board
    board = board_service.create_board("Project Alpha", Privacy.PRIVATE, user1.user_id)
    print(f"Created board: {board.name} (ID: {board.id}, URL: {board.url})")
    
    # Add members to board
    board_service.add_member(board.id, user2.user_id)
    print(f"Added {user2.name} to the board")
    
    # Create lists
    todo_list = list_service.create_list(board.id, "To Do")
    in_progress_list = list_service.create_list(board.id, "In Progress")
    done_list = list_service.create_list(board.id, "Done")
    print(f"Created lists: {todo_list.name}, {in_progress_list.name}, {done_list.name}")
    
    # Create cards
    card1 = card_service.create_card(todo_list.id, "Setup development environment", "Install Python and dependencies")
    card2 = card_service.create_card(todo_list.id, "Design database schema", "Create ERD for the application")
    card3 = card_service.create_card(in_progress_list.id, "Implement user authentication", "Add login/logout functionality")
    
    print(f"Created cards: {card1.name}, {card2.name}, {card3.name}")
    
    # Assign users to cards
    card_service.assign_user(card1.id, user1.user_id)
    card_service.assign_user(card3.id, user2.user_id)
    print(f"Assigned {user1.name} to '{card1.name}'")
    print(f"Assigned {user2.name} to '{card3.name}'")
    
    # Move a card
    card_service.move_card(card1.id, in_progress_list.id)
    print(f"Moved '{card1.name}' to '{in_progress_list.name}'")
    
    # Display board status
    print("\n=== Board Status ===")
    for list_id in board.lists:
        task_list = list_service.get_list(list_id)
        print(f"\n{task_list.name}:")
        cards = card_service.get_cards_by_list(list_id)
        for card in cards:
            assigned = f" (Assigned to: {card.assigned_user})" if card.assigned_user else " (Unassigned)"
            print(f"  - {card.name}{assigned}")


if __name__ == "__main__":
    main()
    demonstrate_multiple_boards()