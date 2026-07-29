"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export function ReportList() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/v1/reports");
        const data = await res.json();
        setReports(data.data || []);
      } catch {
        setReports([]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="text-surface-400">Loading...</div>;

  return (
    <div className="space-y-3">
      {reports.length === 0 ? (
        <div className="card text-center">
          <p className="text-surface-300">No reports generated yet.</p>
          <Link href="/assessments" className="btn-primary mt-4 inline-block">Go to Assessments</Link>
        </div>
      ) : (
        reports.map((r) => (
          <Link key={r.id} href={`/reports/${r.id}`} className="card flex items-center justify-between hover:border-accent/50 transition">
            <div>
              <h3 className="font-medium text-white">{r.title}</h3>
              <p className="text-sm text-surface-400">{r.format} • {r.finding_count} findings</p>
            </div>
            <span className="text-xs text-surface-500">{new Date(r.generated_at).toLocaleDateString()}</span>
          </Link>
        ))
      )}
    </div>
  );
}
