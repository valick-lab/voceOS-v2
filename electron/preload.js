const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  sendCommand: (command) => {
    ipcRenderer.send("to-python", command);
  },

  onResponse: (callback) => {
    ipcRenderer.on("python-response", (_, data) => {
      callback(data);
    });
  },
});