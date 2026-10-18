
"use client";

export default function OpenCreateButton({ kind, children }: { kind: "ticket" | "customer" | "user"; children: React.ReactNode }) {
  return <button className="button primary" onClick={() => window.dispatchEvent(new Event(`open-create-${kind}`))}>{children}</button>;
}
