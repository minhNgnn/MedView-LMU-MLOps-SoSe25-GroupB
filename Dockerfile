FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including libGL)
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-0

# Install Python dependencies
COPY ml/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# install python
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY ml/ ./ml/

# Set default command
ENTRYPOINT ["python", "-u", "./ml/train_cloud.py"]
