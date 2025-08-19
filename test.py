# tests/test_app.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_account():
    response = client.post("/account/", json={"name": "Alice", "balance": 100})
    assert response.status_code == 200
    assert "account_id" in response.json()
