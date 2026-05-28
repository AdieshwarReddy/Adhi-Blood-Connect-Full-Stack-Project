import { Heart, User, Building2 } from "lucide-react";
import type { Role } from "@/context/AuthContext";
import { cn } from "@/lib/utils";

const roles: { value: Role; label: string; icon: typeof Heart }[] = [
  { value: "donor", label: "Donor", icon: Heart },
  { value: "patient", label: "Patient", icon: User },
  { value: "hospital", label: "Hospital", icon: Building2 },
];

export function RoleSelector({ value, onChange }: { value: Role; onChange: (r: Role) => void }) {
  return (
    <div className="grid grid-cols-3 gap-2">
      {roles.map((r) => {
        const active = value === r.value;
        return (
          <button
            type="button"
            key={r.value}
            onClick={() => onChange(r.value)}
            className={cn(
              "flex flex-col items-center gap-1.5 rounded-xl border p-3 text-xs font-medium transition",
              active
                ? "border-primary bg-accent text-primary shadow-soft"
                : "border-border bg-card text-muted-foreground hover:border-primary/40 hover:text-foreground",
            )}
          >
            <r.icon className={cn("h-5 w-5", active && "text-primary")} />
            {r.label}
          </button>
        );
      })}
    </div>
  );
}
