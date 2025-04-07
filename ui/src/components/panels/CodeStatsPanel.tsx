import React, { useEffect, useState } from 'react';

interface FileStats {
  file: string;
  size_bytes: number;
  modified: string;
  line_count: number;
}

const CodeStatsPanel: React.FC = () => {
  const [stats, setStats] = useState<FileStats[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:5000/code-stats')
      .then((res) => res.json())
      .then((data: FileStats[]) => {
        setStats(data);
      })
      .catch((err) => {
        setError(err.toString());
      });
  }, []);

  if (error) {
    return <div>Error loading code stats: {error}</div>;
  }

  return (
    <div>
      <h2>Code Statistics</h2>
      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>Size (bytes)</th>
            <th>Last Modified</th>
            <th>Line Count</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((s) => (
            <tr key={s.file}>
              <td>{s.file}</td>
              <td>{s.size_bytes}</td>
              <td>{s.modified}</td>
              <td>{s.line_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CodeStatsPanel;