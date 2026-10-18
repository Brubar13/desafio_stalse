
"use client";

import { useRouter, useSearchParams } from "next/navigation";
import type { Customer, SessionUser } from "@/lib/types";

export default function TicketFilters({
  customers,
  user,
  canCreate,
}: {
  customers: Customer[];
  user: SessionUser;
  canCreate: boolean;
}) {
  const router = useRouter();
  const params = useSearchParams();
  const assigned = params.get("assigned_user_id") === String(user.id);
  const customerId = params.get("customer_id") ?? "";
  const status = params.get("status") ?? "";

  function update(key: string, value: string) {
    const next = new URLSearchParams(params.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.push(`/tickets${next.size ? `?${next.toString()}` : ""}`);
  }

  return (
    <div className="filter-bar">
      <label className="checkbox-label">
        <input type="checkbox" checked={assigned}
          onChange={(event) => update("assigned_user_id", event.target.checked ? String(user.id) : "")} />
        Visualizar apenas meus tickets
      </label>
      <label className="filter-control">
        <span>Cliente</span>
        <select value={customerId} onChange={(event) => update("customer_id", event.target.value)}>
          <option value="">Todos os clientes</option>
          {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.name}</option>)}
        </select>
      </label>
      <label className="filter-control">
        <span>Status</span>
        <select value={status} onChange={(event) => update("status", event.target.value)}>
          <option value="">Todos</option>
          <option value="open">Open</option>
          <option value="closed">Closed</option>
        </select>
      </label>
      {canCreate && <button className="button primary" onClick={() => window.dispatchEvent(new Event("open-create-ticket"))}>Criar Ticket</button>}
    </div>
  );
}
