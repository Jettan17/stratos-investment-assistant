"use client";

import { useState } from "react";
import type { StockRecommendation } from "@/lib/api";
import { getQuickAnalysis } from "@/lib/api";

interface StockAnalysisCardProps {
  symbol: string;
  onClose?: () => void;
}

const recommendationColors = {
  strong_buy: "text-green-400 bg-green-900/30",
  buy: "text-green-300 bg-green-900/20",
  hold: "text-yellow-400 bg-yellow-900/20",
  sell: "text-orange-400 bg-orange-900/20",
  strong_sell: "text-red-400 bg-red-900/30",
};

const recommendationLabels = {
  strong_buy: "Strong Buy",
  buy: "Buy",
  hold: "Hold",
  sell: "Sell",
  strong_sell: "Strong Sell",
};

const riskColors = {
  low: "text-green-400",
  medium: "text-yellow-400",
  high: "text-red-400",
};

export default function StockAnalysisCard({
  symbol,
  onClose,
}: StockAnalysisCardProps) {
  const [analysis, setAnalysis] = useState<StockRecommendation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await getQuickAnalysis(symbol);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get analysis");
    } finally {
      setIsLoading(false);
    }
  };

  if (!analysis && !isLoading && !error) {
    return (
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-slate-200">
            Analysis: {symbol}
          </h3>
          {onClose && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-slate-200"
            >
              ×
            </button>
          )}
        </div>
        <button
          onClick={fetchAnalysis}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Get AI Analysis
        </button>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-slate-200">
            Analysis: {symbol}
          </h3>
        </div>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-400"></div>
          <span className="ml-3 text-slate-400">Analyzing...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-slate-200">
            Analysis: {symbol}
          </h3>
          {onClose && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-slate-200"
            >
              ×
            </button>
          )}
        </div>
        <div className="text-red-400 text-center py-4">{error}</div>
        <button
          onClick={fetchAnalysis}
          className="w-full bg-slate-700 hover:bg-slate-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!analysis) return null;

  return (
    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-200">{symbol}</h3>
          <span
            className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium ${recommendationColors[analysis.recommendation]}`}
          >
            {recommendationLabels[analysis.recommendation]}
          </span>
        </div>
        <div className="text-right">
          {onClose && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-slate-200 text-xl"
            >
              ×
            </button>
          )}
          <div className="mt-2">
            <div className="text-xs text-slate-500">Confidence</div>
            <div className="text-lg font-semibold text-primary-400">
              {Math.round(analysis.confidence * 100)}%
            </div>
          </div>
        </div>
      </div>

      <p className="text-slate-300 mb-4">{analysis.summary}</p>

      <div className="grid md:grid-cols-2 gap-4 mb-4">
        <div>
          <h4 className="text-sm font-medium text-green-400 mb-2">Pros</h4>
          <ul className="space-y-1">
            {analysis.pros.map((pro, i) => (
              <li key={i} className="text-sm text-slate-400 flex items-start gap-2">
                <span className="text-green-400">+</span>
                {pro}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-medium text-red-400 mb-2">Cons</h4>
          <ul className="space-y-1">
            {analysis.cons.map((con, i) => (
              <li key={i} className="text-sm text-slate-400 flex items-start gap-2">
                <span className="text-red-400">-</span>
                {con}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-slate-700">
        <div>
          <span className="text-xs text-slate-500">Risk Level</span>
          <div className={`font-medium capitalize ${riskColors[analysis.risk_level]}`}>
            {analysis.risk_level}
          </div>
        </div>
        {analysis.target_price && (
          <div className="text-right">
            <span className="text-xs text-slate-500">Target Price</span>
            <div className="font-medium text-slate-200">
              ${analysis.target_price.toFixed(2)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
