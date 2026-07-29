import Link from "next/link";
import { AssessmentList } from "@/components/assessments/AssessmentList";

export default function AssessmentsPage() {
  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Assessments</h1>
          <p className="mt-1 text-sm text-surface-300">View and manage security assessments</p>
        </div>
        <Link href="/assessments/new" className="btn-primary">New Assessment</Link>
      </div>
      <AssessmentList />
    </div>
  );
}
