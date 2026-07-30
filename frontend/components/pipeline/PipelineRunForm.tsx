"use client";
import { authFetch } from "@/lib/api/auth-fetch";

import { useState } from "react";

interface PipelineJob {
  id: string;
  project_id: string;
  target: string;
  status: string;
  steps: { name: string; status: string; error?: string }[];
  results: Record<string, any>;
  error_message: string | null;
}

export function PipelineRunForm({ projectId }: { projectId: string }) {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [job, setJob] = useState<PipelineJob | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setJob(null);

    try {
      const res = await authFetch("/api/v1/pipeline/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": getUserId(),
        },
        body: JSON.stringify({ project_id: projectId, target }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error?.message || "Pipeline failed");
        return;
      }
      setJob(data.data);
    } catch {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="card space-y-3">
        <h2 className="text-lg font-semibold text-white">Scan Pipeline</h2>
        <p className="text-sm text-surface-400">Nmap → HTTPX → Store Results</p>
        {error && <div className="rounded-lg bg-danger/10 p-3 text-sm text-danger">{error}</div>}
        <div>
          <label className="mb-1 block text-sm text-surface-300">Target (IP / hostname)</label>
          <input
            className="input-field"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="192.168.1.1"
            required
          />
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Pipeline Running..." : "Start Pipeline"}
        </button>
      </form>

      {loading && <PipelineProgress />}
      {job && <PipelineResults job={job} />}
    </div>
  );
}

function PipelineProgress() {
  return (
    <div className="card space-y-3">
      <h3 className="font-medium text-accent">Pipeline Running...</h3>
      <div className="space-y-2">
        <div className="flex items-center gap-3 text-sm">
          <span className="h-2 w-2 animate-pulse rounded-full bg-accent" />
          <span className="text-surface-300">Nmap Scan</span>
        </div>
        <div className="h-2 w-full rounded-full bg-surface-700">
          <div className="h-2 w-1/3 animate-pulse rounded-full bg-accent" />
        </div>
        <div className="flex items-center gap-3 text-sm text-surface-400">
          <span className="h-2 w-2 rounded-full bg-surface-500" />
          <span>HTTPX Probe</span>
        </div>
      </div>
    </div>
  );
}

function PipelineResults({ job }: { job: PipelineJob }) {
  const nmapResult = job.results?.nmap;
  const httpxResult = job.results?.httpx;
  const urls = httpxResult?.urls || [];

  if (job.status === "failed") {
    return (
      <div className="card border-danger/50">
        <h3 className="font-semibold text-danger">Pipeline Failed</h3>
        <p className="mt-1 text-sm text-surface-300">{job.error_message}</p>
        {job.steps.map((s, i) => (
          <div key={i} className="mt-2 text-sm">
            <span className="text-surface-400">{s.name}:</span>{" "}
            <span className={s.status === "failed" ? "text-danger" : "text-success"}>
              {s.status}
            </span>
            {s.error && <span className="ml-2 text-surface-400">({s.error})</span>}
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="card">
        <h3 className="font-semibold text-white">Pipeline Complete</h3>
        <p className="text-xs text-surface-400">Target: {job.target} | Status: {job.status}</p>
        <div className="mt-2 flex gap-2">
          {job.steps.map((s, i) => (
            <span
              key={i}
              className={`rounded-full px-2 py-0.5 text-xs ${
                s.status === "completed"
                  ? "bg-success/20 text-success"
                  : s.status === "failed"
                    ? "bg-danger/20 text-danger"
                    : "bg-surface-600 text-surface-300"
              }`}
            >
              {s.name}: {s.status}
            </span>
          ))}
        </div>
      </div>

      {nmapResult && nmapResult.hosts && nmapResult.hosts.length > 0 && (
        <div className="card">
          <h3 className="mb-2 font-medium text-white">Nmap — Live Hosts ({nmapResult.hosts.length})</h3>
          {nmapResult.hosts.map((h: any, i: number) => (
            <div key={i} className="mb-2 text-sm">
              <span className="text-accent">{h.ips?.[0] || "N/A"}</span>
              {h.os_matches?.[0] && (
                <span className="ml-2 text-surface-400">OS: {h.os_matches[0].name}</span>
              )}
            </div>
          ))}
        </div>
      )}

      {urls.length > 0 && (
        <div className="card">
          <h3 className="mb-3 font-medium text-white">HTTPX Results ({urls.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-surface-600 text-surface-400">
                  <th className="pb-2 pr-3">URL</th>
                  <th className="pb-2 pr-3">Status</th>
                  <th className="pb-2 pr-3">Title</th>
                  <th className="pb-2 pr-3">Server</th>
                  <th className="pb-2 pr-3">Tech</th>
                  <th className="pb-2 pr-3">Size</th>
                </tr>
              </thead>
              <tbody>
                {urls.map((u: any, i: number) => (
                  <tr key={i} className="border-b border-surface-700 text-white">
                    <td className="py-2 pr-3 font-mono text-xs">{u.url}</td>
                    <td className="py-2 pr-3">
                      <span className={`badge-${u.status_code < 300 ? "low" : u.status_code < 400 ? "medium" : "high"}`}>
                        {u.status_code}
                      </span>
                    </td>
                    <td className="py-2 pr-3 text-surface-300">{u.title || "-"}</td>
                    <td className="py-2 pr-3">{u.server || "-"}</td>
                    <td className="py-2 pr-3">
                      {u.tech?.length ? u.tech.join(", ") : "-"}
                    </td>
                    <td className="py-2 pr-3">{u.content_length ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {urls.length === 0 && job.status === "completed" && (
        <div className="card text-center text-surface-400">
          <p>HTTPX found no web services on discovered hosts.</p>
        </div>
      )}
    </div>
  );
}

function getUserId(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("user_id") || "";
}
