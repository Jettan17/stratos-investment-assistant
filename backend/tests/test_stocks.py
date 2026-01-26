"""Tests for stock screening endpoint."""

import pytest
from unittest.mock import patch, MagicMock

from services.stock_service import StockData, ConservativeScreener, fetch_stock_data


# Mock stock data for testing
MOCK_STOCKS = [
    StockData(
        symbol="JNJ",
        name="Johnson & Johnson",
        sector="Healthcare",
        price=155.50,
        dividend_yield=3.0,
        pe_ratio=15.2,
        market_cap=375.0,
        beta=0.55,
    ),
    StockData(
        symbol="MSFT",
        name="Microsoft",
        sector="Technology",
        price=420.50,
        dividend_yield=0.7,
        pe_ratio=35.2,
        market_cap=3100.0,
        beta=0.89,
    ),
    StockData(
        symbol="KO",
        name="Coca-Cola",
        sector="Consumer Staples",
        price=62.80,
        dividend_yield=2.9,
        pe_ratio=24.5,
        market_cap=270.0,
        beta=0.58,
    ),
]


@pytest.fixture
def mock_fetch_stocks():
    """Mock the fetch_multiple_stocks function."""
    with patch("api.routes.stocks.fetch_multiple_stocks") as mock:
        mock.return_value = MOCK_STOCKS
        yield mock


def test_screen_stocks_returns_list(client, mock_fetch_stocks):
    """Test that stock screening returns a list of stocks."""
    response = client.get("/api/v1/stocks/screen")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    assert isinstance(data["stocks"], list)
    assert len(data["stocks"]) == 3


def test_screen_stocks_with_sector_filter(client, mock_fetch_stocks):
    """Test stock screening with sector filter."""
    response = client.get("/api/v1/stocks/screen?sector=Healthcare")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    assert len(data["stocks"]) == 1
    assert data["stocks"][0]["symbol"] == "JNJ"


def test_screen_stocks_with_dividend_filter(client, mock_fetch_stocks):
    """Test stock screening with minimum dividend yield filter."""
    response = client.get("/api/v1/stocks/screen?min_dividend_yield=2.0")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    # JNJ (3.0%) and KO (2.9%) pass the filter
    assert len(data["stocks"]) == 2


def test_screen_stocks_with_pe_filter(client, mock_fetch_stocks):
    """Test stock screening with max P/E ratio filter."""
    response = client.get("/api/v1/stocks/screen?max_pe_ratio=25")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    # JNJ (15.2) and KO (24.5) pass the filter
    assert len(data["stocks"]) == 2


def test_screen_stocks_with_beta_filter(client, mock_fetch_stocks):
    """Test stock screening with max beta filter."""
    response = client.get("/api/v1/stocks/screen?max_beta=0.6")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    # JNJ (0.55) and KO (0.58) pass the filter
    assert len(data["stocks"]) == 2


def test_screen_stocks_with_multiple_filters(client, mock_fetch_stocks):
    """Test stock screening with multiple filters combined."""
    response = client.get(
        "/api/v1/stocks/screen?min_dividend_yield=2.0&max_pe_ratio=20"
    )
    assert response.status_code == 200
    data = response.json()
    # Only JNJ passes both filters
    assert len(data["stocks"]) == 1
    assert data["stocks"][0]["symbol"] == "JNJ"


def test_get_stock_details(client):
    """Test getting details for a specific stock."""
    with patch("api.routes.stocks.fetch_stock_data") as mock:
        mock.return_value = MOCK_STOCKS[0]
        response = client.get("/api/v1/stocks/JNJ")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "JNJ"


def test_get_stock_details_not_found(client):
    """Test getting details for a non-existent stock."""
    with patch("api.routes.stocks.fetch_stock_data") as mock:
        mock.return_value = None
        response = client.get("/api/v1/stocks/INVALID")
        assert response.status_code == 404


def test_get_stock_universe(client, mock_fetch_stocks):
    """Test getting the stock universe list."""
    response = client.get("/api/v1/stocks/universe")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "JNJ" in data


# Unit tests for ConservativeScreener
class TestConservativeScreener:
    """Unit tests for the ConservativeScreener class."""

    def test_passes_all_criteria(self):
        """Test stock that passes all criteria."""
        screener = ConservativeScreener(
            min_dividend_yield=2.0,
            max_pe_ratio=20.0,
            min_market_cap=100.0,
            max_beta=1.0,
        )
        assert screener.passes_criteria(MOCK_STOCKS[0])  # JNJ

    def test_fails_dividend_criteria(self):
        """Test stock that fails dividend yield criteria."""
        screener = ConservativeScreener(min_dividend_yield=2.0)
        assert not screener.passes_criteria(MOCK_STOCKS[1])  # MSFT (0.7%)

    def test_fails_pe_criteria(self):
        """Test stock that fails P/E ratio criteria."""
        screener = ConservativeScreener(max_pe_ratio=20.0)
        assert not screener.passes_criteria(MOCK_STOCKS[1])  # MSFT (35.2)

    def test_fails_beta_criteria(self):
        """Test stock that fails beta criteria."""
        screener = ConservativeScreener(max_beta=0.5)
        assert not screener.passes_criteria(MOCK_STOCKS[0])  # JNJ (0.55)

    def test_screen_filters_correctly(self):
        """Test that screen method filters stocks correctly."""
        screener = ConservativeScreener(min_dividend_yield=2.5)
        result = screener.screen(MOCK_STOCKS)
        assert len(result) == 2  # JNJ (3.0%) and KO (2.9%)

    def test_get_applied_filters(self):
        """Test that applied filters are returned correctly."""
        screener = ConservativeScreener(
            min_dividend_yield=2.0,
            max_pe_ratio=25.0,
            sector="Healthcare",
        )
        filters = screener.get_applied_filters()
        assert filters["min_dividend_yield"] == 2.0
        assert filters["max_pe_ratio"] == 25.0
        assert filters["sector"] == "Healthcare"
