import { AssessmentForm } from "@/components/assessments/AssessmentForm";

export default function NewAssessmentPage() {
  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">New Assessment</h1>
      <div className="card max-w-2xl">
        <AssessmentForm />
      </div>
    </div>
  );
}
