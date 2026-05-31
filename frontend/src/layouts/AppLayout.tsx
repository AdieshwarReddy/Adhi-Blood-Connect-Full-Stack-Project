import type { ReactNode } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Chatbot } from "@/components/Chatbot";

export function AppLayout({ children, footer = true }: { children: ReactNode; footer?: boolean }) {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">{children}</main>
      {footer && <Footer />}
      <Chatbot />
    </div>
  );
}
