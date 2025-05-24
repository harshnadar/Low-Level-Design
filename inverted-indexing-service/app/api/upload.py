from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.services.indexing_service import IndexingService
# from app.utils.helpers import allowed_file, error_response, success_response
import app.utils.helpers as helpers


upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a text file and index its content"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify(helpers.error_response('No file provided')), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify(helpers.error_response('No file selected')), 400
        
        # Validate file extension
        if not helpers.allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return jsonify(helpers.error_response('Only .txt files are allowed')), 400
        
        # Secure the filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            return jsonify(helpers.error_response(f'File {filename} already exists')), 409
        
        file.save(filepath)
        
        # Index the file
        indexing_service = IndexingService()
        indexed = indexing_service.index_file(filepath, filename)
        
        if indexed:
            return jsonify(helpers.success_response(
                message=f'File {filename} uploaded and indexed successfully',
                data={'filename': filename}
            )), 201
        else:
            # Remove file if indexing failed
            os.remove(filepath)
            return jsonify(helpers.error_response('Failed to index file')), 500
            
    except Exception as e:
        return jsonify(helpers.error_response(f'Error uploading file: {str(e)}')), 500