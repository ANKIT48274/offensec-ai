"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

export function ReportViewer() {
  const { id } = useParams<{ id: string }>();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`/api/v1/reports/${id}`);
        const data = await res.json();
        setReport(data.data);
      } catch {
        setReport(null);
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchData();
  }, [id]);

  if (loading) return <div className="text-surface-400">Loading...</div>;
  if (!report) return <div className="text-danger">Report not found.</div>;

  return (
    <div>
      <Link href="/reports" className="text-sm text-accent hover:underline">← Back to Reports</Link>
      <h1 className="mt-2 text-2xl font-bold text-white">{report.title}</h1>
      <p className="mt-1 text-sm text-surface-400">{report.format} • {report.finding_count} findings</p>

      <div className="mt-6 card">
        <pre className="whitespace-pre-wrap font-mono text-sm text-white">{report.content || "Report content not available."}</pre>
      </div>
    </div>
  );
}
