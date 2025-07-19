import os
from typing import Any, Dict

import cv2
import numpy as np
import wandb
from ultralytics import YOLO
from wandb.integration.ultralytics import add_wandb_callback


def train_model(
    model_name: str = "simple",
    batch_size: int = -1,
    epochs: int = 10,
    wandb_logging: bool = False,
    connect_to_gcs: bool = True,
    num_workers: int = -1,
) -> Any:
    """
    Trains the YOLO model using the ml/configs/data_config/data.yaml for data splits.
    `num_workers` controls PyTorch DataLoader workers under the hood.
    """
    # 1) Pick a sane default for num_workers
    if num_workers < 0:
        import multiprocessing

        num_workers = max(1, multiprocessing.cpu_count() - 1)

    pretrained_weights_path = (
        f"/gcs/brain-tumor-data/models/{model_name}.pt" if connect_to_gcs else f"ml/models/{model_name}.pt"
    )

    print("Training model with pretrained weights:", pretrained_weights_path)
    t_model = YOLO(pretrained_weights_path)

    # 2) (Optional) W&B logging
    if wandb_logging:
        print("Initializing Weights & Biases for logging…")

        wandb.login()
        os.system("yolo settings wandb=True")
        wandb.init(
            project="BrainTumorDetection",
            job_type="training",
            config={
                "model_name": model_name,
                "batch_size": batch_size,
                "epochs": epochs,
                "num_workers": num_workers,
            },
        )

        add_wandb_callback(t_model)

    results = t_model.train(
        data="ml/configs/data_config/data_cloud.yaml" if connect_to_gcs else "ml/configs/data_config/data.yaml",
        epochs=epochs,
        patience=20,
        batch=batch_size,
        optimizer="auto",
        project="/gcs/brain-tumor-data/outputs/" if connect_to_gcs else "ml/models/",
        name=model_name,
        save=False,
        workers=num_workers,
    )

    return results


def normalize_image(image: np.ndarray) -> np.ndarray:
    return image.astype(np.float32) / 255.0


def resize_image(image: np.ndarray, size=(640, 640)) -> np.ndarray:
    return cv2.resize(image, size)


def get_prediction_from_array(image: np.ndarray):
    """
    Run inference on an already-loaded image array via the best saved model.
    Returns (results, annotated_image).
    """
    best_model_path = "ml/models/yolov8n/weights/epoch10_yolov8n.pt"
    if image is None:
        return None, None

    # Ensure BGR uint8 640×640
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)
    if image.shape[:2] != (640, 640):
        image = resize_image(image, size=(640, 640))

    model = YOLO(best_model_path)
    results = model.predict(source=image, imgsz=640, conf=0.5)
    annotated_image = results[0].plot()
    return results, annotated_image
