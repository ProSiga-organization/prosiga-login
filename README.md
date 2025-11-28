# PróSiga Login

Serviço de Autenticação do Sistema de Gerenciamento Acadêmico

## 🚀 Tecnologias

- **FastAPI** - Framework web Python moderno
- **SQLAlchemy** - ORM Python
- **PostgreSQL** - Banco de dados relacional (compartilhado com backend principal)
- **JWT (JSON Web Tokens)** - Autenticação stateless
- **Passlib + bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI

## 📋 Pré-requisitos

- Python 3.10+
- PostgreSQL 13+ (mesmo banco do backend principal)
- pip para gerenciamento de dependências

## ⚙️ Configuração

### 1. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_CONNECT_URL=postgresql://usuario:senha@localhost:5432/prosiga_db
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Para produção (Render):
```env
DB_CONNECT_URL=postgresql://prosiga_db_user:senha@host.oregon-postgres.render.com/prosiga_db
SECRET_KEY=chave_production_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **IMPORTANTE**: Use a mesma `DB_CONNECT_URL` do backend principal, pois compartilham o mesmo banco de dados!

## 🏃 Executando o projeto

### Opção 1: Desenvolvimento local (sem Docker)

```bash
uvicorn app.main:app --reload --port 9000
```

Acesse:
- API: http://localhost:9000
- Documentação interativa (Swagger): http://localhost:9000/docs
- Health check: http://localhost:9000/

### Opção 2: Com Docker 🐳

O projeto possui `Dockerfile` e `docker-compose.yml` configurados.

**Subir o serviço:**
```bash
docker-compose up --build
```

**Subir em background:**
```bash
docker-compose up -d
```

**Parar o serviço:**
```bash
docker-compose down
```

**Ver logs:**
```bash
docker-compose logs -f
```

**Serviços disponíveis via Docker:**
- Auth API: http://localhost:9000
- Documentação: http://localhost:9000/docs

### Porta padrão

Por convenção, este serviço roda na **porta 9000** para não conflitar com o backend principal (porta 8000).

## 🔐 Funcionalidades

### 1. Login (POST /login/)

Autentica usuário e retorna token JWT.

**Requisição:**
```bash
curl -X POST "http://localhost:9000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@email.com&password=senha123"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Validações:**
- Usuário deve existir
- Status deve ser `ATIVO` (não `NOVO`)
- Senha deve estar correta

### 2. Obter usuário atual (GET /login/me)

Retorna dados do usuário autenticado via token JWT.

**Requisição:**
```bash
curl -X GET "http://localhost:9000/login/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "id": 1,
  "cpf": "11122233301",
  "nome": "Bruno Alves",
  "email": "bruno@email.com",
  "tipo_usuario": "aluno",
  "status": "ATIVO",
  "matricula": "20250001",
  "id_curso": 1
}
```

## 📁 Estrutura do projeto

```
prosiga-login/
├── app/
│   ├── main.py                    # Aplicação principal FastAPI
│   ├── config.py                  # Configurações e variáveis de ambiente
│   ├── database.py                # Conexão SQLAlchemy
│   ├── model.py                   # Modelos (compartilhados com backend)
│   ├── security.py                # JWT, hash de senhas
│   └── login/
│       ├── router.py              # Rotas de autenticação
│       ├── repository.py          # Lógica de acesso ao banco
│       └── schema.py              # Schemas Pydantic
├── requirements.txt               # Dependências Python
├── Dockerfile                     # Imagem Docker
├── Procfile                       # Configuração Render
├── runtime.txt                    # Versão Python (Render)
└── README.md
```

## 🔌 Endpoints

### POST /login/
Realiza login e retorna token JWT.

**Body (form-urlencoded):**
- `username` (string): Email do usuário
- `password` (string): Senha

**Resposta:**
```json
{
  "access_token": "token_jwt",
  "token_type": "bearer"
}
```

