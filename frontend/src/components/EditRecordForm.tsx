
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { AppUser, Customer, Ticket } from "@/lib/types";
import { formatPhone } from "@/lib/phone";

type Props =
  | { kind: "ticket"; record: Ticket; isAdmin: boolean; id: number }
  | { kind: "customer"; record: Customer; isAdmin: boolean; currentUserId: number }
  | { kind: "user"; record: AppUser; isAdmin: boolean; currentUserId: number };

export default function EditRecordForm(props: Props) {
  const { kind, record, isAdmin } = props;
  const router = useRouter();
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [phone, setPhone] = useState(kind === "customer" ? record.phone ?? "" : "");

  const editable = kind === "ticket"
    ? isAdmin || (record as Ticket).assigned_user_id === props.currentUserId ||
      (record as Ticket).assigned_user?.id === props.currentUserId
    : kind === "user" ? isAdmin || record.id === props.currentUserId : isAdmin;

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    const form = new FormData(event.currentTarget);
    let endpoint = "";
    let payload: Record<string, unknown> = {};

    if (kind === "ticket") {
      endpoint = `/tickets/${record.id}`;
      payload = { status: form.get("status"), priority: form.get("priority") };
    } else if (kind === "customer") {
      endpoint = `/customer/${record.id}`;
      payload = { name: form.get("name"), email: form.get("email"), phone: phone || null };
    } else {
      endpoint = `/user/${record.id}`;
      payload = {
        name: form.get("name"), email: form.get("email"),
        ...(String(form.get("password") ?? "").trim() ? { password: form.get("password") } : {}),
        ...(isAdmin ? { role: form.get("role"), is_active: form.get("is_active") === "true" } : {}),
      };
    }

    try {
      const response = await fetch(`/api/backend${endpoint}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => null);
      if (!response.ok) throw new Error(data?.message ?? data?.detail ?? "Não foi possível atualizar o registro.");
      setEditing(false);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setBusy(false);
    }
  }

  if (!editable) return null;

  return (
    <section className="edit-panel">
      {!editing ? (
        <button className="button primary" onClick={() => setEditing(true)}>Atualizar {kind === "ticket" ? "ticket" : kind === "customer" ? "customer" : "usuário"}</button>
      ) : (
        <form className="form" onSubmit={submit}>
          {kind === "ticket" ? <>
            <label htmlFor="status">Status</label>
            <select id="status" name="status" defaultValue={(record as Ticket).status}>
              <option value="open">Open</option><option value="closed">Closed</option>
            </select>
            <label htmlFor="priority">Prioridade</label>
            <select id="priority" name="priority" defaultValue={(record as Ticket).priority}>
              <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option>
            </select>
          </> : kind === "customer" ? <>
            <label htmlFor="name">Nome</label><input id="name" name="name" required defaultValue={(record as Customer).name} />
            <label htmlFor="email">E-mail</label><input id="email" name="email" type="email" required defaultValue={(record as Customer).email} />
            <label htmlFor="phone">Telefone</label>
            <input id="phone" value={phone} onChange={(event) => setPhone(formatPhone(event.target.value))} />
          </> : <>
            <label htmlFor="name">Nome</label><input id="name" name="name" required defaultValue={(record as AppUser).name} />
            <label htmlFor="email">E-mail</label><input id="email" name="email" type="email" required defaultValue={(record as AppUser).email} />
            <label htmlFor="password">Nova senha (opcional)</label><input id="password" name="password" type="password" autoComplete="new-password" />
            {isAdmin && <>
              <label htmlFor="role">Perfil</label>
              <select id="role" name="role" defaultValue={(record as AppUser).role}>
                <option value="user">Usuário</option><option value="admin">Admin</option>
              </select>
              <label htmlFor="is_active">Ativo</label>
              <select id="is_active" name="is_active" defaultValue={String((record as AppUser).is_active)}>
                <option value="true">True</option><option value="false">False</option>
              </select>
            </>}
          </>}
          {error && <div className="alert error" role="alert">{error}</div>}
          <div className="button-row">
            <button type="button" className="button secondary" disabled={busy} onClick={() => { setEditing(false); setError(""); }}>Cancelar</button>
            <button className="button primary" disabled={busy}>{busy ? "Salvando..." : "Confirmar"}</button>
          </div>
        </form>
      )}
    </section>
  );
}
