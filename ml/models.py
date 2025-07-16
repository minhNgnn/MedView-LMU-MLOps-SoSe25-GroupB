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
) -> Any:
    """Trains the machine learning model."""

    print("Training model with pretrained weights:", f"ml/models/{model_name}.pt")
    t_model = YOLO(f"ml/models/{model_name}.pt")

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
        data="ml/configs/data_config/data.yaml",
        epochs=epochs,
        patience=20,
        batch=batch_size,
        optimizer="auto",
        project="ml/models/",
        name=model_name,
    )
    return results
