import io
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from backend.src.api import app

client = TestClient(app)


class TestPredictEndpoint:
    def test_predict_with_valid_image_returns_200(self):
        test_image = Image.new("RGB", (100, 100), color="red")
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        with patch("backend.src.predict_helpers.get_prediction_from_array") as mock_predict:
            # For success
            mock_predict.return_value = (np.full((100, 100, 3), 128, dtype=np.uint8), "dummy_result")
            response = client.post(
                "/predict",
                files={"file": ("test.jpg", img_byte_arr.getvalue(), "image/jpeg")},
            )
            assert response.status_code == 200
            assert response.headers["content-type"] == "image/jpeg"
            mock_predict.assert_called_once()

    def test_predict_with_invalid_file_type_returns_400(self):
        test_content = b"This is not an image"
        response = client.post("/predict", files={"file": ("test.txt", test_content, "text/plain")})
        assert response.status_code == 400
        data = response.json()
        assert "File must be an image" in data["detail"]

    def test_predict_with_empty_file_returns_400(self):
        response = client.post("/predict", files={"file": ("empty.jpg", b"", "image/jpeg")})
        assert response.status_code == 400
        data = response.json()
        assert "Empty file received" in data["detail"]

    def test_predict_with_large_file_returns_413(self):
        large_content = b"x" * (11 * 1024 * 1024)
        response = client.post("/predict", files={"file": ("large.jpg", large_content, "image/jpeg")})
        assert response.status_code == 413
        data = response.json()
        assert "File size exceeds maximum limit" in data["detail"]

    def test_predict_with_invalid_image_returns_400(self):
        invalid_content = b"This is not a valid image"
        response = client.post("/predict", files={"file": ("invalid.jpg", invalid_content, "image/jpeg")})
        assert response.status_code == 400
        data = response.json()
        assert "Invalid image file" in data["detail"]

    def test_predict_model_returns_none_returns_500(self):
        test_image = Image.new("RGB", (100, 100), color="red")
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        with patch("backend.src.predict_helpers.get_prediction_from_array") as mock_predict:
            # For failure
            mock_predict.return_value = (None, None)
            response = client.post(
                "/predict",
                files={"file": ("test.jpg", img_byte_arr.getvalue(), "image/jpeg")},
            )
            assert response.status_code == 500
            data = response.json()
            assert "Prediction failed" in data["detail"]
            mock_predict.assert_called_once()
