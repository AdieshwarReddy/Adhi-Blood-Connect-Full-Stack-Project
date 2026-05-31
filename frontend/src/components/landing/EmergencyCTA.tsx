import { Siren, ArrowRight } from "lucide-react";
import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

export function EmergencyCTA() {
  return (
    <section className="container mx-auto px-4 py-12">
      <div className="overflow-hidden rounded-3xl border bg-primary-gradient p-8 text-primary-foreground shadow-elevated md:p-12">
        <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div className="flex items-start gap-4">
            <div className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-white/15 backdrop-blur animate-pulse-ring">
              <Siren className="h-6 w-6" />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.2em] opacity-80">Emergency</p>
              <h3 className="mt-1 text-2xl font-bold md:text-3xl">Need blood urgently?</h3>
              <p className="mt-1 max-w-md text-sm opacity-90">
                Post an emergency request and notify thousands of nearby verified donors instantly.
              </p>
            </div>
          </div>
          <Link to="/requests">
            <Button size="lg" variant="secondary" className="gap-2 bg-white text-primary hover:bg-white/90">
              Post Emergency Request <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
