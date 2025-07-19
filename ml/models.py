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
<<<<<<< Updated upstream
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

    print(f"Training model with pretrained weights: ml/models/{model_name}.pt")
    t_model = YOLO(f"ml/models/{model_name}.pt")

    # 2) (Optional) W&B logging
    if wandb_logging:
        print("Initializing Weights & Biases for logging…")
        
=======
) -> Any:
    """Trains the machine learning model."""

    print("Training model with pretrained weights:", f"ml/models/{model_name}.pt")
    t_model = YOLO(f"ml/models/{model_name}.pt")

    if wandb_logging:
        print("Initializing Weights & Biases for logging...")
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream

        add_wandb_callback(t_model)

=======
        add_wandb_callback(t_model)

>>>>>>> Stashed changes
    results = t_model.train(
        data="ml/configs/data_config/data.yaml",
        epochs=epochs,
        patience=20,
        batch=batch_size,
        optimizer="auto",
        project="ml/models/",
        name=model_name,
        save=False,
        workers=num_workers,
    )

    return results
<<<<<<< Updated upstream


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


def export_model_to_onnx():
    """
    Export the trained YOLO model to ONNX format.
    """
    pt_path = "models/yolov8n/weights/epoch10_yolov8n.pt"
    model = YOLO(pt_path)
    model.export(format="onnx", dynamic=True, imgsz=640, opset=12)


def get_prediction_from_onnx_array(image: np.ndarray):
    """
    Run inference on an image via the exported ONNX model.
    Returns ((boxes, scores, class_ids), annotated_image).
    """
    onnx_path = "ml/models/yolov8n/weights/epoch10_yolov8n.onnx"
    sess = ort.InferenceSession(onnx_path)
    input_name = sess.get_inputs()[0].name

    img = resize_image(image, size=(640, 640)).astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))[None]  # CHW and batch dim

    outputs = sess.run(None, {input_name: img})
    preds = outputs[0]  # shape (1, num_boxes, 85)

    # Postprocess YOLO outputs
    conf_thres = 0.5
    boxes, scores, class_ids = [], [], []
    for pred in preds[0]:
        score = float(pred[4])
        if score > conf_thres:
            x1, y1, x2, y2 = map(int, pred[:4])
            cls = int(np.argmax(pred[5:]))
            boxes.append([x1, y1, x2, y2])
            scores.append(score)
            class_ids.append(cls)

    # Draw annotations
    annotated = resize_image(image, size=(640, 640)).copy()
    for (x1, y1, x2, y2), s, cid in zip(boxes, scores, class_ids):
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated,
            f"{cid}: {s:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    return (boxes, scores, class_ids), annotated


=======
>>>>>>> Stashed changes
