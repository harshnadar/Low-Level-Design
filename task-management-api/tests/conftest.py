import pytest
from app import create_app
from app.services.task_service import all_tasks

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear all tasks before each test."""
    all_tasks.clear()
    yield
    all_tasks.clear()

@pytest.fixture
def sample_task():
    """A sample task for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "task_status": "PENDING",
        "task_priority": "MEDIUM"
    }

@pytest.fixture
def sample_task_id(client, sample_task):
    """Create a task and return its ID."""
    response = client.post('/api/tasks', json=sample_task)
    data = response.get_json()
    return data['data']['task']['id']