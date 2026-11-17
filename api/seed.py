"""Données initiales. Lancer une fois : scalingo --app <app-api> run python seed.py"""
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Todo

SEED = ["Déployer l'API sur Scalingo", "Déployer le client", "Activer l'Auto Deploy"]

with SessionLocal() as db:
    if db.scalars(select(Todo)).first() is None:
        db.add_all(Todo(title=t) for t in SEED)
        db.commit()
        print("Seed OK")
    else:
        print("Base déjà peuplée, rien à faire")
