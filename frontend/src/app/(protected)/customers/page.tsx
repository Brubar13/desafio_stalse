
import { requireUser } from "@/lib/session";
import { serverApi } from "@/lib/server-api";
import type { Customer } from "@/lib/types";
import { CustomerCard } from "@/components/RecordCard";
import CreateModal from "@/components/CreateModal";
import OpenCreateButton from "@/components/OpenCreateButton";
import ErrorMessage from "@/components/ErrorMessage";
import { getApiErrorMessage } from "@/lib/api-error";

export default async function CustomersPage() {
  const user = await requireUser();
  let customers: Customer[] = [];
  let error = "";
  try { customers = await serverApi<Customer[]>("/customer"); }
  catch (err) { error = getApiErrorMessage(err); }

  return (
    <>
      <div className="page-heading"><div><h1>Customers</h1><p className="muted">Clientes cadastrados no sistema.</p></div>
        {user.profileType === "admin" && <OpenCreateButton kind="customer">Criar novo customer</OpenCreateButton>}
      </div>
      {error && <ErrorMessage message={error} />}
      {!error && customers.length === 0 && <div className="empty-state"><h2>Nenhum customer cadastrado</h2></div>}
      <section className="card-grid">{customers.map((customer) => <CustomerCard key={customer.id} customer={customer} />)}</section>
      {user.profileType === "admin" && <CreateModal kind="customer" />}
    </>
  );
}
