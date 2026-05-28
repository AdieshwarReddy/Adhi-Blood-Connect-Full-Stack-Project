import { Heart, Users, Building2, Activity } from "lucide-react";

const stats = [
  { icon: Users, value: "12,847", label: "Active Donors" },
  { icon: Heart, value: "38,421", label: "Lives Saved" },
  { icon: Building2, value: "256", label: "Hospitals" },
  { icon: Activity, value: "184", label: "Live Requests" },
];

export function Stats() {
  return (
    <section className="container mx-auto px-4 py-16">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="rounded-2xl border bg-card p-6 shadow-soft transition hover:-translate-y-1 hover:shadow-elevated">
            <div className="grid h-11 w-11 place-items-center rounded-xl bg-accent text-primary">
              <s.icon className="h-5 w-5" />
            </div>
            <p className="mt-4 text-3xl font-bold tracking-tight">{s.value}</p>
            <p className="text-sm text-muted-foreground">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
