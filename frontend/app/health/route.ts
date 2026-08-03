import { NextResponse } from "next/server";

/**
 * Health check endpoint for container orchestration.
 * Returns 200 when the frontend is serving traffic.
 */
export function GET() {
  return NextResponse.json({ status: "ok", service: "frontend" });
}
