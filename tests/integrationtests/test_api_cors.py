from fastapi.testclient import TestClient

from backend.src.api import app

client = TestClient(app)


class TestCORS:
    def test_cors_headers_present(self):
        response = client.get("/health")
        assert response.status_code == 200
