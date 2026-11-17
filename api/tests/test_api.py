from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# Base SQLite en mémoire UNIQUEMENT pour les tests (jamais en production)
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_todo_lifecycle():
    r = client.post("/todos", json={"title": "test"})
    assert r.status_code == 201
    todo_id = r.json()["id"]
    assert client.patch(f"/todos/{todo_id}").json()["done"] is True
    assert any(t["id"] == todo_id for t in client.get("/todos").json())
    assert client.delete(f"/todos/{todo_id}").status_code == 204
