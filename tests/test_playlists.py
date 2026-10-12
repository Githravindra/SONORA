from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_catalog_list_tracks():
    resp = client.get("/api/v1/catalog/tracks")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert isinstance(data, list)


def test_catalog_list_genres():
    resp = client.get("/api/v1/catalog/genres")
    assert resp.status_code == 200, resp.text
