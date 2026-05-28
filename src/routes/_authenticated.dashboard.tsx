import { createFileRoute } from "@tanstack/react-router";
import { Calendar, Bell, Activity, Heart, Phone } from "lucide-react";
import { toast } from "sonner";
import { AppLayout } from "@/layouts/AppLayout";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BloodBadge } from "@/components/BloodBadge";
import { MapPlaceholder } from "@/components/MapPlaceholder";
import { useAuth } from "@/context/AuthContext";
import { dummyRequests, dummyNotifications } from "@/lib/dummy";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/_authenticated/dashboard")({
  head: () => ({ meta: [{ title: "Dashboard · Adhi Bloodconnect" }] }),
  component: Dashboard,
});

const history = [
  { date: "2025-02-12", hospital: "Apollo Hospital", units: 1, status: "Completed" },
  { date: "2024-11-08", hospital: "Fortis", units: 1, status: "Completed" },
  { date: "2024-08-15", hospital: "Manipal", units: 1, status: "Completed" },
];

function Dashboard() {
  const { user, updateUser } = useAuth();

  return (
    <AppLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Donor dashboard</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Hello, {user?.name?.split(" ")[0] || "Donor"} 👋</h1>
          <p className="mt-1 text-muted-foreground">Your impact, requests near you, and donation history — all in one place.</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Profile card */}
          <Card className="p-6 lg:col-span-1">
            <div className="flex items-center gap-4">
              <BloodBadge group={user?.bloodGroup || "O+"} size="lg" />
              <div>
                <p className="font-semibold">{user?.name}</p>
                <p className="text-xs text-muted-foreground">{user?.email}</p>
                <Badge className="mt-1 bg-success/15 text-success hover:bg-success/15">Verified donor</Badge>
              </div>
            </div>

            <div className="mt-6 space-y-4 border-t pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Availability</p>
                  <p className="text-xs text-muted-foreground">Toggle to receive emergency alerts</p>
                </div>
                <Switch
                  checked={user?.available ?? true}
                  onCheckedChange={(v) => {
                    updateUser({ available: v });
                    toast.success(v ? "You're now available to donate" : "Availability paused");
                  }}
                />
              </div>
              <div className="flex items-center gap-3 rounded-xl bg-muted/50 p-3 text-sm">
                <Calendar className="h-4 w-4 text-primary" />
                <div>
                  <p className="font-medium">Last donation</p>
                  <p className="text-xs text-muted-foreground">Feb 12, 2025 · Apollo Hospital</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="rounded-xl border p-3">
                  <p className="text-xl font-bold text-primary">14</p>
                  <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Donations</p>
                </div>
                <div className="rounded-xl border p-3">
                  <p className="text-xl font-bold text-primary">42</p>
                  <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Lives saved</p>
                </div>
                <div className="rounded-xl border p-3">
                  <p className="text-xl font-bold text-primary">96%</p>
                  <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Reliability</p>
                </div>
              </div>
            </div>
          </Card>

          {/* Emergency requests */}
          <Card className="p-6 lg:col-span-2">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="flex items-center gap-2 text-lg font-semibold">
                  <Activity className="h-4 w-4 text-primary" /> Nearby emergency requests
                </h2>
                <p className="text-xs text-muted-foreground">Live alerts from hospitals within 10 km</p>
              </div>
            </div>
            <div className="mt-4 space-y-3">
              {dummyRequests.slice(0, 3).map((r) => (
                <div key={r.id} className="flex items-center justify-between rounded-xl border bg-background p-4">
                  <div className="flex items-center gap-3">
                    <BloodBadge group={r.bloodGroup} size="sm" />
                    <div>
                      <p className="text-sm font-medium">{r.patient} · {r.units} units</p>
                      <p className="text-xs text-muted-foreground">{r.hospital} · {r.createdAt}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={cn(
                        "rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest",
                        r.urgency === "Critical" && "bg-primary/15 text-primary animate-pulse-ring",
                        r.urgency === "High" && "bg-warning/20 text-warning-foreground",
                        r.urgency === "Moderate" && "bg-muted text-muted-foreground",
                      )}
                    >
                      {r.urgency}
                    </span>
                    <Button size="sm" className="gap-1.5 bg-primary-gradient">
                      <Phone className="h-3 w-3" /> Respond
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Map */}
          <div className="lg:col-span-2">
            <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold">
              <Heart className="h-4 w-4 text-primary" /> Donors near you
            </h2>
            <MapPlaceholder />
          </div>

          {/* Notifications */}
          <Card className="p-6">
            <h2 className="flex items-center gap-2 text-lg font-semibold">
              <Bell className="h-4 w-4 text-primary" /> Notifications
            </h2>
            <div className="mt-4 space-y-3">
              {dummyNotifications.map((n) => (
                <div key={n.id} className="rounded-xl border p-3">
                  <p className="text-sm font-medium">{n.title}</p>
                  <p className="text-xs text-muted-foreground">{n.body}</p>
                  <p className="mt-1 text-[10px] uppercase tracking-widest text-muted-foreground">{n.time} ago</p>
                </div>
              ))}
            </div>
          </Card>

          {/* History */}
          <Card className="p-6 lg:col-span-3">
            <h2 className="text-lg font-semibold">Donation history</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-xs uppercase tracking-widest text-muted-foreground">
                    <th className="py-3 pr-4">Date</th>
                    <th className="py-3 pr-4">Hospital</th>
                    <th className="py-3 pr-4">Units</th>
                    <th className="py-3 pr-4">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h) => (
                    <tr key={h.date} className="border-b last:border-0">
                      <td className="py-3 pr-4">{new Date(h.date).toLocaleDateString()}</td>
                      <td className="py-3 pr-4">{h.hospital}</td>
                      <td className="py-3 pr-4">{h.units}</td>
                      <td className="py-3 pr-4">
                        <Badge className="bg-success/15 text-success hover:bg-success/15">{h.status}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
