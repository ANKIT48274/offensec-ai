"use client";

import { useState } from "react";

interface Scan {
  id: string;
  project_id: string;
  target: string;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  error_message: string | null;
  json_result: { hosts: any[]; scan_info: any } | null;
}

export function ScanRunForm({ projectId }: { projectId: string }) {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [scan, setScan] = useState<Scan | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setScan(null);

    try {
      const res = await fetch("/api/v1/scans", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": getUserId(),
        },
        body: JSON.stringify({ project_id: projectId, target }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error?.message || "Scan failed");
        return;
      }
      setScan(data.data);
    } catch {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="card space-y-3">
        <h2 className="text-lg font-semibold text-white">Run Nmap Scan</h2>
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
          {loading ? "Scanning..." : "Run Scan"}
        </button>
      </form>

      {loading && (
        <div className="card text-center">
          <div className="mb-2 text-accent">Scan in progress...</div>
          <div className="h-2 w-full rounded-full bg-surface-700">
            <div className="h-2 w-1/2 animate-pulse rounded-full bg-accent" />
          </div>
        </div>
      )}

      {scan && <ScanResults scan={scan} />}
    </div>
  );
}

function ScanResults({ scan }: { scan: Scan }) {
  const hosts = scan.json_result?.hosts || [];
  const info = scan.json_result?.scan_info || {};

  if (scan.status === "failed") {
    return (
      <div className="card border-danger/50">
        <h2 className="text-lg font-semibold text-danger">Scan Failed</h2>
        <p className="mt-2 text-sm text-surface-300">{scan.error_message}</p>
      </div>
    );
  }

  if (hosts.length === 0) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-white">Scan Complete</h2>
        <p className="mt-2 text-sm text-surface-400">No hosts found. Target may be offline or blocked.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="card">
        <h2 className="text-lg font-semibold text-white">Scan Results</h2>
        <p className="text-xs text-surface-400">
          Target: {scan.target} | Elapsed: {info.elapsed || "N/A"}s | Finished: {info.finished_time || "N/A"}
        </p>
      </div>

      {hosts.map((host: any, i: number) => (
        <div key={i} className="card space-y-3">
          <div className="flex items-center gap-3">
            <span className={`badge-${host.status?.state === "up" ? "high" : "medium"}`}>
              {host.status?.state || "unknown"}
            </span>
            <span className="font-mono text-white">{host.ips?.[0] || "N/A"}</span>
            {host.hostnames?.[0]?.name && (
              <span className="text-sm text-surface-400">({host.hostnames[0].name})</span>
            )}
          </div>

          {host.os_matches && host.os_matches.length > 0 && (
            <div className="text-sm">
              <span className="text-surface-300">OS: </span>
              <span className="text-white">{host.os_matches[0].name}</span>
              <span className="ml-1 text-surface-400">({host.os_matches[0].accuracy}%)</span>
            </div>
          )}

          {host.os_guesses && host.os_guesses.length > 0 && (
            <div className="text-xs text-surface-400">
              {host.os_guesses.map((g: any, j: number) => (
                <span key={j}>
                  {g.vendor} {g.os_family} {g.os_gen} ({g.accuracy}%){j < host.os_guesses.length - 1 ? ", " : ""}
                </span>
              ))}
            </div>
          )}

          {host.ports && host.ports.length > 0 && (
            <div>
              <h3 className="mb-2 text-sm font-medium text-surface-300">Open Ports ({host.ports.length})</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-surface-600 text-surface-400">
                      <th className="pb-2 pr-4">Port</th>
                      <th className="pb-2 pr-4">Protocol</th>
                      <th className="pb-2 pr-4">State</th>
                      <th className="pb-2 pr-4">Service</th>
                      <th className="pb-2 pr-4">Version</th>
                    </tr>
                  </thead>
                  <tbody>
                    {host.ports.map((p: any, j: number) => (
                      <tr key={j} className="border-b border-surface-700 text-white">
                        <td className="py-2 pr-4 font-mono">{p.port}</td>
                        <td className="py-2 pr-4">{p.protocol}</td>
                        <td className="py-2 pr-4">
                          <span className={`badge-${p.state === "open" ? "high" : "medium"}`}>{p.state}</span>
                        </td>
                        <td className="py-2 pr-4">{p.service || "-"}</td>
                        <td className="py-2 pr-4 text-surface-300">{p.product} {p.version}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {host.scripts && host.scripts.length > 0 && (
            <div>
              <h3 className="mb-2 text-sm font-medium text-surface-300">Host Scripts</h3>
              {host.scripts.map((s: any, j: number) => (
                <div key={j} className="mb-1 text-sm">
                  <span className="text-accent">{s.id}:</span>{" "}
                  <span className="text-surface-300">{s.output}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function getUserId(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("user_id") || "";
}
