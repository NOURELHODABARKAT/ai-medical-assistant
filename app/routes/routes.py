from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def index():
    return jsonify({"message": "🚀 AI Medical Assistant API is running!"})