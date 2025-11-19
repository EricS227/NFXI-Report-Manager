import jwt
from functools import wraps
from flask import request, jsonify
from app.config import Config

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Missing Token"}), 401
        
        token = auth.split()[1]

        try:
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        return fn(*args, **kwargs, user=decoded)
    
    return wrapper
        