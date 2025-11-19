from functools import wraps
from flask import abort
from flask import request, jsonify
import jwt
import os
from flask_login import current_user

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Beaer "):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Token não enviado"}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload.get("role") != "admin":
                return jsonify({"error": "Acesso negado: somente admin"}), 403
        except Exception:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(*args, **kwargs)
    return wrapper
