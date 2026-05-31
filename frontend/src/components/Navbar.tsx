import { Link, useRouter } from "@tanstack/react-router";
import { Menu, LogOut, User as UserIcon } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Logo } from "./Logo";
import { ThemeToggle } from "./ThemeToggle";
import { NotificationBell } from "./NotificationBell";
import { useAuth } from "@/context/AuthContext";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/donors", label: "Find Donors" },
  { to: "/requests", label: "Emergency" },
  { to: "/dashboard", label: "Dashboard" },
];

export function Navbar() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center">
          <Logo />
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {navLinks.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className="rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              activeProps={{ className: "rounded-lg px-3 py-2 text-sm font-semibold text-primary bg-accent" }}
            >
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-1">
          {user && <NotificationBell />}
          <ThemeToggle />
          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full bg-primary-gradient text-primary-foreground">
                  <UserIcon className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>
                  <div className="flex flex-col">
                    <span className="font-semibold">{user.name}</span>
                    <span className="text-xs font-normal text-muted-foreground">{user.email}</span>
                    <span className="mt-1 text-[10px] uppercase tracking-widest text-primary">{user.role}</span>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => router.navigate({ to: "/dashboard" })}>
                  Dashboard
                </DropdownMenuItem>
                {user.role === "admin" && (
                  <DropdownMenuItem onClick={() => router.navigate({ to: "/admin" })}>
                    Admin
                  </DropdownMenuItem>
                )}
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => { logout(); router.navigate({ to: "/" }); }}>
                  <LogOut className="mr-2 h-4 w-4" /> Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="hidden gap-2 md:flex">
              <Button variant="ghost" onClick={() => router.navigate({ to: "/login" })}>Login</Button>
              <Button onClick={() => router.navigate({ to: "/signup" })} className="bg-primary-gradient">
                Get Started
              </Button>
            </div>
          )}

          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <div className="mt-8 flex flex-col gap-1">
                {navLinks.map((l) => (
                  <Link
                    key={l.to}
                    to={l.to}
                    onClick={() => setOpen(false)}
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-muted"
                  >
                    {l.label}
                  </Link>
                ))}
                {!user && (
                  <div className="mt-4 flex flex-col gap-2">
                    <Button variant="outline" onClick={() => { setOpen(false); router.navigate({ to: "/login" }); }}>Login</Button>
                    <Button className="bg-primary-gradient" onClick={() => { setOpen(false); router.navigate({ to: "/signup" }); }}>
                      Get Started
                    </Button>
                  </div>
                )}
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
