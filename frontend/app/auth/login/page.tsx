import Link from "next/link";
import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-900">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-white">OffenSec AI</h1>
          <p className="mt-2 text-sm text-surface-300">Sign in to your account</p>
        </div>
        <LoginForm />
        <p className="mt-4 text-center text-sm text-surface-400">
          Don&apos;t have an account?{" "}
          <Link href="/auth/register" className="text-accent hover:underline">Create one</Link>
        </p>
      </div>
    </main>
  );
}
