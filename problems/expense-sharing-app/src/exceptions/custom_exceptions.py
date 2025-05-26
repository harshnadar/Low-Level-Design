class InvalidSplitException(Exception):
    """Raised when split validation fails"""
    pass

class UserNotFoundException(Exception):
    """Raised when user is not found"""
    pass

class GroupNotFoundException(Exception):
    """Raised when group is not found"""
    pass

class InvalidExpenseException(Exception):
    """Raised when expense data is invalid"""
    pass