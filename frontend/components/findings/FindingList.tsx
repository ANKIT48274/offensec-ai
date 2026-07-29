"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const BADGE: Record<string, string> = {
  critical: "badge-critical",
  high: "badge-high",
  medium: "badge-medium",
  low: "badge-low",
};

export function FindingList() {
  const [findings, setFindings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/v1/findings");
        const data = await res.json();
        setFindings(data.data || []);
      } catch {
        setFindings([]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="text-surface-400">Loading...</div>;

  return (
    <div className="space-y-3">
      {findings.length === 0 ? (
        <div className="card text-center">
          <p className="text-surface-300">No findings yet.</p>
        </div>
      ) : (
        findings.map((f) => (
          <Link key={f.id} href={`/findings/${f.id}`} className="card flex items-center justify-between hover:border-accent/50 transition">
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <span className={BADGE[f.severity] || "badge-medium"}>{f.severity}</span>
                <h3 className="font-medium text-white">{f.title}</h3>
              </div>
              <p className="mt-1 text-sm text-surface-400 line-clamp-1">{f.target && `Target: ${f.target}`}</p>
            </div>
            <span className="text-xs text-surface-500">{f.status}</span>
          </Link>
        ))
      )}
    </div>
  );
}
