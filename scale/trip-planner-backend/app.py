from flask import Flask, jsonify
from routes import hello_world



def create_app():
    """Factory function to create a Flask app instance."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(hello_world.bp)

      # Load configuration from config.py
    return app


app = create_app()
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
    app.run(host='0.0.0.0', port=8080, debug=True)