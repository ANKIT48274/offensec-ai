"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

export function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProjects() {
      try {
        const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : "";
        const res = await fetch("/api/v1/projects", {
          headers: token ? { "Authorization": `Bearer ${token}` } : {},
        });
        const data = await res.json();
        setProjects(data.data || []);
      } catch {
        setProjects([]);
      } finally {
        setLoading(false);
      }
    }
    fetchProjects();
  }, []);

  if (loading) {
    return <div className="text-surface-400">Loading projects...</div>;
  }

  if (projects.length === 0) {
    return (
      <div className="card text-center">
        <p className="text-surface-300">No projects yet.</p>
        <Link href="/projects/new" className="btn-primary mt-4 inline-block">
          Create your first project
        </Link>
      </div>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {projects.map((project) => (
        <Link key={project.id} href={`/projects/${project.id}`} className="card hover:border-accent/50 transition">
          <h3 className="font-semibold text-white">{project.name}</h3>
          <p className="mt-1 text-sm text-surface-400 line-clamp-2">
            {project.description || "No description"}
          </p>
          <p className="mt-3 text-xs text-surface-500">
            Created {new Date(project.created_at).toLocaleDateString()}
          </p>
        </Link>
      ))}
    </div>
  );
}
