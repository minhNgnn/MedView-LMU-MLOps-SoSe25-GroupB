# dockerfiles/sweep.Dockerfile
FROM python:3.10-slim
WORKDIR /app

# 1) Install Python deps and wandb
COPY ml/requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt wandb

# 2) Copy only the code & configs needed for the sweep
COPY ml/train.py                  ./train.py
COPY ml/models.py                 ./models.py
COPY ml/configs/sweep.yaml  ./sweep.yaml
COPY ml/configs/data_config/data.yaml ./data.yaml

# 3) Run the sweep
ENTRYPOINT ["bash","-lc"]
CMD ["wandb sweep ml/configs/sweep.yaml && wandb agent personal-id/project-name/sweep id"]
