
import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET() {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;
  const rawUser = cookieStore.get("session_user")?.value;

  if (!token || !rawUser) {
    return NextResponse.json({ message: "Sessão não encontrada." }, { status: 401 });
  }

  try {
    return NextResponse.json({ user: JSON.parse(decodeURIComponent(rawUser)) });
  } catch {
    return NextResponse.json({ message: "Sessão inválida." }, { status: 401 });
  }
}
