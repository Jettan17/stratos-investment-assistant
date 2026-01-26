"use client";

import { useState } from "react";
import type { ScreeningFilters } from "@/lib/api";

interface ScreenerFormProps {
  onSubmit: (filters: ScreeningFilters) => void;
  isLoading?: boolean;
  sectors?: string[];
}

export default function ScreenerForm({
  onSubmit,
  isLoading = false,
  sectors = [],
}: ScreenerFormProps) {
  const [filters, setFilters] = useState<ScreeningFilters>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(filters);
  };

  const handleChange = (
    field: keyof ScreeningFilters,
    value: string | undefined
  ) => {
    setFilters((prev) => ({
      ...prev,
      [field]: value === "" ? undefined : field === "sector" ? value : Number(value),
    }));
  };

  const handleReset = () => {
    setFilters({});
  };

  const inputClassName =
    "w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent";
  const labelClassName = "block text-sm font-medium text-slate-300 mb-2";

  return (
    <form onSubmit={handleSubmit} className="bg-slate-800/50 rounded-xl p-6">
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label htmlFor="sector" className={labelClassName}>
            Sector
          </label>
          <select
            id="sector"
            value={filters.sector || ""}
            onChange={(e) => handleChange("sector", e.target.value)}
            className={inputClassName}
          >
            <option value="">All Sectors</option>
            {sectors.map((sector) => (
              <option key={sector} value={sector}>
                {sector}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="min-dividend" className={labelClassName}>
            Min Dividend Yield (%)
          </label>
          <input
            type="number"
            id="min-dividend"
            placeholder="e.g., 2.0"
            step="0.1"
            min="0"
            value={filters.min_dividend_yield ?? ""}
            onChange={(e) => handleChange("min_dividend_yield", e.target.value)}
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="max-pe" className={labelClassName}>
            Max P/E Ratio
          </label>
          <input
            type="number"
            id="max-pe"
            placeholder="e.g., 25"
            step="1"
            min="0"
            value={filters.max_pe_ratio ?? ""}
            onChange={(e) => handleChange("max_pe_ratio", e.target.value)}
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="min-market-cap" className={labelClassName}>
            Min Market Cap ($B)
          </label>
          <input
            type="number"
            id="min-market-cap"
            placeholder="e.g., 10"
            step="1"
            min="0"
            value={filters.min_market_cap ?? ""}
            onChange={(e) => handleChange("min_market_cap", e.target.value)}
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="max-beta" className={labelClassName}>
            Max Beta
          </label>
          <input
            type="number"
            id="max-beta"
            placeholder="e.g., 1.0"
            step="0.1"
            min="0"
            value={filters.max_beta ?? ""}
            onChange={(e) => handleChange("max_beta", e.target.value)}
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="max-debt-equity" className={labelClassName}>
            Max Debt/Equity
          </label>
          <input
            type="number"
            id="max-debt-equity"
            placeholder="e.g., 100"
            step="10"
            min="0"
            value={filters.max_debt_to_equity ?? ""}
            onChange={(e) => handleChange("max_debt_to_equity", e.target.value)}
            className={inputClassName}
          />
        </div>
      </div>

      <div className="flex gap-4 mt-6">
        <button
          type="submit"
          disabled={isLoading}
          className="flex-1 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-800 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
        >
          {isLoading ? "Screening..." : "Screen Stocks"}
        </button>
        <button
          type="button"
          onClick={handleReset}
          className="px-6 py-3 border border-slate-600 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors duration-200"
        >
          Reset
        </button>
      </div>
    </form>
  );
}
