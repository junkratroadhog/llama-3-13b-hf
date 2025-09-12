#!/bin/bash
set -e

MODEL_PATH="/workspace/Llama-3-13b-hf"
HF_TOKEN="${HF_TOKEN}"

# If the model is already downloaded, skip
if [ ! -d "$MODEL_PATH" ]; then
    echo "Logging in to Hugging Face..."
    huggingface-cli login --token $HF_TOKEN

    echo "Cloning LLaMA model repository..."
    GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/meta-llama/Llama-3-13b-hf "$MODEL_PATH"
    
    echo "Pulling LFS files..."
    cd "$MODEL_PATH"
    git lfs pull
else
    echo "Model already exists at $MODEL_PATH, skipping download."
fi

# Start FastAPI
uvicorn app:app --host 0.0.0.0 --port 11434
