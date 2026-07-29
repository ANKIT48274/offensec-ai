import { ProjectForm } from "@/components/projects/ProjectForm";

export default function NewProjectPage() {
  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">New Project</h1>
      <div className="card max-w-2xl">
        <ProjectForm />
      </div>
    </div>
  );
}
