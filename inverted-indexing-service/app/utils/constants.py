class StatusCode:
    """HTTP Status Codes"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

class ErrorMessage:
    """Standard error messages"""
    
    # Validation errors
    MISSING_REQUIRED_FIELDS = "Missing required fields in request body"
    INVALID_REQUEST_BODY = "Invalid request body"
    INVALID_TASK_STATUS = "Invalid task status"
    INVALID_TASK_PRIORITY = "Invalid task priority"
    
    # Server errors
    INTERNAL_SERVER_ERROR = "Internal server error"
    SERVICE_UNAVAILABLE = "Service temporarily unavailable"