import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import SystemInfoPanel from '../SystemInfoPanel';

beforeEach(() => {
  vi.resetAllMocks();
  // Global mock returning initial stats
  (window as any).electronAPI = {
    getSystemStats: vi.fn().mockResolvedValue({
      cpu: '30%',
      memory: '4.2 GB / 8 GB',
      uptime: '2h 12m'
    })
  };
});

describe('SystemInfoPanel Polling Behavior (Real Timers)', () => {
  it(
    'updates system stats after polling interval',
    async () => {
      // Use a slightly longer polling interval for test stability (e.g., 100ms)
      render(<SystemInfoPanel pollingInterval={100} />);

      // Wait for the initial render to show the initial stats ("30%")
      expect(await screen.findByText(/30%/)).toBeInTheDocument();

      // At this point, depending on scheduling the API might have been called once or twice.
      // We don’t assert an exact count here—only that it was called at least once.
      expect((window as any).electronAPI.getSystemStats).toHaveBeenCalled();

      // Update the mock so that the next polling call returns new data
      (window as any).electronAPI.getSystemStats.mockResolvedValueOnce({
        cpu: '40%',
        memory: '5.0 GB / 8 GB',
        uptime: '3h 00m'
      });

      // Wait for a little longer than the polling interval (e.g., 150ms)
      await new Promise((resolve) => setTimeout(resolve, 150));

      // Check that the polling function was called again
      // Now it should have been called at least twice.
      expect((window as any).electronAPI.getSystemStats).toHaveBeenCalledTimes(2);

      // Verify that the UI now reflects the updated stats ("40%")
      await waitFor(() => {
        expect(screen.getByText(/40%/)).toBeInTheDocument();
      });
    },
    3000 // Test timeout
  );
});