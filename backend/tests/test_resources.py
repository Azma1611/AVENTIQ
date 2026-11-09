from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_and_filter_resources():
    # 1. List all
    resp = client.get("/api/v1/resources")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] > 0

    # 2. Filter by skill
    resp_fastapi = client.get("/api/v1/resources?skill=FastAPI")
    assert resp_fastapi.status_code == 200
    fastapi_data = resp_fastapi.json()["data"]
    assert fastapi_data["total"] >= 1
    assert any("FastAPI" in item["skill_tags"] for item in fastapi_data["items"])

    # 3. Filter by search query
    resp_search = client.get("/api/v1/resources?search=Docker")
    assert resp_search.status_code == 200
    search_data = resp_search.json()["data"]
    assert search_data["total"] >= 1

