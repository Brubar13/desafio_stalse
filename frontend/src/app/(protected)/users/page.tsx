
import { requireAdmin } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import type { AppUser } from "@/lib/types";
import { UserCard } from "@/components/RecordCard";
import CreateModal from "@/components/CreateModal";
import OpenCreateButton from "@/components/OpenCreateButton";
import ErrorMessage from "@/components/ErrorMessage";
import { getApiErrorMessage } from "@/lib/api-error";

export default async function UsersPage() {
  await requireAdmin();
  let users: AppUser[] = [];
  let error = "";
  try { users = await serverApi<AppUser[]>("/user/all_users"); }
  catch (err) { error = getApiErrorMessage(err); }

  return (
    <>
      <div className="page-heading"><div><h1>Usuários</h1><p className="muted">Gerencie os usuários do sistema.</p></div>
        <OpenCreateButton kind="user">Novo usuário</OpenCreateButton>
      </div>
      {error && <ErrorMessage message={error} />}
      {!error && users.length === 0 && <div className="empty-state"><h2>Nenhum usuário encontrado</h2></div>}
      <section className="card-grid">{users.map((user) => <UserCard key={user.id} user={user} />)}</section>
      <CreateModal kind="user" />
    </>
  );
}
