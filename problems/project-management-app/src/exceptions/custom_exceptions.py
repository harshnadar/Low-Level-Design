class ProjectManagementException(Exception):
    """Base exception for project management application"""
    pass


class ResourceNotFoundException(ProjectManagementException):
    """Exception raised when a resource is not found"""
    pass


class InvalidOperationException(ProjectManagementException):
    """Exception raised when an invalid operation is attempted"""
    pass


class UnauthorizedAccessException(ProjectManagementException):
    """Exception raised when unauthorized access is attempted"""
    pass


class ValidationException(ProjectManagementException):
    """Exception raised when validation fails"""
    pass