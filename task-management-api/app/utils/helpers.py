import logging
import app.utils.constants as constants

def ping_response():
    return {"message": "pong"}

def error_response(message, status_code):
    """
    Create a standardized error response
    :param message: Error message
    :param status_code: HTTP status code
    :return: Tuple with response dict and status code
    """
    return {
        "status": "error",
        "message": message
    }, status_code


def success_response(data=None, message=None, status_code=constants.StatusCode.OK):
    """
    Create a standardized success response
    :param data: Response data
    :param message: Success message
    :param status_code: HTTP status code
    :return: Tuple with response dict and status code
    """
    response = {
        "status": "success"
    }
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return response, status_code


def validate_request_body(request_body: dict, required_fields: set) -> bool:
    """
    Validate the request body against the required fields.

    Args:
        request_body (dict): The request body to validate.
        required_fields (list): A list of required fields.

    Returns:
        bool: True if the request body is valid, False otherwise.
    """
    if not request_body:
        logging.error("Request body is empty")
        return False
    if not required_fields.issubset(request_body.keys()):
        logging.error("Missing some required fields in request body")
        return False
    return True