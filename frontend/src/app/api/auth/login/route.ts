
import { NextRequest, NextResponse } from "next/server";

const BASE_URL = process.env.FASTAPI_BASE_URL ?? "http://127.0.0.1:8000";

export async function POST(request: NextRequest) {
  let credentials: { email?: string; password?: string };
  try {
    credentials = await request.json();
  } catch {
    return NextResponse.json({ message: "Corpo da requisição inválido." }, { status: 400 });
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ email: credentials.email, password: credentials.password }),
      cache: "no-store",
    });

    const data = await response.json().catch(() => null);
    if (!response.ok) {
      return NextResponse.json(
        { message: extractMessage(data) ?? "Não foi possível entrar.", details: data },
        { status: response.status },
      );
    }

    const token = data?.tokens?.token;
    if (!token || data?.id == null || !data?.email || !data?.profileType) {
      return NextResponse.json(
        { message: "A resposta de login da API está em um formato inesperado." },
        { status: 502 },
      );
    }

    const user = {
      id: Number(data.id),
      nome: String(data.nome ?? data.name ?? ""),
      email: String(data.email),
      profileType: String(data.profileType),
    };

    const result = NextResponse.json({ user });
    const secure = process.env.NODE_ENV === "production";
    result.cookies.set("access_token", String(token), {
      httpOnly: true,
      secure,
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60,
    });
    result.cookies.set("session_user", encodeURIComponent(JSON.stringify(user)), {
      httpOnly: true,
      secure,
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60,
    });
    return result;
  } catch {
    return NextResponse.json(
      { message: "Não foi possível conectar ao FastAPI. Confira se ele está rodando." },
      { status: 503 },
    );
  }
}

function extractMessage(body: unknown): string | null {
  if (!body || typeof body !== "object") return null;
  const obj = body as Record<string, unknown>;
  if (typeof obj.detail === "string") return obj.detail;
  if (Array.isArray(obj.detail)) return obj.detail.map((x) =>
    x && typeof x === "object" && "msg" in x ? String((x as { msg: unknown }).msg) : String(x)
  ).join(" ");
  if (typeof obj.message === "string") return obj.message;
  return null;
}
