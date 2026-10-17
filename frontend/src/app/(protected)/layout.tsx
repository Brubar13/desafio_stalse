
import Header from "@/components/Header";
import { requireUser } from "@/lib/session";

export default async function ProtectedLayout({ children }: { children: React.ReactNode }) {
  await requireUser();
  return <><Header /><main className="page-container">{children}</main></>;
}
