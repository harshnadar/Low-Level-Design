from flask import Flask
from app.api.upload import upload_bp
from app.api.ping import ping_bp
from app.api.search import search_bp
from app.api.files import files_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'txt'}
    
    # # Ensure upload directory exists
    # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(ping_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(files_bp)
    
    return app

app = create_app()