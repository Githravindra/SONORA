from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_and_empty():
    r = client.get("/api/v1/search", params={"q": "midnight"})
    assert r.status_code == 200
    assert "tracks" in r.json()

    empty = client.get("/api/v1/search", params={"q": "zzzzzzzzzz"})
    assert empty.status_code == 200
