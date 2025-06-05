from flask import Blueprint, jsonify, request
from repositories.itinerary_repository import ItineraryRepository
from repositories.trip_repository import TripRepository
from models.itinerary import Itinerary
import uuid
from datetime import datetime

bp = Blueprint('itineraries', __name__, url_prefix='/api/itineraries')
itinerary_repo = ItineraryRepository()
trip_repo = TripRepository()

@bp.route('', methods=['GET'])
def get_all_itineraries():
    try:
        trip_id = request.args.get('trip_id')
        if trip_id:
            itineraries = itinerary_repo.get_by_trip_id(trip_id)
        else:
            itineraries = itinerary_repo.get_all()
        return jsonify(itineraries), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<itinerary_id>', methods=['GET'])
def get_itinerary(itinerary_id):
    try:
        itinerary = itinerary_repo.get_by_id(itinerary_id)
        if not itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        return jsonify(itinerary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
def create_itinerary():
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['trip_id', 'day', 'activities']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify trip exists
        trip = trip_repo.get_by_id(data['trip_id'])
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        # Validate day is positive integer
        if not isinstance(data['day'], int) or data['day'] < 1:
            return jsonify({'error': 'Day must be a positive integer'}), 400
        
        # Validate activities is a list
        if not isinstance(data['activities'], list):
            return jsonify({'error': 'Activities must be a list'}), 400
        
        # Create itinerary
        itinerary = Itinerary(
            id=str(uuid.uuid4()),
            trip_id=data['trip_id'],
            day=data['day'],
            activities=data['activities'],
            notes=data.get('notes', '')
        )
        
        created_itinerary = itinerary_repo.create(itinerary.to_dict())
        return jsonify(created_itinerary), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<itinerary_id>', methods=['PUT'])
def update_itinerary(itinerary_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate day if provided
        if 'day' in data and (not isinstance(data['day'], int) or data['day'] < 1):
            return jsonify({'error': 'Day must be a positive integer'}), 400
        
        # Validate activities if provided
        if 'activities' in data and not isinstance(data['activities'], list):
            return jsonify({'error': 'Activities must be a list'}), 400
        
        updated_itinerary = itinerary_repo.update(itinerary_id, data)
        if not updated_itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        return jsonify(updated_itinerary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    try:
        if itinerary_repo.delete(itinerary_id):
            return jsonify({'message': 'Itinerary deleted successfully'}), 200
        return jsonify({'error': 'Itinerary not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500