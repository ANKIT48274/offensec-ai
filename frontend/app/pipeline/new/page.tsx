"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { PipelineRunForm } from "@/components/pipeline/PipelineRunForm";

function NewPipelineContent() {
  const searchParams = useSearchParams();
  const projectId = searchParams.get("project_id") || "";

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">New Pipeline Scan</h1>
      <PipelineRunForm projectId={projectId} />
    </div>
  );
}

export default function NewPipelinePage() {
  return (
    <Suspense fallback={<div className="p-6 text-surface-400">Loading...</div>}>
      <NewPipelineContent />
    </Suspense>
  );
}
