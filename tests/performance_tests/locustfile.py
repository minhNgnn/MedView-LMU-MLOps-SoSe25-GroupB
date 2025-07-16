import os

from google.cloud import storage
from locust import HttpUser, between, task


# Download a training image from GCP bucket at startup
def get_gcp_image_bytes():
    bucket_name = "brain-tumor-data"
    prefix = "BrainTumorYolov8/train/images/"
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = list(client.list_blobs(bucket_name, prefix=prefix))
        image_blobs = [b for b in blobs if b.name.lower().endswith((".jpg", ".jpeg", ".png"))]
        if image_blobs:
            blob = image_blobs[0]
            return blob.download_as_bytes()
    except Exception as e:
        print(f"Failed to download image from GCP: {e}")
    # Fallback: generate a small dummy JPEG header
    return b"\xff\xd8\xff\xe0" + b"0" * 1024 + b"\xff\xd9"


class PredictUser(HttpUser):
    wait_time = between(1, 3)
    image_bytes = get_gcp_image_bytes()

    @task
    def predict(self):
        files = {"file": ("test.jpg", self.image_bytes, "image/jpeg")}
        self.client.post("/predict", files=files)
