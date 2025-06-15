import jwt
from datetime import datetime, timedelta
from app.config import Config


def generate_jwt(payload):
    payload['exp'] = datetime.utcnow() + timedelta(days=Config.JWT_EXP_DAYS)
    return jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
