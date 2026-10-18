
import Link from "next/link";
import { notFound } from "next/navigation";
import { requireUser } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import type { Customer } from "@/lib/types";
import EditRecordForm from "@/components/EditRecordForm";
import ErrorMessage from "@/components/ErrorMessage";
import { getApiErrorMessage } from "@/lib/api-error";

export default async function CustomerDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const user = await requireUser();
  const { id } = await params;
  let customer: Customer;
  try { customer = await serverApi<Customer>(`/customer/${encodeURIComponent(id)}`); }
  catch (error) {
    if (error && typeof error === "object" && "status" in error && (error as { status: number }).status === 404) notFound();
    return <ErrorMessage message={getApiErrorMessage(error)} />;
  }

  return (
    <section className="detail-card">
      <Link href="/customers" className="back-link">← Voltar para customers</Link>
      <p className="eyebrow">Customer #{customer.id}</p><h1>{customer.name}</h1>
      <dl className="detail-list">
        <div><dt>Nome</dt><dd>{customer.name}</dd></div>
        <div><dt>E-mail</dt><dd>{customer.email}</dd></div>
        <div><dt>Telefone</dt><dd>{customer.phone || "Não informado"}</dd></div>
      </dl>
      <EditRecordForm kind="customer" record={customer} isAdmin={user.profileType === "admin"} currentUserId={user.id} />
    </section>
  );
}
