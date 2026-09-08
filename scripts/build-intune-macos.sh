#!/bin/bash
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT_DIR/scripts/prepare-bundled-build.sh" macos

cd "$ROOT_DIR/frontend"
CSC_IDENTITY_AUTO_DISCOVERY=false npm run dist -- --publish never
cd "$ROOT_DIR"

"$ROOT_DIR/scripts/build-intune-pkg.sh"
echo "Created frontend/dist/FormulaForge-AI-Intune.pkg"
