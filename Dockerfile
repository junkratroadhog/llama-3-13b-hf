FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

ARG MODEL_PATH="/workspace/Llama-3-13b-hf"
ARG API_PORT=11434

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git git-lfs python3 python3-pip build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Enable Git LFS
RUN git lfs install

# Set working directory
WORKDIR /workspace

# Copy requirements first (better cache)
COPY requirements.txt /workspace/requirements.txt

# Install Python dependencies
RUN python3 -m pip install --upgrade pip \
 && python3 -m pip install --no-cache-dir -r /workspace/requirements.txt

# Download the LLaMA model during build
RUN if [ ! -d "$MODEL_PATH" ]; then \
        git clone https://huggingface.co/meta-llama/Llama-3-13b-hf $MODEL_PATH; \
    fi

# Copy app server (done last so code changes don’t break cache)
COPY app.py /workspace/app.py

EXPOSE $API_PORT

# Run FastAPI with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "11434"]
