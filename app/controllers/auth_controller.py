from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from app.models import get_db
from app.services.auth_service import AuthService
from app.models import User
from app.models import engine, SessionLocal

auth_bp = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class LoginUser(UserMixin):
    def __init__(self, user):
        self.id = str(user.id)
        self.username = user.username
        self.role = user.role
        self.active = user.active
    
    def get_role(self):
        return self.role
    

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).get(int(user_id))
        if user:
            return LoginUser(user)
        return None
    finally:
        db.close()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    db = next(get_db())
    service = AuthService(db)
    user = service.authenticate(username, password)
    if not user:
        flash("Usuário ou senha inválidos", "danger")
        return redirect(url_for("auth.login"))
    login_user(LoginUser(user))
    flash("Login efetuado", "success")
    return redirect(url_for("relatorio.home"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Desconectado", "info")
    return redirect(url_for("auth.login"))