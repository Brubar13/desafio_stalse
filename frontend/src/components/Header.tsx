
"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/components/AuthProvider";

export default function Header() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const isAdmin = user?.profileType === "admin";

  return (
    <header className="site-header">
      <Link className="brand" href="/tickets" aria-label="Página de tickets">TicketDesk</Link>
      <div className="header-actions">
        <span className="header-user">{user?.nome ?? user?.email ?? ""}</span>
        <button className="icon-button" aria-label="Abrir menu" aria-expanded={open}
          onClick={() => setOpen((value) => !value)}>☰</button>
        {open && (
          <nav className="header-menu">
            <Link href="/tickets" onClick={() => setOpen(false)}>Tickets</Link>
            <Link href="/customers" onClick={() => setOpen(false)}>Customers</Link>
            {isAdmin && <Link href="/users" onClick={() => setOpen(false)}>Usuários</Link>}
            <Link href={`/users/${user?.id}`} onClick={() => setOpen(false)}>Alterar meus dados</Link>
            <button onClick={() => void logout()}>Sair</button>
          </nav>
        )}
      </div>
    </header>
  );
}
