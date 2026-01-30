/**
 * API client for Stratos Investment Assistant backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Stock {
  symbol: string;
  name: string;
  sector: string;
  price: number;
  dividend_yield: number | null;
  pe_ratio: number | null;
  market_cap: number | null;
  beta: number | null;
  debt_to_equity: number | null;
  fifty_two_week_high: number | null;
  fifty_two_week_low: number | null;
}

export interface StockScreenResponse {
  stocks: Stock[];
  total: number;
  filters_applied: Record<string, string | number>;
}

export interface ScreeningFilters {
  sector?: string;
  min_dividend_yield?: number;
  max_pe_ratio?: number;
  min_market_cap?: number;
  max_beta?: number;
  max_debt_to_equity?: number;
}

export interface UserPreferences {
  id: number;
  name: string;
  min_dividend_yield: number | null;
  max_pe_ratio: number | null;
  min_market_cap: number | null;
  max_beta: number | null;
  max_debt_to_equity: number | null;
  preferred_sectors: string[];
  created_at: string;
  updated_at: string;
}

export interface WatchlistItem {
  id: number;
  symbol: string;
  added_at: string;
  notes: string | null;
  target_price: number | null;
  is_active: boolean;
}

export interface StockRecommendation {
  symbol: string;
  recommendation: "strong_buy" | "buy" | "hold" | "sell" | "strong_sell";
  confidence: number;
  summary: string;
  pros: string[];
  cons: string[];
  target_price: number | null;
  risk_level: "low" | "medium" | "high";
}

export interface PortfolioAnalysis {
  overall_score: number;
  diversification_score: number;
  risk_assessment: string;
  summary: string;
  recommendations: string[];
  sector_allocation: Record<string, number>;
}

export interface PortfolioHolding {
  id: number;
  symbol: string;
  shares: number;
  purchase_price: number;
  purchase_date: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface PortfolioHoldingWithValue extends PortfolioHolding {
  name: string | null;
  current_price: number | null;
  current_value: number | null;
  gain_loss: number | null;
  gain_loss_percent: number | null;
}

export interface PortfolioSummary {
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  holdings_count: number;
  holdings: PortfolioHoldingWithValue[];
}

export interface PortfolioHoldingCreate {
  symbol: string;
  shares: number;
  purchase_price: number;
  purchase_date?: string;
  notes?: string;
}

export type AlertType = "price_above" | "price_below" | "percent_change";

export interface Alert {
  id: number;
  symbol: string;
  alert_type: AlertType;
  target_value: number;
  is_active: boolean;
  is_triggered: boolean;
  triggered_at: string | null;
  created_at: string;
  notes: string | null;
}

export interface AlertCreate {
  symbol: string;
  alert_type: AlertType;
  target_value: number;
  notes?: string;
}

export interface AlertCheck {
  alert: Alert;
  current_price: number | null;
  should_trigger: boolean;
  message: string;
}

/**
 * Screen stocks based on conservative investment criteria
 */
