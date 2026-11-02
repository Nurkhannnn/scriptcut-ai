from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "ScriptCut AI"}

def test_list_projects():
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert len(response.json()) > 0
