import numpy as np
from ultralytics import YOLO

from ml.utils import resize_image

BEST_MODEL_PATH = "ml/models/yolov8n/weights/epoch10_yolov8n.pt"


def get_prediction_from_array(image: np.ndarray):
    """
    Run YOLO prediction on an input image array and return the annotated image and the YOLO result object.
    """
    if image is not None:
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        if image.shape[:2] != (640, 640):
            image = resize_image(image, size=(640, 640))
        best_model = YOLO(BEST_MODEL_PATH)
        results = best_model.predict(source=image, imgsz=640, conf=0.5)
        annotated_image = results[0].plot()
        return annotated_image, results[0]
    else:
        return None, None
