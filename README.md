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
