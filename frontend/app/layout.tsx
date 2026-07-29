import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OffenSec AI",
  description: "AI-Powered Offensive Security Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-surface-900 text-white antialiased">
        {children}
      </body>
    </html>
  );
}
