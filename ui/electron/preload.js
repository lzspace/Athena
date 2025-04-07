// ui/electron/preload.ts
import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  getSystemStats: () => ipcRenderer.invoke("get-system-stats"),
});

// Typescript helper (optional)
declare global {
  interface Window {
    electronAPI: {
      getSystemStats: () => Promise<{
        cpu: string;
        memory: string;
        uptime: string;
      }>;
    };
  }
}
