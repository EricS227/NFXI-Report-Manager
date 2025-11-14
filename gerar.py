import pandas as pd
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


# Corrigido: pymysql
engine = create_engine("mysql+pymysql://user:senha@localhost/nxfi")


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




def gerar_relatorio_fluxo_caixa(mes, ano):

    try:
        query = f"""
            SELECT data, categoria, centro_custo, tipo, valor
            FROM transacoes_financeiras
            WHERE MONTH(data) = {mes} AND YEAR(data) = {ano};
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            print("Nenhum dado encontrado para esse período")
            return
        
        df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
        df["valor"] = df["valor"].apply(formatar_moeda)

        entradas = df[df['tipo'] == 'entrada']
        saidas = df[df['tipo'] == 'saida']

        total_entrada = entradas['valor'].str.replace("R$ ", "").str.replace(",", "").str.replace(",", ".").astype(float).sum()
        total_saida = saidas['valor'].str.replace("R$ ", "").str.replace(".", "").str.replace(",", ".").astype(float).sum()
        saldo_final = total_entrada - total_saida

        doc = SimpleDocTemplate(
            f"fluxo_caixa_{mes}_{ano}.pdf",
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
            textColor = colors.black,
            spaceAfter=10
        )

        conteudo = []

        conteudo.append(Paragraph(f"Relatório de Fluxo de Caixa - {mes}/{ano}", titulo))
        conteudo.append(Spacer(1, 20))

        resumo_texto = f"""
        <b>Entradas:</b> {formatar_moeda(total_entrada)}<br/>
        <b>Saídas:</b> {formatar_moeda(total_saida)}<br/>
        <b>Saldo Final:</b> {formatar_moeda(saldo_final)}

        """
        conteudo.append(Paragraph(resumo_texto, resumo_style))
        conteudo.append(Spacer(1,20))

        tabela_dados = [df.columns.tolist()] + df.values.tolist()
        tabela= Table(tabela_dados)

        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1, -1), 0.3, colors.grey),
            ('FONTNAME', (0, 0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ])) 

        conteudo.append(tabela)

        doc.build(conteudo)

        print("Relatório gerado com sucesso: fluxo_caixa_{mes}_{ano}.pdf")

    except Exception as e:
        print("Erro ao gerar relatório:", str(e))

# Teste
gerar_relatorio_fluxo_caixa(10, 2025)
