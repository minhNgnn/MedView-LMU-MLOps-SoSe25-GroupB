from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.src.api import app

client = TestClient(app)


class TestExceptionHandlers:
    def test_validation_error_handler(self):
        response = client.post("/predict", data={"invalid": "data"})
        assert response.status_code == 422

    def test_database_error_handler(self):
        with patch("backend.src.api.engine") as mock_engine:
            from sqlalchemy.exc import SQLAlchemyError

            mock_engine.connect.side_effect = SQLAlchemyError("Database error")
            response = client.get("/patients")
            assert response.status_code == 500
            data = response.json()
            assert "Database error occurred" in data["detail"]

    def test_global_exception_handler(self):
        with patch("backend.src.api.engine") as mock_engine:
            mock_engine.connect.side_effect = Exception("Unexpected error")
            response = client.get("/patients")
            assert response.status_code == 500
            data = response.json()
            assert "Internal server error" in data["detail"]
