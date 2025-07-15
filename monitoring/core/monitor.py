"""
Main monitoring orchestrator for brain tumor image drift detection.
"""

import logging
import os
import random
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset
from fastapi import HTTPException
from google.cloud import storage
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from supabase import Client, create_client

from .drift_detector import DriftDetector
from .feature_extractor import ImageFeatureExtractor

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "reports"

load_dotenv()

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    pass

logger = logging.getLogger(__name__)


class BrainTumorImageMonitor:
    """Data drift monitoring system specifically for brain tumor image classification."""

    def __init__(self, database_url: str, reports_dir: str = "monitoring/reports"):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.feature_extractor = ImageFeatureExtractor()
        self.drift_detector = DriftDetector()

        # Feature columns
        self.image_columns = self.feature_extractor.image_columns
        self.tumor_features = self.feature_extractor.tumor_features

        # Reference data from train images
        self.reference_data = self._load_reference_data_from_gcs()

    def _load_reference_data_from_gcs(self, n_images: int = 50) -> pd.DataFrame:
        """Download n_images from GCS train/images/ and extract features for reference data."""
        bucket_name = "brain-tumor-data"
        prefix = "BrainTumorYolov8/train/images/"
        label_prefix = "BrainTumorYolov8/train/labels/"
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = list(storage_client.list_blobs(bucket_name, prefix=prefix))
        image_blobs = [b for b in blobs if b.name.lower().endswith((".jpg", ".jpeg", ".png"))]
        if len(image_blobs) == 0:
            raise RuntimeError("No images found in GCS train/images/ for reference data.")
        selected_blobs = random.sample(image_blobs, min(n_images, len(image_blobs)))
        features = []
        for blob in selected_blobs:
            with tempfile.NamedTemporaryFile(suffix=Path(blob.name).suffix) as tmp:
                blob.download_to_filename(tmp.name)
                img = cv2.imread(tmp.name)
                label_file = blob.name.replace("images/", "labels/").rsplit(".", 1)[0] + ".txt"
                label_blob = storage_client.bucket(bucket_name).blob(label_file)
                prediction_class = "unknown"
                if label_blob.exists():
                    label_blob.download_to_filename(tmp.name + ".txt")
                    with open(tmp.name + ".txt", "r") as f:
                        label_content = f.read().strip()
                        if label_content:
                            # Use the first class index in the label file
                            prediction_class = label_content.split()[0]
                if img is not None:
                    feat = self.feature_extractor.extract_features(img)
                    feat["prediction_confidence"] = 0.0
                    feat["prediction_class"] = prediction_class
                    feat["num_detections"] = 0
                    feat["model_version"] = "reference"
                    feat["processing_time_ms"] = 0
                    features.append(feat)
        if not features:
            raise RuntimeError("No features extracted from GCS images.")
        df = pd.DataFrame(features)
        if "timestamp" not in df.columns:
            df["timestamp"] = pd.to_datetime("2020-01-01")
        # Ensure all required columns are present
        required_columns = [
            "prediction_confidence",
            "prediction_class",
            "num_detections",
            "model_version",
            "processing_time_ms",
        ]
        for col in required_columns:
            if col not in df.columns:
                df[col] = (
                    0.0 if "confidence" in col or "num_detections" in col or "processing_time" in col else "unknown"
                )
        return df

    def extract_brain_tumor_features(self, image: np.ndarray) -> Dict[str, float]:
        """Extract comprehensive features from brain tumor images."""
        return self.feature_extractor.extract_features(image)

    def get_reference_data(self) -> pd.DataFrame:
        """Get reference brain tumor image data from GCS train images."""
        return self.reference_data

    def _log_data_split_and_overlap(self, reference_data, current_data):
        logger.info(
            f"Reference data: {len(reference_data)} samples, "
            f"timestamp range: {reference_data['timestamp'].min()} to "
            f"{reference_data['timestamp'].max()}"
        )
        logger.info(
            f"Current data: {len(current_data)} samples, "
            f"timestamp range: {current_data['timestamp'].min()} to "
            f"{current_data['timestamp'].max()}"
        )
        overlap_info = self.drift_detector.check_overlap(reference_data, current_data)
        logger.info(f"Timestamp overlap between reference and current: {overlap_info.get('overlap_count', 0)} records")

    def get_current_data(self, days: int = 7) -> pd.DataFrame:
        """Get current brain tumor image data from the database."""
        try:
            with self.engine.connect() as conn:
                query = text(
                    """
                    SELECT image_width, image_height, image_channels, image_size_bytes,
                           brightness_mean, brightness_std, contrast_mean, contrast_std,
                           entropy, skewness, kurtosis, mean_intensity, std_intensity,
                           tumor_area_ratio, tumor_detection_confidence,
                           num_tumors_detected, largest_tumor_area, tumor_density,
                           tumor_location_x, tumor_location_y, tumor_shape_regularity,
                           prediction_confidence, prediction_class, timestamp
                    FROM predictions_log
                    ORDER BY timestamp DESC
                    LIMIT 50
                """
                )
                result = conn.execute(query)
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                if df.empty:
                    return self._create_synthetic_current_data(days)
                return df
        except SQLAlchemyError as e:
            logger.error(f"Database error getting current data: {e}")
            return self._create_synthetic_current_data(days)

    def _create_synthetic_current_data(self, days: int) -> pd.DataFrame:
        """Create synthetic current data with slight drift."""
        n_samples = 100
        data = {
            "image_width": np.random.normal(512, 60, n_samples),
            "image_height": np.random.normal(512, 60, n_samples),
            "image_channels": np.full(n_samples, 1),
            "image_size_bytes": np.random.normal(262144, 60000, n_samples),
            "brightness_mean": np.random.normal(125, 25, n_samples),  # Slightly brighter
            "brightness_std": np.random.normal(45, 12, n_samples),
            "contrast_mean": np.random.normal(18, 6, n_samples),  # Slightly more contrast
            "contrast_std": np.random.normal(9, 3, n_samples),
            "entropy": np.random.normal(7.8, 0.6, n_samples),  # Slightly higher entropy
            "skewness": np.random.normal(0.1, 0.6, n_samples),  # Slight positive skew
            "kurtosis": np.random.normal(3.2, 1.2, n_samples),
            "mean_intensity": np.random.normal(125, 25, n_samples),
            "std_intensity": np.random.normal(45, 12, n_samples),
            "tumor_area_ratio": np.random.uniform(0, 0.18, n_samples),  # Slightly larger tumors
            "tumor_detection_confidence": np.random.uniform(0.65, 0.95, n_samples),
            "num_tumors_detected": np.random.poisson(1.2, n_samples),  # Slightly more tumors
            "largest_tumor_area": np.random.uniform(0, 0.12, n_samples),
            "tumor_density": np.random.uniform(0.15, 0.85, n_samples),
            "tumor_location_x": np.random.uniform(100, 412, n_samples),
            "tumor_location_y": np.random.uniform(100, 412, n_samples),
            "tumor_shape_regularity": np.random.uniform(0.25, 0.85, n_samples),
            "prediction_confidence": np.random.uniform(0.65, 0.95, n_samples),
            "prediction_class": np.random.choice(["benign", "malignant", "normal"], n_samples, p=[0.4, 0.3, 0.3]),
        }
        return pd.DataFrame(data)

    def log_prediction(self, image: np.ndarray, prediction: Dict):
        """Log brain tumor prediction data for monitoring."""
        try:
            # Extract comprehensive image features
            image_features = self.extract_brain_tumor_features(image)

            # Prepare prediction log data (no patient_id)
            log_data = {
                "timestamp": datetime.now(),
                "prediction_confidence": prediction.get("confidence", 0.0),
                "prediction_class": prediction.get("class", "unknown"),
                "num_detections": prediction.get("num_detections", 0),
                "model_version": prediction.get("model_version", "yolov8n"),
                "processing_time_ms": prediction.get("processing_time_ms", 0),
                **image_features,
            }

            # Store in database
            with self.engine.connect() as conn:
                # Insert into predictions_log table (no patient_id)
                insert_query = text(
                    """
                    INSERT INTO predictions_log (
                        timestamp, prediction_confidence, prediction_class,
                        num_detections, model_version, processing_time_ms,
                        image_width, image_height, image_channels, image_size_bytes,
                        brightness_mean, brightness_std, contrast_mean, contrast_std,
                        entropy, skewness, kurtosis, mean_intensity, std_intensity,
                        tumor_area_ratio, tumor_detection_confidence,
                        num_tumors_detected, largest_tumor_area, tumor_density,
                        tumor_location_x, tumor_location_y, tumor_shape_regularity
                    ) VALUES (
                        :timestamp, :prediction_confidence, :prediction_class,
                        :num_detections, :model_version, :processing_time_ms,
                        :image_width, :image_height, :image_channels, :image_size_bytes,
                        :brightness_mean, :brightness_std, :contrast_mean, :contrast_std,
                        :entropy, :skewness, :kurtosis, :mean_intensity, :std_intensity,
                        :tumor_area_ratio, :tumor_detection_confidence,
                        :num_tumors_detected, :largest_tumor_area, :tumor_density,
                        :tumor_location_x, :tumor_location_y, :tumor_shape_regularity
                    )
                """
                )
                conn.execute(insert_query, log_data)
                conn.commit()
                logger.info(f"Logged brain tumor prediction: {log_data}")

        except Exception as e:
            logger.error(f"Error logging brain tumor prediction: {e}")

    def generate_brain_tumor_drift_report(self, days: int = 7) -> str:
        """Generate comprehensive brain tumor image drift report and upload to Supabase Storage."""
        try:
            reference_data = self.get_reference_data()
            current_data = self.get_current_data(days)
            if reference_data.empty or current_data.empty:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient data for brain tumor drift analysis",
                )
            self._log_data_split_and_overlap(reference_data, current_data)
            drift_report = Report(
                metrics=[
                    DataDriftPreset(
                        columns=self.image_columns + self.tumor_features,
                        drift_share=0.1,
                    ),
                    DataSummaryPreset(columns=self.image_columns + self.tumor_features),
                ]
            )
            snapshot = drift_report.run(current_data=current_data, reference_data=reference_data)
            import datetime
            import io

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"brain_tumor_drift_report_{timestamp}.html"
            # Save directly to file and upload to Supabase
            import tempfile

            with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=True, encoding="utf-8") as tmp:
                snapshot.save_html(tmp.name)
                tmp.seek(0)
                html_bytes = tmp.read().encode("utf-8")
                if supabase:
                    supabase.storage.from_(SUPABASE_BUCKET).upload(
                        report_filename, html_bytes, {"content-type": "text/html"}
                    )
                    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(report_filename)
                    return public_url
                else:
                    raise HTTPException(status_code=500, detail="Supabase client not configured")
        except Exception as e:
            logger.error(f"Error generating brain tumor drift report: {e}")
            raise HTTPException(status_code=500, detail="Error generating brain tumor drift report")

    def analyze_feature_drift(self, days: int = 7) -> Dict:
        """Analyze feature distributions and drift indicators."""
        try:
            reference_data = self.get_reference_data()
            current_data = self.get_current_data(days)

            if reference_data.empty or current_data.empty:
                return {"error": "Insufficient data for analysis"}

            # Log the split details for debugging
            logger.info(
                f"Reference data: {len(reference_data)} samples, "
                f"timestamp range: {reference_data['timestamp'].min()} to "
                f"{reference_data['timestamp'].max()}"
            )
            logger.info(
                f"Current data: {len(current_data)} samples, "
                f"timestamp range: {current_data['timestamp'].min()} to "
                f"{current_data['timestamp'].max()}"
            )

            # Check for overlap
            overlap_info = self.drift_detector.check_overlap(reference_data, current_data)
            logger.info(
                f"Timestamp overlap between reference and current: {overlap_info.get('overlap_count', 0)} records"
            )

            # Analyze drift
            analysis = self.drift_detector.analyze_feature_drift(reference_data, current_data)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing feature drift: {e}")
            return {"error": str(e)}

    def get_brain_tumor_dashboard_data(self) -> Dict:
        """Get data for brain tumor monitoring dashboard."""
        try:
            # Get recent brain tumor predictions
            with self.engine.connect() as conn:
                # Query recent predictions
                query = text(
                    """
                    SELECT
                        COUNT(*) as total_predictions_today,
                        AVG(prediction_confidence) as average_confidence,
                        MODE() WITHIN GROUP (ORDER BY prediction_class) as most_common_class,
                        AVG(tumor_detection_confidence) as avg_tumor_confidence,
                        COUNT(CASE WHEN prediction_class = 'malignant' THEN 1 END) as malignant_count,
                        COUNT(CASE WHEN prediction_class = 'benign' THEN 1 END) as benign_count,
                        COUNT(CASE WHEN prediction_class = 'normal' THEN 1 END) as normal_count
                    FROM predictions_log
                    WHERE DATE(timestamp) = CURRENT_DATE
                """
                )
                result = conn.execute(query)
                row = result.fetchone()

                if row:
                    dashboard_data = {
                        "total_predictions_today": row[0] or 0,
                        "average_confidence": float(row[1] or 0),
                        "most_common_class": row[2] or "unknown",
                        "avg_tumor_confidence": float(row[3] or 0),
                        "malignant_count": row[4] or 0,
                        "benign_count": row[5] or 0,
                        "normal_count": row[6] or 0,
                        "last_drift_check": datetime.now().isoformat(),
                        "alerts": [],
                    }
                else:
                    dashboard_data = {
                        "total_predictions_today": 0,
                        "average_confidence": 0.0,
                        "most_common_class": "unknown",
                        "avg_tumor_confidence": 0.0,
                        "malignant_count": 0,
                        "benign_count": 0,
                        "normal_count": 0,
                        "last_drift_check": datetime.now().isoformat(),
                        "alerts": [],
                    }

                return dashboard_data

        except Exception as e:
            logger.error(f"Error getting brain tumor dashboard data: {e}")
            return {"error": str(e)}
