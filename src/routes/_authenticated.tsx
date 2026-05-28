import { createFileRoute, Outlet, useRouter } from "@tanstack/react-router";
import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";

export const Route = createFileRoute("/_authenticated")({
  component: AuthGuard,
});

function AuthGuard() {
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Defer the check to allow AuthProvider to hydrate from localStorage
    const id = setTimeout(() => {
      const raw = typeof window !== "undefined" ? localStorage.getItem("adhi_auth_user") : null;
      if (!raw && !user) router.navigate({ to: "/login" });
    }, 50);
    return () => clearTimeout(id);
  }, [user, router]);

  return <Outlet />;
}
