# 1) Base image
FROM python:3.11-slim

# 2) System deps for OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1-mesa-glx \
      libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# 3) Work directory
WORKDIR /app

# Add this so Python can import ml, backend, and monitoring under /app
ENV PYTHONPATH=/app/backend/src:/app/ml:/app/monitoring

# 4) Copy & install Python deps
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5) Copy your app code + model weights + configs + monitoring
COPY backend/src/ ./backend/src/
COPY monitoring/ ./monitoring/
COPY ml/predict.py /app/backend/src/ml/predict.py
COPY ml/utils.py /app/backend/src/ml/utils.py
# Create the weights directory and copy only the ONNX model file
RUN mkdir -p /app/backend/src/ml/models/yolov8n/weights/
COPY ml/models/yolov8n/weights/epoch10_yolov8n.pt /app/backend/src/ml/models/yolov8n/weights/epoch10_yolov8n.pt
# If needed, also copy configs:
# COPY ml/configs/ /app/ml/configs/

# 6) Expose the HTTP port
EXPOSE 8000

# 7) Set working directory and start the FastAPI server using the PORT env variable
WORKDIR /app/backend/src
ENTRYPOINT uvicorn api:app --host 0.0.0.0 --port $PORT
