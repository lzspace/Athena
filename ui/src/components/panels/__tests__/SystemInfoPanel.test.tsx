// ui/src/components/panels/__tests__/SystemInfoPanel.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import SystemInfoPanel from '../SystemInfoPanel';

// Mock the electronAPI global
beforeEach(() => {
  vi.resetAllMocks();
  (window as any).electronAPI = {
    getSystemStats: vi.fn().mockResolvedValue({
      cpu: '30%',
      memory: '4.2 GB / 8 GB',
      uptime: '2h 12m'
    })
  };
});

describe('SystemInfoPanel', () => {
  it('renders system info stats', async () => {
    render(<SystemInfoPanel />);

    // Wait for the async fetch and update
    expect(await screen.findByText(/🧠 CPU Load:/)).toBeInTheDocument();
    expect(screen.getByText(/💾 Memory:/)).toBeInTheDocument();
    expect(screen.getByText(/⏱️ Uptime:/)).toBeInTheDocument();
  });

  it('shows error when system stats fail to load', async () => {
    (window as any).electronAPI.getSystemStats = vi.fn().mockRejectedValue(new Error('Mock error'));

    render(<SystemInfoPanel />);

    expect(await screen.findByText(/Failed to load system data/)).toBeInTheDocument();
  });
});
