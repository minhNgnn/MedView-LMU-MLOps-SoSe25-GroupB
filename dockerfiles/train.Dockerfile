# 1) Start from a minimal Python image
FROM python:3.11-slim

# Make pip retry and wait longer, to survive flaky networks
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_RETRIES=5
ENV PIP_RESUME_RETRIES=5

# 3) Set working directory
WORKDIR /app

# 2) Install system deps for OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

# 4) Copy only the dependency spec first, then install
COPY ml/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5) Copy your code, configs, and model files
COPY ml/ ./ml/

# 6) (Optional) If you want to install your project as a package:
# RUN pip install --no-deps --no-cache-dir .

# 7) When someone runs the image, execute your training script
ENTRYPOINT ["python", "-u", "-m", "ml.train"]
