import { Bell } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { dummyNotifications } from "@/lib/dummy";
import { cn } from "@/lib/utils";

export function NotificationBell() {
  const [items] = useState(dummyNotifications);
  const unread = items.filter((n) => !n.read).length;

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-4 w-4" />
          {unread > 0 && (
            <span className="absolute right-1 top-1 grid h-4 min-w-4 place-items-center rounded-full bg-primary px-1 text-[10px] font-bold text-primary-foreground animate-pulse-ring">
              {unread}
            </span>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-80 p-0">
        <div className="border-b p-3">
          <p className="text-sm font-semibold">Notifications</p>
          <p className="text-xs text-muted-foreground">Live emergency alerts</p>
        </div>
        <div className="max-h-80 overflow-y-auto">
          {items.map((n) => (
            <div key={n.id} className="flex gap-3 border-b p-3 last:border-0 hover:bg-muted/50">
              <span
                className={cn(
                  "mt-1 h-2 w-2 shrink-0 rounded-full",
                  n.type === "emergency" && "bg-primary",
                  n.type === "info" && "bg-warning",
                  n.type === "success" && "bg-success",
                )}
              />
              <div className="flex-1">
                <p className="text-sm font-medium">{n.title}</p>
                <p className="text-xs text-muted-foreground">{n.body}</p>
                <p className="mt-1 text-[10px] uppercase tracking-wider text-muted-foreground">{n.time}</p>
              </div>
            </div>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}