**Erros:**
- `401 Unauthorized`: Credenciais inválidas ou usuário não ativo

### GET /login/me
Retorna dados do usuário autenticado.

**Headers:**
- `Authorization: Bearer {token}`

**Resposta:**
```json
{
  "id": 1,
  "nome": "Nome do Usuário",
  "email": "email@exemplo.com",
  "tipo_usuario": "aluno|professor|coordenador",
  "status": "ATIVO|NOVO|INATIVO"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido ou expirado

### GET /
Health check do serviço.

**Resposta:**
```json
{
  "status": "fine"
}
```

## 🔒 Segurança

### Hashing de senhas

- Utiliza **bcrypt** via **passlib**
- Senhas nunca são armazenadas em texto plano
- Algoritmo: `bcrypt` com salt automático

### JWT Tokens

- **Algoritmo**: HS256 (configurável)
- **Expiração**: 30 minutos (configurável)
- **Payload**: Contém apenas o email do usuário (`sub`)
- **Secret Key**: Deve ser mantida em segredo (variável de ambiente)

### Geração de SECRET_KEY

Para gerar uma chave secreta segura:

```python
import secrets
print(secrets.token_urlsafe(32))
```

## 🌐 CORS

Configurado para aceitar requisições de:
- `http://localhost:3000` (desenvolvimento frontend)
- `https://*.vercel.app` (produção e preview deployments)

Regex utilizado: `r"https?://(localhost|.*\.vercel\.app)(:\d+)?"`

## 🌐 Deploy

### Render

O projeto está configurado para deploy no Render como Web Service:

**Configuração:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python Version: Definida em `runtime.txt`

**URL de produção**: https://prosiga-login.onrender.com

### Variáveis de ambiente no Render

Configure no painel do Render:
- `DB_CONNECT_URL` - URL do banco PostgreSQL (mesma do backend)
- `SECRET_KEY` - Chave secreta para JWT
- `ALGORITHM` - `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`

## 🔗 Serviços relacionados

- **Frontend**: [prosiga-front](../prosiga-front) - Next.js
- **Backend Principal**: [back-prosiga](../back-prosiga) - FastAPI

## 🔄 Fluxo de autenticação

```
1. Usuário → Frontend: Envia email e senha
2. Frontend → Login Service: POST /login/
3. Login Service → Database: Valida credenciais
4. Login Service → Frontend: Retorna JWT token
5. Frontend: Armazena token no localStorage
6. Frontend → Login Service: GET /login/me (com token)
7. Login Service → Frontend: Retorna dados do usuário
8. Frontend: Redireciona baseado em tipo_usuario
```

## 🐛 Debugging

### Problemas comuns

**Erro "Email ou senha incorretos":**
- Verifique se o usuário fez primeiro acesso
- Confirme que o status é `ATIVO` (não `NOVO`)
- Teste a senha manualmente

**Erro "invalid session id":**
- Token JWT expirou (padrão: 30 minutos)
- SECRET_KEY mudou entre ambientes
- Token foi gerado por outra instância

**Erro de conexão com banco:**
- Verifique se `DB_CONNECT_URL` está correto
- Confirme que é o mesmo banco do backend principal
- Teste conexão com `psql`

### Testar endpoints manualmente

```bash
# Login
curl -X POST "http://localhost:9000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=bruno@email.com&password=teste-bruno"

# Obter usuário (substitua TOKEN pelo retornado acima)
curl -X GET "http://localhost:9000/login/me" \
  -H "Authorization: Bearer TOKEN"
```

## 📊 Monitoramento

### Logs importantes

```python
# Sucesso no login
"Login bem-sucedido para: email@exemplo.com"

# Falha no login
"Tentativa de login falhou: credenciais inválidas"

# Token inválido
"Token JWT inválido ou expirado"
```

## 📄 Licença

Este projeto é parte do sistema acadêmico PróSiga.
