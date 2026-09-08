$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
$Model = Join-Path $RootDir "bundled-ai\qwen2.5-3b-instruct-q4_k_m.gguf"
$Runtime = Join-Path $RootDir "bundled-ai\llama-server.exe"

foreach ($Asset in @($Model, $Runtime)) {
    if (-not (Test-Path $Asset)) {
        throw "Missing bundled AI asset: $Asset"
    }
}

Push-Location (Join-Path $RootDir "frontend")
try {
    npm run dist -- --win nsis --publish never
}
finally {
    Pop-Location
}

Write-Host "Create the Intune .intunewin file on Windows with Microsoft's Win32 Content Prep Tool."
