from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    CORS(app)
    app.config.from_object('app.config.Config')
    limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

    from .routes.auth import auth_bp
    from .routes.api2 import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

__all__ = ["create_app"]