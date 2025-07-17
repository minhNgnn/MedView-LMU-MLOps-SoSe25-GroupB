"""
Image feature extraction for brain tumor monitoring.
"""

import logging
from typing import Dict

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ImageFeatureExtractor:
    """Extract comprehensive features from brain tumor images."""

    def __init__(self):
        # Image feature columns for brain tumor analysis
        self.image_columns = [
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
        ]

        # Brain tumor specific features
        self.tumor_features = [
            "num_tumors_detected",
            "largest_tumor_area",
            "tumor_density",
            "tumor_location_x",
            "tumor_location_y",
            "tumor_shape_regularity",
        ]

    def extract_features(self, image: np.ndarray) -> Dict[str, float]:
        """Extract comprehensive features from brain tumor images."""
        if image is None:
            return {}

        # Basic image properties
        height, width = image.shape[:2]
        channels = image.shape[2] if len(image.shape) > 2 else 1

        # Convert to grayscale for analysis
        if channels == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Basic statistics
        brightness_mean = np.mean(gray)
        brightness_std = np.std(gray)

        # Contrast analysis
        contrast_mean = np.mean(np.abs(np.diff(gray, axis=1)))
        contrast_std = np.std(np.abs(np.diff(gray, axis=1)))

        # Image entropy (measure of texture complexity)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist / hist.sum()  # Normalize
        entropy = -np.sum(hist * np.log2(hist + 1e-10))

        # Statistical moments
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)

        # Skewness and kurtosis (shape of intensity distribution)
        skewness = np.mean(((gray - mean_intensity) / std_intensity) ** 3)
        kurtosis = np.mean(((gray - mean_intensity) / std_intensity) ** 4) - 3

        # Tumor-specific features
        tumor_features = self._extract_tumor_specific_features(gray)

        return {
            "image_width": float(width),
            "image_height": float(height),
            "image_channels": float(channels),
            "image_size_bytes": float(image.nbytes),
            "brightness_mean": float(brightness_mean),
            "brightness_std": float(brightness_std),
            "contrast_mean": float(contrast_mean),
            "contrast_std": float(contrast_std),
            "entropy": float(entropy),
            "skewness": float(skewness),
            "kurtosis": float(kurtosis),
            "mean_intensity": float(mean_intensity),
            "std_intensity": float(std_intensity),
            **tumor_features,
        }

    def _extract_tumor_specific_features(self, gray_image: np.ndarray) -> Dict[str, float]:
        """Extract tumor-specific features from the image."""
        # Ensure the image is 2D
        gray_image = np.squeeze(gray_image)
        height, width = gray_image.shape

        # Simulate tumor detection (replace with actual YOLO predictions)
        num_tumors = np.random.randint(0, 3)  # 0-2 tumors
        largest_tumor_area = np.random.uniform(0, 0.1)  # 0-10% of image
        tumor_density = np.random.uniform(0, 1.0)
        tumor_location_x = np.random.uniform(0, width)
        tumor_location_y = np.random.uniform(0, height)
        tumor_shape_regularity = np.random.uniform(0, 1.0)

        return {
            "num_tumors_detected": float(num_tumors),
            "largest_tumor_area": float(largest_tumor_area),
            "tumor_density": float(tumor_density),
            "tumor_location_x": float(tumor_location_x),
            "tumor_location_y": float(tumor_location_y),
            "tumor_shape_regularity": float(tumor_shape_regularity),
            "tumor_area_ratio": float(largest_tumor_area),
            "tumor_detection_confidence": float(np.random.uniform(0.5, 0.95)),
        }
