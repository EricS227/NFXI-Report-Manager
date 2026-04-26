NFXI Report Manager

Web application for cash flow management and financial reporting, with user authentication, role-based access control, dashboard, CSV import, and PDF report generation by month and year.
Aplicação web para gerenciamento de fluxo de caixa e geração de relatórios financeiros, com autenticação de usuários, controle de acesso por perfil, dashboard, importação via CSV e geração de relatórios em PDF por mês e ano.

Tech Stack / Tecnologias

Python 3
Flask
Flask-Login (session-based auth / autenticação por sessão)
SQLAlchemy (ORM)
SQLite
ReportLab (PDF generation / geração de PDF)
pandas (data processing for reports / processamento de dados para relatórios)
Werkzeug (password hashing / hash de senhas)
Chart.js (dashboard charts / gráficos do dashboard)


Features / Funcionalidades
English

User registration and login with hashed passwords
Role-based access control (admin, financeiro)
Financial transactions management (income and expense)
Dashboard with income/expense/balance summary, monthly totals, and totals by category
CSV import for bulk transactions
On-demand PDF cash flow report generation by month and year
REST API for user administration (admin only)

Português

Registro e login de usuários com senhas hasheadas
Controle de acesso por perfil (admin, financeiro)
Gerenciamento de transações financeiras (entrada e saída)
Dashboard com resumo de entradas/saídas/saldo, totais mensais e totais por categoria
Importação de transações em lote via CSV
Geração sob demanda de relatórios de fluxo de caixa em PDF por mês e ano
API REST para administração de usuários (apenas admin)


Purpose / Objetivo
This project was developed to practice real-world backend concepts with Flask: layered project organization (routes, services, repositories, models), authentication and role-based authorization, data persistence with SQLAlchemy, bulk CSV import, PDF generation with ReportLab, and a JSON REST API alongside server-rendered pages.
Este projeto foi desenvolvido para praticar conceitos reais de backend com Flask: organização em camadas (rotas, serviços, repositórios, models), autenticação e autorização por perfil, persistência de dados com SQLAlchemy, importação em lote via CSV, geração de PDF com ReportLab, e uma API REST JSON convivendo com páginas renderizadas no servidor.

Project Structure / Estrutura do Projeto
NFXI-Report-Manager/
├── main.py                       # Flask entry point / Ponto de entrada do Flask
├── create_db_and_admin.py        # Initializes DB and default admin user / Inicializa DB e admin padrão
├── requirements.txt
├── exemplo_transacoes.csv        # Sample CSV for import / CSV de exemplo para importação
├── .env.example
├── .gitignore
├── app/
│   ├── models.py                 # SQLAlchemy models and engine / Models e engine do SQLAlchemy
│   ├── config.py
│   ├── controllers/              # Request handlers / Tratadores de requisição
│   ├── routes/                   # Flask blueprints / Blueprints do Flask
│   ├── services/                 # Business logic / Regras de negócio
│   ├── repositories/             # Data access layer / Camada de acesso a dados
│   ├── transactions/             # Transactions module (models, service, router) / Módulo de transações
│   ├── auth/                     # Auth helpers / Auxiliares de autenticação
│   └── utils/                    # Security helpers, DB helpers / Utilitários de segurança e DB
├── relatorio/
│   └── gerar_relatorio.py        # PDF report generator (ReportLab) / Gerador de relatório em PDF
├── templates/                    # Jinja2 templates / Templates Jinja2
│   ├── index.html                # Home: report generator / Home: gerador de relatório
│   ├── dashboard.html            # Metrics dashboard / Dashboard de métricas
│   ├── login.html
│   ├── register.html
│   ├── transacoes.html           # Transactions CRUD / CRUD de transações
│   └── importar.html             # CSV import / Importação CSV
└── static/
    └── style.css

