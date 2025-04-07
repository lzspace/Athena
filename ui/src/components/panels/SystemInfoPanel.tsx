import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertTriangle } from "lucide-react";

interface SystemInfo {
  cpu: string;
  memory: string;
  uptime: string;
}

interface SystemInfoPanelProps {
  pollingInterval?: number; // Optional polling interval in ms (defaults to 5000)
}

export default function SystemInfoPanel({ pollingInterval = 5000 }: SystemInfoPanelProps) {
  const [stats, setStats] = useState<SystemInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const result = await window.electronAPI.getSystemStats();
        setStats(result);
      } catch (err) {
        console.error("Failed to fetch system stats:", err);
        setError("Failed to load system data.");
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, pollingInterval);
    return () => clearInterval(interval);
  }, [pollingInterval]);

  return (
    <div className="w-full h-full px-6 py-10 flex flex-col items-center justify-center text-white bg-slate-950">
      <h2 className="text-3xl font-bold mb-6 text-center">System Overview</h2>
      {error && (
        <Alert variant="destructive" className="mb-6 w-full max-w-xl text-white bg-red-800/30 border border-red-500">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            <div>
              <AlertTitle className="text-lg">Error</AlertTitle>
              <AlertDescription className="text-sm">{error}</AlertDescription>
            </div>
          </div>
        </Alert>
      )}
      {stats ? (
        <Card className="bg-slate-800 border border-slate-700 w-full max-w-3xl">
          <CardContent className="p-6 text-base grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div><strong>🧠 CPU Load:</strong> {stats.cpu}</div>
            <div><strong>💾 Memory:</strong> {stats.memory}</div>
            <div><strong>⏱️ Uptime:</strong> {stats.uptime}</div>
          </CardContent>
        </Card>
      ) : !error ? (
        <div className="text-slate-400 text-base text-center">Loading system stats...</div>
      ) : null}
    </div>
  );
}