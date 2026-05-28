import { cn } from "@/lib/utils";

export function BloodBadge({ group, size = "md" }: { group: string; size?: "sm" | "md" | "lg" }) {
  const sizes = {
    sm: "h-8 w-8 text-xs",
    md: "h-12 w-12 text-sm",
    lg: "h-16 w-16 text-lg",
  } as const;
  return (
    <div
      className={cn(
        "grid place-items-center rounded-full bg-primary-gradient font-bold text-primary-foreground shadow-soft ring-2 ring-background",
        sizes[size],
      )}
    >
      {group}
    </div>
  );
}
