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
COPY ml/models/ ./ml/models/
COPY ml/configs/ ./ml/configs/

# 6) Expose the HTTP port
EXPOSE 8000

# 7) Start the FastAPI server
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
WORKDIR /app/backend/src

