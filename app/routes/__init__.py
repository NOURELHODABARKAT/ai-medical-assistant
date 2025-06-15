from flask import Flask
from .api2 import api_bp
from app.auth import auth_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.secret_key = app.config['SECRET_KEY']

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app