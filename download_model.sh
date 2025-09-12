#!/bin/bash
set -e

MODEL_PATH="${MODEL_PATH:-/workspace/Llama-3-13b-hf}"
HF_TOKEN="${HF_TOKEN:?HF_TOKEN must be set}"

git lfs install

if [ ! -d "$MODEL_PATH/.git" ]; then
    echo "Cloning LLaMA repository with token..."
    git clone https://hf:${HF_TOKEN}@huggingface.co/meta-llama/Llama-3-13b-hf "$MODEL_PATH"
fi

cd "$MODEL_PATH"
git lfs pull
