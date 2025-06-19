from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Assuming predict_model and load_model are available in the models module
# For now, we'll use a placeholder
# from src.ml_backend.models.predict_model import load_model, predict

app = FastAPI()

class PatientData(BaseModel):
    age: int
    gender: str
    bloodPressure: int
    bloodSugar: int
    cholesterol: int
    smoker: bool

# Placeholder for loaded model
# ml_model = load_model("path/to/your/model.pkl")

def normalize_image(image):
    return image / 255.0

def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)

# @app.post("/predict")
# async def get_prediction(best_model_path: str, test_image_path: str) -> Dict:
def get_prediction(best_model_path: str, test_image_path: str) -> Dict:
    """Predicts health risks based on patient data."""
    print("Received prediction request for patient data:", test_image_path)
    image = cv2.imread(test_image_path)
    if image is not None:
        # Resize image
        resized_image = resize_image(image, size=(640, 640))
        # Normalize image
        normalized_image = normalize_image(resized_image)
        
        # Convert the normalized image to uint8 data type
        normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)
        
        # Predict with the model
        best_model = YOLO(best_model_path)
        results = best_model.predict(source=normalized_image_uint8, imgsz=640, conf=0.5)
        
        # Plot image with labels
        annotated_image = results[0].plot(line_width=1)
        annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        # plt.imshow(annotated_image_rgb)
        cv2.imwrite("reports/test_prediction.jpg", annotated_image_rgb)

    # Mock prediction result for API endpoint
    # mock_result = {
    #     "heartDiseaseRisk": 70,
    #     "diabetesRisk": 55,
    #     "confidence": 88,
    #     "recommendations": [
    #         "Consult a nutritionist for dietary advice",
    #         "Increase physical activity",
    #         "Schedule regular check-ups"
    #     ]
    # }
    return annotated_image_rgb

if __name__ == "__main__":
    get_prediction(best_model_path="models/yolov8n/weights/epoch10_yolov8n.pt", test_image_path="data/BrainTumor/BrainTumorYolov8/test/images/30_jpg.rf.ed67030833ab55428267e6f9c38cc730.jpg")