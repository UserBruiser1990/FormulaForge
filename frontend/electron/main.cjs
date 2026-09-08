const { app, BrowserWindow, dialog, ipcMain, shell } = require("electron");
const { join } = require("node:path");
const { execFile, spawn } = require("node:child_process");
const { autoUpdater } = require("electron-updater");

let backendProcess;
let bundledAiProcess;
let mainWindow;
const BUNDLED_MODEL = "qwen2.5-3b-instruct-q4_k_m.gguf";

function backendCommand() {
  if (app.isPackaged) {
    const executable = process.platform === "win32" ? "formulaforge-backend.exe" : "formulaforge-backend";
    return join(process.resourcesPath, "backend", executable);
  }

  return join(__dirname, "../../backend/venv/bin/uvicorn");
}

function startBundledAi() {
  const runtimeName = process.platform === "win32" ? "llama-server.exe" : "llama-server";
  const runtimePath = app.isPackaged
    ? join(process.resourcesPath, "bundled-ai", runtimeName)
    : join(__dirname, "../../bundled-ai", runtimeName);
  const modelPath = app.isPackaged
    ? join(process.resourcesPath, "bundled-ai", BUNDLED_MODEL)
    : join(__dirname, "../../bundled-ai", BUNDLED_MODEL);

  if (!require("node:fs").existsSync(runtimePath) || !require("node:fs").existsSync(modelPath)) {
    return null;
  }

  bundledAiProcess = spawn(
    runtimePath,
    ["--model", modelPath, "--host", "127.0.0.1", "--port", "11435", "--ctx-size", "4096"],
    { cwd: join(runtimePath, ".."), stdio: "ignore" },
  );
  bundledAiProcess.on("error", (error) => {
    dialog.showErrorBox("FormulaForge AI runtime could not start", error.message);
  });
  return "http://127.0.0.1:11435/v1";
}

function startBackend(aiUrl) {
  const command = backendCommand();
  const args = app.isPackaged
    ? []
    : ["main:app", "--host", "127.0.0.1", "--port", "8000"];
  const cwd = app.isPackaged ? process.resourcesPath : join(__dirname, "../../backend");

  backendProcess = spawn(command, args, {
    cwd,
    stdio: "ignore",
    env: { ...process.env, ...(aiUrl ? { FORMULAFORGE_AI_URL: aiUrl, FORMULAFORGE_AI_MODEL: "local-model" } : {}) },
  });
  backendProcess.on("error", (error) => {
    dialog.showErrorBox(
      "FormulaForge backend could not start",
      `Unable to start the local API (${error.message}).`,
    );
  });
}

function runOllama(args) {
  return new Promise((resolve, reject) => {
    execFile(
      "ollama",
      args,
      { timeout: 30 * 60 * 1000 },
      (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr.trim() || error.message));
          return;
        }
        resolve(stdout);
      },
    );
  });
}

function hasModel(modelList) {
  return modelList
    .split("\n")
    .slice(1)
    .some((line) => line.trim().split(/\s+/)[0] === OLLAMA_MODEL);
}

async function ensureOllama() {
  if (bundledAiProcess) {
    return;
  }
  const ollamaModel = "llama3.1:8b";
  try {
    const models = await runOllama(["list"]);
    if (models
      .split("\n")
      .slice(1)
      .some((line) => line.trim().split(/\s+/)[0] === ollamaModel)) {
      return;
    }

    await dialog.showMessageBox({
      type: "info",
      title: "Downloading FormulaForge model",
      message: `The ${ollamaModel} model is not installed.`,
      detail: "FormulaForge will download it now. This is only needed once and requires approximately 5 GB of storage.",
      buttons: ["Download"],
      defaultId: 0,
    });
    await runOllama(["pull", ollamaModel]);
  } catch (error) {
    const result = await dialog.showMessageBox({
      type: "warning",
      title: "Ollama setup required",
      message: "FormulaForge needs a local AI runtime to generate results.",
      detail: error.message,
      buttons: ["Open Ollama Download", "Continue"],
      defaultId: 0,
    });
    if (result.response === 0) {
      await shell.openExternal("https://ollama.com/download");
    }
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 900,
    minHeight: 640,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: join(__dirname, "preload.cjs"),
    },
  });
  mainWindow.loadFile(join(__dirname, "../dist/index.html"));
}

function configureUpdater() {
  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = true;
  autoUpdater.on("update-available", (info) => {
    mainWindow?.webContents.send("update-status", {
      state: "available",
      version: info.version,
    });
  });
  autoUpdater.on("update-not-available", (info) => {
    mainWindow?.webContents.send("update-status", {
      state: "current",
      version: info.version,
    });
  });
  autoUpdater.on("download-progress", (progress) => {
    mainWindow?.webContents.send("update-status", {
      state: "downloading",
      percent: Math.round(progress.percent),
    });
  });
  autoUpdater.on("update-downloaded", () => {
    mainWindow?.webContents.send("update-status", { state: "downloaded" });
  });
}

ipcMain.handle("check-for-updates", async () => {
  if (!app.isPackaged) {
    return { state: "unavailable", message: "Updates are available in the installed app." };
  }

  try {
    const result = await autoUpdater.checkForUpdates();
    return {
      state: result?.updateInfo.version === app.getVersion() ? "current" : "checking",
      version: result?.updateInfo.version,
    };
  } catch (error) {
    return { state: "error", message: error.message };
  }
});

ipcMain.handle("download-update", async () => {
  await autoUpdater.downloadUpdate();
  return { state: "downloading" };
});

ipcMain.handle("install-update", () => {
  autoUpdater.quitAndInstall();
});

app.whenReady().then(() => {
  const aiUrl = startBundledAi();
  startBackend(aiUrl);
  createWindow();
  configureUpdater();
  ensureOllama();
});

app.on("before-quit", () => {
  backendProcess?.kill();
  bundledAiProcess?.kill();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
