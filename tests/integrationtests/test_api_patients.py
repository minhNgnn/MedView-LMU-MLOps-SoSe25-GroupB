from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from backend.src.api import app

client = TestClient(app)


class TestPatientsEndpoints:
    @patch("backend.src.api.engine")
    def test_get_patients_returns_200(self, mock_engine):
        mock_conn = Mock()
        mock_result = Mock()
        mock_result.mappings.return_value = [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "gender": "M",
                "phone_number": "123-456-7890",
                "email": "john@example.com",
                "address": "123 Main St",
                "blood_pressure": "120/80",
                "blood_sugar": "100",
                "cholesterol": "200",
                "smoking_status": "Never",
                "alcohol_consumption": "Occasional",
                "exercise_frequency": "3x/week",
                "activity_level": "Moderate",
            }
        ]
        mock_conn.execute.return_value = mock_result
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        response = client.get("/patients")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["first_name"] == "John"

    @patch("backend.src.api.engine")
    def test_get_patients_database_error_returns_500(self, mock_engine):
        mock_engine.connect.side_effect = Exception("Database connection failed")
        response = client.get("/patients")
        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]

    def test_get_patient_with_valid_id_returns_200(self):
        with patch("backend.src.api.engine") as mock_engine:
            mock_conn = Mock()
            mock_result = Mock()
            mock_row = Mock()
            mock_row._mapping = {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "gender": "M",
                "phone_number": "123-456-7890",
                "email": "john@example.com",
                "address": "123 Main St",
                "blood_pressure": "120/80",
                "blood_sugar": "100",
                "cholesterol": "200",
                "smoking_status": "Never",
                "alcohol_consumption": "Occasional",
                "exercise_frequency": "3x/week",
                "activity_level": "Moderate",
            }
            mock_result.fetchone.return_value = mock_row
            mock_conn.execute.return_value = mock_result
            mock_engine.connect.return_value.__enter__.return_value = mock_conn
            response = client.get("/patients/1")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["first_name"] == "John"

    def test_get_patient_with_invalid_id_returns_400(self):
        response = client.get("/patients/0")
        assert response.status_code == 400
        data = response.json()
        assert "Patient ID must be a positive integer" in data["detail"]
        response = client.get("/patients/-1")
        assert response.status_code == 400
        data = response.json()
        assert "Patient ID must be a positive integer" in data["detail"]

    def test_get_patient_not_found_returns_404(self):
        with patch("backend.src.api.engine") as mock_engine:
            mock_conn = Mock()
            mock_result = Mock()
            mock_result.fetchone.return_value = None
            mock_conn.execute.return_value = mock_result
            mock_engine.connect.return_value.__enter__.return_value = mock_conn
            response = client.get("/patients/999")
            assert response.status_code == 404
            data = response.json()
            assert "Patient not found" in data["detail"]

    @patch("backend.src.api.engine")
    def test_get_patient_database_error_returns_500(self, mock_engine):
        mock_engine.connect.side_effect = Exception("Database connection failed")
        response = client.get("/patients/1")
        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]
