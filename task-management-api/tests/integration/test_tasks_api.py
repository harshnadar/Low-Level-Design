import pytest
import json
import app.utils.constants as constants 

class TestTasksAPI:
    """Integration tests for the Tasks API endpoints."""
    
    def test_create_task_success(self, client, sample_task):
        """Test successful task creation."""
        response = client.post('/api/tasks', json=sample_task)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['message'] == 'Task created successfully'
        assert 'task' in data['data']
        assert data['data']['task']['title'] == sample_task['title']
        assert data['data']['task']['description'] == sample_task['description']
        assert 'id' in data['data']['task']
    
    def test_create_task_missing_title(self, client):
        """Test task creation with missing title."""
        task_data = {"description": "Task without title"}
        response = client.post('/api/tasks', json=task_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == constants.ErrorMessage.MISSING_REQUIRED_FIELDS
    
    def test_create_task_missing_description(self, client):
        """Test task creation with missing description."""
        task_data = {"title": "Task without description"}
        response = client.post('/api/tasks', json=task_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == constants.ErrorMessage.MISSING_REQUIRED_FIELDS
    
    def test_create_task_invalid_json(self, client):
        """Test task creation with invalid JSON."""
        response = client.post('/api/tasks', 
                             data="invalid json",
                             content_type='application/json')
        
        assert response.status_code == 500
    
    def test_get_all_tasks_empty(self, client):
        """Test getting all tasks when none exist."""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['tasks'] == []
    
    def test_get_all_tasks_with_data(self, client, sample_task):
        """Test getting all tasks when tasks exist."""
        # Create multiple tasks
        client.post('/api/tasks', json=sample_task)
        client.post('/api/tasks', json={
            "title": "Second Task",
            "description": "Another test task"
        })
        
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert len(data['data']['tasks']) == 2
    
    def test_get_task_by_id_success(self, client, sample_task_id):
        """Test getting a specific task by ID."""
        response = client.get(f'/api/tasks/{sample_task_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['task']['id'] == sample_task_id
    
    def test_get_task_by_id_not_found(self, client):
        """Test getting a non-existent task."""
        response = client.get('/api/tasks/non-existent-id')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == 'Task not found'
    
    def test_update_task_success(self, client, sample_task_id):
        """Test successful task update."""
        update_data = {
            "title": "Updated Title",
            "task_status": "IN_PROGRESS"
        }
        response = client.patch(f'/api/tasks/{sample_task_id}', json=update_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['task']['title'] == "Updated Title"
        assert data['data']['task']['task_status'] == "IN_PROGRESS"
        assert data['data']['task']['description'] == "This is a test task"  # Unchanged
    
    def test_update_task_not_found(self, client):
        """Test updating a non-existent task."""
        update_data = {"title": "Updated Title"}
        response = client.patch('/api/tasks/non-existent-id', json=update_data)
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == 'Task not found'
    
    def test_update_task_no_data(self, client, sample_task_id):
        """Test updating a task with no data."""
        response = client.patch(f'/api/tasks/{sample_task_id}', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == 'No data provided for update'
    
    def test_update_task_invalid_fields(self, client, sample_task_id):
        """Test updating a task with invalid fields only."""
        update_data = {"invalid_field": "value"}
        response = client.patch(f'/api/tasks/{sample_task_id}', json=update_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == 'No valid fields provided for update'
    
    def test_delete_task_success(self, client, sample_task_id):
        """Test successful task deletion."""
        response = client.delete(f'/api/tasks/{sample_task_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['message'] == 'Task deleted successfully'
        assert data['data']['deleted_task']['id'] == sample_task_id
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{sample_task_id}')
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task."""
        response = client.delete('/api/tasks/non-existent-id')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
        assert data['message'] == 'Task not found'