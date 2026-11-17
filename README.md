# Mise en prod & Hébergement 1

Todo list déployée sur Scalingo : client React/TypeScript + API FastAPI + PostgreSQL managé.

## Architecture

```
Navigateur ──HTTPS──> App 1 : client (React/Vite, buildpack Node.js)
Navigateur ──HTTPS──> App 2 : API (FastAPI, buildpack Python) ──SQL──> Addon PostgreSQL Starter 512
```

- `client/` : React + TypeScript + Vite, servi par `serve -s dist` sur `$PORT`.
- `api/` : FastAPI, SQLAlchemy, migrations Alembic, `Procfile` (web + postdeploy).
- Seule l'API parle à la base. Pas de disque, pas de SQLite en production.
- Monorepo : chaque app Scalingo pointe vers son dossier via `PROJECT_DIR`.

## Développement local

```bash
docker compose up -d                 # PostgreSQL local
cd api && cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head && python seed.py
uvicorn app.main:app --reload        # http://localhost:8000/docs

cd ../client && cp .env.example .env
npm install && npm run dev           # http://localhost:5173
```

## Variables d'environnement (sans valeurs)

| App | Variable | Rôle |
|---|---|---|
| API | `PROJECT_DIR` | `api` (monorepo) |
| API | `SCALINGO_POSTGRESQL_URL` | fournie automatiquement par l'addon |
| API | `CORS_ORIGINS` | URL publique du client |
| Client | `PROJECT_DIR` | `client` (monorepo) |
| Client | `VITE_API_URL` | URL publique de l'API (figée au build) |

## Procédure de déploiement

1. Créer les apps : `scalingo create <nom>-api` et `scalingo create <nom>-client`.
2. API : `scalingo --app <nom>-api env-set PROJECT_DIR=api`, puis
   `scalingo --app <nom>-api addons-add postgresql postgresql-starter-512`.
3. Lier chaque app au dépôt GitHub (dashboard, onglet Deploy) et activer Auto Deploy sur `main`.
4. Premier déploiement de l'API, puis `scalingo --app <nom>-api env-set CORS_ORIGINS=https://<url-client>`.
5. Client : `env-set PROJECT_DIR=client VITE_API_URL=https://<url-api>` **avant** le déploiement.
6. Seed (une fois) : `scalingo --app <nom>-api run python seed.py`.
7. Vérifier `https://<url-api>/health` et `/docs`, puis le client.

## Coût mensuel

- Estimé (simulateur Scalingo) : _à compléter_
- Réel (Billing) : _à compléter_

## En cas de panne

_À compléter avec les commandes réellement testées :_

```bash
scalingo --app <nom>-api logs --lines 200
scalingo --app <nom>-api deployments            # liste
scalingo --app <nom>-api deployment-rollback    # rollback (vérifier la syntaxe avec scalingo help)
scalingo --app <nom>-api --addon <id> backups   # sauvegardes PostgreSQL
```
