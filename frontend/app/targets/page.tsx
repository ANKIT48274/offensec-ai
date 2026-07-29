import { TargetList } from "@/components/targets/TargetList";

export default function TargetsPage() {
  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Targets</h1>
      </div>
      <TargetList />
    </div>
  );
}
