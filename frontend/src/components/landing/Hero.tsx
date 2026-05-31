import { ArrowRight, Sparkles, Siren } from "lucide-react";
import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-hero-gradient">
      <div className="container mx-auto grid gap-12 px-4 py-20 md:grid-cols-2 md:py-28">
        <div className="flex flex-col justify-center">
          <div className="inline-flex w-fit items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-soft">
            <Sparkles className="h-3 w-3 text-primary" /> AI-powered matching · 12,000+ donors
          </div>
          <h1 className="mt-6 text-4xl font-bold tracking-tight md:text-6xl">
            Connecting lives through{" "}
            <span className="bg-primary-gradient bg-clip-text text-transparent">intelligent</span> blood donation.
          </h1>
          <p className="mt-5 max-w-lg text-base text-muted-foreground md:text-lg">
            Adhi Bloodconnect uses AI to match patients with verified donors nearby — in seconds, not hours.
            Every drop counts. Every match saves a life.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/signup">
              <Button size="lg" className="gap-2 bg-primary-gradient shadow-elevated">
                Become a Donor <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link to="/requests">
              <Button size="lg" variant="outline" className="gap-2">
                <Siren className="h-4 w-4 text-primary" /> Request Blood
              </Button>
            </Link>
          </div>
          <div className="mt-10 flex items-center gap-6 text-sm text-muted-foreground">
            <div>
              <p className="text-2xl font-bold text-foreground">12.8K+</p>
              <p>Verified donors</p>
            </div>
            <div className="h-10 w-px bg-border" />
            <div>
              <p className="text-2xl font-bold text-foreground">38K+</p>
              <p>Lives saved</p>
            </div>
            <div className="h-10 w-px bg-border" />
            <div>
              <p className="text-2xl font-bold text-foreground">256+</p>
              <p>Partner hospitals</p>
            </div>
          </div>
        </div>

        <div className="relative">
          <div className="absolute -inset-4 rounded-3xl bg-primary-gradient opacity-20 blur-3xl" />
          <div className="relative rounded-3xl border bg-card p-6 shadow-elevated">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-widest text-muted-foreground">Live request</p>
                <p className="mt-1 font-semibold">Apollo Hospital, Bangalore</p>
              </div>
              <span className="rounded-full bg-primary/10 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-primary animate-pulse-ring">
                Critical
              </span>
            </div>
            <div className="mt-6 grid grid-cols-3 gap-3">
              {["O+", "A-", "B+"].map((g) => (
                <div key={g} className="rounded-xl border bg-background p-3 text-center">
                  <p className="text-2xl font-bold text-primary">{g}</p>
                  <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Needed now</p>
                </div>
              ))}
            </div>
            <div className="mt-6 space-y-3">
              {[
                { name: "Arjun K.", dist: "2.4 km", g: "O+" },
                { name: "Priya S.", dist: "4.1 km", g: "A+" },
                { name: "Vikram S.", dist: "3.2 km", g: "O-" },
              ].map((d) => (
                <div key={d.name} className="flex items-center justify-between rounded-xl border bg-background p-3">
                  <div className="flex items-center gap-3">
                    <div className="grid h-9 w-9 place-items-center rounded-full bg-primary-gradient text-xs font-bold text-primary-foreground">
                      {d.g}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{d.name}</p>
                      <p className="text-xs text-muted-foreground">{d.dist} away</p>
                    </div>
                  </div>
                  <span className="h-2 w-2 rounded-full bg-success" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
