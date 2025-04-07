import '@testing-library/jest-dom';

import { vi } from "vitest";

globalThis.window = Object.create(window);
globalThis.window.electronAPI = {
  getSystemStats: vi.fn().mockResolvedValue({
    cpu: "25%",
    memory: "6 GB / 16 GB",
    uptime: "2 hours 15 minutes"
  }),
};