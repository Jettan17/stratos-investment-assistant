"use client";

import { useState, useEffect } from "react";
import type { PortfolioSummary, PortfolioHoldingCreate } from "@/lib/api";
import { getPortfolio, addHolding, deleteHolding } from "@/lib/api";

function formatCurrency(value: number | null): string {
  if (value === null || value === undefined) return "N/A";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

function formatPercent(value: number | null): string {
  if (value === null || value === undefined) return "N/A";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function getGainLossColor(value: number | null): string {
  if (value === null) return "text-slate-400";
  if (value > 0) return "text-green-400";
  if (value < 0) return "text-red-400";
  return "text-slate-400";
}

export default function PortfolioCard() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newHolding, setNewHolding] = useState<PortfolioHoldingCreate>({
    symbol: "",
    shares: 0,
    purchase_price: 0,
  });

  const fetchPortfolio = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getPortfolio();
      setPortfolio(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load portfolio");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const handleAddHolding = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newHolding.symbol || newHolding.shares <= 0 || newHolding.purchase_price <= 0) {
      return;
    }

    try {
      await addHolding(newHolding);
      setNewHolding({ symbol: "", shares: 0, purchase_price: 0 });
      setShowAddForm(false);
      fetchPortfolio();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add holding");
    }
  };

  const handleDeleteHolding = async (holdingId: number) => {
    if (!confirm("Are you sure you want to remove this holding?")) return;

    try {
      await deleteHolding(holdingId);
      fetchPortfolio();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete holding");
    }
  };

  if (isLoading && !portfolio) {
    return (
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-400"></div>
          <span className="ml-3 text-slate-400">Loading portfolio...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-slate-200">My Portfolio</h3>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="text-sm bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {showAddForm ? "Cancel" : "+ Add Holding"}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Add Holding Form */}
      {showAddForm && (
        <form onSubmit={handleAddHolding} className="mb-6 p-4 bg-slate-800 rounded-lg">
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Symbol</label>
              <input
                type="text"
                value={newHolding.symbol}
                onChange={(e) =>
                  setNewHolding({ ...newHolding, symbol: e.target.value.toUpperCase() })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
                placeholder="AAPL"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Shares</label>
              <input
                type="number"
                value={newHolding.shares || ""}
                onChange={(e) =>
                  setNewHolding({ ...newHolding, shares: parseFloat(e.target.value) || 0 })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
                placeholder="100"
                step="0.01"
                min="0"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Purchase Price</label>
              <input
                type="number"
                value={newHolding.purchase_price || ""}
                onChange={(e) =>
                  setNewHolding({
                    ...newHolding,
                    purchase_price: parseFloat(e.target.value) || 0,
                  })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
                placeholder="150.00"
                step="0.01"
                min="0"
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Add to Portfolio
          </button>
        </form>
      )}

      {/* Portfolio Summary */}
      {portfolio && portfolio.holdings_count > 0 && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-sm text-slate-400">Total Value</div>
              <div className="text-xl font-semibold text-slate-200">
                {formatCurrency(portfolio.total_value)}
              </div>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-sm text-slate-400">Total Cost</div>
              <div className="text-xl font-semibold text-slate-200">
                {formatCurrency(portfolio.total_cost)}
              </div>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-sm text-slate-400">Total Gain/Loss</div>
              <div
                className={`text-xl font-semibold ${getGainLossColor(portfolio.total_gain_loss)}`}
              >
                {formatCurrency(portfolio.total_gain_loss)}
              </div>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-sm text-slate-400">Return</div>
              <div
                className={`text-xl font-semibold ${getGainLossColor(portfolio.total_gain_loss_percent)}`}
              >
                {formatPercent(portfolio.total_gain_loss_percent)}
              </div>
            </div>
          </div>

          {/* Holdings Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-700 text-slate-400">
                  <th className="py-2 px-3">Symbol</th>
                  <th className="py-2 px-3">Name</th>
                  <th className="py-2 px-3 text-right">Shares</th>
                  <th className="py-2 px-3 text-right">Avg Cost</th>
                  <th className="py-2 px-3 text-right">Current</th>
                  <th className="py-2 px-3 text-right">Value</th>
                  <th className="py-2 px-3 text-right">Gain/Loss</th>
                  <th className="py-2 px-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.holdings.map((holding) => (
                  <tr
                    key={holding.id}
                    className="border-b border-slate-800 hover:bg-slate-800/50"
                  >
                    <td className="py-2 px-3 font-semibold text-primary-400">
                      {holding.symbol}
                    </td>
                    <td className="py-2 px-3 text-slate-300">
                      {holding.name || "-"}
                    </td>
                    <td className="py-2 px-3 text-right text-slate-200">
                      {holding.shares.toFixed(2)}
                    </td>
                    <td className="py-2 px-3 text-right text-slate-200">
                      {formatCurrency(holding.purchase_price)}
                    </td>
                    <td className="py-2 px-3 text-right text-slate-200">
                      {formatCurrency(holding.current_price)}
                    </td>
                    <td className="py-2 px-3 text-right text-slate-200">
                      {formatCurrency(holding.current_value)}
                    </td>
                    <td
                      className={`py-2 px-3 text-right ${getGainLossColor(holding.gain_loss)}`}
                    >
                      {formatCurrency(holding.gain_loss)}{" "}
                      <span className="text-xs">
                        ({formatPercent(holding.gain_loss_percent)})
                      </span>
                    </td>
                    <td className="py-2 px-3 text-center">
                      <button
                        onClick={() => handleDeleteHolding(holding.id)}
                        className="text-red-400 hover:text-red-300 transition-colors"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Empty State */}
      {portfolio && portfolio.holdings_count === 0 && !showAddForm && (
        <div className="text-center py-8 text-slate-400">
          <p className="text-lg">No holdings in your portfolio yet.</p>
          <p className="text-sm mt-2">Add your first holding to start tracking.</p>
        </div>
      )}
    </div>
  );
}
