from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_login import LoginManager, login_required
from relatorio.gerar_relatorio import gerar_relatorio_fluxo_caixa
import os
from app.routes.user_routes import user_bp
from app.models import SessionLocal, User

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

class LoginUser:
    def __init__(self, user):
        self.id = str(user.id)
        self.username = user.username
        self.role = user.role
        self.active = user.active
        self.is_authenticated = True
        self.is_active = user.active
        self.is_anonymous = False

    def get_id(self):
        return self.id

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

@app.route("/")
@login_required
def home():
    return render_template("index.html", resumo=None, pdf_file=None)

@app.route("/gerar", methods=["POST"])
@login_required
def gerar():
    mes = request.form.get("mes")
    ano = request.form.get("ano")

    if not mes or not ano:
        flash("Selecione o mês e ano", "warning")
        return render_template("index.html", resumo=None, pdf_file=None)

    resultado = gerar_relatorio_fluxo_caixa(int(mes), int(ano))

    if not resultado:
        flash("Nenhum dado encontrado para esse período", "warning")
        return render_template("index.html", resumo=None, pdf_file=None)

    caminho_pdf, resumo = resultado

    filename = os.path.basename(caminho_pdf)

    return render_template(
        "index.html",
        resumo=resumo,
        pdf_file=filename
    )

@app.route("/download/<filename>")
@login_required
def download(filename):
    caminho = os.path.join("relatorios", filename)
    return send_file(caminho, as_attachment=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    from werkzeug.security import check_password_hash
    from flask_login import login_user

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and user.active and check_password_hash(user.password_hash, password):
            login_user(LoginUser(user))
            flash("Login efetuado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos", "danger")
            return redirect(url_for("login"))
    finally:
        db.close()

@app.route("/logout")
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    flash("Desconectado", "info")
    return redirect(url_for("login"))

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
