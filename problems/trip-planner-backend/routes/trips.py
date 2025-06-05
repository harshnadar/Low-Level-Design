from flask import Blueprint, jsonify, request
from repositories.trip_repository import TripRepository
from models.trip import Trip
import uuid
from datetime import datetime

bp = Blueprint('trips', __name__, url_prefix='/api/trips')
trip_repo = TripRepository()

@bp.route('', methods=['GET'])
def get_all_trips():
    try:
        trips = trip_repo.get_all()
        return jsonify(trips), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    try:
        trip = trip_repo.get_by_id(trip_id)
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        return jsonify(trip), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
def create_trip():
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'destination', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate dates
        try:
            start_date = datetime.fromisoformat(data['start_date'])
            end_date = datetime.fromisoformat(data['end_date'])
            if end_date < start_date:
                return jsonify({'error': 'End date must be after start date'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}), 400
        
        # Create trip
        trip = Trip(
            id=str(uuid.uuid4()),
            name=data['name'],
            destination=data['destination'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data.get('description', ''),
            budget=data.get('budget', 0.0)
        )
        
        created_trip = trip_repo.create(trip.to_dict())
        return jsonify(created_trip), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<trip_id>', methods=['PUT'])
def update_trip(trip_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate dates if provided
        if 'start_date' in data or 'end_date' in data:
            existing_trip = trip_repo.get_by_id(trip_id)
            if not existing_trip:
                return jsonify({'error': 'Trip not found'}), 404
            
            start_date = data.get('start_date', existing_trip.get('start_date'))
            end_date = data.get('end_date', existing_trip.get('end_date'))
            
            try:
                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date)
                if end < start:
                    return jsonify({'error': 'End date must be after start date'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        updated_trip = trip_repo.update(trip_id, data)
        if not updated_trip:
            return jsonify({'error': 'Trip not found'}), 404
        return jsonify(updated_trip), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    try:
        if trip_repo.delete(trip_id):
            return jsonify({'message': 'Trip deleted successfully'}), 200
        return jsonify({'error': 'Trip not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500