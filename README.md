# FormulaForge AI

FormulaForge AI converts plain-English Excel requests into formulas, explanations,
corrections, VBA, and Power Query M code. The app runs locally with FastAPI,
React, and Ollama.

## Development

Start Ollama with the `llama3.1:8b` model available, then run:

```sh
cd backend
uvicorn main:app --reload
```

In another terminal:

```sh
cd frontend
npm run dev
```

The frontend uses `http://localhost:8000` by default. For a hosted deployment,
set `VITE_API_URL` before building, for example:

```sh
VITE_API_URL=https://api.example.com npm run build
```

## Desktop installers

Install PyInstaller in the backend virtual environment:

```sh
cd backend
pip install pyinstaller
./build-backend.sh
```

On Windows, run `build-backend.ps1` instead. Build the desktop installer from
the frontend directory:

```sh
cd frontend
npm install
npm run dist
```

This produces a macOS DMG on macOS and a Windows NSIS installer on Windows.
On first launch, the packaged app checks whether Ollama is available and whether
the exact `llama3.1:8b` model is already installed. It skips the download when
both resources are present. If the model is missing, it asks before downloading
it; if Ollama is missing, it opens the official download page. Initial setup
requires an internet connection and approximately 5 GB of model storage.

### Intune pilot deployment for macOS

For a managed pilot, build an Intune-compatible package after building the
desktop app:

```sh
./scripts/build-intune-pkg.sh
```

Upload `frontend/dist/FormulaForge-AI-Intune.pkg` to Intune as a macOS
line-of-business app. The package installs FormulaForge AI into `/Applications`
and clears the quarantine attribute as an administrator-controlled exception
for this unsigned pilot build. This does not replace Apple signing or
notarization and should only be deployed to managed devices.

Ollama and the `llama3.1:8b` model are separate prerequisites. Deploy Ollama
through an approved Intune package or install it separately, then ensure the
model is available before launching FormulaForge.

## Updates

The desktop app checks the public GitHub Releases feed when **Check for updates**
is clicked. If a newer release is found, the app downloads it and offers a
restart to install. Releases must be created with matching macOS and Windows
installer assets. The browser development build does not perform update checks.
