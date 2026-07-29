import { SettingsPanel } from "@/components/settings/SettingsPanel";

export default function SettingsPage() {
  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-white">Settings</h1>
      <SettingsPanel />
    </div>
  );
}
