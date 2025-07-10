from typing import List, Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split

def load_raw_data(file_path: str) -> Any:
    """Loads raw data from a specified file path."""
    print(f"Loading raw data from: {file_path}")
    # Placeholder for actual data loading logic
    data = pd.read_csv(file_path)
    # return f"Mock raw data from {file_path}"
    return data

def clean_data(data: Any) -> Any:
    """Cleans the raw data."""
    print("Cleaning data...")
    # Placeholder for actual data cleaning logic
    return f"Mock cleaned data from {data}"

def save_processed_data(data: Any, file_path: str):
    """Saves processed data to a specified file path."""
    print(f"Saving processed data to: {file_path}")
    # Placeholder for actual data saving logic
    pass

def split_data(X, y, test_size: float = 0.3, random_state: int = 42) -> Dict[str, Any]:
    X_train , X_test , y_train , y_test = train_test_split(X, y, test_size=test_size , random_state=random_state)
    return X_train , X_test , y_train , y_test
