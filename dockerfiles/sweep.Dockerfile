# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install OS-level deps (TLS certs, etc.)
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 1) Install Python deps + wandb
COPY ml/requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt wandb

# 2) Copy code & configs
COPY ml/train.py         ./train.py
COPY ml/models.py        ./models.py
COPY ml/configs/sweep.yaml ./sweep.yaml
COPY ml/configs/data_config/data.yaml ./data.yaml

# 3) Copy and make entrypoint executable
COPY dockerfiles/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# 4) Default env‑vars (override at `docker run` time)
ENV WANDB_ENTITY=theerdhasara-ludwig-maximilianuniversity-of-munich \
    WANDB_PROJECT=BrainTumorDetection \
    SWEEP_CONFIG=sweep.yaml \
    NUM=1

# 5) Launch
ENTRYPOINT ["bash", "./entrypoint.sh"]

