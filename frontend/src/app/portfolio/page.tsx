"use client";

import Link from "next/link";
import Logo from "@/components/Logo";
import PortfolioCard from "@/components/PortfolioCard";
import AlertsCard from "@/components/AlertsCard";

export default function PortfolioPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      <div className="container mx-auto px-4 py-12">
        <header className="flex flex-col items-center mb-8">
          <Link href="/">
            <Logo size="md" />
          </Link>
          <nav className="mt-4 flex gap-4">
            <Link
              href="/"
              className="text-slate-400 hover:text-slate-200 transition-colors"
            >
              Screener
            </Link>
            <span className="text-primary-400 font-medium">Portfolio</span>
          </nav>
        </header>

        <section className="max-w-6xl mx-auto space-y-8">
          <div>
            <h2 className="text-2xl font-semibold mb-6 text-primary-300">
              Portfolio Tracker
            </h2>
            <p className="text-slate-400 mb-8">
              Track your long-term investments and monitor performance over time.
            </p>
            <PortfolioCard />
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-6 text-primary-300">
              Price Alerts
            </h2>
            <p className="text-slate-400 mb-8">
              Set up alerts to be notified when stocks reach your target prices.
            </p>
            <AlertsCard />
          </div>
        </section>
      </div>
    </main>
  );
}
