from flask import Flask, jsonify
from routes import hello_world, trips, itineraries

app = Flask(__name__)

app.register_blueprint(hello_world.bp)
app.register_blueprint(trips.bp)
app.register_blueprint(itineraries.bp)

# Add error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False))