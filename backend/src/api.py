import io
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Union

import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
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
from monitoring.core.monitor import BrainTumorImageMonitor

load_dotenv()


monitor_router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@asynccontextmanager
async def lifespan(app):
    app.state.monitor = BrainTumorImageMonitor(DATABASE_URL)
    logger.info("Monitoring system initialized successfully")
    yield
    # (Optional) Add any cleanup code here


app = FastAPI(lifespan=lifespan)

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


# --- Monitoring system setup ---

# --- Monitoring endpoints ---


def get_monitor(request: Request):
    monitor = getattr(request.app.state, "monitor", None)
    if monitor is None:
        raise HTTPException(status_code=500, detail="Monitor not initialized")
    return monitor


@monitor_router.get("/dashboard")
async def get_monitoring_dashboard(request: Request):
    try:
        dashboard_data = get_monitor(request).get_brain_tumor_dashboard_data()
        return JSONResponse(content=dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Error getting dashboard data")


@monitor_router.get("/drift-report")
async def generate_drift_report(request: Request, days: int = 7):
    try:
        report_path = get_monitor(request).generate_brain_tumor_drift_report(days)
        return JSONResponse(
            content={
                "message": "Brain tumor drift report generated successfully",
                "report_path": report_path,
                "days_analyzed": days,
            }
        )
    except Exception as e:
        logger.error(f"Error generating drift report: {e}")
        raise HTTPException(status_code=500, detail="Error generating drift report")


@monitor_router.get("/feature-analysis")
async def analyze_feature_drift(request: Request, days: int = 7):
    try:
        analysis = get_monitor(request).analyze_feature_drift(days)
        return JSONResponse(content=analysis)
    except Exception as e:
        logger.error(f"Error analyzing feature drift: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing feature drift")


@monitor_router.get("/data-quality")
async def run_data_quality_tests(request: Request):
    try:
        # Placeholder for data quality tests
        results = {
            "data_quality": True,
            "missing_values_test": True,
            "outliers_test": True,
            "drift_test": True,
            "timestamp": "2025-07-13T20:00:00",
        }
        return JSONResponse(content=results)
    except Exception as e:
        logger.error(f"Error running data quality tests: {e}")
        raise HTTPException(status_code=500, detail="Error running data quality tests")


@monitor_router.get("/report/{report_name}")
async def get_report(request: Request, report_name: str):
    try:
        report_path = get_monitor(request).reports_dir / report_name
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        with open(report_path, "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail="Error getting report")


@monitor_router.get("/reference-sample")
def get_reference_sample(request: Request, n: int = 5):
    try:
        df = get_monitor(request).get_reference_data()
        return df.head(n).to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@monitor_router.get("/current-sample")
def get_current_sample(request: Request, n: int = 5):
    try:
        monitor = get_monitor(request)
        df = monitor.get_current_data()
        return df.head(n).to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


# Register monitoring router
app.include_router(monitor_router)


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "Backend is running"}


# Validate file size after reading (10MB limit)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(
    request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)
) -> StreamingResponse:
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
        annotated_image, yolo_result = get_prediction_from_array(image)

        if annotated_image is None:
            logger.error("Model did not return an annotated image")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Prediction failed: no annotated image returned",
            )

        # Log prediction for monitoring as a background task
        try:
            # Extract actual model output
            if yolo_result is not None and hasattr(yolo_result, "boxes"):
                confidences = yolo_result.boxes.conf.cpu().numpy() if hasattr(yolo_result.boxes, "conf") else []
                classes = yolo_result.boxes.cls.cpu().numpy() if hasattr(yolo_result.boxes, "cls") else []
                confidence = float(confidences.max()) if len(confidences) > 0 else 0.0
                class_idx = int(classes[confidences.argmax()]) if len(classes) > 0 else -1
                num_detections = len(confidences)
            else:
                confidence = 0.0
                class_idx = -1
                num_detections = 0

            prediction_info = {
                "confidence": confidence,
                "class": str(class_idx),  # Replace with class name if you have a mapping
                "num_detections": num_detections,
                "model_version": "yolov8n",
            }
            monitor = getattr(request.app.state, "monitor", None)
            if monitor is not None:
                background_tasks.add_task(monitor.log_prediction, image, prediction_info)
            else:
                logger.warning("Monitor system is not initialized; skipping monitoring log.")
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


@app.get("/patients", status_code=status.HTTP_200_OK)
def get_patients() -> JSONResponse:
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM patients")
            result = conn.execute(query)
            patients = []
            # If result has .mappings() (as in tests), use it; else, iterate result
            rows = result.mappings() if hasattr(result, "mappings") else result
            for row in rows:
                patient = dict(row)
                # Convert datetime fields to ISO format
                for k, v in patient.items():
                    if hasattr(v, "isoformat"):
                        patient[k] = v.isoformat()
                patients.append(patient)
            return JSONResponse(content=patients)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Database error occurred"})
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/patients/{id}", status_code=status.HTTP_200_OK)
def get_patient(id: int) -> Dict:
    # Validate patient ID
    if id <= 0:
        raise HTTPException(status_code=400, detail="Patient ID must be a positive integer")

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
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
