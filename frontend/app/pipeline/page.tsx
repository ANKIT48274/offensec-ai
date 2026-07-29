"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface PipelineJobSummary {
  id: string;
  target: string;
  status: string;
  steps: { name: string; status: string }[];
  created_at: string;
}

export default function PipelinePage() {
  const [jobs, setJobs] = useState<PipelineJobSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/v1/pipeline/jobs?project_id=");
        const data = await res.json();
        setJobs(data.data || []);
      } catch {
        setJobs([]);
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
        <div>
          <h1 className="text-2xl font-bold text-white">Pipeline</h1>
          <p className="mt-1 text-sm text-surface-400">Multi-tool scan queue: Nmap → HTTPX → Results</p>
        </div>
        <Link href="/pipeline/new" className="btn-primary">New Pipeline Scan</Link>
      </div>

      {jobs.length === 0 ? (
        <div className="card text-center text-surface-300">No pipeline jobs yet.</div>
      ) : (
        <div className="space-y-3">
          {jobs.map((j) => (
            <div key={j.id} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-mono text-white">{j.target}</p>
                  <p className="text-xs text-surface-400">
                    {new Date(j.created_at).toLocaleString()}
                  </p>
                </div>
                <span className={`badge-${j.status === "completed" ? "low" : j.status === "failed" ? "critical" : "medium"}`}>
                  {j.status}
                </span>
              </div>
              <div className="mt-2 flex gap-2">
                {j.steps.map((s, i) => (
                  <span
                    key={i}
                    className={`rounded-full px-2 py-0.5 text-xs ${
                      s.status === "completed" ? "bg-success/20 text-success" :
                      s.status === "running" ? "bg-accent/20 text-accent" :
                      s.status === "failed" ? "bg-danger/20 text-danger" :
                      "bg-surface-600 text-surface-400"
                    }`}
                  >
                    {s.name}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
