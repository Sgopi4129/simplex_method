import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const backendUrl = process.env.SIMPLEX_BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json({ error: "SIMPLEX_BACKEND_URL is not configured." }, { status: 503 });
    }

    const response = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(await request.json()),
    });
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    const message = error instanceof Error ? error.message : "The simplex calculation failed.";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}