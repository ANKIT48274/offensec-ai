"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

export function FindingDetail() {
  const { id } = useParams<{ id: string }>();
  const [finding, setFinding] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`/api/v1/findings/${id}`);
        const data = await res.json();
        setFinding(data.data);
      } catch {
        setFinding(null);
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchData();
  }, [id]);

  if (loading) return <div className="text-surface-400">Loading...</div>;
  if (!finding) return <div className="text-danger">Finding not found.</div>;

  return (
    <div>
      <Link href="/findings" className="text-sm text-accent hover:underline">← Back to Findings</Link>
      <h1 className="mt-2 text-2xl font-bold text-white">{finding.title}</h1>

      <div className="mt-6 card space-y-4">
        <div className="grid grid-cols-3 gap-4">
          <div><span className="text-xs text-surface-400">Severity</span><p className="font-medium text-white capitalize">{finding.severity}</p></div>
          <div><span className="text-xs text-surface-400">Confidence</span><p className="font-medium text-white">{finding.confidence}</p></div>
          <div><span className="text-xs text-surface-400">Status</span><p className="font-medium text-white">{finding.status}</p></div>
        </div>

        {finding.target && (
          <div><span className="text-xs text-surface-400">Target</span><p className="font-mono text-sm text-white">{finding.target}</p></div>
        )}

        {finding.description && (
          <div><span className="text-xs text-surface-400">Description</span><p className="mt-1 text-sm text-white whitespace-pre-wrap">{finding.description}</p></div>
        )}

        {finding.cvss_score !== null && (
          <div><span className="text-xs text-surface-400">CVSS Score</span><p className="font-medium text-white">{finding.cvss_score}</p></div>
        )}

        {finding.remediation && (
          <div>
            <span className="text-xs text-surface-400">Remediation</span>
            <p className="mt-1 text-sm text-white whitespace-pre-wrap">{finding.remediation}</p>
          </div>
        )}
      </div>
    </div>
  );
}
