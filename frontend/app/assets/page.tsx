"use client";

import { useEffect, useState } from "react";
import { AssetList } from "@/components/assets/AssetList";

export default function AssetsPage() {
  const [projectId, setProjectId] = useState("");

  useEffect(() => {
    const pid = new URLSearchParams(window.location.search).get("project_id") || "";
    setProjectId(pid);
  }, []);

  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">Assets</h1>
      <p className="mb-6 text-sm text-surface-400">Discovered hosts, domains, URLs and technologies from all scans.</p>
      <AssetList projectId={projectId} />
    </div>
  );
}
