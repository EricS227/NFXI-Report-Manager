from flask import Blueprint, request, jsonify
from app.models import SessionLocal
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    db = SessionLocal()
    service = AuthService(db)

    token = service.authenticate(username, password)

    db.close()

    if not token:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"token": token})