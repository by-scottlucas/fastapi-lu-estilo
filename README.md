# FastAPI - Lu Estilo

## 📌 Introdução

Este projeto é uma **API backend** desenvolvida com **FastAPI** voltada para o setor de **confecção**, visando facilitar a comunicação entre o **time comercial**, os **clientes** e a **empresa**.

A aplicação oferece funcionalidades como autenticação, gerenciamento de clientes, produtos e pedidos, além de filtros, paginação e uploads de arquivos.

Ela segue uma arquitetura limpa, com separação clara de responsabilidades entre módulos como `routes`, `schemas`, `models`, `services`, entre outros.

## 🚀 Como Rodar o Projeto

Para executar o projeto localmente, siga os passos abaixo:

1. **Clone o repositório**

```bash
   git clone https://github.com/by-scottlucas/fastapi-lu-estilo.git
```

2. **Acesse o diretório do projeto**

```bash
   cd fastapi-lu-estilo
```

3. **Crie um arquivo `.env` baseado no `.env.example`**

```env
   TEST_DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco_test
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
   SECRET_KEY=sua_chave_secreta
   UPLOAD_PATH=seu_diretorio_upload
```

4. **Crie e ative o ambiente virtual**

```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
```

5. **Instale as dependências**

```bash
   pip install -r requirements.txt
```

6. **Execute a aplicação**

```bash
   uvicorn main:app --reload
```

7. **Acesse a documentação interativa**

* [http://localhost:8000/docs](http://localhost:8000/docs)

## 📂 Estrutura do Projeto

```bash
├── app/
│   ├── database/         # Conexão com o banco de dados
│   ├── docs/             # Respostas de exemplo para documentação Swagger
│   ├── enums/            # Enums usados em schemas e models
│   ├── models/           # Models (tabelas) do banco de dados
│   ├── routes/           # Rotas da API
│   ├── schemas/          # Schemas para validação e documentação
│   ├── services/         # Lógica de negócio
│   ├── utils/            # Funções utilitárias (como handler de erros)
│   └── dependencies.py   # Dependências e proteção de rotas
├── migrations/           # Arquivos do Alembic (migrations)
├── tests/                # Testes automatizados
├── main.py               # Arquivo principal da aplicação
├── .env.example          # Arquivo de exemplo de variáveis de ambiente
├── .gitignore
├── alembic.ini
├── LICENSE
├── README.md
└── requirements.txt
```

## 🛠️ Tecnologias Utilizadas

* **FastAPI** – Framework web moderno e rápido
* **Uvicorn** – Servidor ASGI
* **PostgreSQL** – Banco de dados relacional
* **SQLAlchemy** – ORM para mapeamento objeto-relacional
* **Alembic** – Controle de versões do banco de dados
* **JWT (pyjwt)** – Autenticação com tokens
* **Passlib / Bcrypt** – Hash de senhas
* **Python-dotenv** – Gerenciamento de variáveis de ambiente
* **Pytest + HTTPX** – Testes automatizados

## 📦 Funcionalidades

### 🔐 Autenticação (`/api/v1/auth`)

* `POST /login`: Autenticação de usuário
* `POST /register`: Registro de novo usuário
* `POST /refresh-token`: Geração de novo token JWT

### 👥 Clientes (`/api/v1/clients`)

* `GET /`: Listar todos os clientes com paginação e filtro por nome/email
* `POST /`: Criar cliente com validação de CPF e e-mail únicos
* `GET /{id}`: Obter informações de um cliente específico
* `PUT /{id}`: Atualizar cliente
* `DELETE /{id}`: Remover cliente

### 📦 Produtos (`/api/v1/products`)

* `GET /`: Listar produtos com filtros por categoria, preço e disponibilidade
* `POST /`: Criar produto com: descrição, valor, código de barras, seção, estoque, validade e imagens
* `GET /{id}`: Obter informações de um produto específico
* `PUT /{id}`: Atualizar produto
* `DELETE /{id}`: Excluir produto

### 🧾 Pedidos (`/api/v1/orders`)

* `GET /`: Listar pedidos com filtros por período, seção, ID, status e cliente
* `POST /`: Criar pedido com múltiplos produtos, validando estoque
* `GET /{id}`: Obter detalhes de um pedido específico
* `PUT /{id}`: Atualizar status ou informações do pedido
* `DELETE /{id}`: Excluir pedido

## 🧪 Testes

Execute os testes automatizados com:

```bash
pytest
```

## 📜 Licença

Este projeto está licenciado sob a [**Licença MIT**](./LICENSE).

## 👨‍💻 Autor

Este projeto foi desenvolvido por **Lucas Santos Silva**, Desenvolvedor Full Stack, graduado pela **Escola Técnica do Estado de São Paulo (ETEC)** nos cursos de **Informática (Suporte)** e **Informática para Internet**.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/bylucasss/)