import pytest
from app.services.task_service import create_task, get_task_by_id, update_task, delete_task
from app.services.task_service import all_tasks

class TestTaskService:
    """Unit tests for task service functions."""
    
    def test_create_task_service(self):
        """Test task creation at service level."""
        task_data = {
            "title": "Service Test Task",
            "description": "Testing service layer"
        }
        
        response, status_code = create_task(task_data)
        
        assert status_code == 201
        assert response['status'] == 'success'
        assert 'task' in response['data']
        assert len(all_tasks) == 1
    
    def test_get_task_by_id_service(self):
        """Test getting task by ID at service level."""
        # Create a task first
        task_data = {"title": "Test", "description": "Test"}
        create_response, _ = create_task(task_data)
        task_id = create_response['data']['task']['id']
        
        # Get the task
        response, status_code = get_task_by_id(task_id)
        
        assert status_code == 200
        assert response['status'] == 'success'
        assert response['data']['task']['id'] == task_id
    
    def test_update_task_service(self):
        """Test task update at service level."""
        # Create a task first
        task_data = {"title": "Original", "description": "Original desc"}
        create_response, _ = create_task(task_data)
        task_id = create_response['data']['task']['id']
        
        # Update the task
        update_data = {"title": "Updated"}
        response, status_code = update_task(task_id, update_data)
        
        assert status_code == 200
        assert response['status'] == 'success'
        assert response['data']['task']['title'] == "Updated"
        assert response['data']['task']['description'] == "Original desc"
    
    def test_delete_task_service(self):
        """Test task deletion at service level."""
        # Create a task first
        task_data = {"title": "To Delete", "description": "Will be deleted"}
        create_response, _ = create_task(task_data)
        task_id = create_response['data']['task']['id']
        
        # Delete the task
        response, status_code = delete_task(task_id)
        
        assert status_code == 200
        assert response['status'] == 'success'
        assert task_id not in all_tasks