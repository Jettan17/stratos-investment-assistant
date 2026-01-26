"""AI-powered stock analysis and recommendation service."""

import json
import logging
import os
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel

from services.stock_service import StockData

logger = logging.getLogger(__name__)


class StockRecommendation(BaseModel):
    """AI-generated stock recommendation."""

    symbol: str
    recommendation: str  # "strong_buy", "buy", "hold", "sell", "strong_sell"
    confidence: float  # 0.0 to 1.0
    summary: str
    pros: list[str]
    cons: list[str]
    target_price: Optional[float] = None
    risk_level: str  # "low", "medium", "high"


class PortfolioAnalysis(BaseModel):
    """AI-generated portfolio analysis."""

    overall_score: float  # 0.0 to 10.0
    diversification_score: float
    risk_assessment: str
    summary: str
    recommendations: list[str]
    sector_allocation: dict[str, float]


def get_openai_client() -> Optional[OpenAI]:
    """Get OpenAI client if API key is configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not configured")
        return None
    return OpenAI(api_key=api_key)


def analyze_stock(stock: StockData) -> StockRecommendation:
    """Generate AI-powered analysis for a single stock."""
    client = get_openai_client()

    if not client:
        # Return rule-based recommendation if no API key
        return _rule_based_recommendation(stock)

    prompt = f"""Analyze this stock for a conservative long-term investor (10+ year horizon):

Stock: {stock.symbol} - {stock.name}
Sector: {stock.sector}
Current Price: ${stock.price:.2f}
Dividend Yield: {stock.dividend_yield:.2f}% if stock.dividend_yield else "N/A"
P/E Ratio: {stock.pe_ratio:.1f} if stock.pe_ratio else "N/A"
Market Cap: ${stock.market_cap:.1f}B if stock.market_cap else "N/A"
Beta: {stock.beta:.2f} if stock.beta else "N/A"
Debt/Equity: {stock.debt_to_equity:.1f}% if stock.debt_to_equity else "N/A"

Provide analysis in JSON format:
{{
    "recommendation": "strong_buy|buy|hold|sell|strong_sell",
    "confidence": 0.0-1.0,
    "summary": "2-3 sentence summary",
    "pros": ["pro1", "pro2", "pro3"],
    "cons": ["con1", "con2"],
    "target_price": null or number,
    "risk_level": "low|medium|high"
}}

Focus on dividend stability, value metrics, and long-term growth potential for conservative investors."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a conservative investment analyst focusing on dividend-paying blue-chip stocks for long-term investors. Respond only with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        result = json.loads(response.choices[0].message.content)
        return StockRecommendation(symbol=stock.symbol, **result)

    except Exception as e:
        logger.error(f"AI analysis failed for {stock.symbol}: {e}")
        return _rule_based_recommendation(stock)


