import io
import logging
import os
<<<<<<< Updated upstream
from contextlib import asynccontextmanager
from datetime import datetime

# Always load .env from the project root
from pathlib import Path
=======
>>>>>>> Stashed changes
from typing import Dict, List, Optional, Union

import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import (
<<<<<<< Updated upstream
    APIRouter,
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
from prometheus_client import Counter, Histogram, Summary, make_asgi_app
=======
>>>>>>> Stashed changes
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

<<<<<<< Updated upstream
from backend.src.predict_helpers import (
    create_image_response,
    decode_image,
    log_prediction_background,
    run_model_prediction,
    validate_image_file,
)
from ml.predict import get_prediction_from_array
from monitoring.core.monitor import SUPABASE_BUCKET, BrainTumorImageMonitor, supabase

project_root = Path(__file__).resolve().parents[3]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)
=======
from ml.predict import get_prediction_from_array

load_dotenv()
>>>>>>> Stashed changes


monitor_router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
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
<<<<<<< Updated upstream

engine = create_engine(DATABASE_URL)


# --- Monitoring system setup ---

# --- Monitoring endpoints ---


def get_monitor(request: Request) -> BrainTumorImageMonitor:
    monitor = getattr(request.app.state, "monitor", None)
    if monitor is None:
        raise HTTPException(status_code=500, detail="Monitor not initialized")
    return monitor


@monitor_router.get("/dashboard")
async def get_monitoring_dashboard(request: Request) -> JSONResponse:
    try:
        dashboard_data: Dict = get_monitor(request).get_brain_tumor_dashboard_data()
        return JSONResponse(content=dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Error getting dashboard data")


@monitor_router.get("/drift-report")
async def generate_drift_report(request: Request, days: int = 7) -> JSONResponse:
    try:
        report_filename: str = get_monitor(request).generate_brain_tumor_drift_report(days)
        # If the returned value is a full URL, extract just the filename
        if report_filename.startswith("http"):
            import os

            report_filename = os.path.basename(report_filename)
        return JSONResponse(
            content={
                "message": "Brain tumor drift report generated successfully",
                "report_path": report_filename,  # <-- just the filename
                "days_analyzed": days,
            }
        )
    except Exception as e:
        logger.error(f"Error generating drift report: {e}")
        raise HTTPException(status_code=500, detail="Error generating drift report")


@monitor_router.get("/report/{report_name}")
async def get_report(request: Request, report_name: str) -> HTMLResponse:
    try:
        if supabase:
            logger.info(f"Trying to download from Supabase bucket '{SUPABASE_BUCKET}' with object path '{report_name}'")
            response = supabase.storage.from_(SUPABASE_BUCKET).download(report_name)
            if response:
                # response is bytes
                content = response.decode("utf-8")
                return HTMLResponse(content=content)
            else:
                raise HTTPException(status_code=404, detail="Report not found in Supabase Storage")
        else:
            raise HTTPException(
                status_code=500,
                detail="Supabase client not configured",
            )
    except Exception as e:
        logger.error(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail="Error getting report")


# Register monitoring router
app.include_router(monitor_router)
=======

engine = create_engine(DATABASE_URL)
>>>>>>> Stashed changes


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "Backend is running"}


# Validate file size after reading (10MB limit)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


<<<<<<< Updated upstream
# Prometheus metrics
predict_counter = Counter("predict_requests_total", "Total number of prediction requests")
predict_latency = Histogram("predict_latency_seconds", "Prediction request latency in seconds")
predict_size_summary = Summary("predict_image_size_bytes", "Summary of uploaded image sizes in bytes")

# Mount /metrics endpoint
app.mount("/metrics", make_asgi_app())


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(
    request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)
) -> StreamingResponse:
    predict_counter.inc()
    with predict_latency.time():
        validate_image_file(file)
        try:
            contents: bytes = await file.read()
            predict_size_summary.observe(len(contents))
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB",
                )
            if len(contents) == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file received")
            image = decode_image(contents)
            annotated_image, yolo_result = run_model_prediction(image)
            log_prediction_background(request, background_tasks, image, yolo_result)
            return create_image_response(annotated_image)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Unexpected error in predict endpoint")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during prediction",
            )

=======
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

>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
def get_patient(id: int) -> Dict[str, Union[str, int, float, None]]:
=======
def get_patient(id: int) -> Dict:
    # Validate patient ID
>>>>>>> Stashed changes
    if id <= 0:
        raise HTTPException(status_code=400, detail="Patient ID must be a positive integer")

    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM patients WHERE id = :id")
            result = conn.execute(query, {"id": id})
            patient = result.fetchone()

            if patient is None:
                raise HTTPException(status_code=404, detail="Patient not found")

<<<<<<< Updated upstream
            patient_dict = dict(patient._mapping)
            # Convert all datetime fields to ISO strings
            for k, v in patient_dict.items():
                if isinstance(v, datetime):
                    patient_dict[k] = v.isoformat()
            return patient_dict
=======
            return dict(patient._mapping)
>>>>>>> Stashed changes
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
