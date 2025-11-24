from app.models import engine, Base, SessionLocal
from app.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, Integer, String, Date, Numeric, text

# Set up all database tables / Configura todas as tabelas do banco
Base.metadata.create_all(bind=engine)

# Create transactions table for income and expenses / Cria tabela de transações para entradas e saídas
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transacoes_financeiras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            centro_custo VARCHAR(100) NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            valor DECIMAL(10, 2) NOT NULL
        )
    """))
    conn.commit()

db = SessionLocal()

try:
    # Create admin user if it doesn't exist / Cria usuário admin se ainda não existir
    if not db.query(User).filter(User.username == "admin").first():
        user = User(
            username="admin",
            password_hash=generate_password_hash("changeme"),
            role="admin",
            active=True
        )
        db.add(user)
        db.commit()
        print("Admin criado: admin / changeme")
    else:
        print("Admin já existe")

    # Add sample data so you can test the system / Insere dados de exemplo pra você testar o sistema
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM transacoes_financeiras"))
        count = result.scalar()

        if count == 0:
            conn.execute(text("""
                INSERT INTO transacoes_financeiras (data, categoria, centro_custo, tipo, valor) VALUES
                ('2025-11-01', 'Vendas', 'Comercial', 'entrada', 5000.00),
                ('2025-11-05', 'Salários', 'RH', 'saida', 3000.00),
                ('2025-11-10', 'Serviços', 'Operacional', 'entrada', 2500.00),
                ('2025-11-15', 'Aluguel', 'Administrativo', 'saida', 1500.00),
                ('2025-11-20', 'Consultoria', 'Comercial', 'entrada', 4000.00),
                ('2025-11-25', 'Materiais', 'Operacional', 'saida', 800.00)
            """))
            conn.commit()
            print("Dados de exemplo inseridos para Novembro/2025")
        else:
            print(f"Já existem {count} transações no banco")

finally:
    db.close()
