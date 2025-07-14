import io
import logging
from typing import Dict

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ml.models import get_prediction_from_array
from ultralytics import YOLO
import matplotlib.pyplot as plt
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Add this block after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:8080"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Global exception handler for unhandled exceptions
def format_error(detail: str):
    return {"detail": detail}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content=format_error("Internal server error"))

# PostgreSQL connection (adjust user/password/host as needed)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class PatientData(BaseModel):
    age: int
    gender: str
    blood_pressure: int
    blood_sugar: int
    cholesterol: int
    smoker: bool


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    logger.info("Received file: %s", file.filename)
    contents = await file.read()
    logger.info("File size: %d bytes", len(contents))
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        logger.error("cv2.imdecode failed: invalid image file")
        raise HTTPException(status_code=400, detail="Invalid image file")
    logger.info("Image shape: %s, dtype: %s", image.shape, image.dtype)
    results, annotated_image = get_prediction_from_array(image)
    # results, annotated_image = get_prediction_from_onnx_array(image)
    if annotated_image is None:
        logger.error("Model did not return an annotated image")
        raise HTTPException(status_code=500, detail="Prediction failed: no annotated image returned")
    _, img_encoded = cv2.imencode(".jpg", annotated_image)
    logger.info("Returning annotated image, size: %d bytes", len(img_encoded))
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")


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

