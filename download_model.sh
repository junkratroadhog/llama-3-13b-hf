#!/bin/bash
set -e

MODEL_PATH="${MODEL_PATH:-/workspace/models/Llama-3-8B}"
HF_TOKEN="${HF_TOKEN:?HF_TOKEN must be set}"

mkdir -p "$MODEL_PATH"

echo "Downloading quantized GGUF model..."
huggingface-cli login --token $HF_TOKEN
huggingface-cli download TheBloke/Meta-Llama-3-8B-Instruct-GGUF \
  --include "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf" \
  --local-dir "$MODEL_PATH"
