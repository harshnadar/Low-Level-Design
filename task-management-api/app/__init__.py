from flask import Flask
from app.api.ping import ping_bp
from app.api.auth import auth_bp
from app.api.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(ping_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app

app = create_app()