Database / Banco de Dados
The application uses SQLite (file database.db, created automatically on first run by create_db_and_admin.py).
A aplicação utiliza SQLite (arquivo database.db, criado automaticamente na primeira execução por create_db_and_admin.py).
Tables / Tabelas
users — managed by SQLAlchemy / gerenciada pelo SQLAlchemy
Column / ColunaType / TipoNotes / ObservaçõesidINTEGERPrimary keyusernameVARCHAR(150)Unique, required / Único, obrigatóriopassword_hashVARCHAR(256)Werkzeug hashroleVARCHAR(50)admin or financeiroactiveBOOLEANDefault truecreated_atDATETIMESet by database / Definido pelo banco
transacoes_financeiras — created via raw SQL / criada via SQL direto
Column / ColunaType / TipoNotes / ObservaçõesidINTEGERPrimary key, auto-incrementdataDATEFormat YYYY-MM-DDcategoriaVARCHAR(100)e.g. Vendas, Salários, Aluguelcentro_custoVARCHAR(100)e.g. Comercial, RH, OperacionaltipoVARCHAR(20)entrada or saidavalorDECIMAL(10,2)Monetary value / Valor monetário

Quick Start / Início Rápido
Requirements / Requisitos

Python 3.10+
pip

Installation / Instalação
bash# Clone the repository / Clone o repositório
git clone https://github.com/EricS227/NFXI-Report-Manager.git
cd NFXI-Report-Manager

# (Optional) Create a virtual environment / (Opcional) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# Install dependencies / Instale as dependências
pip install -r requirements.txt

# Initialize database, default admin, and sample data / Inicializa o banco, admin padrão e dados de exemplo
python create_db_and_admin.py

# Run the application / Execute a aplicação
python main.py
The application will be available at / A aplicação estará disponível em:
http://localhost:5000
Default Admin / Admin Padrão
The create_db_and_admin.py script creates a default user on first run:
O script create_db_and_admin.py cria um usuário padrão na primeira execução:

Username: admin
Password: changeme


Change this password immediately after the first login in a real environment.
Altere essa senha imediatamente após o primeiro login em um ambiente real.


Routes / Rotas
Web / Web (HTML)
Route / RotaMethod / MétodoAccess / AcessoDescription / Descrição/loginGET, POSTPublic / PúblicoLogin page / Página de login/registerGET, POSTPublic / PúblicoUser registration (role financeiro) / Registro de usuário/logoutGETAuthenticated / AutenticadoEnd session / Encerra a sessão/GETAuthenticatedHome with report generation form / Home com form de geração/dashboardGETAuthenticatedMetrics dashboard / Dashboard de métricas/transacoesGET, POSTAuthenticatedList and create transactions / Lista e cria transações/importarGET, POSTAuthenticatedCSV import page / Página de importação CSV/gerarPOSTAuthenticatedGenerate PDF for month/year / Gera PDF para mês/ano/download/<filename>GETAuthenticatedDownload a generated PDF / Baixa um PDF gerado
API REST (JSON)
Prefix / Prefixo: /api/users — all routes require admin role / todas as rotas exigem perfil admin.
Route / RotaMethod / MétodoDescription / Descrição/api/users/GETList all users / Lista todos os usuários/api/users/POSTCreate user / Cria usuário/api/users/<id>PUTUpdate user / Atualiza usuário/api/users/<id>DELETERemove user / Remove usuário

CSV Import Format / Formato do CSV de Importação
Required column headers (first row). See exemplo_transacoes.csv for a complete sample.
Cabeçalhos obrigatórios (primeira linha). Veja exemplo_transacoes.csv para um exemplo completo.
csvdata,categoria,centro_custo,tipo,valor
2025-12-01,Vendas,Comercial,entrada,5000.00
2025-12-05,Salários,RH,saida,3000.00

data: date in YYYY-MM-DD / data no formato YYYY-MM-DD
tipo: entrada or saida / entrada ou saida
valor: decimal (point as separator) / decimal (ponto como separador)


PDF Reports / Relatórios em PDF
Generated through the home page by selecting month and year. The report includes:
Gerados a partir da página inicial selecionando mês e ano. O relatório inclui:

Total income, total expense, final balance / Total de entradas, total de saídas, saldo final
Detailed table of transactions for the period / Tabela detalhada das transações do período

PDF files are saved in the relatorios/ folder (created automatically, ignored by git).
Os arquivos PDF são salvos na pasta relatorios/ (criada automaticamente, ignorada pelo git).

Author / Autor
Eric Simões

GitHub: @EricS227
