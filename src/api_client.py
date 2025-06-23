import requests


def predict_tumor_api(image_file):
    files = {"image_file": image_file.getvalue()}
    response = requests.post("http://localhost:8000/api/predict", files=files)
    return response.content
