import pytest
from fastapi.testclient import TestClient

from backend.src.api import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Backend is running"
