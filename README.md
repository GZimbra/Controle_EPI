# Controle de EPI

Sistema FastAPI para controle corporativo de retirada de EPIs com LGPD, audit trail e retencao legal.

## Estrutura

O codigo da aplicacao fica em:

```text
epi_system/
```

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- SQLite em dev e PostgreSQL em producao via `DATABASE_URL`
- Fernet para criptografia em repouso
- JWT Bearer
- APScheduler para backup, CA vencido e estoque minimo
- HTML/CSS/JavaScript vanilla em `epi_system/index.html`

## Setup local

```powershell
cd "C:\Users\Zimbra\Documents\Projetos\PROFISSIONAL\Controle de EPI\epi_system"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
Copy-Item .env.example .env
# Ajuste SECRET_KEY, FERNET_KEY e CPF_PEPPER no .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

OpenAPI:

```text
http://localhost:8000/docs
```

Usuario seed:

```text
admin / admin123-change
```

## Frontend

Arquivo standalone:

```text
epi_system/index.html
```

Por padrao:

```js
const DEMO_MODE = true;
```

Com `DEMO_MODE = true`, a interface usa dados mock locais e abre direto no navegador.

Para consumir a API real, altere para:

```js
const DEMO_MODE = false;
```

Abas principais da interface:

- `Solicitar EPI`: fluxo direto para registrar retirada com assinatura digital.
- `Base de Dados`: acompanhamento consolidado de EPIs, colaboradores, retiradas e export JSON.

## Docker

Configure `epi_system/.env`:

```env
DATABASE_URL=postgresql+psycopg://epi:epi_change_me@postgres:5432/epi
SECRET_KEY=troque
FERNET_KEY=gere_com_cryptography
CPF_PEPPER=troque
CORS_ORIGINS=http://localhost:8000
```

Suba:

```powershell
cd "C:\Users\Zimbra\Documents\Projetos\PROFISSIONAL\Controle de EPI\epi_system"
docker compose up --build
```

## Vercel

O projeto esta preparado para deploy direto pela raiz do repositorio.

Arquivos relevantes:

- `vercel.json`: publica `epi_system/index.html` e direciona rotas da API para `api/index.py`
- `api/index.py`: handler serverless da aplicacao FastAPI, adicionando `epi_system/` ao `PYTHONPATH`
- `requirements.txt`: aponta para `epi_system/requirements.txt`
- `.vercelignore`: remove testes, backups, Docker e arquivos locais do deploy

No painel da Vercel:

```text
Framework Preset: Other
Root Directory: ./
Build Command: vazio
Output Directory: vazio
Install Command: vazio ou pip install -r requirements.txt
```

Variaveis obrigatorias no painel da Vercel:

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
VERCEL=1
AUTO_CREATE_TABLES=true
```

Notas operacionais:

- Use PostgreSQL em producao. SQLite na Vercel nao e persistente.
- Scheduler e backup local sao desativados automaticamente quando `VERCEL=1`.
- Para producao real, substitua storage local de assinaturas por storage externo criptografado.
- `AUTO_CREATE_TABLES=true` cria o schema automaticamente no primeiro cold start para facilitar o primeiro deploy.
- A aplicacao nao exige login. A interface abre direto no painel.
- Para operacao controlada, depois do primeiro deploy execute migration externamente e altere `AUTO_CREATE_TABLES=false`.
- Alternativa manual para migrar o banco de producao:

```powershell
cd epi_system
alembic upgrade head
```

## Endpoints principais

- `POST /epis`, `GET /epis`, `GET /epis/alertas`, `PATCH /epis/{id}`, `DELETE /epis/{id}`
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

## Seguranca e conformidade

- CPF nunca e armazenado em claro: `SHA-256(cpf + salt + pepper)`.
- Assinatura nao e armazenada em claro: imagem base64 vira arquivo criptografado Fernet; banco guarda hash e path.
- `audit_log` e separado e imutavel por listener SQLAlchemy.
- Logs de auditoria pseudonimizam campos pessoais e assinatura.
- Exclusao de titular e soft delete para preservar obrigacoes legais.
- CORS e explicito por `CORS_ORIGINS`.
- Erros HTTP internos retornam mensagem generica.
- Backups sao retidos por `BACKUP_RETENTION_YEARS`, padrao 5 anos.

## Testes

```powershell
cd epi_system
pytest
```