def _rule_based_recommendation(stock: StockData) -> StockRecommendation:
    """Generate recommendation using rule-based logic when AI is unavailable."""
    score = 0
    pros = []
    cons = []

    # Dividend yield scoring
    if stock.dividend_yield:
        if stock.dividend_yield >= 3.0:
            score += 2
            pros.append(f"Strong dividend yield of {stock.dividend_yield:.1f}%")
        elif stock.dividend_yield >= 2.0:
            score += 1
            pros.append(f"Decent dividend yield of {stock.dividend_yield:.1f}%")
        else:
            cons.append(f"Low dividend yield of {stock.dividend_yield:.1f}%")

    # P/E ratio scoring
    if stock.pe_ratio:
        if stock.pe_ratio < 15:
            score += 2
            pros.append(f"Attractive P/E ratio of {stock.pe_ratio:.1f}")
        elif stock.pe_ratio < 25:
            score += 1
            pros.append(f"Reasonable P/E ratio of {stock.pe_ratio:.1f}")
        else:
            score -= 1
            cons.append(f"High P/E ratio of {stock.pe_ratio:.1f}")

    # Beta scoring (volatility)
    if stock.beta:
        if stock.beta < 0.8:
            score += 2
            pros.append(f"Low volatility (beta: {stock.beta:.2f})")
        elif stock.beta < 1.0:
            score += 1
            pros.append(f"Below-market volatility (beta: {stock.beta:.2f})")
        elif stock.beta > 1.2:
            score -= 1
            cons.append(f"Higher volatility (beta: {stock.beta:.2f})")

    # Market cap scoring
    if stock.market_cap:
        if stock.market_cap >= 100:
            score += 1
            pros.append("Large-cap stability")
        elif stock.market_cap < 10:
            cons.append("Smaller market cap, potentially more volatile")

    # Debt scoring
    if stock.debt_to_equity:
        if stock.debt_to_equity < 50:
            score += 1
            pros.append("Low debt levels")
        elif stock.debt_to_equity > 100:
            score -= 1
            cons.append("Higher debt levels")

    # Determine recommendation
    if score >= 5:
        recommendation = "strong_buy"
        confidence = 0.85
    elif score >= 3:
        recommendation = "buy"
        confidence = 0.70
    elif score >= 1:
        recommendation = "hold"
        confidence = 0.60
    elif score >= -1:
        recommendation = "sell"
        confidence = 0.55
    else:
        recommendation = "strong_sell"
        confidence = 0.50

    # Determine risk level
    if stock.beta and stock.beta < 0.8:
        risk_level = "low"
    elif stock.beta and stock.beta > 1.2:
        risk_level = "high"
    else:
        risk_level = "medium"

    # Generate summary
    summary = f"{stock.name} is a {stock.sector} stock "
    if recommendation in ["strong_buy", "buy"]:
        summary += "that shows favorable characteristics for conservative long-term investors."
    elif recommendation == "hold":
        summary += "with mixed metrics. Consider monitoring before making investment decisions."
    else:
        summary += "that may not align well with conservative investment criteria."

    return StockRecommendation(
        symbol=stock.symbol,
        recommendation=recommendation,
        confidence=confidence,
        summary=summary,
        pros=pros if pros else ["Established company"],
        cons=cons if cons else ["Limited data available"],
        target_price=None,
        risk_level=risk_level,
    )


def analyze_portfolio(stocks: list[StockData]) -> PortfolioAnalysis:
    """Analyze a portfolio of stocks."""
    if not stocks:
        return PortfolioAnalysis(
            overall_score=0.0,
            diversification_score=0.0,
            risk_assessment="No stocks in portfolio",
            summary="Add stocks to your portfolio to receive analysis.",
            recommendations=["Add diversified stocks to your portfolio"],
            sector_allocation={},
        )

    # Calculate sector allocation
    sector_counts: dict[str, int] = {}
    for stock in stocks:
        sector_counts[stock.sector] = sector_counts.get(stock.sector, 0) + 1

    total = len(stocks)
    sector_allocation = {k: v / total * 100 for k, v in sector_counts.items()}

    # Calculate diversification score (more sectors = better)
    num_sectors = len(sector_counts)
    diversification_score = min(10.0, num_sectors * 2.0)

    # Calculate average beta for risk assessment
    betas = [s.beta for s in stocks if s.beta]
    avg_beta = sum(betas) / len(betas) if betas else 1.0

    if avg_beta < 0.8:
        risk_assessment = "Low risk - Portfolio has below-market volatility"
    elif avg_beta < 1.0:
        risk_assessment = "Moderate risk - Portfolio volatility near market average"
    else:
        risk_assessment = "Higher risk - Portfolio has above-market volatility"

    # Calculate overall score
    avg_dividend = sum(s.dividend_yield for s in stocks if s.dividend_yield) / max(
        1, len([s for s in stocks if s.dividend_yield])
    )
    overall_score = min(10.0, diversification_score * 0.3 + (avg_dividend * 1.5) + (5 - avg_beta * 2))

    # Generate recommendations
    recommendations = []
    if num_sectors < 3:
        recommendations.append("Consider diversifying across more sectors")
    if avg_beta > 1.0:
        recommendations.append("Portfolio is more volatile than market - consider lower-beta stocks")
    if avg_dividend < 2.0:
        recommendations.append("Consider adding higher dividend-yield stocks")
    if not recommendations:
        recommendations.append("Portfolio is well-balanced for conservative investing")

    summary = f"Portfolio contains {len(stocks)} stocks across {num_sectors} sectors. "
    summary += f"Average portfolio beta is {avg_beta:.2f}."

    return PortfolioAnalysis(
        overall_score=round(overall_score, 1),
        diversification_score=round(diversification_score, 1),
        risk_assessment=risk_assessment,
        summary=summary,
        recommendations=recommendations,
        sector_allocation=sector_allocation,
    )
