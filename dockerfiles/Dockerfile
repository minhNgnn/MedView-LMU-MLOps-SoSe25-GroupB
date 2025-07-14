FROM python:3.10-slim

# install python
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY ml/ ml/
WORKDIR /
RUN pip install -r ml/requirements.txt --no-cache-dir

ENTRYPOINT ["python", "-u", "ml/train.py"]