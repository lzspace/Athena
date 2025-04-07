"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const url_1 = require("url");
let mainWindow = null;
function createWindow() {
    mainWindow = new electron_1.BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"), // or .ts if compiled separately
        },
    });
    const startUrl = process.env.VITE_DEV_SERVER_URL ??
        (0, url_1.format)({
            pathname: path.join(__dirname, "../dist/index.html"),
            protocol: "file:",
            slashes: true,
        });
    mainWindow.loadURL(startUrl);
}
electron_1.app.whenReady().then(() => {
    createWindow();
    electron_1.app.on("activate", () => {
        if (electron_1.BrowserWindow.getAllWindows().length === 0)
            createWindow();
    });
});
electron_1.app.on("window-all-closed", () => {
    if (process.platform !== "darwin")
        electron_1.app.quit();
});
// Expose system stats via IPC
electron_1.ipcMain.handle("get-system-stats", async () => {
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
