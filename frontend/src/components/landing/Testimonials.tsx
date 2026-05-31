import { Quote } from "lucide-react";

const items = [
  { name: "Dr. Anjali Rao", role: "Apollo Hospital", text: "Adhi has cut our blood sourcing time from hours to minutes. It's life-saving infrastructure." },
  { name: "Rohan Mehta", role: "Donor · 14 donations", text: "I love the reminders and how easy it is to respond. Feels good knowing exactly who I'm helping." },
  { name: "Sunita Iyer", role: "Patient's family", text: "We got 3 donor matches within 8 minutes during a critical emergency. Forever grateful." },
];

export function Testimonials() {
  return (
    <section className="bg-muted/30 py-20">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Voices</p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight md:text-4xl">Stories from our community</h2>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {items.map((t) => (
            <div key={t.name} className="rounded-2xl border bg-card p-6 shadow-soft">
              <Quote className="h-7 w-7 text-primary/40" />
              <p className="mt-3 text-sm leading-relaxed text-foreground">{t.text}</p>
              <div className="mt-5 border-t pt-4">
                <p className="text-sm font-semibold">{t.name}</p>
                <p className="text-xs text-muted-foreground">{t.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
