"use client";

export function AnalyticsDashboard() {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      <div className="card"><h3 className="text-sm text-surface-400">Total Assessments</h3><p className="mt-2 text-3xl font-bold text-white">0</p></div>
      <div className="card"><h3 className="text-sm text-surface-400">Total Findings</h3><p className="mt-2 text-3xl font-bold text-white">0</p></div>
      <div className="card"><h3 className="text-sm text-surface-400">Critical</h3><p className="mt-2 text-3xl font-bold text-critical">0</p></div>
      <div className="card"><h3 className="text-sm text-surface-400">High</h3><p className="mt-2 text-3xl font-bold text-danger">0</p></div>
      <div className="card md:col-span-2 lg:col-span-4">
        <h3 className="text-sm text-surface-400">Finding Distribution</h3>
        <div className="mt-4 flex h-48 items-center justify-center rounded-lg bg-surface-700">
          <p className="text-surface-400">Analytics data will appear here</p>
        </div>
      </div>
    </div>
  );
}
