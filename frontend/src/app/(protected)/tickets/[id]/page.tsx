
import Link from "next/link";
import { notFound } from "next/navigation";
import { requireUser } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import { getApiErrorMessage } from "@/lib/api-error";
import type { Ticket } from "@/lib/types";
import { displayPriority, displayStatus, displayUserName } from "@/lib/format";
import EditRecordForm from "@/components/EditRecordForm";
import ErrorMessage from "@/components/ErrorMessage";

export default async function TicketDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const user = await requireUser();
  const { id } = await params;
  let ticket: Ticket;
  try {
    ticket = await serverApi<Ticket>(`/tickets/${encodeURIComponent(id)}`);
  } catch (error) {
    if (error && typeof error === "object" && "status" in error && (error as { status: number }).status === 404) notFound();
    return <ErrorMessage message={getApiErrorMessage(error)} />;
  }

  return (
    <section className="detail-card">
      <Link href="/tickets" className="back-link">← Voltar para tickets</Link>
      <p className="eyebrow">Ticket #{ticket.id}</p>
      <h1>{ticket.subject}</h1>
      <dl className="detail-list">
        <div><dt>Cliente</dt><dd>{ticket.customer?.name ?? `#${ticket.customer_id ?? "—"}`}</dd></div>
        <div><dt>Responsável</dt><dd>{displayUserName(ticket.assigned_user)}</dd></div>
        <div><dt>Canal</dt><dd>{ticket.channel}</dd></div>
        <div><dt>Status</dt><dd>{displayStatus(ticket.status)}</dd></div>
        <div><dt>Prioridade</dt><dd>{displayPriority(ticket.priority)}</dd></div>
        <div><dt>Criado em</dt><dd>{ticket.created_at ? new Date(ticket.created_at).toLocaleString("pt-BR") : "—"}</dd></div>
        <div><dt>Atualizado em</dt><dd>{ticket.updated_at ? new Date(ticket.updated_at).toLocaleString("pt-BR") : "—"}</dd></div>
      </dl>
      <EditRecordForm kind="ticket" record={ticket} isAdmin={user.profileType === "admin"} currentUserId={user.id} />
    </section>
  );
}
