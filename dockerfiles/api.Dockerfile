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

# Set PYTHONPATH so Python can import backend, ml, and monitoring as top-level packages
ENV PYTHONPATH=/app

# 4) Copy & install Python deps
COPY backend/requirements.txt ./
COPY monitoring/requirements.txt ./monitoring-requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r monitoring-requirements.txt
# All monitoring dependencies are included in backend/requirements.txt

# 5) Copy your app code + monitoring system + only necessary ML files
COPY backend/src/ ./backend/src/
COPY monitoring/ ./monitoring/
COPY ml/predict.py ./ml/predict.py
COPY ml/utils.py ./ml/utils.py
# Copy model weights for inference
RUN mkdir -p /app/ml/models/yolov8n/weights/
COPY ml/models/yolov8n/weights/epoch10_yolov8n.pt /app/ml/models/yolov8n/weights/epoch10_yolov8n.pt
# If needed, also copy configs:
# COPY ml/configs/ ./ml/configs/

# 6) Expose the HTTP port
EXPOSE 8000

# 7) Set working directory and start the FastAPI server using the PORT env variable
WORKDIR /app/backend/src
ENTRYPOINT uvicorn api:app --host 0.0.0.0 --port $PORT
