from fastapi.testclient import TestClient

from app.main import app


def test_register_returns_tokens():
    client = TestClient(app)
    response = client.post("/api/auth/register", json={"email": "test@example.com", "full_name": "Test User", "password": "password123"})
    assert response.status_code in {201, 409}
    if response.status_code == 201:
        assert "access_token" in response.json()
