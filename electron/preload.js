const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  sendCommand: (command) => {
    ipcRenderer.send("to-python", command);
  },

  onResponse: (callback) => {
    const listener = (_event, data) => {
      callback(data);
    };
    ipcRenderer.on("python-response", listener);
    return () => ipcRenderer.removeListener("python-response", listener);
  },
});