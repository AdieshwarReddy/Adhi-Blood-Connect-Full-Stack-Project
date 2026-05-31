import { Droplet } from "lucide-react";

export function Logo({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  const sizes = { sm: "h-7 w-7", md: "h-9 w-9", lg: "h-12 w-12" } as const;
  const text = { sm: "text-base", md: "text-lg", lg: "text-2xl" } as const;
  return (
    <div className="flex items-center gap-2.5">
      <div className={`${sizes[size]} grid place-items-center rounded-xl bg-primary-gradient shadow-soft`}>
        <Droplet className="h-1/2 w-1/2 fill-primary-foreground text-primary-foreground" />
      </div>
      <div className="flex flex-col leading-none">
        <span className={`${text[size]} font-bold tracking-tight text-foreground`}>Adhi Blood<span className="text-primary">connect</span></span>
        <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Save lives, smarter</span>
      </div>
    </div>
  );
}
