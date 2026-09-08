#!/bin/bash
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-$ROOT_DIR/bundled-ai}"
MODEL_NAME="qwen2.5-3b-instruct-q4_k_m.gguf"
MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/${MODEL_NAME}?download=true"

mkdir -p "$TARGET_DIR"
curl --fail --location --retry 3 --output "$TARGET_DIR/$MODEL_NAME" "$MODEL_URL"
echo "Downloaded $TARGET_DIR/$MODEL_NAME"
echo "Place the matching llama.cpp llama-server binary beside the model."
