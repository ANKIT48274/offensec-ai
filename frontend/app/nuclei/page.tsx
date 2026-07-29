"use client";

import { Suspense, useEffect, useState } from "react";
import { NucleiResultsView } from "@/components/nuclei/NucleiResults";

function NucleiPageContent() {
  const [projectId, setProjectId] = useState("");

  useEffect(() => {
    const pid = new URLSearchParams(window.location.search).get("project_id") || "";
    setProjectId(pid);
  }, []);

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">Nuclei Findings</h1>
      <p className="mb-6 text-sm text-surface-400">
        Automated vulnerability scanning results from Nuclei engine.
      </p>
      <NucleiResultsView projectId={projectId} />
    </div>
  );
}

export default function NucleiPage() {
  return (
    <Suspense fallback={<div className="p-6 text-surface-400">Loading...</div>}>
      <NucleiPageContent />
    </Suspense>
  );
}
