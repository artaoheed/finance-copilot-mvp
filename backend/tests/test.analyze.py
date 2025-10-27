# backend/tests/test_analyze.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_analyze_empty():
    response = client.post("/analyze")
    assert response.status_code == 200
    assert "error" in response.json()

