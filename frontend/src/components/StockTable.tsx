"use client";

import type { Stock } from "@/lib/api";

interface StockTableProps {
  stocks: Stock[];
  onAddToWatchlist?: (symbol: string) => void;
  onAnalyze?: (symbol: string) => void;
}

function formatNumber(value: number | null, decimals: number = 2): string {
  if (value === null || value === undefined) return "N/A";
  return value.toFixed(decimals);
}

function formatMarketCap(value: number | null): string {
  if (value === null || value === undefined) return "N/A";
  if (value >= 1000) return `$${(value / 1000).toFixed(1)}T`;
  return `$${value.toFixed(1)}B`;
}

function formatPercent(value: number | null): string {
  if (value === null || value === undefined) return "N/A";
  return `${value.toFixed(2)}%`;
}

function getBetaColor(beta: number | null): string {
  if (beta === null) return "text-slate-400";
  if (beta < 0.8) return "text-green-400";
  if (beta < 1.0) return "text-green-300";
  if (beta < 1.2) return "text-yellow-400";
  return "text-red-400";
}

function getDividendColor(dividend: number | null): string {
  if (dividend === null) return "text-slate-400";
  if (dividend >= 3) return "text-green-400";
  if (dividend >= 2) return "text-green-300";
  if (dividend >= 1) return "text-yellow-400";
  return "text-slate-400";
}

export default function StockTable({
  stocks,
  onAddToWatchlist,
  onAnalyze,
}: StockTableProps) {
  if (stocks.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        <p className="text-lg">No stocks match your criteria.</p>
        <p className="text-sm mt-2">Try adjusting your filters.</p>
      </div>
    );
  }

  const hasActions = onAddToWatchlist || onAnalyze;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-slate-700 text-slate-300 text-sm">
            <th className="py-3 px-4 font-medium">Symbol</th>
            <th className="py-3 px-4 font-medium">Name</th>
            <th className="py-3 px-4 font-medium">Sector</th>
            <th className="py-3 px-4 font-medium text-right">Price</th>
            <th className="py-3 px-4 font-medium text-right">Div Yield</th>
            <th className="py-3 px-4 font-medium text-right">P/E</th>
            <th className="py-3 px-4 font-medium text-right">Market Cap</th>
            <th className="py-3 px-4 font-medium text-right">Beta</th>
            {hasActions && (
              <th className="py-3 px-4 font-medium text-center">Actions</th>
            )}
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr
              key={stock.symbol}
              className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors"
            >
              <td className="py-3 px-4 font-semibold text-primary-400">
                {stock.symbol}
              </td>
              <td className="py-3 px-4 text-slate-200">{stock.name}</td>
              <td className="py-3 px-4 text-slate-400 text-sm">
                {stock.sector}
              </td>
              <td className="py-3 px-4 text-right text-slate-200">
                ${formatNumber(stock.price)}
              </td>
              <td
                className={`py-3 px-4 text-right ${getDividendColor(stock.dividend_yield)}`}
              >
                {formatPercent(stock.dividend_yield)}
              </td>
              <td className="py-3 px-4 text-right text-slate-200">
                {formatNumber(stock.pe_ratio, 1)}
              </td>
              <td className="py-3 px-4 text-right text-slate-200">
                {formatMarketCap(stock.market_cap)}
              </td>
              <td
                className={`py-3 px-4 text-right ${getBetaColor(stock.beta)}`}
              >
                {formatNumber(stock.beta)}
              </td>
              {hasActions && (
                <td className="py-3 px-4 text-center">
                  <div className="flex items-center justify-center gap-2">
                    {onAnalyze && (
                      <button
                        onClick={() => onAnalyze(stock.symbol)}
                        className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
                      >
                        Analyze
                      </button>
                    )}
                    {onAddToWatchlist && (
                      <button
                        onClick={() => onAddToWatchlist(stock.symbol)}
                        className="text-sm text-primary-400 hover:text-primary-300 transition-colors"
                      >
                        + Watch
                      </button>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
