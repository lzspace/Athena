// ui/src/components/panels/__tests__/SystemInfoPanel.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import SystemInfoPanel from '../SystemInfoPanel'
import { describe, it, vi, beforeEach } from 'vitest'

// Mock electronAPI
beforeEach(() => {
  vi.resetAllMocks()
  // @ts-ignore
  global.window.electronAPI = {
    getSystemStats: vi.fn().mockResolvedValue({
      cpu: 'Intel Core i7',
      memory: '4096 / 8192 MB',
      uptime: '42 min',
    }),
  }
})

describe('SystemInfoPanel', () => {
  it('displays system stats after successful fetch', async () => {
    render(<SystemInfoPanel />)

    await waitFor(() => {
      expect(screen.getByText(/Intel Core i7/)).toBeInTheDocument()
      expect(screen.getByText(/4096 \/ 8192 MB/)).toBeInTheDocument()
      expect(screen.getByText(/42 min/)).toBeInTheDocument()
    })
  })

  it('shows error alert if fetching fails', async () => {
    // @ts-ignore
    window.electronAPI.getSystemStats = vi.fn().mockRejectedValue(new Error('Fail'))

    render(<SystemInfoPanel />)

    await waitFor(() => {
      expect(screen.getByText(/Failed to load system data/)).toBeInTheDocument()
    })
  })
})