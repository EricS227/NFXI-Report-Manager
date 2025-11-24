from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_login import LoginManager, login_required
from relatorio.gerar_relatorio import gerar_relatorio_fluxo_caixa
import os
import csv
import io
from app.routes.user_routes import user_bp
from app.models import SessionLocal, User, engine
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Initialize login manager / Inicializa o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.route("/dashboard")
@login_required
def dashboard():
    with engine.connect() as conn:
        # Get summary / Obtém resumo geral
        result = conn.execute(text("""
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END), 0) as income,
                COALESCE(SUM(CASE WHEN tipo = 'saida' THEN valor ELSE 0 END), 0) as expense,
                COUNT(*) as count
            FROM transacoes_financeiras
        """))
        row = result.fetchone()
        summary = {
            "income": formatar_moeda(float(row[0])),
            "expense": formatar_moeda(float(row[1])),
            "balance": formatar_moeda(float(row[0]) - float(row[1])),
            "count": row[2]
        }

        # Get monthly totals / Obtém totais mensais
        result = conn.execute(text("""
            SELECT strftime('%Y-%m', data) as month, SUM(valor) as total
            FROM transacoes_financeiras
            GROUP BY strftime('%Y-%m', data)
            ORDER BY month
        """))
        monthly = [{"month": row[0], "total": float(row[1])} for row in result]

        # Get totals by category / Obtém totais por categoria
        result = conn.execute(text("""
            SELECT categoria, SUM(valor) as total
            FROM transacoes_financeiras
            GROUP BY categoria
        """))
        categories = [[row[0], float(row[1])] for row in result]

    return render_template("dashboard.html", summary=summary, monthly=monthly, categories=categories)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    from werkzeug.security import generate_password_hash

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("As senhas não coincidem", "danger")
        return redirect(url_for("register"))

    db = SessionLocal()
    try:
        # Check if user already exists / Verifica se o usuário já existe
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            flash("Usuário já existe", "danger")
            return redirect(url_for("register"))

        # Create new user / Cria novo usuário
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="financeiro",
            active=True
        )
        db.add(user)
        db.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("login"))
    finally:
        db.close()

@app.route("/transacoes", methods=["GET", "POST"])
@login_required
def transacoes():
    if request.method == "POST":
        data = request.form.get("data")
        categoria = request.form.get("categoria")
        centro_custo = request.form.get("centro_custo")
        tipo = request.form.get("tipo")
        valor = request.form.get("valor")

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO transacoes_financeiras (data, categoria, centro_custo, tipo, valor)
                VALUES (:data, :categoria, :centro_custo, :tipo, :valor)
            """), {
                "data": data,
                "categoria": categoria,
                "centro_custo": centro_custo,
                "tipo": tipo,
                "valor": float(valor)
            })
            conn.commit()

        flash("Transação adicionada com sucesso!", "success")
        return redirect(url_for("transacoes"))

    # GET - list recent transactions / Lista as transações recentes
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT data, categoria, centro_custo, tipo, valor
            FROM transacoes_financeiras
            ORDER BY data DESC
            LIMIT 20
        """))
        transacoes_list = [dict(row._mapping) for row in result]

    return render_template("transacoes.html", transacoes=transacoes_list)




@app.route("/importar", methods=["GET", "POST"])
@login_required
def importar():
    if request.method == "POST":
        arquivo = request.files.get("arquivo")

        if not arquivo or not arquivo.filename.endswith('.csv'):
            flash("Por favor, envie um arquivo CSV válido", "danger")
            return redirect(url_for("importar"))

        try:
            # Read CSV content / Lê o conteúdo do CSV
            stream = io.StringIO(arquivo.stream.read().decode("utf-8"))
            reader = csv.DictReader(stream)

            count = 0
            with engine.connect() as conn:
                for row in reader:
                    conn.execute(text("""
                        INSERT INTO transacoes_financeiras (data, categoria, centro_custo, tipo, valor)
                        VALUES (:data, :categoria, :centro_custo, :tipo, :valor)
                    """), {
                        "data": row["data"],
                        "categoria": row["categoria"],
                        "centro_custo": row["centro_custo"],
                        "tipo": row["tipo"],
                        "valor": float(row["valor"])
                    })
                    count += 1
                conn.commit()

            flash(f"{count} transações importadas com sucesso!", "success")
            return redirect(url_for("transacoes"))

        except Exception as e:
            flash(f"Erro ao importar: {str(e)}", "danger")
            return redirect(url_for("importar"))

    return render_template("importar.html")

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
