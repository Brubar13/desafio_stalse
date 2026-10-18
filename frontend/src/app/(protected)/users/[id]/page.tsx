
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { requireUser } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import type { AppUser } from "@/lib/types";
import EditRecordForm from "@/components/EditRecordForm";
import ErrorMessage from "@/components/ErrorMessage";
import { getApiErrorMessage } from "@/lib/api-error";

export default async function UserDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const sessionUser = await requireUser();
  const { id } = await params;
  const isAdmin = sessionUser.profileType === "admin";
  if (!isAdmin && Number(id) !== sessionUser.id) redirect("/tickets");

  let user: AppUser;
  try { user = await serverApi<AppUser>(`/user/${encodeURIComponent(id)}`); }
  catch (error) {
    if (error && typeof error === "object" && "status" in error && (error as { status: number }).status === 404) notFound();
    return <ErrorMessage message={getApiErrorMessage(error)} />;
  }

  return (
    <section className="detail-card">
      <Link href={isAdmin ? "/users" : "/tickets"} className="back-link">← Voltar</Link>
      <p className="eyebrow">Usuário #{user.id}</p><h1>{user.name}</h1>
      <dl className="detail-list">
        <div><dt>Nome</dt><dd>{user.name}</dd></div>
        <div><dt>E-mail</dt><dd>{user.email}</dd></div>
        {isAdmin && <div><dt>Perfil</dt><dd>{user.role}</dd></div>}
        {isAdmin && <div><dt>Status</dt><dd>{user.is_active ? "Ativo" : "Inativo"}</dd></div>}
      </dl>
      <EditRecordForm kind="user" record={user} isAdmin={isAdmin} currentUserId={sessionUser.id} />
    </section>
  );
}
