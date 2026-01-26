"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Logo from "@/components/Logo";
import ScreenerForm from "@/components/ScreenerForm";
import StockTable from "@/components/StockTable";
import StockAnalysisCard from "@/components/StockAnalysisCard";
import {
  screenStocks,
  getAvailableSectors,
  addToWatchlist,
  type Stock,
  type ScreeningFilters,
} from "@/lib/api";

export default function Home() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [sectors, setSectors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [filtersApplied, setFiltersApplied] = useState<Record<string, string | number>>({});
  const [analyzingStock, setAnalyzingStock] = useState<string | null>(null);

  // Fetch available sectors on mount
  useEffect(() => {
    getAvailableSectors()
      .then(setSectors)
      .catch((err) => console.error("Failed to load sectors:", err));
  }, []);

  const handleScreenStocks = async (filters: ScreeningFilters) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const result = await screenStocks(filters);
      setStocks(result.stocks);
      setFiltersApplied(result.filters_applied);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to screen stocks");
      setStocks([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddToWatchlist = async (symbol: string) => {
    try {
      await addToWatchlist(symbol);
      alert(`${symbol} added to watchlist!`);
    } catch (err) {
      alert(`Failed to add ${symbol} to watchlist`);
    }
  };

  const handleAnalyze = (symbol: string) => {
    setAnalyzingStock(symbol);
  };

  const handleCloseAnalysis = () => {
    setAnalyzingStock(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      <div className="container mx-auto px-4 py-12">
        <header className="flex flex-col items-center mb-12">
          <Logo size="lg" />
          <nav className="mt-4 flex gap-4">
            <span className="text-primary-400 font-medium">Screener</span>
            <Link
              href="/portfolio"
              className="text-slate-400 hover:text-slate-200 transition-colors"
            >
              Portfolio
            </Link>
          </nav>
          <p className="mt-4 text-lg text-slate-300 max-w-2xl text-center">
            Find stable, long-term investment opportunities for your
            conservative portfolio. Built for investors with a 10+ year horizon.
          </p>
        </header>

        <section className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-semibold mb-6 text-primary-300">
            Conservative Stock Screener
          </h2>

          <ScreenerForm
            onSubmit={handleScreenStocks}
            isLoading={isLoading}
            sectors={sectors}
          />

          {/* Results Section */}
          {error && (
            <div className="mt-6 p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-300">
              {error}
            </div>
          )}

          {hasSearched && !error && (
            <div className="mt-8">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-slate-200">
                  Results ({stocks.length} stocks)
                </h3>
                {Object.keys(filtersApplied).length > 0 && (
                  <div className="text-sm text-slate-400">
                    Filters:{" "}
                    {Object.entries(filtersApplied)
                      .map(([key, value]) => `${key.replace(/_/g, " ")}: ${value}`)
                      .join(", ")}
                  </div>
                )}
              </div>

              <div className="bg-slate-800/50 rounded-xl overflow-hidden">
                <StockTable
                  stocks={stocks}
                  onAddToWatchlist={handleAddToWatchlist}
                  onAnalyze={handleAnalyze}
                />
              </div>

              {analyzingStock && (
                <div className="mt-6">
                  <StockAnalysisCard
                    symbol={analyzingStock}
                    onClose={handleCloseAnalysis}
                  />
                </div>
              )}
            </div>
          )}

          {/* Investment Philosophy - show when no search yet */}
          {!hasSearched && (
            <div className="mt-8 bg-slate-800/30 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-medium text-slate-200 mb-3">
                Investment Philosophy
              </h3>
              <ul className="space-y-2 text-slate-400">
                <li className="flex items-start gap-2">
                  <span className="text-primary-400">✓</span>
                  Focus on stable, dividend-paying companies
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-400">✓</span>
                  Long-term growth with lower volatility
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-400">✓</span>
                  Quality metrics: strong balance sheets, consistent earnings
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-400">✓</span>
                  10+ year investment horizon recommended
                </li>
              </ul>

              <div className="mt-6 pt-6 border-t border-slate-700">
                <h4 className="text-sm font-medium text-slate-300 mb-3">
                  Default Conservative Criteria
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div className="bg-slate-800/50 p-3 rounded-lg">
                    <div className="text-slate-400">Dividend Yield</div>
                    <div className="text-primary-400 font-semibold">&gt; 2%</div>
                  </div>
                  <div className="bg-slate-800/50 p-3 rounded-lg">
                    <div className="text-slate-400">P/E Ratio</div>
                    <div className="text-primary-400 font-semibold">&lt; 25</div>
                  </div>
                  <div className="bg-slate-800/50 p-3 rounded-lg">
                    <div className="text-slate-400">Market Cap</div>
                    <div className="text-primary-400 font-semibold">&gt; $10B</div>
                  </div>
                  <div className="bg-slate-800/50 p-3 rounded-lg">
                    <div className="text-slate-400">Beta</div>
                    <div className="text-primary-400 font-semibold">&lt; 1.0</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
