import { createFileRoute, useRouter, Link } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Logo } from "@/components/Logo";
import { RoleSelector } from "@/components/RoleSelector";
import { GoogleButton } from "@/components/GoogleButton";
import { useAuth, type Role } from "@/context/AuthContext";
import { BLOOD_GROUPS } from "@/lib/dummy";

export const Route = createFileRoute("/signup")({
  head: () => ({ meta: [{ title: "Sign up · Adhi Bloodconnect" }] }),
  component: SignupPage,
});

function SignupPage() {
  const router = useRouter();
  const { signup, loginWithGoogle } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("donor");
  const [bloodGroup, setBloodGroup] = useState("O+");
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password) return toast.error("Please fill all fields");
    setLoading(true);
    try {
      await signup(name, email, password, role, bloodGroup);
      toast.success("Account created!");
      router.navigate({ to: "/dashboard" });
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-hero-gradient">
      <div className="container mx-auto flex min-h-screen items-center justify-center px-4 py-10">
        <Card className="w-full max-w-md p-8 shadow-elevated">
          <div className="flex justify-center"><Logo size="lg" /></div>
          <h1 className="mt-6 text-center text-2xl font-bold">Create your account</h1>
          <p className="mt-1 text-center text-sm text-muted-foreground">Join thousands saving lives every day.</p>

          <div className="mt-6">
            <Label className="mb-2 block text-xs uppercase tracking-widest text-muted-foreground">I am a</Label>
            <RoleSelector value={role} onChange={setRole} />
          </div>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div>
              <Label htmlFor="name">Full name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
            </div>
            {role === "donor" && (
              <div>
                <Label>Blood group</Label>
                <Select value={bloodGroup} onValueChange={setBloodGroup}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {BLOOD_GROUPS.map((g) => <SelectItem key={g} value={g}>{g}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            )}
            <Button type="submit" className="w-full bg-primary-gradient" disabled={loading}>
              {loading ? "Creating..." : "Create account"}
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
            Already a member? <Link to="/login" className="font-semibold text-primary hover:underline">Sign in</Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
