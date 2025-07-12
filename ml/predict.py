import numpy as np
from ultralytics import YOLO
from ml.utils import resize_image

BEST_MODEL_PATH = "ml/models/yolov8n/weights/epoch10_yolov8n.pt"

def get_prediction_from_array(image: np.ndarray) -> 'np.ndarray | None':
    """
    Run YOLO prediction on an input image array and return the annotated image.

    Args:
        image (np.ndarray): Input image as a numpy array (BGR, uint8 or float, any size).

    Returns:
        np.ndarray or None: Image with predictions drawn on it, or None if input is invalid.
    """
    if image is not None:
        # Ensure image is uint8 BGR and correct size
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        if image.shape[:2] != (640, 640):
            image = resize_image(image, size=(640, 640))
        best_model = YOLO(BEST_MODEL_PATH)
        results = best_model.predict(source=image, imgsz=640, conf=0.5)
        # Get annotated image from results (BGR numpy array)
        annotated_image = results[0].plot()
        return annotated_image
    else:
        return None
    