#!/usr/bin/env sh
set -eu

rm -rf dist build
python -m PyInstaller --clean --noconfirm formulaforge-backend.spec
