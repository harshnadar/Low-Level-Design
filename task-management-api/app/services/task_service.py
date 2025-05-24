from app.models.task import Task
import app.utils.constants as constants
import app.utils.helpers as helpers
import logging
import datetime

all_tasks = {}

def create_task(data: dict) -> dict:
    """
    Create a new task with the given data.
    :param data: Dictionary containing task details.
    :return: Dictionary with the created task details.
    """
    # Placeholder for task creation logic
    # In a real application, this would involve database operations
    try:
        # Extract task data
        title = data.get("title")
        description = data.get("description")
        task_status = data.get("task_status", constants.TaskStatus.PENDING)
        task_priority = data.get("task_priority", constants.TaskPriority.MEDIUM)
        
        # Create task
        task = Task(title=title, description=description, task_status=task_status, task_priority=task_priority)
        task_info = task.get_task_info()
        all_tasks[task_info['id']] = task_info
        
        logging.info(f"Task created: {task_info}")
        # Return success response
        return helpers.success_response(
            data={"task": task_info},
            message=constants.SuccessMessage.TASK_CREATED,
            status_code=constants.StatusCode.CREATED
        )
    except Exception as e:
        # Log the error
        logging.error(f"Error creating task: {str(e)}")
        return helpers.error_response(
            message=constants.ErrorMessage.TASK_CREATION_FAILED,
            status_code=constants.StatusCode.INTERNAL_SERVER_ERROR
        )

def get_task_by_id(task_id: int) -> dict:
    """
    Retrieve a task by its ID.
    :param task_id: ID of the task to retrieve.
    :return: Dictionary with the task details or an error message.
    """
    task = all_tasks.get(task_id)
    if not task:
        logging.error(f"Task with ID {task_id} not found")
        return helpers.error_response(
            message=constants.ErrorMessage.TASK_NOT_FOUND,
            status_code=constants.StatusCode.NOT_FOUND
        )
    return helpers.success_response(
        data={"task": task},
        message="Task retrieved successfully",
        status_code=constants.StatusCode.OK
    )

def get_all_tasks() -> dict:
    """
    Retrieve all tasks.
    :return: Dictionary with all tasks.
    """
    return helpers.success_response(
        data={"tasks": list(all_tasks.values())},
        message="All tasks retrieved successfully",
        status_code=constants.StatusCode.OK
    )

def update_task(task_id: int, updated_data: dict) -> dict:
    """
    Update a task with the given ID and data.
    :param task_id: ID of the task to update.
    :param updated_data: Dictionary containing the updated task details.
    :return: Tuple with response and status code.
    """
    # Check if task exists
    if task_id not in all_tasks:
        return helpers.error_response(
            message=constants.ErrorMessage.TASK_NOT_FOUND,
            status_code=constants.StatusCode.NOT_FOUND
        )
    
    # Update the task fields
    task = all_tasks[task_id]
    for field, value in updated_data.items():
        if field in task:
            task[field] = value
    
    # Update the updated_at timestamp
    task['updated_at'] = datetime.datetime.now()
    
    logging.info(f"Task {task_id} updated: {updated_data}")
    
    return helpers.success_response(
        data={"task": task},
        message=constants.SuccessMessage.TASK_UPDATED,
        status_code=constants.StatusCode.OK
    )

def delete_task(task_id: int) -> dict:
    """
    Delete a task with the given ID.
    :param task_id: ID of the task to delete.
    :return: Tuple with response and status code.
    """
    # Check if task exists
    if task_id not in all_tasks:
        logging.error(f"Task with ID {task_id} not found for deletion")
        return helpers.error_response(
            message=constants.ErrorMessage.TASK_NOT_FOUND,
            status_code=constants.StatusCode.NOT_FOUND
        )
    
    # Remove the task from the dictionary
    deleted_task = all_tasks.pop(task_id)
    
    logging.info(f"Task {task_id} deleted successfully")
    return helpers.success_response(
        data={"deleted_task": deleted_task},
        message=constants.SuccessMessage.TASK_DELETED,
        status_code=constants.StatusCode.OK
    )