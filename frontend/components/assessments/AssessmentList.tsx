"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export function AssessmentList() {
  const [assessments, setAssessments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/v1/assessments");
        const data = await res.json();
        setAssessments(data.data || []);
      } catch {
        setAssessments([]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="text-surface-400">Loading...</div>;

  if (assessments.length === 0) {
    return (
      <div className="card text-center">
        <p className="text-surface-300">No assessments yet.</p>
        <Link href="/assessments/new" className="btn-primary mt-4 inline-block">Start your first assessment</Link>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {assessments.map((a) => (
        <Link key={a.id} href={`/assessments/${a.id}`} className="card flex items-center justify-between hover:border-accent/50 transition">
          <div>
            <h3 className="font-medium text-white">{a.name}</h3>
            <p className="text-sm text-surface-400">Status: {a.status}</p>
          </div>
          <span className={`text-sm ${a.status === "in_progress" ? "text-accent" : "text-surface-500"}`}>{a.status}</span>
        </Link>
      ))}
    </div>
  );
}
