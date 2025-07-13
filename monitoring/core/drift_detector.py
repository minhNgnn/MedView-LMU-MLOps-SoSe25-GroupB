"""
Drift detection for brain tumor image monitoring.
"""

import logging
from datetime import datetime
from typing import Dict, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DriftDetector:
    """Detect data drift in brain tumor image features."""

    def __init__(self, drift_threshold: float = 1.0):
        self.drift_threshold = drift_threshold
        self.key_features = ["brightness_mean", "contrast_mean", "entropy", "tumor_detection_confidence"]

    def analyze_feature_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame) -> Dict:
        """Analyze feature distributions and drift indicators."""
        try:
            if reference_data.empty or current_data.empty:
                return {"error": "Insufficient data for analysis"}

            analysis = {}

            for feature in self.key_features:
                if feature in reference_data.columns and feature in current_data.columns:
                    ref_mean = float(reference_data[feature].mean())
                    ref_std = float(reference_data[feature].std())
                    curr_mean = float(current_data[feature].mean())
                    curr_std = float(current_data[feature].std())

                    # Calculate drift indicators
                    mean_diff = abs(curr_mean - ref_mean)
                    std_diff = abs(curr_std - ref_std)
                    drift_score = (mean_diff / ref_std) + (std_diff / ref_std)

                    analysis[feature] = {
                        "reference_mean": ref_mean,
                        "reference_std": ref_std,
                        "current_mean": curr_mean,
                        "current_std": curr_std,
                        "mean_difference": mean_diff,
                        "std_difference": std_diff,
                        "drift_score": drift_score,
                        "significant_drift": bool(drift_score > self.drift_threshold),
                    }

                    logger.info(
                        f"Feature {feature}: ref_mean={ref_mean:.2f}, "
                        f"curr_mean={curr_mean:.2f}, drift_score={drift_score:.2f}"
                    )

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing feature drift: {e}")
            return {"error": str(e)}

    def check_overlap(self, reference_data: pd.DataFrame, current_data: pd.DataFrame) -> Dict:
        """Check for overlap between reference and current datasets."""
        try:
            ref_timestamps = set(reference_data["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"))
            curr_timestamps = set(current_data["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"))
            overlap = ref_timestamps.intersection(curr_timestamps)

            return {
                "reference_count": len(reference_data),
                "current_count": len(current_data),
                "overlap_count": len(overlap),
                "clean_split": len(overlap) == 0,
            }
        except Exception as e:
            logger.error(f"Error checking overlap: {e}")
            return {"error": str(e)}

    def get_drift_summary(self, analysis: Dict) -> Dict:
        """Generate a summary of drift detection results."""
        if "error" in analysis:
            return analysis

        drifted_features = []
        total_features = len(analysis)

        for feature, data in analysis.items():
            if data.get("significant_drift", False):
                drifted_features.append(
                    {"feature": feature, "drift_score": data["drift_score"], "mean_difference": data["mean_difference"]}
                )

        return {
            "total_features": total_features,
            "drifted_features_count": len(drifted_features),
            "drift_percentage": (len(drifted_features) / total_features) * 100 if total_features > 0 else 0,
            "drifted_features": drifted_features,
            "timestamp": datetime.now().isoformat(),
        }
