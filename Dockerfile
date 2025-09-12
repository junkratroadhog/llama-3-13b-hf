FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

ARG MODEL_PATH="/workspace/Llama-3-13b-hf"
ARG API_PORT=11434

RUN apt-get update && apt-get install -y git git-lfs python3 python3-pip build-essential curl \
    && rm -rf /var/lib/apt/lists/*

RUN git lfs install && \
    mkdir -p $MODEL_PATH && \
    git clone https://huggingface.co/meta-llama/Llama-3-13b-hf $MODEL_PATH || true

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r /workspace/requirements.txt

COPY app.py /workspace/app.py

EXPOSE $API_PORT

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "11434"]
