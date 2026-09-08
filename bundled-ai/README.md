# Bundled AI runtime

This directory is intentionally kept out of source control because the native
`llama.cpp` server binaries and GGUF model are large platform-specific assets.

For a packaged build, place these files here:

- macOS: `llama-server` and `qwen2.5-3b-instruct-q4_k_m.gguf`
- Windows: `llama-server.exe` and `qwen2.5-3b-instruct-q4_k_m.gguf`

The Electron main process starts the bundled runtime on port `11435` when both
files are present. If they are absent, it falls back to the existing Ollama
integration.
