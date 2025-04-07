import { app, BrowserWindow, ipcMain } from "electron";
import * as os from "os";
import * as path from "path";
import { format } from "url";

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"), // or .ts if compiled separately
    },
  });

  const startUrl =
    process.env.VITE_DEV_SERVER_URL ??
    format({
      pathname: path.join(__dirname, "../dist/index.html"),
      protocol: "file:",
      slashes: true,
    });

  mainWindow.loadURL(startUrl);
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// Expose system stats via IPC
ipcMain.handle("get-system-stats", async () => {
  const cpus = os.cpus();
  const cpuLoad = cpus[0].times;
  const total = Object.values(cpuLoad).reduce((acc, val) => acc + val, 0);

  const memory = `${(os.totalmem() / 1e9).toFixed(2)} GB / ${(os.freemem() / 1e9).toFixed(2)} GB`;
  const uptime = `${Math.floor(os.uptime() / 60)} min`;

  return {
    cpu: `${((cpuLoad.user / total) * 100).toFixed(2)}%`,
    memory,
    uptime,
  };
});

/*
ipcMain.handle("get-system-stats", async () => {
  const cpus = os.cpus();
  const totalMem = os.totalmem() / 1024 / 1024;
  const freeMem = os.freemem() / 1024 / 1024;
  const uptime = os.uptime();

  return {
    cpu: `${cpus[0].model} (${cpus.length} cores)`,
    memory: `${(totalMem - freeMem).toFixed(1)} / ${totalMem.toFixed(1)} MB`,
    uptime: `${Math.floor(uptime / 60)} min`,
  };
  */
 