import { MapPin, Navigation } from "lucide-react";
import { Card } from "@/components/ui/card";

export function MapPlaceholder() {
  const pins = [
    { top: "30%", left: "25%", label: "O+" },
    { top: "55%", left: "60%", label: "A-" },
    { top: "20%", left: "70%", label: "B+" },
    { top: "70%", left: "35%", label: "AB+" },
    { top: "45%", left: "45%", label: "O-" },
  ];
  return (
    <Card className="relative h-72 overflow-hidden p-0">
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            "linear-gradient(var(--color-border) 1px, transparent 1px), linear-gradient(90deg, var(--color-border) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          opacity: 0.4,
        }}
      />
      <div className="absolute inset-0 bg-hero-gradient" />
      {pins.map((p, i) => (
        <div key={i} className="absolute -translate-x-1/2 -translate-y-1/2" style={{ top: p.top, left: p.left }}>
          <div className="grid h-9 w-9 place-items-center rounded-full bg-primary-gradient text-[10px] font-bold text-primary-foreground shadow-elevated animate-pulse-ring">
            {p.label}
          </div>
        </div>
      ))}
      <div className="absolute bottom-4 left-4 flex items-center gap-2 rounded-lg border bg-card/90 px-3 py-2 text-xs backdrop-blur">
        <MapPin className="h-3 w-3 text-primary" /> 5 donors nearby
      </div>
      <div className="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-lg border bg-card/90 backdrop-blur">
        <Navigation className="h-4 w-4 text-primary" />
      </div>
    </Card>
  );
}
