import os
from typing import Any, Dict

import cv2
import numpy as np
from ultralytics import YOLO

import wandb
from wandb.integration.ultralytics import add_wandb_callback


def train_model(
    model_name: str = "simple",
    batch_size: int = -1,
    epochs: int = 10,
    wandb_logging: bool = False,
    connect_to_gcs: bool = True,
) -> Any:
    """Trains the machine learning model."""

    pretrained_weights_path = (
        f"/gcs/brain-tumor-data/models/{model_name}.pt" if connect_to_gcs else f"ml/models/{model_name}.pt"
    )

    print("Training model with pretrained weights:", pretrained_weights_path)
    t_model = YOLO(pretrained_weights_path)

    if wandb_logging:
        print("Initializing Weights & Biases for logging...")
        wandb.login()
        os.system("yolo settings wandb=True")
        wandb.init(
            project="BrainTumorDetection",
            job_type="training",
            #    config={"model_name": model_name, "batch_size": batch_size, "epochs": epochs},
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
    )
    return results
