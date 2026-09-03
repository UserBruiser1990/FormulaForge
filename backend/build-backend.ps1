$ErrorActionPreference = "Stop"

Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
python -m PyInstaller --clean --noconfirm formulaforge-backend.spec
