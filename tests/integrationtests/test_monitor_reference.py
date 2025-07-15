import pytest
from fastapi.testclient import TestClient

from backend.src.api import app


def test_reference_sample_endpoint():
    with TestClient(app) as client:
        response = client.get("/monitoring/reference-sample?n=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        if data:
            expected_cols = [
                "image_width",
                "image_height",
                "image_channels",
                "image_size_bytes",
                "brightness_mean",
                "brightness_std",
                "contrast_mean",
                "contrast_std",
                "entropy",
                "skewness",
                "kurtosis",
                "mean_intensity",
                "std_intensity",
                "tumor_area_ratio",
                "tumor_detection_confidence",
                "num_tumors_detected",
                "largest_tumor_area",
                "tumor_density",
                "tumor_location_x",
                "tumor_location_y",
                "tumor_shape_regularity",
            ]
            for col in expected_cols:
                assert col in data[0]


def test_current_sample_endpoint():
    with TestClient(app) as client:
        response = client.get("/monitoring/current-sample?n=5")
        assert response.status_code == 200
        data = response.json()
        # Accept either a list (if data) or an error dict (if DB is empty)
        assert isinstance(data, (list, dict))
        if isinstance(data, list) and data:
            expected_cols = [
                "image_width",
                "image_height",
                "image_channels",
                "image_size_bytes",
                "brightness_mean",
                "brightness_std",
                "contrast_mean",
                "contrast_std",
                "entropy",
                "skewness",
                "kurtosis",
                "mean_intensity",
                "std_intensity",
                "tumor_area_ratio",
                "tumor_detection_confidence",
                "num_tumors_detected",
                "largest_tumor_area",
                "tumor_density",
                "tumor_location_x",
                "tumor_location_y",
                "tumor_shape_regularity",
                "prediction_confidence",
                "prediction_class",
                "timestamp",
            ]
            for col in expected_cols:
                assert col in data[0]
