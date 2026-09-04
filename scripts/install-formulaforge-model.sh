#!/bin/bash
set -eu

MODEL="llama3.1:8b"
OLLAMA="/Applications/Ollama.app/Contents/Resources/ollama"

if [ ! -x "$OLLAMA" ]; then
  OLLAMA="/usr/local/bin/ollama"
fi

if [ ! -x "$OLLAMA" ]; then
  echo "Ollama is not installed." >&2
  exit 1
fi

open -a Ollama
sleep 15

if "$OLLAMA" list | awk 'NR > 1 {print $1}' | grep -Fxq "$MODEL"; then
  echo "$MODEL is already installed."
  exit 0
fi

"$OLLAMA" pull "$MODEL"
