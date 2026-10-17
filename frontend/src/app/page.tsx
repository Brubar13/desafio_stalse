
import { Suspense } from "react";
import LoginForm from "@/components/LoginForm";
import { getSessionUser } from "@/lib/session";
import { redirect } from "next/navigation";

export default async function HomePage() {
  const user = await getSessionUser();
  if (user) redirect("/tickets");

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-brand-mark">T</div>
        <h1>TicketDesk</h1>
        <p className="muted">Entre para gerenciar seus tickets</p>
        <Suspense fallback={<p>Carregando...</p>}><LoginForm /></Suspense>
      </section>
    </main>
  );
}
