"""AI-powered analysis endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.ai_service import (
    StockRecommendation,
    PortfolioAnalysis,
    analyze_stock,
    analyze_portfolio,
)
from services.stock_service import fetch_stock_data, fetch_multiple_stocks

router = APIRouter(prefix="/analysis", tags=["Analysis"])


class AnalyzeRequest(BaseModel):
    """Request model for portfolio analysis."""

    symbols: list[str]


@router.get("/stock/{symbol}", response_model=StockRecommendation)
async def get_stock_analysis(symbol: str):
    """
    Get AI-powered analysis and recommendation for a stock.

    Returns a comprehensive analysis including:
    - Buy/Hold/Sell recommendation
    - Confidence score
    - Pros and cons
    - Risk level assessment
    """
    stock = fetch_stock_data(symbol.upper())

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"Stock {symbol.upper()} not found",
        )

    return analyze_stock(stock)


@router.post("/portfolio", response_model=PortfolioAnalysis)
async def analyze_portfolio_endpoint(request: AnalyzeRequest):
    """
    Analyze a portfolio of stocks.

    Provides:
    - Overall portfolio score
    - Diversification assessment
    - Risk analysis
    - Sector allocation breakdown
    - Recommendations for improvement
    """
    if not request.symbols:
        raise HTTPException(
            status_code=400,
            detail="At least one stock symbol is required",
        )

    if len(request.symbols) > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum 50 stocks can be analyzed at once",
        )

    symbols = [s.upper() for s in request.symbols]
    stocks = fetch_multiple_stocks(symbols)

    if not stocks:
        raise HTTPException(
            status_code=404,
            detail="No valid stocks found for the provided symbols",
        )

    return analyze_portfolio(stocks)


@router.get("/quick/{symbol}")
async def get_quick_analysis(symbol: str):
    """
    Get a quick rule-based analysis without AI.

    Faster response, uses predefined rules for conservative investing criteria.
    """
    stock = fetch_stock_data(symbol.upper())

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"Stock {symbol.upper()} not found",
        )

    # Import here to avoid circular dependency
    from services.ai_service import _rule_based_recommendation

    return _rule_based_recommendation(stock)
