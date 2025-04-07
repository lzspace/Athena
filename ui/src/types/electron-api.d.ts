// ui/src/types/electron-api.d.ts
export {};

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