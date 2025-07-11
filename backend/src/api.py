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
