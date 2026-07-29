import { ScanRunForm } from "@/components/scans/ScanRunForm";

interface Props {
  searchParams: Promise<{ project_id?: string }>;
}

export default async function NewScanPage({ searchParams }: Props) {
  const params = await searchParams;
  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">Nmap Scan</h1>
      <ScanRunForm projectId={params.project_id || ""} />
    </div>
  );
}
