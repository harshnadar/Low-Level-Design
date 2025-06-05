from flask import Blueprint, request, jsonify

bp = Blueprint('hello_world', __name__, url_prefix='/api/hello_world')

@bp.route('', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200