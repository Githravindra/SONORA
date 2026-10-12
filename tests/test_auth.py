from fastapi.testclient import TestClient

from app.db.session import SessionLocal, init_db
from app.main import app


client = TestClient(app)


def override_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()
