from typing import Dict, Set, List
import threading

class InvertedIndex:
    """Thread-safe inverted index implementation"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.index = {}  # term -> set of filenames
                    cls._instance.files = {}   # filename -> set of terms
        return cls._instance
    
    def add_term(self, term: str, filename: str) -> None:
        """Add a term-filename mapping to the index"""
        with self._lock:
            if term not in self.index:
                self.index[term] = set()
            self.index[term].add(filename)
            
            if filename not in self.files:
                self.files[filename] = set()
            self.files[filename].add(term)
    
    def search_term(self, term: str) -> List[str]:
        """Search for files containing a term"""
        with self._lock:
            return list(self.index.get(term, set()))
    
    def remove_file(self, filename: str) -> bool:
        """Remove a file from the index"""
        with self._lock:
            if filename not in self.files:
                return False
            
            # Remove filename from all term entries
            terms_to_remove = self.files[filename]
            for term in terms_to_remove:
                if term in self.index:
                    self.index[term].discard(filename)
                    if not self.index[term]:  # Remove empty sets
                        del self.index[term]
            
            # Remove file entry
            del self.files[filename]
            return True
    
    def get_all_files(self) -> List[str]:
        """Get all indexed files"""
        with self._lock:
            return list(self.files.keys())
    
    def get_file_terms(self, filename: str) -> List[str]:
        """Get all terms in a file"""
        with self._lock:
            return list(self.files.get(filename, set()))