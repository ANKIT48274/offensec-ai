"use client";

import { useState } from "react";

export function SettingsPanel() {
  const [activeTab, setActiveTab] = useState("profile");

  const tabs = [
    { id: "profile", label: "Profile" },
    { id: "ai", label: "AI Configuration" },
    { id: "plugins", label: "Plugins" },
    { id: "api", label: "API Keys" },
  ];

  return (
    <div>
      <div className="flex gap-1 rounded-lg bg-surface-800 p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-md px-4 py-2 text-sm transition ${
              activeTab === tab.id ? "bg-accent text-white" : "text-surface-300 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="mt-6 card">
        {activeTab === "profile" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">Profile Settings</h2>
            <div className="grid gap-4 md:grid-cols-2">
              <div><label className="block text-sm text-surface-300">Email</label><input className="input-field mt-1" defaultValue="user@example.com" /></div>
              <div><label className="block text-sm text-surface-300">Username</label><input className="input-field mt-1" defaultValue="offensec_user" /></div>
            </div>
            <button className="btn-primary">Save Changes</button>
          </div>
        )}
        {activeTab === "ai" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">AI Configuration</h2>
            <p className="text-sm text-surface-400">Configure the AI model provider and settings.</p>
          </div>
        )}
        {activeTab === "plugins" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">Plugin Management</h2>
            <p className="text-sm text-surface-400">Enable, disable, and configure plugins.</p>
          </div>
        )}
        {activeTab === "api" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white">API Keys</h2>
            <p className="text-sm text-surface-400">Manage API keys for external integrations.</p>
          </div>
        )}
      </div>
    </div>
  );
}