export async function screenStocks(
  filters: ScreeningFilters = {}
): Promise<StockScreenResponse> {
  const params = new URLSearchParams();

  if (filters.sector) params.append("sector", filters.sector);
  if (filters.min_dividend_yield !== undefined)
    params.append("min_dividend_yield", String(filters.min_dividend_yield));
  if (filters.max_pe_ratio !== undefined)
    params.append("max_pe_ratio", String(filters.max_pe_ratio));
  if (filters.min_market_cap !== undefined)
    params.append("min_market_cap", String(filters.min_market_cap));
  if (filters.max_beta !== undefined)
    params.append("max_beta", String(filters.max_beta));
  if (filters.max_debt_to_equity !== undefined)
    params.append("max_debt_to_equity", String(filters.max_debt_to_equity));

  const url = `${API_BASE_URL}/api/v1/stocks/screen?${params.toString()}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to screen stocks: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get detailed information about a specific stock
 */
export async function getStockDetails(symbol: string): Promise<Stock> {
  const response = await fetch(`${API_BASE_URL}/api/v1/stocks/${symbol}`);

  if (!response.ok) {
    throw new Error(`Failed to get stock details: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get the list of stocks in the conservative universe
 */
export async function getStockUniverse(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/stocks/universe`);

  if (!response.ok) {
    throw new Error(`Failed to get stock universe: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get available sectors for filtering
 */
export async function getAvailableSectors(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/stocks/sectors`);

  if (!response.ok) {
    throw new Error(`Failed to get sectors: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Compare multiple stocks
 */
export async function compareStocks(
  symbols: string[]
): Promise<{ stocks: Stock[]; count: number }> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/stocks/compare/${symbols.join(",")}`
  );

  if (!response.ok) {
    throw new Error(`Failed to compare stocks: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get user preferences
 */
export async function getPreferences(
  name: string = "default"
): Promise<UserPreferences> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/preferences?name=${name}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get preferences: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Save user preferences
 */
export async function savePreferences(
  preferences: Partial<UserPreferences>
): Promise<UserPreferences> {
  const response = await fetch(`${API_BASE_URL}/api/v1/preferences`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(preferences),
  });

  if (!response.ok) {
    throw new Error(`Failed to save preferences: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get watchlist
 */
export async function getWatchlist(
  activeOnly: boolean = true
): Promise<WatchlistItem[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/watchlist?active_only=${activeOnly}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get watchlist: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Add stock to watchlist
 */
export async function addToWatchlist(
  symbol: string,
  notes?: string,
  targetPrice?: number
): Promise<WatchlistItem> {
  const response = await fetch(`${API_BASE_URL}/api/v1/watchlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      symbol,
      notes,
      target_price: targetPrice,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to add to watchlist: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Remove stock from watchlist
 */
export async function removeFromWatchlist(symbol: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/watchlist/${symbol}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Failed to remove from watchlist: ${response.statusText}`);
  }
}

/**
 * Get AI-powered analysis for a stock
 */
export async function getStockAnalysis(
  symbol: string
): Promise<StockRecommendation> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/analysis/stock/${symbol}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get stock analysis: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get quick rule-based analysis for a stock (no AI)
 */
export async function getQuickAnalysis(
  symbol: string
): Promise<StockRecommendation> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/analysis/quick/${symbol}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get quick analysis: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Analyze a portfolio of stocks
 */
export async function analyzePortfolio(
  symbols: string[]
): Promise<PortfolioAnalysis> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis/portfolio`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbols }),
  });

  if (!response.ok) {
    throw new Error(`Failed to analyze portfolio: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get portfolio with current values
 */
export async function getPortfolio(): Promise<PortfolioSummary> {
  const response = await fetch(`${API_BASE_URL}/api/v1/portfolio/`);

  if (!response.ok) {
    throw new Error(`Failed to get portfolio: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Add a holding to portfolio
 */
export async function addHolding(
  holding: PortfolioHoldingCreate
): Promise<PortfolioHolding> {
  const response = await fetch(`${API_BASE_URL}/api/v1/portfolio/holdings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(holding),
  });

  if (!response.ok) {
    throw new Error(`Failed to add holding: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Update a portfolio holding
 */
export async function updateHolding(
  holdingId: number,
  updates: Partial<PortfolioHoldingCreate>
): Promise<PortfolioHolding> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/portfolio/holdings/${holdingId}`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to update holding: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete a portfolio holding
 */
export async function deleteHolding(holdingId: number): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/portfolio/holdings/${holdingId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to delete holding: ${response.statusText}`);
  }
}

/**
 * Get all alerts
 */
export async function getAlerts(activeOnly: boolean = true): Promise<Alert[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/alerts/?active_only=${activeOnly}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get alerts: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Create a new alert
 */
export async function createAlert(alert: AlertCreate): Promise<Alert> {
  const response = await fetch(`${API_BASE_URL}/api/v1/alerts/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(alert),
  });

  if (!response.ok) {
    throw new Error(`Failed to create alert: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete an alert
 */
export async function deleteAlert(alertId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/alerts/${alertId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Failed to delete alert: ${response.statusText}`);
  }
}

/**
 * Check all alerts for triggers
 */
export async function checkAlerts(): Promise<AlertCheck[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/alerts/check/all`);

  if (!response.ok) {
    throw new Error(`Failed to check alerts: ${response.statusText}`);
  }

  return response.json();
}
