import { createFileRoute } from "@tanstack/react-router";
import { AppLayout } from "@/layouts/AppLayout";
import { Hero } from "@/components/landing/Hero";
import { EmergencyCTA } from "@/components/landing/EmergencyCTA";
import { Stats } from "@/components/landing/Stats";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Testimonials } from "@/components/landing/Testimonials";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Adhi Bloodconnect — Intelligent Blood Donation" },
      { name: "description", content: "AI-powered blood donation platform connecting donors, patients, and hospitals in real time." },
      { property: "og:title", content: "Adhi Bloodconnect" },
      { property: "og:description", content: "Connecting lives through intelligent blood donation." },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <AppLayout>
      <Hero />
      <Stats />
      <EmergencyCTA />
      <HowItWorks />
      <Testimonials />
    </AppLayout>
  );
}
