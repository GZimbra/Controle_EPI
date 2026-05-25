# Controle de EPI

Sistema FastAPI para controle corporativo de retirada de EPIs com LGPD, audit trail e retenção legal.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- SQLite em dev e PostgreSQL em produção via `DATABASE_URL`
- Fernet para criptografia em repouso
- JWT Bearer
- APScheduler para backup, CA vencido e estoque mínimo

## Setup local

```powershell
cd "C:\Users\Zimbra\Documents\Projetos\PROFISSIONAL\Controle de EPI\epi_system"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY
Copy-Item .env.example .env
# Ajuste SECRET_KEY, FERNET_KEY e CPF_PEPPER no .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

OpenAPI: `http://localhost:8000/docs`

Usuário seed: `admin`  
Senha seed: `admin123-change`

## Docker

Configure `.env`:

```env
DATABASE_URL=postgresql+psycopg://epi:epi_change_me@postgres:5432/epi
SECRET_KEY=troque
FERNET_KEY=gere_com_cryptography
CPF_PEPPER=troque
CORS_ORIGINS=http://localhost:8000
```

Suba:

```powershell
docker compose up --build
```

## Vercel

O projeto está preparado para deploy com root em `epi_system`.

Arquivos relevantes:

- `vercel.json`: publica `index.html` e direciona rotas da API para `api/index.py`
- `api/index.py`: handler serverless da aplicação FastAPI
- `.vercelignore`: remove testes, backups, Docker e arquivos locais do deploy

Variáveis obrigatórias no painel da Vercel:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/database
SECRET_KEY=troque_por_valor_forte
FERNET_KEY=gere_com_cryptography
CPF_PEPPER=troque_por_valor_forte
CORS_ORIGINS=https://seu-projeto.vercel.app
DPO_CONTACT=dpo@empresa.com.br
PRIVACY_POLICY_VERSION=2026-05-25
SIGNATURE_STORAGE_DIR=/tmp/signatures
BACKUP_DIR=/tmp/backups
```

Notas operacionais:

- Use PostgreSQL em produção. SQLite na Vercel não é persistente.
- Scheduler e backup local são desativados automaticamente quando `VERCEL=1`.
- Para produção real, substitua storage local de assinaturas por storage externo criptografado.
- Rode a migration no banco de produção antes do primeiro uso:

```powershell
alembic upgrade head
```

## Endpoints principais

- `POST /auth/login`
- `POST /epis`, `GET /epis`, `PATCH /epis/{id}`, `DELETE /epis/{id}`
- `POST /colaboradores`, `GET /colaboradores`, `PATCH /colaboradores/{id}`, `DELETE /colaboradores/{id}`
- `POST /retiradas`, `GET /retiradas`, `PATCH /retiradas/{id}/status`
- `GET /audit`, `GET /audit/export.json`, `GET /audit/export.csv`
- `POST /lgpd/acesso`
- `POST /lgpd/correcao`
- `POST /lgpd/exclusao`
- `POST /lgpd/portabilidade`
- `POST /lgpd/revogacao-consentimento`
- `GET /lgpd/compartilhamento`
- `POST /lgpd/oposicao`
- `GET /lgpd/revisao-decisao-automatizada`
- `GET /lgpd/ripd`
- `GET /privacidade`

## Segurança e conformidade

- CPF nunca é armazenado em claro: `SHA-256(cpf + salt + pepper)`.
- Assinatura não é armazenada em claro: imagem base64 vira arquivo criptografado Fernet; banco guarda hash e path.
- `audit_log` é separado e imutável por listener SQLAlchemy.
- Logs de auditoria pseudonimizam campos pessoais e assinatura.
- Exclusão de titular é soft delete para preservar obrigações legais.
- CORS é explícito por `CORS_ORIGINS`.
- Erros HTTP internos retornam mensagem genérica.
- Backups são retidos por `BACKUP_RETENTION_YEARS`, padrão 5 anos.

## Testes

```powershell
pytest
```
