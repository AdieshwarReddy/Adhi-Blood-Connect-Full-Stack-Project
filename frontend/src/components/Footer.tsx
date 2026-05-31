import { Link } from "@tanstack/react-router";
import { Logo } from "./Logo";
import { Facebook, Instagram, Twitter, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t bg-muted/30">
      <div className="container mx-auto grid gap-8 px-4 py-12 md:grid-cols-4">
        <div className="md:col-span-2">
          <Logo />
          <p className="mt-4 max-w-sm text-sm text-muted-foreground">
            Connecting Lives Through Intelligent Blood Donation. Powered by AI to match donors with patients in seconds.
          </p>
          <div className="mt-4 flex gap-3">
            {[Facebook, Instagram, Twitter].map((Icon, i) => (
              <a key={i} href="#" className="grid h-9 w-9 place-items-center rounded-full border bg-card text-muted-foreground hover:border-primary hover:text-primary">
                <Icon className="h-4 w-4" />
              </a>
            ))}
          </div>
        </div>
        <div>
          <h4 className="mb-3 text-sm font-semibold">Platform</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link to="/donors" className="hover:text-primary">Find Donors</Link></li>
            <li><Link to="/requests" className="hover:text-primary">Emergency</Link></li>
            <li><Link to="/dashboard" className="hover:text-primary">Dashboard</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="mb-3 text-sm font-semibold">Company</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><a href="#" className="hover:text-primary">About</a></li>
            <li><a href="#" className="hover:text-primary">Privacy</a></li>
            <li><a href="#" className="hover:text-primary">Contact</a></li>
          </ul>
        </div>
      </div>
      <div className="border-t">
        <div className="container mx-auto flex flex-col items-center justify-between gap-2 px-4 py-4 text-xs text-muted-foreground md:flex-row">
          <p>© 2026 Adhi Bloodconnect. All rights reserved.</p>
          <p className="flex items-center gap-1">Made with <Heart className="h-3 w-3 fill-primary text-primary" /> to save lives</p>
        </div>
      </div>
    </footer>
  );
}
