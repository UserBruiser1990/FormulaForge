#!/bin/bash
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_PATH="${1:-$ROOT_DIR/frontend/dist/mac-arm64/FormulaForge AI.app}"
OUTPUT_PATH="${2:-$ROOT_DIR/frontend/dist/FormulaForge-AI-Intune.pkg}"

if [ ! -d "$APP_PATH" ]; then
  echo "Build the macOS app first or pass its .app path as the first argument." >&2
  exit 1
fi

VERSION="$(node -p "require('$ROOT_DIR/frontend/package.json').version")"
mkdir -p "$(dirname "$OUTPUT_PATH")"

pkgbuild \
  --component "$APP_PATH" \
  --install-location /Applications \
  --scripts "$ROOT_DIR/scripts" \
  --identifier com.formulaforge.ai \
  --version "$VERSION" \
  "$OUTPUT_PATH"

echo "Created $OUTPUT_PATH"
