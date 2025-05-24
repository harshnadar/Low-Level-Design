from flask import jsonify

def ping():
    return jsonify({"message": "pong"}), 200