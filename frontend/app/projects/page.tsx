import Link from "next/link";
import { ProjectList } from "@/components/projects/ProjectList";

export default function ProjectsPage() {
  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Projects</h1>
          <p className="mt-1 text-sm text-surface-300">Manage your security assessment projects</p>
        </div>
        <Link href="/projects/new" className="btn-primary">
          New Project
        </Link>
      </div>
      <ProjectList />
    </div>
  );
}
