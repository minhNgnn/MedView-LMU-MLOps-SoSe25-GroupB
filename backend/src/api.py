from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

# Import ML logic from the ml package
from ml import models  # adjust as needed

app = FastAPI()

# Add CORS middleware for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL connection (adjust user/password/host as needed)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class PatientData(BaseModel):
    age: int
    gender: str
    bloodPressure: int
    bloodSugar: int
    cholesterol: int
    smoker: bool

# Placeholder for loaded model
# ml_model = models.predict_model.load_model("path/to/your/model.pkl")

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
        results = best_model.predict(source=normalized_image_uint8, imgsz=640, conf=0.5,
                                     project="reports", name="test_prediction", save=True, save_txt=True, save_conf=True, line_width=1)

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

@app.get("/patients")
def get_patients():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, first_name, last_name, age, gender, phone_number, email, address, blood_pressure, blood_sugar, cholesterol, smoking_status, alcohol_consumption, exercise_frequency, activity_level FROM patients LIMIT 10"))
        patients = [dict(row) for row in result]
    return JSONResponse(content=patients)

@app.get("/patients/{id}")
def get_patient(id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, first_name, last_name, age, gender, phone_number, email, address, blood_pressure, blood_sugar, cholesterol, smoking_status, alcohol_consumption, exercise_frequency, activity_level FROM patients WHERE id = :id"), {"id": id})
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return dict(row)

if __name__ == "__main__":
    get_prediction(best_model_path="ml/models/yolov8n/weights/epoch10_yolov8n.pt", test_image_path="data/BrainTumor/test_images/30_jpg.rf.ed67030833ab55428267e6f9c38cc730.jpg")
