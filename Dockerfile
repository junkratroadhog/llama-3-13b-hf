FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

ARG MODEL_PATH="/workspace/Llama-3-13b-hf"
ARG API_PORT=11434
ARG HF_TOKEN

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git git-lfs python3 python3-pip build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Enable Git LFS
RUN git lfs install

# Set working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r /workspace/requirements.txt

# Copy app server
COPY app.py /workspace/app.py

EXPOSE $API_PORT

# Run FastAPI with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "11434"]
