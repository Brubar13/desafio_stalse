
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { AppUser, Customer } from "@/lib/types";
import { formatPhone } from "@/lib/phone";

type Kind = "ticket" | "customer" | "user";
type Props = {
  kind: Kind;
  customers?: Customer[];
  users?: AppUser[];
};

export default function CreateModal({ kind, customers = [], users = [] }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [phone, setPhone] = useState("");

  useEffect(() => {
    const eventName = `open-create-${kind}`;
    const handler = () => { setError(""); setOpen(true); };
    window.addEventListener(eventName, handler);
    return () => window.removeEventListener(eventName, handler);
  }, [kind]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    const form = new FormData(event.currentTarget);
    let endpoint = "";
    let payload: Record<string, unknown> = {};

    if (kind === "customer") {
      endpoint = "/customer/create";
      payload = { name: form.get("name"), email: form.get("email"), phone: phone || null };
    } else if (kind === "user") {
      endpoint = "/user/create";
      payload = {
        name: form.get("name"), email: form.get("email"), password: form.get("password"),
        role: form.get("role"), is_active: true,
      };
    } else {
      endpoint = "/tickets/create";
      payload = {
        customer_id: Number(form.get("customer_id")),
        assigned_user_id: form.get("assigned_user_id") ? Number(form.get("assigned_user_id")) : null,
        channel: form.get("channel"), subject: form.get("subject"),
        priority: form.get("priority"), status: "open",
      };
    }

    try {
      const response = await fetch(`/api/backend${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => null);
      if (!response.ok) throw new Error(data?.message ?? data?.detail ?? "Não foi possível criar o registro.");
      setOpen(false);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setBusy(false);
    }
  }

  if (!open) return null;

  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(event) => {
      if (event.target === event.currentTarget) setOpen(false);
    }}>
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-heading">
          <h2 id="modal-title">
            {kind === "ticket" ? "Criar ticket" : kind === "customer" ? "Criar customer" : "Criar usuário"}
          </h2>
          <button className="icon-button" type="button" onClick={() => setOpen(false)} aria-label="Fechar">×</button>
        </div>
        <form className="form" onSubmit={submit}>
          {kind !== "ticket" ? <>
            <label htmlFor="name">Nome</label><input id="name" name="name" required maxLength={150} />
            <label htmlFor="email">E-mail</label><input id="email" name="email" type="email" required />
            {kind === "customer" ? <>
              <label htmlFor="phone">Telefone (opcional)</label>
              <input id="phone" value={phone} onChange={(event) => setPhone(formatPhone(event.target.value))}
                placeholder="(11) 97465-3600" />
            </> : <>
              <label htmlFor="password">Senha</label><input id="password" name="password" type="password" required />
              <label htmlFor="role">Perfil</label>
              <select id="role" name="role" defaultValue="user"><option value="user">Usuário</option><option value="admin">Admin</option></select>
            </>}
          </> : <>
            <label htmlFor="customer_id">Customer</label>
            <select id="customer_id" name="customer_id" required defaultValue="">
              <option value="" disabled>Selecione um customer</option>
              {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.name}</option>)}
            </select>
            <label htmlFor="assigned_user_id">Usuário responsável (opcional)</label>
            <select id="assigned_user_id" name="assigned_user_id" defaultValue="">
              <option value="">Não atribuído</option>
              {users.filter((user) => user.is_active).map((user) =>
                <option key={user.id} value={user.id}>{user.name}</option>)}
            </select>
            <label htmlFor="channel">Canal</label><input id="channel" name="channel" required placeholder="WEB, API, PHONE..." />
            <label htmlFor="subject">Assunto</label><textarea id="subject" name="subject" required rows={4} />
            <label htmlFor="priority">Prioridade</label>
            <select id="priority" name="priority" defaultValue="medium">
              <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option>
            </select>
          </>}
          {error && <div className="alert error" role="alert">{error}</div>}
          <div className="button-row">
            <button type="button" className="button secondary" onClick={() => setOpen(false)}>Cancelar</button>
            <button className="button primary" disabled={busy}>{busy ? "Salvando..." : "Confirmar"}</button>
          </div>
        </form>
      </section>
    </div>
  );
}
