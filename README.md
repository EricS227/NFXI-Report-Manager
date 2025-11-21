# 💰 NFxi Report - Cash Flow System / Sistema de Fluxo de Caixa

Web system for financial management and PDF cash flow report generation.

Sistema web para gerenciamento financeiro e geração de relatórios de fluxo de caixa em PDF.

## ✨ Features / Funcionalidades

- 🔐 **Authentication** - User login/logout / Autenticação de usuários
- 📊 **Dashboard** - View income, expenses, and balance / Visualização de entradas, saídas e saldo
- 📄 **PDF Reports** - Generate reports by month/year / Geração de relatórios por mês/ano
- ➕ **Transactions** - Add individual transactions / Cadastro individual de transações
- 📥 **CSV Import** - Bulk import transactions / Importação em lote de transações
- 👥 **User API** - User management (admin) / Gerenciamento de usuários

## 🛠️ Technologies / Tecnologias

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Database:** SQLite
- **PDF:** ReportLab
- **Frontend:** HTML, CSS, Jinja2

## 🚀 Installation / Instalação

```bash
# Clone the repository / Clone o repositório
git clone https://github.com/your-username/relatorio_nfxi.git
cd relatorio_nfxi

# Install dependencies / Instale as dependências
pip install -r requirements.txt

# Setup database / Configure o banco de dados
python create_db_and_admin.py

# Run the application / Execute a aplicação
python main.py
```

Access / Acesse: http://127.0.0.1:5000

## 🔑 Default Credentials / Credenciais Padrão

- **Username / Usuário:** admin
- **Password / Senha:** changeme

## 📁 Project Structure / Estrutura do Projeto

```
relatorio_nfxi/
├── app/
│   ├── models.py           # Database models / Modelos do banco
│   ├── config.py           # Configuration / Configurações
│   ├── routes/             # API routes / Rotas da API
│   ├── services/           # Business logic / Lógica de negócio
│   └── repositories/       # Database access / Acesso ao banco
├── relatorio/
│   └── gerar_relatorio.py  # PDF generation / Geração de PDF
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── relatorios/             # Generated PDFs / PDFs gerados
├── main.py                 # Flask application
├── create_db_and_admin.py  # Database setup
├── requirements.txt        # Dependencies
└── .env                    # Environment variables
```

## 🔌 User API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/users/ | List users / Listar usuários |
| POST | /api/users/ | Create user / Criar usuário |
| PUT | /api/users/:id | Update user / Atualizar usuário |
| DELETE | /api/users/:id | Delete user / Remover usuário |

*Requires admin authentication / Requer autenticação de admin*

## ⚙️ Configuration / Configuração

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
JWT_EXPIRATION=3600
```
