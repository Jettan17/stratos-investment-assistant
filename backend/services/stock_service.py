"""Stock data service using yfinance for real market data."""

import logging
from typing import Optional

import yfinance as yf
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class StockData(BaseModel):
    """Comprehensive stock data model."""

    symbol: str
    name: str
    sector: str
    price: float
    dividend_yield: Optional[float] = None
    pe_ratio: Optional[float] = None
    market_cap: Optional[float] = None  # in billions
    beta: Optional[float] = None
    debt_to_equity: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    forward_pe: Optional[float] = None
    payout_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None


# Conservative stock universe - blue chip dividend payers
CONSERVATIVE_UNIVERSE = [
    # Healthcare
    "JNJ", "PFE", "ABBV", "MRK", "UNH",
    # Consumer Staples
    "PG", "KO", "PEP", "WMT", "COST",
    # Financials
    "JPM", "BRK-B", "V", "MA", "BAC",
    # Technology (stable large caps)
    "MSFT", "AAPL", "CSCO", "IBM", "INTC",
    # Utilities
    "NEE", "DUK", "SO", "D", "AEP",
    # Industrials
    "MMM", "HON", "CAT", "UPS", "RTX",
    # Energy
    "XOM", "CVX", "COP",
    # REITs
    "O", "SPG", "AMT",
]


def fetch_stock_data(symbol: str) -> Optional[StockData]:
    """Fetch real-time stock data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info or "symbol" not in info:
            logger.warning(f"No data found for symbol: {symbol}")
            return None

        # Extract market cap in billions
        market_cap_raw = info.get("marketCap")
        market_cap = market_cap_raw / 1e9 if market_cap_raw else None

        # Extract dividend yield as percentage
        div_yield = info.get("dividendYield")
        dividend_yield = div_yield * 100 if div_yield else None

        # Extract payout ratio as percentage
        payout = info.get("payoutRatio")
        payout_ratio = payout * 100 if payout else None

        return StockData(
            symbol=info.get("symbol", symbol),
            name=info.get("shortName", info.get("longName", symbol)),
            sector=info.get("sector", "Unknown"),
            price=info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
            dividend_yield=dividend_yield,
            pe_ratio=info.get("trailingPE"),
            market_cap=market_cap,
            beta=info.get("beta"),
            debt_to_equity=info.get("debtToEquity"),
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
            forward_pe=info.get("forwardPE"),
            payout_ratio=payout_ratio,
            revenue_growth=info.get("revenueGrowth"),
            profit_margin=info.get("profitMargins"),
        )
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None


def fetch_multiple_stocks(symbols: list[str]) -> list[StockData]:
    """Fetch data for multiple stocks."""
    stocks = []
    for symbol in symbols:
        stock = fetch_stock_data(symbol)
        if stock:
            stocks.append(stock)
    return stocks


class ConservativeScreener:
    """Screen stocks based on conservative investment criteria."""

    # Default conservative criteria
    DEFAULT_CRITERIA = {
        "min_dividend_yield": 2.0,  # > 2%
        "max_pe_ratio": 25.0,  # < 25
        "min_market_cap": 10.0,  # > $10B
        "max_beta": 1.0,  # < 1.0 (less volatile than market)
        "max_debt_to_equity": 100.0,  # < 1.0 ratio (shown as percentage)
    }

    def __init__(
        self,
        min_dividend_yield: Optional[float] = None,
        max_pe_ratio: Optional[float] = None,
        min_market_cap: Optional[float] = None,
        max_beta: Optional[float] = None,
        max_debt_to_equity: Optional[float] = None,
        sector: Optional[str] = None,
    ):
        self.min_dividend_yield = min_dividend_yield
        self.max_pe_ratio = max_pe_ratio
        self.min_market_cap = min_market_cap
        self.max_beta = max_beta
        self.max_debt_to_equity = max_debt_to_equity
        self.sector = sector

    def passes_criteria(self, stock: StockData) -> bool:
        """Check if a stock passes all screening criteria."""
        # Sector filter
        if self.sector:
            if stock.sector.lower() != self.sector.lower():
                return False

        # Dividend yield filter
        if self.min_dividend_yield is not None:
            if not stock.dividend_yield or stock.dividend_yield < self.min_dividend_yield:
                return False

        # P/E ratio filter
        if self.max_pe_ratio is not None:
            if not stock.pe_ratio or stock.pe_ratio > self.max_pe_ratio:
                return False

        # Market cap filter
        if self.min_market_cap is not None:
            if not stock.market_cap or stock.market_cap < self.min_market_cap:
                return False

        # Beta filter
        if self.max_beta is not None:
            if stock.beta and stock.beta > self.max_beta:
                return False

        # Debt to equity filter
        if self.max_debt_to_equity is not None:
            if stock.debt_to_equity and stock.debt_to_equity > self.max_debt_to_equity:
                return False

        return True

    def screen(self, stocks: list[StockData]) -> list[StockData]:
        """Filter stocks based on conservative criteria."""
        return [s for s in stocks if self.passes_criteria(s)]

    def get_applied_filters(self) -> dict:
        """Return dictionary of applied filters."""
        filters = {}
        if self.sector:
            filters["sector"] = self.sector
        if self.min_dividend_yield is not None:
            filters["min_dividend_yield"] = self.min_dividend_yield
        if self.max_pe_ratio is not None:
            filters["max_pe_ratio"] = self.max_pe_ratio
        if self.min_market_cap is not None:
            filters["min_market_cap"] = self.min_market_cap
        if self.max_beta is not None:
            filters["max_beta"] = self.max_beta
        if self.max_debt_to_equity is not None:
            filters["max_debt_to_equity"] = self.max_debt_to_equity
        return filters


def screen_conservative_stocks(
    sector: Optional[str] = None,
    min_dividend_yield: Optional[float] = None,
    max_pe_ratio: Optional[float] = None,
    min_market_cap: Optional[float] = None,
    max_beta: Optional[float] = None,
    use_defaults: bool = False,
) -> tuple[list[StockData], dict]:
    """
    Screen the conservative stock universe based on criteria.

    Returns tuple of (filtered_stocks, applied_filters).
    """
    # Use default conservative criteria if requested
    if use_defaults:
        defaults = ConservativeScreener.DEFAULT_CRITERIA
        min_dividend_yield = min_dividend_yield or defaults["min_dividend_yield"]
        max_pe_ratio = max_pe_ratio or defaults["max_pe_ratio"]
        min_market_cap = min_market_cap or defaults["min_market_cap"]
        max_beta = max_beta or defaults["max_beta"]

    # Fetch all stocks in universe
    stocks = fetch_multiple_stocks(CONSERVATIVE_UNIVERSE)

    # Create screener and filter
    screener = ConservativeScreener(
        min_dividend_yield=min_dividend_yield,
        max_pe_ratio=max_pe_ratio,
        min_market_cap=min_market_cap,
        max_beta=max_beta,
        sector=sector,
    )

    filtered = screener.screen(stocks)
    filters = screener.get_applied_filters()

    return filtered, filters
