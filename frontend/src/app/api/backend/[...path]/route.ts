
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const BASE_URL = process.env.FASTAPI_BASE_URL ?? "http://127.0.0.1:8000";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxy(request: NextRequest, context: RouteContext) {
  const token = (await cookies()).get("access_token")?.value;
  if (!token) return NextResponse.json({ message: "Sessão não encontrada." }, { status: 401 });

  const { path } = await context.params;
  const target = `${BASE_URL}/${path.map(encodeURIComponent).join("/")}${request.nextUrl.search}`;
  try {
    
    const body = ["GET", "HEAD"].includes(request.method) ? undefined : await request.text();
    const upstream = await fetch(target, {
      method: request.method,
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
        ...(body ? { "Content-Type": request.headers.get("content-type") ?? "application/json" } : {}),
      },
      body,
      cache: "no-store",
    });

    const contentType = upstream.headers.get("content-type") ?? "";
    const payload = contentType.includes("application/json")
      ? await upstream.json().catch(() => null)
      : await upstream.text();

    if (upstream.status === 401) {
      const response = NextResponse.json(
        { message: "Sua sessão expirou. Entre novamente.", details: payload },
        { status: 401 },
      );
      response.cookies.set("access_token", "", { httpOnly: true, path: "/", maxAge: 0 });
      response.cookies.set("session_user", "", { httpOnly: true, path: "/", maxAge: 0 });
      return response;
    }

    return NextResponse.json(payload, { status: upstream.status });
  } catch {
    return NextResponse.json(
      { message: "Não foi possível conectar ao FastAPI.", status: 503 },
      { status: 503 },
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
