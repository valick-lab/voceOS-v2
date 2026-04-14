const { app, BrowserWindow, ipcMain } = require("electron");
const { spawn } = require("child_process");

let pyProcess;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: __dirname + "/preload.js",
      contextIsolation: true,
    },
  });

  mainWindow.loadURL("http://localhost:5173");
}

function startPython() {
  pyProcess = spawn("python", ["./backend/main.py"]);

  pyProcess.stdout.on("data", (data) => {
    mainWindow.webContents.send("python-response", data.toString());
  });

  pyProcess.stderr.on("data", (data) => {
    console.error(data.toString());
  });
}

ipcMain.on("to-python", (_, command) => {
  if (pyProcess) {
    pyProcess.stdin.write(JSON.stringify({ command }) + "\n");
  }
});

app.whenReady().then(() => {
  createWindow();
  startPython();
});