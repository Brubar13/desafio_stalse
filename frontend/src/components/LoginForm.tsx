
"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

export default function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message ?? "Falha ao entrar.");
      setUser(data.user);
      router.replace("/tickets");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível entrar.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="form login-form" onSubmit={submit}>
      {params.get("reason") === "session-expired" && (
        <div className="alert error">Sua sessão expirou. Entre novamente.</div>
      )}
      <label htmlFor="email">E-mail</label>
      <input id="email" type="email" autoComplete="username" required value={email}
        onChange={(event) => setEmail(event.target.value)} />
      <label htmlFor="password">Senha</label>
      <input id="password" type="password" autoComplete="current-password" required value={password}
        onChange={(event) => setPassword(event.target.value)} />
      {error && <div className="alert error" role="alert">{error}</div>}
      <button className="button primary" disabled={loading}>
        {loading ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}
