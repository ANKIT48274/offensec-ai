"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Scan {
  id: string;
  project_id: string;
  target: string;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  error_message: string | null;
}

export default function ScansPage() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/v1/scans?project_id=");
        const data = await res.json();
        setScans(data.data || []);
      } catch {
        setScans([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="p-6 text-surface-400">Loading...</div>;

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Scans</h1>
        <Link href="/scans/new" className="btn-primary">New Scan</Link>
      </div>
      {scans.length === 0 ? (
        <div className="card text-center text-surface-300">No scans yet.</div>
      ) : (
        <div className="space-y-3">
          {scans.map((s) => (
            <div key={s.id} className="card flex items-center justify-between">
              <div>
                <p className="font-mono text-white">{s.target}</p>
                <p className="text-xs text-surface-400">
                  {s.started_at ? new Date(s.started_at).toLocaleString() : "N/A"}
                </p>
              </div>
              <span className={`badge-${s.status === "completed" ? "low" : s.status === "failed" ? "critical" : "medium"}`}>
                {s.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
