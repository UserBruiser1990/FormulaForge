#!/bin/bash
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLATFORM="${1:-}"
TARGET_DIR="$ROOT_DIR/bundled-ai"

if [ "$PLATFORM" != "macos" ] && [ "$PLATFORM" != "windows" ]; then
  echo "Usage: $0 macos|windows" >&2
  exit 2
fi

if [ "$PLATFORM" = "macos" ]; then
  RUNTIME="$TARGET_DIR/llama-server"
else
  RUNTIME="$TARGET_DIR/llama-server.exe"
fi

MODEL="$TARGET_DIR/qwen2.5-3b-instruct-q4_k_m.gguf"

for required_file in "$RUNTIME" "$MODEL"; do
  if [ ! -f "$required_file" ]; then
    echo "Missing bundled AI asset: $required_file" >&2
    echo "Obtain the platform-matched llama.cpp runtime and Qwen GGUF model, then rerun." >&2
    exit 1
  fi
done

if [ "$PLATFORM" = "macos" ]; then
  chmod +x "$RUNTIME"
fi

echo "Bundled AI assets are ready for $PLATFORM."
