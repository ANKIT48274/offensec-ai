"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Asset {
  id: string;
  asset_type: string;
  value: string;
  label: string | null;
  ips: string[];
  technologies: string[];
  ports: { port: string; protocol: string; service?: string }[];
  os_guesses: string[];
  scan_count: number;
  first_seen: string | null;
  last_seen: string | null;
}

export function AssetList({ projectId }: { projectId: string }) {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const params = new URLSearchParams({ project_id: projectId, page_size: "100" });
        const res = await fetch(`/api/v1/assets?${params}`);
        const data = await res.json();
        setAssets(data.data || []);
      } catch {
        setAssets([]);
      } finally {
        setLoading(false);
      }
    }
    if (projectId) load();
  }, [projectId]);

  if (loading) return <div className="text-surface-400">Loading assets...</div>;

  return (
    <div className="space-y-3">
      {assets.length === 0 ? (
        <div className="card text-center text-surface-400">No assets discovered yet. Run a scan first.</div>
      ) : (
        assets.map((a) => (
          <Link key={a.id} href={`/assets/${a.id}`} className="card block transition hover:bg-surface-700">
            <div className="flex items-start justify-between">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-surface-700 px-2 py-0.5 text-xs text-surface-300">{a.asset_type}</span>
                  <span className="font-mono text-white">{a.value}</span>
                  {a.label && <span className="text-sm text-surface-400">({a.label})</span>}
                </div>
                {a.ips.length > 0 && (
                  <p className="mt-1 text-xs text-surface-400">IPs: {a.ips.join(", ")}</p>
                )}
              </div>
              <div className="ml-4 text-right text-xs text-surface-400">
                <div>Scanned {a.scan_count}x</div>
                {a.last_seen && <div>{new Date(a.last_seen).toLocaleDateString()}</div>}
              </div>
            </div>
            <div className="mt-2 flex flex-wrap gap-4 text-xs">
              {a.ports.length > 0 && (
                <span className="text-surface-300">{a.ports.length} ports</span>
              )}
              {a.technologies.length > 0 && (
                <span className="text-surface-300">{a.technologies.join(", ")}</span>
              )}
              {a.os_guesses.length > 0 && (
                <span className="text-surface-300">{a.os_guesses[0]}</span>
              )}
            </div>
          </Link>
        ))
      )}
    </div>
  );
}
