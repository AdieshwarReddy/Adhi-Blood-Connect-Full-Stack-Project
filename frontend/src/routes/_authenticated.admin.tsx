import { createFileRoute } from "@tanstack/react-router";
import { Users, Activity, Heart, Building2 } from "lucide-react";
import { AppLayout } from "@/layouts/AppLayout";
import { Card } from "@/components/ui/card";
import { adminStats } from "@/lib/dummy";

export const Route = createFileRoute("/_authenticated/admin")({
  head: () => ({ meta: [{ title: "Admin · Adhi" }] }),
  component: AdminPage,
});

const tiles = [
  { icon: Users, label: "Total donors", value: adminStats.totalDonors.toLocaleString(), delta: "+312 this week" },
  { icon: Activity, label: "Active requests", value: adminStats.activeRequests, delta: "24 critical" },
  { icon: Heart, label: "Lives saved", value: adminStats.livesSaved.toLocaleString(), delta: "All-time" },
  { icon: Building2, label: "Partner hospitals", value: adminStats.hospitalsPartner, delta: "+8 this month" },
];

function AdminPage() {
  const max = Math.max(...adminStats.bloodGroupDistribution.map((b) => b.value));
  return (
    <AppLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Admin overview</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Platform analytics</h1>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {tiles.map((t) => (
            <Card key={t.label} className="p-5">
              <div className="flex items-center justify-between">
                <div className="grid h-10 w-10 place-items-center rounded-xl bg-accent text-primary">
                  <t.icon className="h-5 w-5" />
                </div>
                <span className="text-[10px] uppercase tracking-widest text-muted-foreground">{t.delta}</span>
              </div>
              <p className="mt-4 text-3xl font-bold tracking-tight">{t.value}</p>
              <p className="text-sm text-muted-foreground">{t.label}</p>
            </Card>
          ))}
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <Card className="p-6 lg:col-span-2">
            <h2 className="text-lg font-semibold">Blood group distribution</h2>
            <p className="text-xs text-muted-foreground">% of donors by blood group</p>
            <div className="mt-6 space-y-3">
              {adminStats.bloodGroupDistribution.map((b) => (
                <div key={b.group} className="flex items-center gap-3">
                  <span className="w-10 text-xs font-bold">{b.group}</span>
                  <div className="h-3 flex-1 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full rounded-full bg-primary-gradient transition-all"
                      style={{ width: `${(b.value / max) * 100}%` }}
                    />
                  </div>
                  <span className="w-12 text-right text-xs text-muted-foreground">{b.value}%</span>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="text-lg font-semibold">Recent activity</h2>
            <div className="mt-4 space-y-3">
              {adminStats.recentActivities.map((a) => (
                <div key={a.id} className="flex gap-3 border-b pb-3 last:border-0">
                  <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-primary" />
                  <div>
                    <p className="text-sm">{a.text}</p>
                    <p className="text-[10px] uppercase tracking-widest text-muted-foreground">{a.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
