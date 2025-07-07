import os
from typing import Any, Dict

import cv2
import numpy as np
import wandb
from ultralytics import YOLO
from wandb.integration.ultralytics import add_wandb_callback


def train_model(model_name: str = "simple", batch_size: int = -1, epochs: int = 10, wandb_logging: bool = False) -> Any:
    """Trains the machine learning model."""
    # pretrained_weights_path_dict = {"yolov8n": "models/yolov8n.pt", "yolov9n": "models/yolov9n.pt", "yolov11n": "models/yolov11n.pt",
    #                                 "simple": "models/simple.pt"}
    yaml_data_path_dict = {
        "yolov8n": "data/BrainTumor/BrainTumorYolov8/data.yaml",
        "yolov9n": "data/BrainTumor/BrainTumorYolov9/data.yaml",
        "yolov11n": "data/BrainTumor/BrainTumorYolov11/data.yaml",
        "simple": "configs/data/data.yaml",
    }

    print("Training model with pretrained weights:", f"models/{model_name}.pt")
    T_Model = YOLO(f"models/{model_name}.pt")

    if wandb_logging == True:
        print("Initializing Weights & Biases for logging...")
        wandb.login()
        os.system("yolo settings wandb=True")
        wandb.init(
            project="BrainTumorDetection",
            job_type="training",
            #    config={"model_name": model_name, "batch_size": batch_size, "epochs": epochs},
        )
        add_wandb_callback(T_Model)

    results = T_Model.train(
        data=yaml_data_path_dict[model_name],
        epochs=epochs,
        patience=20,
        batch=batch_size,
        optimizer="auto",
        project="models/",
        name=model_name,
    )
    return results


def normalize_image(image):
    return image / 255.0


def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)


def get_prediction_from_array(image: np.ndarray):
    best_model_path = "models/yolov8n/weights/epoch10_yolov8n.pt"
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
