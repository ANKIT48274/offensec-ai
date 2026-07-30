"use client";
import { authFetch } from "@/lib/api/auth-fetch";

import { useEffect, useState } from "react";

interface NucleiFinding {
  id: string;
  template_id: string;
  template_name: string | null;
  severity: string;
  matched_url: string | null;
  protocol: string | null;
  tags: string[];
  cve_ids: string[];
  cvss_score: string | null;
  description: string | null;
  remediation: string | null;
}

export function NucleiResultsView({ projectId }: { projectId: string }) {
  const [findings, setFindings] = useState<NucleiFinding[]>([]);
  const [loading, setLoading] = useState(true);
  const [severity, setSeverity] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const params = new URLSearchParams({ project_id: projectId });
        if (severity !== "all") params.set("severity", severity);
        if (search) params.set("search", search);
        const res = await authFetch(`/api/v1/nuclei/results?${params}`);
        const data = await res.json();
        setFindings(data.data || []);
      } catch {
        setFindings([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [projectId, severity, search]);

  const severityCounts = {
    critical: findings.filter((f) => f.severity === "critical").length,
    high: findings.filter((f) => f.severity === "high").length,
    medium: findings.filter((f) => f.severity === "medium").length,
    low: findings.filter((f) => f.severity === "low").length,
    info: findings.filter((f) => f.severity === "info").length,
  };

  if (loading) return <div className="text-surface-400">Loading nuclei results...</div>;

  return (
    <div className="space-y-4">
      <div className="card">
        <h3 className="mb-3 font-medium text-white">Nuclei Findings</h3>
        <div className="mb-4 flex flex-wrap gap-4">
          {Object.entries(severityCounts).map(([sev, count]) => (
            count > 0 && (
              <div key={sev} className="text-center">
                <div className={`text-lg font-bold badge-${sev === "critical" ? "critical" : sev === "high" ? "high" : sev === "medium" ? "medium" : "low"}`}>
                  {count}
                </div>
                <div className="text-xs text-surface-400">{sev}</div>
              </div>
            )
          ))}
        </div>

        <div className="mb-4 flex gap-3">
          <select
            className="input-field w-auto"
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
          >
            <option value="all">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
            <option value="info">Info</option>
          </select>
          <input
            className="input-field"
            placeholder="Search templates, URLs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {findings.length === 0 ? (
          <p className="text-surface-400">No findings detected.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-surface-600 text-surface-400">
                  <th className="pb-2 pr-3">Severity</th>
                  <th className="pb-2 pr-3">Template</th>
                  <th className="pb-2 pr-3">URL</th>
                  <th className="pb-2 pr-3">Tags</th>
                  <th className="pb-2 pr-3">CVE</th>
                  <th className="pb-2 pr-3">CVSS</th>
                </tr>
              </thead>
              <tbody>
                {findings.map((f) => (
                  <tr key={f.id} className="border-b border-surface-700 text-white">
                    <td className="py-2 pr-3">
                      <span className={`badge-${f.severity === "critical" ? "critical" : f.severity === "high" ? "high" : f.severity === "medium" ? "medium" : "low"}`}>
                        {f.severity}
                      </span>
                    </td>
                    <td className="py-2 pr-3">
                      <div className="text-white">{f.template_name || f.template_id}</div>
                      <div className="text-xs text-surface-400">{f.template_id}</div>
                    </td>
                    <td className="py-2 pr-3 text-xs text-surface-300">{f.matched_url || "-"}</td>
                    <td className="py-2 pr-3">
                      <div className="flex flex-wrap gap-1">
                        {(f.tags || []).slice(0, 3).map((t, i) => (
                          <span key={i} className="rounded-full bg-surface-700 px-1.5 py-0.5 text-xs text-surface-300">{t}</span>
                        ))}
                      </div>
                    </td>
                    <td className="py-2 pr-3 text-xs text-accent">{(f.cve_ids || []).join(", ") || "-"}</td>
                    <td className="py-2 pr-3">{f.cvss_score || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {findings.length > 0 && (
        <div className="card">
          <h3 className="mb-3 font-medium text-white">Finding Details</h3>
          {findings.slice(0, 5).map((f) => (
            <div key={f.id} className="mb-4 border-b border-surface-700 pb-4 last:border-0">
              <div className="mb-1 flex items-center gap-2">
                <span className={`badge-${f.severity === "critical" ? "critical" : f.severity === "high" ? "high" : f.severity === "medium" ? "medium" : "low"}`}>
                  {f.severity}
                </span>
                <span className="font-medium text-white">{f.template_name || f.template_id}</span>
              </div>
              {f.description && <p className="mb-1 text-sm text-surface-300">{f.description}</p>}
              {f.remediation && (
                <p className="text-sm text-surface-400"><span className="text-warning">Fix:</span> {f.remediation}</p>
              )}
              {f.matched_url && <p className="text-xs text-surface-400">URL: {f.matched_url}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
