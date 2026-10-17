
import Link from "next/link";
import { requireUser } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import type { AppUser, Customer, Ticket } from "@/lib/types";
import { TicketCard } from "@/components/RecordCard";
import TicketFilters from "@/components/TicketFilters";
import CreateModal from "@/components/CreateModal";
import ErrorMessage from "@/components/ErrorMessage";
import { getApiErrorMessage } from "@/lib/api-error";

type Search = Promise<{ customer_id?: string; assigned_user_id?: string; status?: string }>;

export default async function TicketsPage({ searchParams }: { searchParams: Search }) {
  const user = await requireUser();
  const search = await searchParams;
  const query = new URLSearchParams();
  if (search.customer_id) query.set("customer_id", search.customer_id);
  if (search.assigned_user_id) query.set("assigned_user_id", search.assigned_user_id);
  if (search.status) query.set("status", search.status);

  let tickets: Ticket[] = [];
  let customers: Customer[] = [];
  let users: AppUser[] = [];
  let error = "";
  try {
    tickets = await serverApi<Ticket[]>(`/tickets${query.size ? `?${query}` : ""}`);
    // Preferir endpoint próprio de customers; o filtro não depende dos tickets estarem filtrados.
    customers = await serverApi<Customer[]>("/customer");
    if (user.profileType === "admin") users = await serverApi<AppUser[]>("/user/all_users");
  } catch (err) {
    error = getApiErrorMessage(err);
  }

  return (
    <>
      <div className="page-heading"><div><h1>Tickets</h1><p className="muted">Consulte e acompanhe os atendimentos.</p></div></div>
      <TicketFilters customers={customers} user={user} canCreate={user.profileType === "admin"} />
      {error && <ErrorMessage message={error} />}
      {!error && tickets.length === 0 && <div className="empty-state"><h2>Nenhum ticket encontrado</h2><p>Altere os filtros ou crie um ticket novo.</p></div>}
      <section className="card-grid">{tickets.map((ticket) => <TicketCard key={ticket.id} ticket={ticket} />)}</section>
      {user.profileType === "admin" && <CreateModal kind="ticket" customers={customers} users={users} />}
    </>
  );
}
