from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_playlist_flow():
    register = client.post("/api/v1/auth/register", json={"email": "playlist@example.com", "username": "playlistuser", "password": "StrongPass123!"})
    token = register.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = client.post("/api/v1/playlists", json={"name": "My Favorites"}, headers=headers)
    assert create.status_code == 201, create.text
    playlist_id = create.json()["id"]

    add_track = client.post(f"/api/v1/playlists/{playlist_id}/tracks", json={"track_id": "demo-track-1"}, headers=headers)
    assert add_track.status_code == 404

    list_resp = client.get("/api/v1/playlists", headers=headers)
    assert list_resp.status_code == 200
