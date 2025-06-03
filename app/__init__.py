from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    from .routes import api_bp
    app.register_blueprint(api_bp)
    return app

__all__ = ["create_app"]