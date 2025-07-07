# 1) Start from a minimal Python image
FROM python:3.11-slim

# Make pip retry and wait longer, to survive flaky networks
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_RETRIES=5
ENV PIP_RESUME_RETRIES=5


# 3) Set working directory
WORKDIR /app

# 4) Copy only the dependency spec first, then install
#    (source path)                           (dest in /app)
COPY requirements.txt ./requirements.txt
COPY pyproject.toml ./pyproject.toml

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# 5) Copy your code and model files
# Bring in your Hydra config directory
COPY configs/ ./src/ml_backend/configs/
COPY src/    ./src/

COPY models/ ./models/

# 6) (Optional) If you want to install your project as a package:
# RUN pip install --no-deps --no-cache-dir .

# 7) When someone runs the image, execute your training script
ENTRYPOINT ["python", "-u", "src/ml_backend/train.py"]
 
