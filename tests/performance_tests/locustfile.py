import os
import random
from typing import Any, ClassVar, Optional

from google.cloud import storage
from locust import HttpUser, between, task


# Download a training image from GCP bucket at startup
def get_gcp_image_bytes() -> bytes:
    bucket_name: str = "brain-tumor-data"
    prefix: str = "BrainTumorYolov8/train/images/"
    try:
        client: storage.Client = storage.Client()
        bucket: Any = client.bucket(bucket_name)
        blobs: list = list(client.list_blobs(bucket_name, prefix=prefix))
        image_blobs: list = [b for b in blobs if b.name.lower().endswith((".jpg", ".jpeg", ".png"))]
        if image_blobs:
            blob: Any = random.choice(image_blobs)
            print(f"Downloaded image {blob.name} from GCP bucket.")
            return blob.download_as_bytes()
    except Exception as e:
        print(f"Failed to download image from GCP: {e}")
    # Fallback: generate a small dummy JPEG header
    return b"\xff\xd8\xff\xe0" + b"0" * 1024 + b"\xff\xd9"


class PredictUser(HttpUser):
    wait_time: ClassVar = between(1, 3)
    image_bytes: ClassVar[bytes] = get_gcp_image_bytes()

    @task(3)
    def predict(self) -> None:
        files = {"file": ("test.jpg", self.image_bytes, "image/jpeg")}
        self.client.post("/predict", files=files)

    @task(2)
    def get_patients(self) -> None:
        self.client.get("/patients")

    @task(1)
    def predict_invalid(self) -> None:
        # Send an invalid file to /predict to test error handling
        files = {"file": ("bad.txt", b"not an image", "text/plain")}
        self.client.post("/predict", files=files)
