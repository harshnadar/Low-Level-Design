# Task Management API

This is a production-ready Task Management API that allows multiple users to manage their personal tasks. The API is built using Flask and is designed to be secure, well-tested, and ready for deployment.

## Project Structure

The project is organized into several modules:

- **app/**: Contains the main application code.
  - **api/**: Contains the API routes for authentication and task management.
  - **config.py**: Configuration settings for the Flask application.
  - **models/**: Defines the data models for users and tasks.
  - **services/**: Contains business logic for the application.
  - **utils/**: Helper functions used throughout the application.

- **tests/**: Contains the test suite to ensure the functionality of the application.

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed on your machine. You can check your Python version by running:

```
python --version
```

### Installation

1. Clone the repository:

```
git clone <repository-url>
cd task-management-api
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

### Running the Application

To run the Flask application, execute the following command:

```
python run.py
```

You can then access the API at `http://127.0.0.1:5000`.

### Endpoints

- **Ping Endpoint**: A simple endpoint to check if the application is running.
  - **GET** `/api/ping`: Returns a simple message indicating the application is up and running.

## Testing

To run the test suite, use the following command:

```
pytest
```

This will execute all the tests in the `tests/` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for details.