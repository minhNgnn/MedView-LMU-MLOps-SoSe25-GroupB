import io
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from backend.src.api import app

client = TestClient(app)


class TestPredictionIntegration:
    def test_complete_prediction_flow(self):
        test_image = Image.new("RGB", (100, 100), color="blue")
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        with patch("backend.src.api.get_prediction_from_array") as mock_predict:
            annotated_image = np.full((100, 100, 3), 255, dtype=np.uint8)
            mock_predict.return_value = annotated_image
            response = client.post(
                "/predict",
                files={"file": ("test.jpg", img_byte_arr.getvalue(), "image/jpeg")},
            )
            assert response.status_code == 200
            assert response.headers["content-type"] == "image/jpeg"
            response_content = response.content
            assert len(response_content) > 0
            mock_predict.assert_called_once()
            call_args = mock_predict.call_args[0]
            assert isinstance(call_args[0], np.ndarray)
            assert call_args[0].shape == (100, 100, 3)
