import { createFileRoute, useRouter, Link } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Logo } from "@/components/Logo";
import { RoleSelector } from "@/components/RoleSelector";
import { GoogleButton } from "@/components/GoogleButton";
import { useAuth, type Role } from "@/context/AuthContext";

export const Route = createFileRoute("/login")({
  head: () => ({ meta: [{ title: "Login · Adhi Bloodconnect" }] }),
  component: LoginPage,
});

function LoginPage() {
  const router = useRouter();
  const { login, loginWithGoogle } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("donor");
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return toast.error("Please fill all fields");
    setLoading(true);
    try {
      await login(email, password, role);
      toast.success("Welcome back!");
      router.navigate({ to: role === "admin" ? "/admin" : "/dashboard" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-hero-gradient">
      <div className="container mx-auto flex min-h-screen items-center justify-center px-4 py-10">
        <Card className="w-full max-w-md p-8 shadow-elevated">
          <div className="flex justify-center"><Logo size="lg" /></div>
          <h1 className="mt-6 text-center text-2xl font-bold">Welcome back</h1>
          <p className="mt-1 text-center text-sm text-muted-foreground">Sign in to continue saving lives.</p>

          <div className="mt-6">
            <Label className="mb-2 block text-xs uppercase tracking-widest text-muted-foreground">I am a</Label>
            <RoleSelector value={role} onChange={setRole} />
          </div>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
            </div>
            <Button type="submit" className="w-full bg-primary-gradient" disabled={loading}>
              {loading ? "Signing in..." : "Sign in"}
            </Button>
          </form>

          <div className="my-6 flex items-center gap-3 text-xs text-muted-foreground">
            <div className="h-px flex-1 bg-border" /> OR <div className="h-px flex-1 bg-border" />
          </div>

          <GoogleButton onClick={async () => {
            await loginWithGoogle(role);
            toast.success("Signed in with Google");
            router.navigate({ to: "/dashboard" });
          }} />

          <p className="mt-6 text-center text-sm text-muted-foreground">
            New here? <Link to="/signup" className="font-semibold text-primary hover:underline">Create account</Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
