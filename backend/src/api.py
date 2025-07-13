import io
import logging
import os
from typing import Dict, List, Optional, Union

import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import BackgroundTasks

from ml.predict import get_prediction_from_array
from backend.monitoring import init_monitor, get_monitor

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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=format_error("Internal server error")
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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=format_error("Database error occurred")
    )


# PostgreSQL connection (adjust user/password/host as needed)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)

# Initialize monitoring system
init_monitor(DATABASE_URL)


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
            monitor = get_monitor()
            prediction_info = {
                'confidence': 0.8,  # Placeholder - extract from your model output
                'class': 'medical_condition',  # Placeholder
                'num_detections': 1  # Placeholder
            }
            background_tasks.add_task(monitor.log_prediction, image, prediction_info)
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during prediction"
        )


# Monitoring endpoints
@app.get("/monitoring/dashboard")
async def get_monitoring_dashboard() -> JSONResponse:
    """Get brain tumor monitoring dashboard data."""
    try:
        monitor = get_monitor()
        dashboard_data = monitor.get_brain_tumor_dashboard_data()
        return JSONResponse(content=dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Error getting dashboard data")


@app.get("/monitoring/drift-report")
async def generate_drift_report(days: int = 7) -> JSONResponse:
    """Generate brain tumor image drift report."""
    try:
        monitor = get_monitor()
        report_path = monitor.generate_brain_tumor_drift_report(days)
        return JSONResponse(content={
            "message": "Brain tumor drift report generated successfully",
            "report_path": report_path,
            "days_analyzed": days
        })
    except Exception as e:
        logger.error(f"Error generating drift report: {e}")
        raise HTTPException(status_code=500, detail="Error generating drift report")


@app.get("/monitoring/data-quality")
async def run_data_quality_tests() -> JSONResponse:
    """Run brain tumor image quality tests."""
    try:
        monitor = get_monitor()
        results = monitor.run_brain_tumor_quality_tests()
        return JSONResponse(content=results)
    except Exception as e:
        logger.error(f"Error running data quality tests: {e}")
        raise HTTPException(status_code=500, detail="Error running data quality tests")


@app.get("/monitoring/report/{report_name}")
async def get_report(report_name: str) -> HTMLResponse:
    """Get a specific monitoring report."""
    try:
        monitor = get_monitor()
        report_path = monitor.reports_dir / report_name
        
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return HTMLResponse(content=html_content, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading report: {e}")
        raise HTTPException(status_code=500, detail="Error reading report")


@app.get("/patients", status_code=status.HTTP_200_OK)
def get_patients() -> JSONResponse:
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    """SELECT id, first_name, last_name, age, gender, phone_number,
                    email, address, blood_pressure, blood_sugar, cholesterol,
                    smoking_status, alcohol_consumption, exercise_frequency,
                    activity_level FROM patients LIMIT 10"""
                )
            )
            patients: List[Dict] = [dict(row) for row in result.mappings()]
        return JSONResponse(content=patients)

    except SQLAlchemyError as e:
        logger.error(f"Database error in get_patients: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unexpected error in get_patients")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/patients/{id}", status_code=status.HTTP_200_OK)
def get_patient(id: int) -> Dict:
    # Validate patient ID
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient ID must be a positive integer")

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    """SELECT id, first_name, last_name, age, gender, phone_number,
                    email, address, blood_pressure, blood_sugar, cholesterol,
                    smoking_status, alcohol_consumption, exercise_frequency,
                    activity_level FROM patients WHERE id = :id"""
                ),
                {"id": id},
            )
            row = result.fetchone()
            if row is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
            return dict(row._mapping)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_patient: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    except Exception as e:
        logger.exception("Unexpected error in get_patient")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
