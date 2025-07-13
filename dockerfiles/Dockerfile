FROM python:3.10-slim

# install python
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY src/ml/requirements.txt src/ml/requirements.txt
COPY src/ml/ src/ml/
WORKDIR /
RUN pip install -r src/ml/requirements.txt --no-cache-dir

ENTRYPOINT ["python", "-u", "src/ml/train.py"]