from typing import List
from app.models.inverted_index import InvertedIndex

class SearchService:
    """Service for searching indexed content"""
    
    def __init__(self):
        self.index = InvertedIndex()
    
    def search(self, search_term: str) -> List[str]:
        """Search for files containing the given term"""
        return self.index.search_term(search_term)
    
    def search_multiple_terms(self, terms: List[str], operation: str = 'OR') -> List[str]:
        """Search for files containing multiple terms with AND/OR operations"""
        if not terms:
            return []
        
        results_sets = [set(self.index.search_term(term.lower())) for term in terms]
        
        if operation == 'AND':
            # Intersection of all sets
            result = results_sets[0]
            for s in results_sets[1:]:
                result = result.intersection(s)
        else:  # OR operation
            # Union of all sets
            result = set()
            for s in results_sets:
                result = result.union(s)
        
        return list(result)