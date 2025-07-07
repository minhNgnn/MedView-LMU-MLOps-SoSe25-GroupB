from typing import Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import numpy as np
import cv2
from .models import get_prediction_from_array

app = FastAPI()

class PatientData(BaseModel):
    age: int
    gender: str
    bloodPressure: int
    bloodSugar: int
    cholesterol: int
    smoker: bool

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict:
    # Read image file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    results = get_prediction_from_array(image)
    return {"results": str(results)}
