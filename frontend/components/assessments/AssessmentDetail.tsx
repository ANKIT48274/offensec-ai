"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

export function AssessmentDetail() {
  const { id } = useParams<{ id: string }>();
  const [assessment, setAssessment] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`/api/v1/assessments/${id}`);
        const data = await res.json();
        setAssessment(data.data);
      } catch {
        setAssessment(null);
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchData();
  }, [id]);

  if (loading) return <div className="text-surface-400">Loading...</div>;
  if (!assessment) return <div className="text-danger">Assessment not found.</div>;

  return (
    <div>
      <Link href="/assessments" className="text-sm text-accent hover:underline">← Back to Assessments</Link>
      <h1 className="mt-2 text-2xl font-bold text-white">{assessment.name}</h1>
      <p className="mt-1 text-sm text-surface-400">Status: {assessment.status}</p>

      <div className="mt-6 grid gap-6 md:grid-cols-4">
        <div className="card"><h3 className="text-sm text-surface-300">Status</h3><p className="mt-2 text-lg font-bold text-white capitalize">{assessment.status}</p></div>
        <div className="card"><h3 className="text-sm text-surface-300">Findings</h3><p className="mt-2 text-lg font-bold text-white">0</p></div>
        <div className="card"><h3 className="text-sm text-surface-300">Targets</h3><p className="mt-2 text-lg font-bold text-white">{assessment.scope?.targets?.length || 0}</p></div>
        <div className="card"><h3 className="text-sm text-surface-300">Started</h3><p className="mt-2 text-lg font-bold text-white">{assessment.started_at ? new Date(assessment.started_at).toLocaleDateString() : "Not started"}</p></div>
      </div>

      <div className="mt-6 flex gap-3">
        <Link href={`/findings?assessment_id=${assessment.id}`} className="btn-primary">View Findings</Link>
        <Link href={`/reports?assessment_id=${assessment.id}`} className="btn-secondary">Generate Report</Link>
      </div>
    </div>
  );
}
