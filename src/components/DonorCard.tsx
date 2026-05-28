import { MapPin, Phone, Star } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BloodBadge } from "./BloodBadge";
import type { Donor } from "@/lib/dummy";
import { cn } from "@/lib/utils";

export function DonorCard({ donor }: { donor: Donor }) {
  return (
    <Card className="group flex flex-col gap-4 p-5 transition-all hover:-translate-y-1 hover:shadow-elevated">
      <div className="flex items-start gap-3">
        <BloodBadge group={donor.bloodGroup} />
        <div className="min-w-0 flex-1">
          <div className="flex items-center justify-between gap-2">
            <p className="truncate font-semibold">{donor.name}</p>
            <span
              className={cn(
                "rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider",
                donor.available
                  ? "bg-success/15 text-success"
                  : "bg-muted text-muted-foreground",
              )}
            >
              {donor.available ? "Available" : "Resting"}
            </span>
          </div>
          <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
            <MapPin className="h-3 w-3" /> {donor.city} · {donor.distanceKm} km away
          </p>
          <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
            <Star className="h-3 w-3 fill-warning text-warning" /> {donor.reliability}% reliability
          </p>
        </div>
      </div>
      <div className="flex items-center justify-between border-t pt-3 text-xs text-muted-foreground">
        <span>Last donated: {new Date(donor.lastDonation).toLocaleDateString()}</span>
        <Button size="sm" variant="outline" className="h-7 gap-1.5">
          <Phone className="h-3 w-3" /> Contact
        </Button>
      </div>
    </Card>
  );
}
