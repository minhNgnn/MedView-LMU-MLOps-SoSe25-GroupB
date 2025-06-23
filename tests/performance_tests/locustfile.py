import random

from locust import HttpUser, between, task


class MyUser(HttpUser):
    """A simple Locust user class that defines the tasks to be performed by the users."""

    host = "http://localhost:8000"
    wait_time = between(1, 2)

    @task
    def get_root(self) -> None:
        """A task that simulates a user visiting the root URL of the FastAPI app."""
        self.client.get("/health")

    @task(8)
    def predict(self):
        with open("tests/data/sample_image.PNG", "rb") as f:
            files = {"image_file": f}
            self.client.post("/api/predict", files=files)
