"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

function getUserId(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("user_id") || "";
}

export function ProjectForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/v1/projects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": getUserId(),
        },
        body: JSON.stringify({ name, description }),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.error?.message || "Failed to create project");
        return;
      }

      router.push("/projects");
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-lg bg-danger/10 p-3 text-sm text-danger">{error}</div>
      )}
      <div>
        <label htmlFor="name" className="mb-1 block text-sm text-surface-300">Project Name</label>
        <input id="name" className="input-field" value={name} onChange={(e) => setName(e.target.value)} placeholder="My Assessment" required />
      </div>
      <div>
        <label htmlFor="description" className="mb-1 block text-sm text-surface-300">Description</label>
        <textarea id="description" className="input-field min-h-[100px]" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Optional description" />
      </div>
      <div className="flex gap-3">
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Creating..." : "Create Project"}
        </button>
        <button type="button" className="btn-secondary" onClick={() => router.back()}>
          Cancel
        </button>
      </div>
    </form>
  );
}
