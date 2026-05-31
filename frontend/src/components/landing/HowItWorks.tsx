import { UserPlus, Search, HeartHandshake } from "lucide-react";

const steps = [
  { icon: UserPlus, title: "Register", desc: "Sign up as a donor, patient, or hospital in under 60 seconds." },
  { icon: Search, title: "AI Matches", desc: "Our AI finds the best donors by blood group, distance, and reliability." },
  { icon: HeartHandshake, title: "Save a Life", desc: "Connect, donate, and track your impact in real time." },
];

export function HowItWorks() {
  return (
    <section className="container mx-auto px-4 py-20">
      <div className="mx-auto max-w-2xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">How it works</p>
        <h2 className="mt-3 text-3xl font-bold tracking-tight md:text-4xl">Three simple steps to save lives</h2>
        <p className="mt-3 text-muted-foreground">From signup to saving lives — intelligent, fast, and trusted.</p>
      </div>
      <div className="mt-12 grid gap-6 md:grid-cols-3">
        {steps.map((s, i) => (
          <div key={s.title} className="relative rounded-2xl border bg-card p-6 shadow-soft">
            <div className="absolute -top-3 right-6 grid h-8 w-8 place-items-center rounded-full bg-primary-gradient text-sm font-bold text-primary-foreground">
              {i + 1}
            </div>
            <div className="grid h-12 w-12 place-items-center rounded-xl bg-accent text-primary">
              <s.icon className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-semibold">{s.title}</h3>
            <p className="mt-2 text-sm text-muted-foreground">{s.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
