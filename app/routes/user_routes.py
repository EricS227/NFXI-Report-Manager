from flask import Blueprint, request, jsonify
from app.models import get_db
from app.services.user_service import UserService
from app.utils.security import admin_required

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

# Listar todos os usuários
@user_bp.get("/")
@admin_required
def list_users():
    db = get_db()
    service = UserService(db)
    users = service.list_users()
    return jsonify([
        {"id":u.id, "username": u.username, "role": u.role, "active": u.active}
        for u in users
    ])

# criar usuário
@user_bp.post("/")
@admin_required
def create_user():
    data = request.json
    db = get_db()
    service = UserService(db)
    
    user, error = service.create_user(
        data["username"],
        data["password"],
        data.get("role", "financeiro")
    )

    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    }), 201


#atualizar usuário

@user_bp.put("/<int:user_id>")
@admin_required
def update_user(user_id):
    db = get_db()
    service = UserService(db)
    updated, error = service.update_user(user_id, request.json)

    if error:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Usuário atualizado"})

#deletar usuário
@user_bp.delete("/<int:user_id>")
@admin_required
def delete_user(user_id):
    db = get_db()
    service = UserService(db)

    error = service.delete_user(user_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Usuário removido"})