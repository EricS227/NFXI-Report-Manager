import pandas as pd
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

# Corrigido: pymysql
engine = create_engine("mysql+pymysql://user:senha@localhost/nxfi")


def gerar_relatorio_fluxo_caixa(mes, ano):
    query = f"""
        SELECT data, categoria, centro_custo, tipo, valor
        FROM transacoes_financeiras
        WHERE MONTH(data) = {mes} AND YEAR(data) = {ano};
    """

    df = pd.read_sql(query, engine)

    total_entrada = df[df['tipo'] == 'entrada']['valor'].sum()
    total_saida = df[df['tipo'] == 'saida']['valor'].sum()
    saldo_final = total_entrada - total_saida

    doc = SimpleDocTemplate(f"fluxo_caixa_{mes}_{ano}.pdf")
    estilos = getSampleStyleSheet()

    conteudo = [
        Paragraph(f"Relatório de fluxo de caixa - {mes}/{ano}", estilos['Title']),
        Paragraph(f"Entradas: R$ {total_entrada:,.2f}", estilos['Normal']),
        Paragraph(f"Saídas: R$ {total_saida:,.2f}", estilos['Normal']),
        Paragraph(f"Saldo Final: R$ {saldo_final:,.2f}", estilos['Normal']),
        Table([df.columns.tolist()] + df.values.tolist())
    ]

    doc.build(conteudo)

    print(f"Relatório gerado: fluxo_caixa_{mes}_{ano}.pdf")


# Teste
gerar_relatorio_fluxo_caixa(10, 2025)
