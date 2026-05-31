import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Siren, Plus, Phone, MapPin, Navigation } from "lucide-react";
import { toast } from "sonner";
import { AppLayout } from "@/layouts/AppLayout";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { BloodBadge } from "@/components/BloodBadge";
import { BLOOD_GROUPS, dummyRequests, type EmergencyRequest } from "@/lib/dummy";
import { cn } from "@/lib/utils";
import { api } from "@/services/api";

async function handleHelp(request: EmergencyRequest) {
  // 1. Open Google Maps driving directions to the hospital
  const destination = encodeURIComponent(`${request.hospital}, ${request.city ?? "India"}`);
  const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destination}&travelmode=driving`;
  window.open(mapsUrl, "_blank");

  // 2. Notify backend that this donor is responding
  try {
    await api.post("/notifications/respond", {
      request_id: request.id,
      patient_name: request.patient,
      hospital: request.hospital,
    });
    toast.success(`✅ Notified ${request.patient}'s family — you're on the way! Thank you for saving a life 🩸`);
  } catch {
    toast.success(`🗺️ Google Maps opened for ${request.hospital}. Drive safe, lifesaver!`);
  }
}

export const Route = createFileRoute("/_authenticated/requests")({
  head: () => ({ meta: [{ title: "Emergency Requests · Adhi" }] }),
  component: RequestsPage,
});

function RequestsPage() {
  const [requests, setRequests] = useState<EmergencyRequest[]>(dummyRequests);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    patient: "", bloodGroup: "O+", units: 1, hospital: "",
    urgency: "High" as EmergencyRequest["urgency"], contact: "", city: "",
  });

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.patient || !form.hospital || !form.contact) return toast.error("Please fill required fields");
    const newReq: EmergencyRequest = {
      id: crypto.randomUUID(),
      ...form,
      bloodGroup: form.bloodGroup as EmergencyRequest["bloodGroup"],
      createdAt: "just now",
    };
    setRequests((r) => [newReq, ...r]);
    toast.success("Emergency request posted — notifying nearby donors!");
    setOpen(false);
    setForm({ patient: "", bloodGroup: "O+", units: 1, hospital: "", urgency: "High", contact: "", city: "" });
  };

  return (
    <AppLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Emergency module</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight">Active blood requests</h1>
            <p className="mt-1 text-muted-foreground">Real-time emergency requests broadcast to all matching donors.</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button size="lg" className="gap-2 bg-primary-gradient shadow-elevated">
                <Plus className="h-4 w-4" /> New emergency request
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-lg">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Siren className="h-5 w-5 text-primary" /> Post emergency request
                </DialogTitle>
              </DialogHeader>
              <form onSubmit={submit} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="col-span-2">
                    <Label>Patient name</Label>
                    <Input value={form.patient} onChange={(e) => setForm({ ...form, patient: e.target.value })} />
                  </div>
                  <div>
                    <Label>Blood group</Label>
                    <Select value={form.bloodGroup} onValueChange={(v) => setForm({ ...form, bloodGroup: v })}>
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>{BLOOD_GROUPS.map((g) => <SelectItem key={g} value={g}>{g}</SelectItem>)}</SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Units needed</Label>
                    <Input type="number" min={1} value={form.units} onChange={(e) => setForm({ ...form, units: +e.target.value })} />
                  </div>
                  <div className="col-span-2">
                    <Label>Hospital name</Label>
                    <Input value={form.hospital} onChange={(e) => setForm({ ...form, hospital: e.target.value })} />
                  </div>
                  <div>
                    <Label>Urgency</Label>
                    <Select value={form.urgency} onValueChange={(v) => setForm({ ...form, urgency: v as EmergencyRequest["urgency"] })}>
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Critical">Critical</SelectItem>
                        <SelectItem value="High">High</SelectItem>
                        <SelectItem value="Moderate">Moderate</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Contact number</Label>
                    <Input value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} />
                  </div>
                  <div className="col-span-2">
                    <Label>Location / City</Label>
                    <Input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
                  </div>
                </div>
                <Button type="submit" className="w-full bg-primary-gradient">Broadcast to donors</Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {requests.map((r) => (
            <Card key={r.id} className="p-5 transition hover:shadow-elevated">
              <div className="flex items-start justify-between gap-3">
                <div className="flex gap-3">
                  <BloodBadge group={r.bloodGroup} />
                  <div>
                    <p className="font-semibold">{r.patient}</p>
                    <p className="text-xs text-muted-foreground">{r.units} units needed</p>
                  </div>
                </div>
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
              </div>
              <div className="mt-4 space-y-1.5 border-t pt-3 text-sm text-muted-foreground">
                <p className="flex items-center gap-2"><MapPin className="h-3 w-3" /> {r.hospital}, {r.city}</p>
                <p className="flex items-center gap-2"><Phone className="h-3 w-3" /> {r.contact}</p>
                <p className="text-xs">Posted {r.createdAt}</p>
              </div>
              <Button
                className="mt-4 w-full bg-primary-gradient gap-2"
                onClick={() => handleHelp(r)}
              >
                <Navigation className="h-4 w-4" /> I can help — Get Directions
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
