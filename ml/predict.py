import cv2
import numpy as np
from ultralytics import YOLO
from .utils import resize_image

BEST_MODEL_PATH = "ml/models/yolov8n/weights/epoch10_yolov8n.pt"

def get_prediction_from_array(image: np.ndarray) -> tuple:
    """
    Run YOLO prediction on an input image array and return the results and annotated image.

    Args:
        image (np.ndarray): Input image as a numpy array (BGR, uint8 or float, any size).

    Returns:
        tuple: (results, annotated_image)
            - results: YOLO prediction results object
            - annotated_image: np.ndarray or None, image with predictions drawn on it
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
        return results, annotated_image
    else:
        return None, None
