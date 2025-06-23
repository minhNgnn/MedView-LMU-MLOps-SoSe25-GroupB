from typing import Any, Dict, List


def engineer_features(data: Any) -> Any:
    """Performs feature engineering on the cleaned data."""
    print("Engineering features...")
    # Placeholder for actual feature engineering logic
    return f"Mock features from {data}"


def select_features(features: Any) -> Any:
    """Selects relevant features for model training."""
    print("Selecting features...")
    # Placeholder for actual feature selection logic
    features_ = features.drop("Outcome", axis=1)
    # return f"Mock selected features from {features}"
    return features_
