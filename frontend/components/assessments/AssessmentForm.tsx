"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export function AssessmentForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [targets, setTargets] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const targetList = targets.split("\n").filter(Boolean).map((t) => t.trim());
      const res = await fetch("/api/v1/assessments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, targets: targetList }),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.error?.message || "Failed to create assessment");
        return;
      }

      router.push("/assessments");
    } catch {
      setError("Network error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="rounded-lg bg-danger/10 p-3 text-sm text-danger">{error}</div>}
      <div>
        <label className="mb-1 block text-sm text-surface-300">Assessment Name</label>
        <input className="input-field" value={name} onChange={(e) => setName(e.target.value)} placeholder="Internal Pentest Q3" required />
      </div>
      <div>
        <label className="mb-1 block text-sm text-surface-300">Targets (one per line)</label>
        <textarea className="input-field min-h-[120px]" value={targets} onChange={(e) => setTargets(e.target.value)} placeholder="192.168.1.0/24&#10;10.0.0.1&#10;example.com" />
      </div>
      <div className="flex gap-3">
        <button type="submit" className="btn-primary" disabled={loading}>{loading ? "Creating..." : "Create Assessment"}</button>
        <button type="button" className="btn-secondary" onClick={() => router.back()}>Cancel</button>
      </div>
    </form>
  );
}
