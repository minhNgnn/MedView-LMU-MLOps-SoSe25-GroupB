import io
import logging
import os
from typing import Dict, List, Optional, Union

import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from ml.predict import get_prediction_from_array

load_dotenv()


app = FastAPI()

# Add this block after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Global exception handler for unhandled exceptions
def format_error(detail: str) -> Dict[str, str]:
    return {"detail": detail}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error("Internal server error"),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error("Database error occurred"),
    )


# PostgreSQL connection (adjust user/password/host as needed)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "Backend is running"}


# Validate file size after reading (10MB limit)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> StreamingResponse:
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image")

    try:
        logger.info("Received file: %s", file.filename)
        contents: bytes = await file.read()
        logger.info("File size: %d bytes", len(contents))

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        if len(contents) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file received")

        nparr: np.ndarray = np.frombuffer(contents, np.uint8)
        image: Optional[np.ndarray] = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            logger.error("cv2.imdecode failed: invalid image file")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")

        logger.info("Image shape: %s, dtype: %s", image.shape, image.dtype)
        annotated_image: Optional[np.ndarray] = get_prediction_from_array(image)

        if annotated_image is None:
            logger.error("Model did not return an annotated image")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Prediction failed: no annotated image returned",
            )

        # Log prediction for monitoring as a background task
        try:
            prediction_info = {
                "confidence": 0.8,  # Placeholder - extract from your model output
                "class": "medical_condition",  # Placeholder
                "num_detections": 1,  # Placeholder
            }
            # background_tasks.add_task(monitor.log_prediction, image, prediction_info) # Removed as per edit hint
        except Exception as e:
            logger.warning(f"Failed to schedule logging for monitoring: {e}")

        result = cv2.imencode(".jpg", annotated_image)
        _, img_encoded = result
        logger.info("Returning annotated image, size: %d bytes", len(img_encoded))
        return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.exception("Unexpected error in predict endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during prediction",
        )


# Remove all @app.get("/monitoring/...") endpoints


@app.get("/patients", status_code=status.HTTP_200_OK)
def get_patients() -> JSONResponse:
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM patients")
            result = conn.execute(query)
            patients = []
            for row in result:
                patient = dict(row._mapping)
                # Convert datetime fields to ISO format
                for k, v in patient.items():
                    if hasattr(v, "isoformat"):
                        patient[k] = v.isoformat()
                patients.append(patient)
            return JSONResponse(content=patients)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/patients/{id}", status_code=status.HTTP_200_OK)
def get_patient(id: int) -> Dict:
    # Validate patient ID
    if id <= 0:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM patients WHERE id = :id")
            result = conn.execute(query, {"id": id})
            patient = result.fetchone()

            if patient is None:
                raise HTTPException(status_code=404, detail="Patient not found")

            return dict(patient._mapping)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
