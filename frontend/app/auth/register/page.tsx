"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, username, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.error?.message || "Registration failed");
        return;
      }
      router.push("/auth/login");
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-900">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-white">OffenSec AI</h1>
          <p className="mt-2 text-sm text-surface-300">Create your account</p>
        </div>
        <form onSubmit={handleSubmit} className="card space-y-4">
          {error && (
            <div className="rounded-lg bg-danger/10 p-3 text-sm text-danger">{error}</div>
          )}
          <div>
            <label htmlFor="email" className="mb-1 block text-sm text-surface-300">Email</label>
            <input id="email" type="email" className="input-field" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required />
          </div>
          <div>
            <label htmlFor="username" className="mb-1 block text-sm text-surface-300">Username</label>
            <input id="username" className="input-field" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" required minLength={3} />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm text-surface-300">Password</label>
            <input id="password" type="password" className="input-field" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required minLength={8} />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? "Creating account..." : "Create Account"}
          </button>
          <p className="text-center text-sm text-surface-400">
            Already have an account? <Link href="/auth/login" className="text-accent hover:underline">Sign in</Link>
          </p>
        </form>
      </div>
    </main>
  );
}
