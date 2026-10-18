
"use client";

import { useAuth } from "@/components/AuthProvider";

export default function LogoutButton() {
  const { logout } = useAuth();
  return <button className="button secondary" onClick={() => void logout()}>Sair</button>;
}
