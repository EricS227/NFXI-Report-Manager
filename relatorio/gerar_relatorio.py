import pandas as pd
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection using environment variables
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'senha')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'nxfi')

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




def gerar_relatorio_fluxo_caixa(mes, ano):

    try:
        query = """
            SELECT data, categoria, centro_custo, tipo, valor
            FROM transacoes_financeiras
            WHERE MONTH(data) = %s AND YEAR(data) = %s;
        """

        df = pd.read_sql(query, engine, params=(mes, ano))

        if df.empty:
            return None

        
        df['valor_float'] = df['valor'].astype(float)
        
        df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
        df["valor"] = df["valor_float"].apply(formatar_moeda)


        total_entrada = df[df['tipo'] == 'entrada']['valor_float'].sum()
        total_saida = df[df['tipo'] == 'saida']['valor_float'].sum()
        saldo_final = total_entrada - total_saida
        
        #total_entrada = entradas['valor'].str.replace("R$ ", "").str.replace(",", "").str.replace(",", ".").astype(float).sum()
       # total_saida = saidas['valor'].str.replace("R$ ", "").str.replace(".", "").str.replace(",", ".").astype(float).sum()
        #saldo_final = total_entrada - total_saida

        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")

        caminho_pdf = os.path.join("relatorios", f"fluxo_caixa_{mes}_{ano}.pdf")
        doc = SimpleDocTemplate(
            caminho_pdf,
            pagesize=A4,
            rightMargin = 30, leftMargin = 30, topMargin = 30, bottomMargin = 30
        )

        estilos = getSampleStyleSheet()
        titulo = estilos['Title']

        resumo_style = ParagraphStyle(
            'Resumo',
            parent=estilos['Normal'],
            fontSize=12,
            leading=14,
            #textColor = colors.black,
            spaceAfter=10
        )
        
        conteudo = [
            Paragraph(f"Relatório de Fluxo de Caixa - {mes}/{ano}", titulo),
            Spacer(1, 20),
            Paragraph(
                f"<b>Entradas:</b> {formatar_moeda(total_entrada)}<br/>"
                f"<b>Saídas:</b> {formatar_moeda(total_saida)}<br/>"
                f"<b>Saldo Final:</b> {formatar_moeda(saldo_final)}",
                resumo_style
            ),
            Spacer(1, 20)
        ]

        tabela_dados  = [df[['data', 'categoria', 'centro_custo', 'tipo', 'valor']].columns.tolist()] + \
                        df[['data', 'categoria', 'centro_custo', 'tipo', 'valor']].values.tolist()

        tabela = Table(tabela_dados, repeatRows=1)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4682B4")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
        ]))
      
       

        conteudo.append(tabela)

        doc.build(conteudo)

        resumo = {
            "entrada": formatar_moeda(total_entrada),
            "saida": formatar_moeda(total_saida),
            "saldo": formatar_moeda(saldo_final)
        }

        return caminho_pdf , resumo

    except Exception as e:
        print("Erro ao gerar relatório:", str(e))
        return None
