"use client";
import { authFetch } from "@/lib/api/auth-fetch";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

export function ProjectDetail() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [project, setProject] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProject() {
      try {
        const res = await authFetch(`/api/v1/projects/${id}`);
        const data = await res.json();
        setProject(data.data);
      } catch {
        router.push("/projects");
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchProject();
  }, [id, router]);

  if (loading) return <div className="text-surface-400">Loading...</div>;
  if (!project) return null;

  return (
    <div>
      <div className="mb-6">
        <Link href="/projects" className="text-sm text-accent hover:underline">← Back to Projects</Link>
        <h1 className="mt-2 text-2xl font-bold text-white">{project.name}</h1>
        <p className="mt-1 text-surface-400">{project.description || "No description"}</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="card">
          <h3 className="text-sm font-medium text-surface-300">Assessments</h3>
          <p className="mt-2 text-2xl font-bold text-white">0</p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-surface-300">Findings</h3>
          <p className="mt-2 text-2xl font-bold text-white">0</p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-surface-300">Status</h3>
          <p className="mt-2 text-2xl font-bold text-success">Active</p>
        </div>
      </div>

      <div className="mt-6">
        <Link href={`/assessments/new?project_id=${project.id}`} className="btn-primary">
          New Assessment
        </Link>
      </div>
    </div>
  );
}
