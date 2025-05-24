import os
import re
from app.models.inverted_index import InvertedIndex

class IndexingService:
    """Service for indexing text files"""
    
    def __init__(self):
        self.index = InvertedIndex()
    
    def index_file(self, filepath: str, filename: str) -> bool:
        """Read and index a text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract words (alphanumeric sequences)
            words = re.findall(r'\b\w+\b', content.lower())
            
            # Add each unique word to the index
            unique_words = set(words)
            for word in unique_words:
                self.index.add_term(word, filename)
            
            return True
            
        except Exception as e:
            print(f"Error indexing file {filename}: {str(e)}")
            return False
    
    def reindex_all_files(self, upload_folder: str) -> int:
        """Reindex all files in the upload folder"""
        count = 0
        for filename in os.listdir(upload_folder):
            if filename.endswith('.txt'):
                filepath = os.path.join(upload_folder, filename)
                if self.index_file(filepath, filename):
                    count += 1
        return count