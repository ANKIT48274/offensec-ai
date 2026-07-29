"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/projects", label: "Projects", icon: "📁" },
  { href: "/assessments", label: "Assessments", icon: "🔍" },
  { href: "/targets", label: "Targets", icon: "🎯" },
  { href: "/findings", label: "Findings", icon: "⚠️" },
  { href: "/reports", label: "Reports", icon: "📊" },
  { href: "/analytics", label: "Analytics", icon: "📈" },
  { href: "/settings", label: "Settings", icon: "⚙️" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-full w-64 flex-col border-r border-surface-600 bg-surface-800">
      <div className="flex h-14 items-center border-b border-surface-600 px-4">
        <Link href="/projects" className="text-lg font-bold text-accent">
          OffenSec AI
        </Link>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={isActive ? "sidebar-link-active" : "sidebar-link"}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-surface-600 p-3">
        <div className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-surface-300">
          <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center text-xs text-accent">
            U
          </div>
          <div className="flex-1 truncate">
            <p className="text-white">User</p>
            <p className="text-xs text-surface-400">user@example.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
