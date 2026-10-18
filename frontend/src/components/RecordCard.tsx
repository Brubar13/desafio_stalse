
import Link from "next/link";
import type { AppUser, Customer, Ticket } from "@/lib/types";
import { displayPriority, displayStatus, displayUserName } from "@/lib/format";

export function TicketCard({ ticket }: { ticket: Ticket }) {
  return (
    <article className="record-card">
      <div className="card-topline"><span className="eyebrow">Ticket #{ticket.id}</span><span className={`status status-${ticket.status}`}>{displayStatus(ticket.status)}</span></div>
      <h2>{ticket.subject}</h2>
      <p><strong>Cliente:</strong> {ticket.customer?.name ?? `#${ticket.customer_id ?? "—"}`}</p>
      <p><strong>Responsável:</strong> {displayUserName(ticket.assigned_user)}</p>
      <p><strong>Canal:</strong> {ticket.channel}</p>
      <p><strong>Prioridade:</strong> {displayPriority(ticket.priority)}</p>
      <Link className="button secondary card-action" href={`/tickets/${ticket.id}`}>Ver ticket</Link>
    </article>
  );
}

export function CustomerCard({ customer }: { customer: Customer }) {
  return (
    <article className="record-card">
      <span className="eyebrow">Customer #{customer.id}</span>
      <h2>{customer.name}</h2>
      <p><strong>E-mail:</strong> {customer.email}</p>
      <p><strong>Telefone:</strong> {customer.phone || "Não informado"}</p>
      <Link className="button secondary card-action" href={`/customers/${customer.id}`}>Ver customer</Link>
    </article>
  );
}

export function UserCard({ user }: { user: AppUser }) {
  return (
    <article className="record-card">
      <span className="eyebrow">Usuário #{user.id}</span>
      <h2>{user.name}</h2>
      <p><strong>E-mail:</strong> {user.email}</p>
      <p><strong>Perfil:</strong> {user.role}</p>
      <p><strong>Status:</strong> {user.is_active ? "Ativo" : "Inativo"}</p>
      <Link className="button secondary card-action" href={`/users/${user.id}`}>Ver usuário</Link>
    </article>
  );
}
