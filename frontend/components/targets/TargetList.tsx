"use client";

import { useEffect, useState } from "react";

export function TargetList() {
  const [targets, setTargets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/v1/targets");
        const data = await res.json();
        setTargets(data.data || []);
      } catch {
        setTargets([]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="text-surface-400">Loading...</div>;

  return (
    <div className="card">
      {targets.length === 0 ? (
        <p className="text-surface-300">No targets discovered yet.</p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-surface-600 text-left text-surface-400">
              <th className="pb-2 font-medium">Target</th>
              <th className="pb-2 font-medium">Type</th>
              <th className="pb-2 font-medium">Discovered</th>
            </tr>
          </thead>
          <tbody>
            {targets.map((t) => (
              <tr key={t.id} className="border-b border-surface-700 text-white">
                <td className="py-2">{t.value}</td>
                <td className="py-2 text-surface-300">{t.type}</td>
                <td className="py-2 text-surface-400">{new Date(t.discovered_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
