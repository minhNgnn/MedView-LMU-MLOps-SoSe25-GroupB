import cv2
import numpy as np
from ultralytics import YOLO


def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)


def get_prediction_from_array(image: np.ndarray):
    best_model_path = "ml/models/yolov8n/weights/epoch10_yolov8n.pt"
    if image is not None:
        # Ensure image is uint8 BGR and correct size
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        if image.shape[:2] != (640, 640):
            image = resize_image(image, size=(640, 640))
        best_model = YOLO(best_model_path)
        results = best_model.predict(source=image, imgsz=640, conf=0.5)
        # Get annotated image from results (BGR numpy array)
        annotated_image = results[0].plot()
        return results, annotated_image
    else:
        return None, None
