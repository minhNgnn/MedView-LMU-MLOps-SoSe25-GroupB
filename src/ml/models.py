import os
from typing import Any, Dict

import cv2
import numpy as np
import onnxruntime as ort
import wandb
from ultralytics import YOLO
from wandb.integration.ultralytics import add_wandb_callback


def train_model(model_name: str = "simple", batch_size: int = -1, epochs: int = 10, wandb_logging: bool = False) -> Any:
    """Trains the machine learning model."""
    
    print("Training model with pretrained weights:", f"src/ml/models/{model_name}.pt")
    T_Model = YOLO(f"src/ml/models/{model_name}.pt")

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
        data="src/ml/configs/data_config/data.yaml",
        epochs=epochs,
        patience=20,
        batch=batch_size,
        optimizer="auto",
        project="src/ml/models/",
        name=model_name,
    )
    return results


def normalize_image(image):
    return image / 255.0


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


def export_model_to_onnx():
    # Export model to ONNX
    model_path = "models/yolov8n/weights/epoch10_yolov8n.pt"
    # Load the model
    model = YOLO(model_path)
    # Export to ONNX
    model.export(format="onnx", dynamic=True, imgsz=640, opset=12)


def get_prediction_from_onnx_array(image: np.ndarray):
    onnx_path = "ml/models/yolov8n/weights/epoch10_yolov8n.onnx"
    session = ort.InferenceSession(onnx_path)
    input_name = session.get_inputs()[0].name

    # Preprocess: resize, normalize, transpose to CHW, add batch dim
    img = resize_image(image, size=(640, 640))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))  # HWC to CHW
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Run inference
    outputs = session.run(None, {input_name: img})
    preds = outputs[0]  # YOLOv8 ONNX output: (batch, num_boxes, 85)

    # Postprocess: get boxes, scores, class_ids
    conf_thres = 0.5
    iou_thres = 0.5
    boxes = []
    scores = []
    class_ids = []
    for pred in preds[0]:
        score = pred[4]
        if score > conf_thres:
            x1, y1, x2, y2 = pred[0:4]
            class_id = int(np.argmax(pred[5:]))
            boxes.append([int(x1), int(y1), int(x2), int(y2)])
            scores.append(float(score))
            class_ids.append(class_id)

    # Draw boxes on the image
    annotated_image = resize_image(image, size=(640, 640)).copy()
    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = box
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_id}: {score:.2f}"
        cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return (boxes, scores, class_ids), annotated_image
