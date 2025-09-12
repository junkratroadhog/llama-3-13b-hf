#!/bin/bash
set -e

# Variables
MODEL_PATH="${MODEL_PATH:-/workspace/Llama-3-13b-hf}"  # Use env var if provided
HF_TOKEN="${HF_TOKEN:?HF_TOKEN must be set}"          # Fail if HF_TOKEN not provided

# Make sure Git LFS is initialized
git lfs install

# Check if folder is already a git repo
if [ ! -d "$MODEL_PATH/.git" ]; then
    echo "Logging in to Hugging Face..."
    hf auth login --token "$HF_TOKEN"

    echo "Cloning LLaMA repository..."
    GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/meta-llama/Llama-3-13b-hf "$MODEL_PATH"
fi

# Pull LFS files
echo "Pulling LFS files..."
cd "$MODEL_PATH"
git lfs pull

echo "Model download completed!"
