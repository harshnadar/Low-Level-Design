# Project Management Application

This project is a simple project management application similar to Trello, allowing users to manage projects by tracking smaller tasks. The application supports multiple boards, each containing lists and cards for task management.

## Features

- **Boards**: Create and manage multiple boards for different projects.
- **Lists**: Each board can have multiple lists representing sub-projects.
- **Cards**: Each list can contain cards representing smaller tasks.
- **User Management**: Users can be assigned to cards or remain unassigned.
- **CRUD Operations**: Create, read, update, and delete boards, lists, and cards.
- **Privacy Settings**: Boards can be public or private, with a default setting of public.
- **Card Movement**: Move cards between lists within the same board.

## Architecture

The application follows a layered architecture with proper separation of concerns:

- **Models**: Core domain entities (User, Board, List, Card)
- **Services**: Business logic layer (BoardService, ListService, CardService)
- **Repositories**: Data access layer (InMemoryRepository)
- **Exceptions**: Custom exception hierarchy for error handling


## Design Patterns Used

1. **Repository Pattern**: Abstracts data access logic
2. **Service Layer Pattern**: Encapsulates business logic
3. **Factory Pattern**: ID generation using IdGenerator
4. **Dependency Injection**: Services receive dependencies through constructors

## Future Enhancements

- Persistence layer (database integration)
- REST API endpoints
- Authentication and authorization
- Activity logs and notifications
- Card comments and attachments
- Due dates and labels for cards

## Project Structure

```
project-management-app
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── board.py
│   │   ├── list.py
│   │   └── card.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── board_service.py
│   │   ├── list_service.py
│   │   └── card_service.py
│   ├── repositories
│   │   ├── __init__.py
│   │   └── in_memory_repository.py
│   ├── exceptions
│   │   ├── __init__.py
│   │   └── custom_exceptions.py
│   └── utils
│       ├── __init__.py
│       └── id_generator.py
├── tests
│   ├── __init__.py
│   ├── test_board_service.py
│   ├── test_list_service.py
│   └── test_card_service.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/project-management-app.git
   ```
2. Navigate to the project directory:
   ```
   cd project-management-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.