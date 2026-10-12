from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    payload = {"email": "user@example.com", "username": "userone", "password": "StrongPass123!"}
    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    assert token

    login = client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert login.status_code == 200, login.text
    assert login.json()["token_type"] == "bearer"


def test_unauthorized_access():
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401
