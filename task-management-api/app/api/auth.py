from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Auth service is running"}), 200