from flask import Blueprint, jsonify, request, abort
import logging
import app.utils.helpers as helpers
import app.services.task_service as task_service
import app.utils.constants as constants

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    response, status_code = task_service.get_all_tasks()
    return jsonify(response), status_code

@tasks_bp.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    response, status_code = task_service.get_task_by_id(task_id)
    return jsonify(response), status_code

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    # This is a placeholder for task creation logic
    #get the task data from the request
    try:
        data = request.get_json()
        required_fields = {"title", "description"}
        if not helpers.validate_request_body(data, required_fields):
            return jsonify(helpers.error_response(
                message = constants.ErrorMessage.MISSING_REQUIRED_FIELDS,
                status_code = constants.StatusCode.BAD_REQUEST
            )[0]), constants.StatusCode.BAD_REQUEST
        # Assuming the task is created successfully
        response, status_code = task_service.create_task(data)
        return jsonify(response), status_code
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        return jsonify(helpers.error_response(
            message = constants.ErrorMessage.TASK_CREATION_FAILED,
            status_code = constants.StatusCode.INTERNAL_SERVER_ERROR
        )[0]), constants.StatusCode.INTERNAL_SERVER_ERROR

@tasks_bp.route('/api/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    try:
        # Get the update data from request body
        data = request.get_json()
        
        # Validate that some data was provided
        if not data:
            return jsonify(helpers.error_response(
                message="No data provided for update",
                status_code=constants.StatusCode.BAD_REQUEST
            )[0]), constants.StatusCode.BAD_REQUEST
        
        # Optional: Validate which fields can be updated
        allowed_fields = {"title", "description", "task_status", "task_priority"}
        update_fields = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_fields:
            return jsonify(helpers.error_response(
                message="No valid fields provided for update",
                status_code=constants.StatusCode.BAD_REQUEST
            )[0]), constants.StatusCode.BAD_REQUEST
        
        # Call the service to update the task
        response, status_code = task_service.update_task(task_id, update_fields)
        return jsonify(response), status_code
        
    except Exception as e:
        logging.error(f"Error updating task {task_id}: {e}")
        return jsonify(helpers.error_response(
            message=constants.ErrorMessage.TASK_UPDATE_FAILED,
            status_code=constants.StatusCode.INTERNAL_SERVER_ERROR
        )[0]), constants.StatusCode.INTERNAL_SERVER_ERROR

@tasks_bp.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Call the service to delete the task
        response, status_code = task_service.delete_task(task_id)
        return jsonify(response), status_code
        
    except Exception as e:
        logging.error(f"Error deleting task {task_id}: {e}")
        return jsonify(helpers.error_response(
            message=constants.ErrorMessage.TASK_DELETE_FAILED,
            status_code=constants.StatusCode.INTERNAL_SERVER_ERROR
        )[0]), constants.StatusCode.INTERNAL_SERVER_ERROR