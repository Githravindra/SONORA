from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_playback_event_tracking():
    register = client.post("/api/v1/auth/register", json={"email": "playback@example.com", "username": "playbackuser", "password": "StrongPass123!"})
    token = register.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/v1/playback/start", json={"track_id": "demo-track-1"}, headers=headers)
    assert resp.status_code == 200
