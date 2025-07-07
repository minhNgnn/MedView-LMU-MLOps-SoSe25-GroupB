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

# ← Add this so Python can import ml_backend under /app/src
ENV PYTHONPATH=/app/src

# 4) Copy & install Python deps
COPY requirements.txt pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      fastapi==0.95.1 \
      uvicorn[standard]==0.22.0 && \
    pip install --no-cache-dir -r requirements.txt

# 5) Copy your app code + model weights
COPY src/    ./src/
COPY models/ ./models/

# 6) Expose the HTTP port
EXPOSE 8000

# 7) Start the FastAPI server
ENTRYPOINT ["uvicorn", "ml_backend.api:app", "--host", "0.0.0.0", "--port", "8000"]

