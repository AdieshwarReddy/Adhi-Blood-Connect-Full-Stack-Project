import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Search } from "lucide-react";
import { AppLayout } from "@/layouts/AppLayout";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DonorCard } from "@/components/DonorCard";
import { MapPlaceholder } from "@/components/MapPlaceholder";
import { BLOOD_GROUPS, dummyDonors } from "@/lib/dummy";

export const Route = createFileRoute("/_authenticated/donors")({
  head: () => ({ meta: [{ title: "Find Donors · Adhi" }] }),
  component: DonorsPage,
});

function DonorsPage() {
  const [bloodGroup, setBloodGroup] = useState<string>("any");
  const [city, setCity] = useState("");
  const [maxDistance, setMaxDistance] = useState([10]);
  const [onlyAvailable, setOnlyAvailable] = useState(false);

  const cities = useMemo(() => Array.from(new Set(dummyDonors.map((d) => d.city))), []);

  const filtered = dummyDonors.filter((d) =>
    (bloodGroup === "any" || d.bloodGroup === bloodGroup) &&
    (!city || d.city === city) &&
    d.distanceKm <= maxDistance[0] &&
    (!onlyAvailable || d.available)
  );

  return (
    <AppLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Smart donor search</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Find a donor near you</h1>
          <p className="mt-1 text-muted-foreground">Filter by blood group, city, distance, and availability.</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
          <Card className="h-fit p-5">
            <p className="flex items-center gap-2 text-sm font-semibold"><Search className="h-4 w-4 text-primary" /> Filters</p>
            <div className="mt-4 space-y-5">
              <div>
                <Label className="mb-1.5 block text-xs">Blood group</Label>
                <Select value={bloodGroup} onValueChange={setBloodGroup}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="any">Any</SelectItem>
                    {BLOOD_GROUPS.map((g) => <SelectItem key={g} value={g}>{g}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="mb-1.5 block text-xs">City</Label>
                <Select value={city || "all"} onValueChange={(v) => setCity(v === "all" ? "" : v)}>
                  <SelectTrigger><SelectValue placeholder="Any city" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All cities</SelectItem>
                    {cities.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="mb-1.5 block text-xs">Max distance: {maxDistance[0]} km</Label>
                <Slider value={maxDistance} onValueChange={setMaxDistance} min={1} max={20} step={1} />
              </div>
              <div className="flex items-center justify-between rounded-lg border p-3">
                <div>
                  <p className="text-sm font-medium">Available only</p>
                  <p className="text-xs text-muted-foreground">Show ready-to-donate</p>
                </div>
                <Switch checked={onlyAvailable} onCheckedChange={setOnlyAvailable} />
              </div>
            </div>
            <div className="mt-5">
              <Label className="mb-1.5 block text-xs">Name search</Label>
              <Input placeholder="Search by name..." />
            </div>
          </Card>

          <div className="space-y-6">
            <MapPlaceholder />
            <div>
              <p className="mb-4 text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">{filtered.length}</span> donors found
              </p>
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {filtered.map((d) => <DonorCard key={d.id} donor={d} />)}
                {filtered.length === 0 && (
                  <Card className="col-span-full p-8 text-center text-muted-foreground">
                    No donors match these filters. Try widening your search.
                  </Card>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
