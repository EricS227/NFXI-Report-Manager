from flask import Flask, render_template, request, send_file, flash
from relatorio.gerar_relatorio import gerar_relatorio_fluxo_caixa
import os
from app.routes.user_routes import user_bp


app = Flask(__name__)
app.secret_key = ""

@app.route("/")
def home():
    return render_template("index.html", resumo=None, pdf_file=None)

@app.route("/gerar", methods=["POST"])
def gerar():
    mes = request.form.get("mes")
    ano = request.form.get("ano")

    if not mes or not ano:
        flash("Seleciione o mês e ano")
        return render_template("index.html", resumo=None, pdf_file=None)
    
    resultado = gerar_relatorio_fluxo_caixa(int(mes), int(ano))
    
    #caminho_pdf, resumo = gerar_relatorio_fluxo_caixa(int(mes), int(ano))

    if not resultado:
        flash("Nenhum dado encontrado para esse período")
        return render_template("index.html", resumo=None, pdf_file=None)
    
    caminho_pdf, resumo = resultado

    filename = os.path.basename(caminho_pdf)
    
    return render_template(
        "index.html",
        resumo=resumo,
        pdf_file=filename
    )

@app.route("/download/<filename>")
def download(filename):
    caminho = os.path.join("relatorios", filename)
    return send_file(caminho, as_attachment=True)



app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)