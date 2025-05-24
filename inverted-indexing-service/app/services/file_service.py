import os
from typing import List, Dict
from flask import current_app
from app.models.inverted_index import InvertedIndex
from app.services.indexing_service import IndexingService

class FileService:
    """Service for file management operations"""
    
    def __init__(self):
        self.index = InvertedIndex()
    
    def list_all_files(self) -> List[Dict[str, any]]:
        """List all indexed files with metadata"""
        files = []
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        for filename in self.index.get_all_files():
            filepath = os.path.join(upload_folder, filename)
            if os.path.exists(filepath):
                file_info = {
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'terms_count': len(self.index.get_file_terms(filename))
                }
                files.append(file_info)
        
        return files
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file from filesystem and index"""
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return False
        
        # Remove from index
        self.index.remove_file(filename)
        
        # Remove from filesystem
        os.remove(filepath)
        
        return True