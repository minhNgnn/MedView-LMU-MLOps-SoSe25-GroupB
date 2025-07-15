import io
import logging
from typing import Any, Dict, Optional

import cv2
import numpy as np
from fastapi import BackgroundTasks, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from ml.predict import get_prediction_from_array

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image_file(file: UploadFile) -> None:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")


def decode_image(contents: bytes) -> np.ndarray:
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        logger.error("cv2.imdecode failed: invalid image file")
        raise HTTPException(status_code=400, detail="Invalid image file")
    logger.info("Image shape: %s, dtype: %s", image.shape, image.dtype)
    return image


def run_model_prediction(image: np.ndarray) -> tuple[np.ndarray, Any]:
    annotated_image, yolo_result = get_prediction_from_array(image)
    if annotated_image is None:
        logger.error("Model did not return an annotated image")
        raise HTTPException(status_code=500, detail="Prediction failed: no annotated image returned")
    return annotated_image, yolo_result


def log_prediction_background(
    request: Request,
    background_tasks: BackgroundTasks,
    image: np.ndarray,
    yolo_result: Optional[Any],
) -> None:
    try:
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
        prediction_info: Dict[str, Any] = {
            "confidence": confidence,
            "class": str(class_idx),
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


def create_image_response(annotated_image: np.ndarray) -> StreamingResponse:
    result = cv2.imencode(".jpg", annotated_image)
    _, img_encoded = result
    logger.info("Returning annotated image, size: %d bytes", len(img_encoded))
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")
