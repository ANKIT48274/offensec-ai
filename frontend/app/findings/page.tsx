import { FindingList } from "@/components/findings/FindingList";

export default function FindingsPage() {
  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Findings</h1>
      </div>
      <FindingList />
    </div>
  );
}
