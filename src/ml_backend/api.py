import io
from typing import Any, Dict

import cv2
import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ultralytics import YOLO

# Assuming predict_model and load_model are available in the models module
# For now, we'll use a placeholder
# from src.ml_backend.models.predict_model import load_model, predict

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/predict")
async def predict_tumor(image_file: UploadFile = File(...)):
    image_bytes = await image_file.read()
    return StreamingResponse(io.BytesIO(image_bytes), media_type=image_file.content_type)


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
        results = best_model.predict(
            source=normalized_image_uint8,
            imgsz=640,
            conf=0.5,
            project="reports",
            name="test_prediction",
            save=True,
            save_txt=True,
            save_conf=True,
            line_width=1,
        )

        # Plot image with labels
        # annotated_image = results[0].plot(line_width=1)
        # annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        # plt.imshow(annotated_image_rgb)

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
    return results


if __name__ == "__main__":
    get_prediction(
        best_model_path="models/yolov8n/weights/epoch10_yolov8n.pt",
        test_image_path="data/BrainTumor/test_images/30_jpg.rf.ed67030833ab55428267e6f9c38cc730.jpg",
    )
