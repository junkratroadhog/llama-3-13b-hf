#!/bin/bash
set -e

MODEL_PATH=${MODEL_PATH:-"/workspace/Llama-3-13b-hf"}
HF_TOKEN=${HF_TOKEN:-""}

# Ensure git-lfs is initialized
git lfs install

# Login to Hugging Face (non-interactive)
if [ ! -z "$HF_TOKEN" ]; then
    huggingface-cli login --token "$HF_TOKEN"
fi

# Clone repo if not exists
if [ ! -d "$MODEL_PATH" ]; then
    echo "Cloning LLaMA model repository..."
    GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/meta-llama/Llama-3-13b-hf "$MODEL_PATH"
fi

# Pull actual LFS files into the volume
echo "Pulling LFS files into $MODEL_PATH..."
cd "$MODEL_PATH"
git lfs pull

echo "Model download completed!"
