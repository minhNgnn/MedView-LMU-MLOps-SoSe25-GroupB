import bentoml
from bentoml.io import Image as BentoImage, Bytes
import numpy as np
from PIL import Image as PILImage
import io
import cv2
from .models import get_prediction_from_onnx_array

@bentoml.service
class YoloV8OnnxService:
    @bentoml.api(input=BentoImage(), output=Bytes())
    def predict(self, img: PILImage.Image):
        # Convert PIL image to numpy array (BGR for OpenCV)
        img_np = np.array(img)
        if img_np.shape[2] == 4:
            img_np = img_np[:, :, :3]  # Remove alpha if present
        img_np = img_np[:, :, ::-1]  # RGB to BGR
        _, annotated_image = get_prediction_from_onnx_array(img_np)
        # Encode annotated image as JPEG
        
        _, img_encoded = cv2.imencode(".jpg", annotated_image)
        return io.BytesIO(img_encoded.tobytes()).getvalue() 