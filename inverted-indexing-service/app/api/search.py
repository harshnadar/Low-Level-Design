from flask import Blueprint, request, jsonify
from app.services.search_service import SearchService
from app.utils.helpers import error_response, success_response

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search():
    """Search for a term across all indexed files"""
    try:
        # Get search term from query parameters
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify(error_response('Search term is required')), 400
        
        # Perform search
        search_service = SearchService()
        results = search_service.search(search_term.lower())
        
        return jsonify(success_response(
            message=f'Search completed for term: {search_term}',
            data={
                'search_term': search_term,
                'files_found': len(results),
                'files': results
            }
        )), 200
        
    except Exception as e:
        return jsonify(error_response(f'Error searching: {str(e)}')), 500