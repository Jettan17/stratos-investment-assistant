"""Stock screening and analysis endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from services.stock_service import (
    CONSERVATIVE_UNIVERSE,
    ConservativeScreener,
    StockData,
    fetch_multiple_stocks,
    fetch_stock_data,
)

router = APIRouter(prefix="/stocks", tags=["Stocks"])


class Stock(BaseModel):
    """Stock data model for API responses."""

    symbol: str
    name: str
    sector: str
    price: float
    dividend_yield: Optional[float] = None
    pe_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    beta: Optional[float] = None
    debt_to_equity: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None


class StockScreenResponse(BaseModel):
    """Response model for stock screening."""

    stocks: list[Stock]
    total: int
    filters_applied: dict


def stock_data_to_response(stock: StockData) -> Stock:
    """Convert StockData to API response Stock."""
    return Stock(
        symbol=stock.symbol,
        name=stock.name,
        sector=stock.sector,
        price=stock.price,
        dividend_yield=stock.dividend_yield,
        pe_ratio=stock.pe_ratio,
        market_cap=stock.market_cap,
        beta=stock.beta,
        debt_to_equity=stock.debt_to_equity,
        fifty_two_week_high=stock.fifty_two_week_high,
        fifty_two_week_low=stock.fifty_two_week_low,
    )


@router.get("/screen", response_model=StockScreenResponse)
async def screen_stocks(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    min_dividend_yield: Optional[float] = Query(
        None, description="Minimum dividend yield (%)"
    ),
    max_pe_ratio: Optional[float] = Query(None, description="Maximum P/E ratio"),
    min_market_cap: Optional[float] = Query(
        None, description="Minimum market cap in billions"
    ),
    max_beta: Optional[float] = Query(
        None, description="Maximum beta (volatility relative to market)"
    ),
    max_debt_to_equity: Optional[float] = Query(
        None, description="Maximum debt to equity ratio"
    ),
):
    """
    Screen stocks based on conservative investment criteria.

    Filter stocks by sector, dividend yield, P/E ratio, market cap, beta,
    and debt-to-equity ratio to find stable long-term investment opportunities.

    The conservative stock universe includes blue-chip dividend-paying companies
    across sectors like Healthcare, Consumer Staples, Financials, Technology,
    Utilities, Industrials, Energy, and REITs.
    """
    # Fetch stock data for the conservative universe
    stocks_data = fetch_multiple_stocks(CONSERVATIVE_UNIVERSE)

    # Create screener with criteria
    screener = ConservativeScreener(
        min_dividend_yield=min_dividend_yield,
        max_pe_ratio=max_pe_ratio,
        min_market_cap=min_market_cap,
        max_beta=max_beta,
        max_debt_to_equity=max_debt_to_equity,
        sector=sector,
    )

    # Filter stocks
    filtered = screener.screen(stocks_data)
    filters = screener.get_applied_filters()

    # Convert to response format
    response_stocks = [stock_data_to_response(s) for s in filtered]

    return StockScreenResponse(
        stocks=response_stocks,
        total=len(response_stocks),
        filters_applied=filters,
    )


@router.get("/universe", response_model=list[str])
async def get_stock_universe():
    """
    Get the list of stocks in the conservative investment universe.

    Returns the ticker symbols of all stocks that are screened by default.
    """
    return CONSERVATIVE_UNIVERSE


@router.get("/sectors", response_model=list[str])
async def get_available_sectors():
    """
    Get list of available sectors for filtering.

    Returns unique sectors found in the conservative stock universe.
    """
    stocks = fetch_multiple_stocks(CONSERVATIVE_UNIVERSE)
    sectors = sorted(set(s.sector for s in stocks if s.sector != "Unknown"))
    return sectors


@router.get("/{symbol}", response_model=Stock)
async def get_stock_details(symbol: str):
    """
    Get detailed information about a specific stock.

    Returns comprehensive data including price, dividend yield,
    P/E ratio, and other key metrics for conservative investors.
    """
    stock = fetch_stock_data(symbol.upper())

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"Stock with symbol '{symbol.upper()}' not found or data unavailable",
        )

    return stock_data_to_response(stock)


@router.get("/compare/{symbols}")
async def compare_stocks(symbols: str):
    """
    Compare multiple stocks side by side.

    Provide comma-separated symbols (e.g., 'JNJ,PG,KO').
    """
    symbol_list = [s.strip().upper() for s in symbols.split(",")]

    if len(symbol_list) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 stocks can be compared at once",
        )

    stocks = fetch_multiple_stocks(symbol_list)

    if not stocks:
        raise HTTPException(
            status_code=404,
            detail="No stock data found for the provided symbols",
        )

    return {
        "stocks": [stock_data_to_response(s) for s in stocks],
        "count": len(stocks),
    }
