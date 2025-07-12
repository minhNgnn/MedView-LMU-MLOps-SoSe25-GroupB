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

# Add this so Python can import ml and backend under /app
ENV PYTHONPATH=/app/backend/src:/app/ml

# 4) Copy & install Python deps
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5) Copy your app code + model weights + configs
COPY backend/src/ ./backend/src/
# COPY ml/predict.py /app/backend/src/ml/predict.py
# COPY ml/models/ /app/backend/src/ml/models/
# If needed, also copy configs:
# COPY ml/configs/ /app/backend/src/ml/configs/

# 6) Expose the HTTP port
EXPOSE 8000

# 7) Set working directory and start the FastAPI server using the PORT env variable
WORKDIR /app/backend/src
ENTRYPOINT uvicorn api:app --host 0.0.0.0 --port $PORT
