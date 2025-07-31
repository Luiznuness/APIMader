# Mader

API para gerenciamento de usuários, autores e livros, desenvolvida com FastAPI, SQLAlchemy (async), PostgreSQL e autenticação JWT.

## Requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Docker ou Podman (opcional, para ambiente de desenvolvimento/teste)

## Instalação

Clone o repositório e instale as dependências:

```sh
git clone https://github.com/seu-usuario/mader.git
cd mader
poetry install
```

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/nome_db
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPITE_MINUTES=30
```

## Rodando com Docker ou Podman

Você pode subir o banco de dados e a aplicação usando Docker Compose ou Podman Compose:

```sh
docker compose up --build
# ou
podman compose up --build
```

A aplicação estará disponível em `http://localhost:8000`.

## Rodando Localmente

1. Suba um banco PostgreSQL localmente.
2. Ajuste o `.env` conforme necessário.
3. Execute:

```sh
poetry run fastapi dev mader/app.py
```

## Testes

Execute os testes com cobertura:

```sh
poetry run pytest --cov=mader --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`.

## Estrutura do Projeto

```
mader
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── Autores.py
│   │   ├── base_model.py
│   │   ├── Livros.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── autores.py
│   │   ├── livros.py
│   ├── schemas.py
│   ├── security.py
│   ├── settings.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_app.py
│   │   ├── test_auth.py
│   │   ├── test_autores.py
│   │   ├── test_db.py
│   │   ├── test_livros.py
│   │   ├── test_user.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── compose.yaml
├── Dockerfile
```

## Endpoints Principais

- `POST /users` - Criação de usuário
- `GET /users` - Listagem de usuários (com paginação)
- `GET /users/{id}` - Detalhes do usuário
- `PUT /users/{id}` - Atualização de usuário (autenticado)
- `DELETE /users/{id}` - Remoção de usuário (autenticado)
- `POST /auth/token` - Geração de token JWT
- `POST /auth/refresh-token` - Refresh do token JWT
- `POST /autores` - Criação de autor (autenticado)
- `GET /autores` - Listagem de autores (autenticado, com filtros)
- `GET /autores/{id}` - Detalhes do autor
- `PUT /autores/{id}` - Atualização de autor (autenticado)
- `DELETE /autores/{id}` - Remoção de autor (autenticado)
- `POST /livros/{id_autor}` - Criação de livro para autor (autenticado)
- `GET /livros` - Listagem de livros (autenticado, com filtros)
- `PATCH /livros/{id_autor}` - Atualização de livro (autenticado)

## Exemplo de Requisição

### Criar Usuário

```json
POST /users
{
  "username": "test",
  "email": "test@test.com",
  "password": "test"
}
```

### Obter Token

```sh
curl -X POST http://localhost:8000/auth/token -d "username=test@test.com&password=test"
```

### Criar Autor

```json
POST /autores/
Headers: Authorization: Bearer <token>
{
  "name": "Napolen Hill"
}
```

### Criar Livro

```json
POST /livros/1
Headers: Authorization: Bearer <token>
{
  "ano": 1937,
  "titulo": "Pense Enriqueça"
}
```

## Licença