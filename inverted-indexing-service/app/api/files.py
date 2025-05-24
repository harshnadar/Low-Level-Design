from flask import Blueprint, jsonify
from app.services.file_service import FileService
from app.utils.helpers import success_response, error_response

files_bp = Blueprint('files', __name__)

@files_bp.route('/api/files', methods=['GET'])
def list_files():
    """List all indexed files"""
    try:
        file_service = FileService()
        files = file_service.list_all_files()
        
        return jsonify(success_response(
            message='Files retrieved successfully',
            data={
                'total_files': len(files),
                'files': files
            }
        )), 200
        
    except Exception as e:
        return jsonify(error_response(f'Error listing files: {str(e)}')), 500

@files_bp.route('/api/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a file and remove it from index"""
    try:
        file_service = FileService()
        deleted = file_service.delete_file(filename)
        
        if deleted:
            return jsonify(success_response(
                message=f'File {filename} deleted successfully'
            )), 200
        else:
            return jsonify(error_response(f'File {filename} not found')), 404
            
    except Exception as e:
        return jsonify(error_response(f'Error deleting file: {str(e)}')), 500