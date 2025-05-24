def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def success_response(message, data=None):
    """Create a success response"""
    response = {
        'status': 'success',
        'message': message
    }
    if data:
        response['data'] = data
    return response

def error_response(message):
    """Create an error response"""
    return {
        'status': 'error',
        'message': message
    }