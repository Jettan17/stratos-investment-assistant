"""Tests for user preferences and watchlist endpoints."""

import pytest


def test_get_default_preferences(client):
    """Test getting default preferences creates them if not exist."""
    response = client.get("/api/v1/preferences")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "default"
    assert "min_dividend_yield" in data
    assert "max_pe_ratio" in data


def test_save_preferences(client):
    """Test saving user preferences."""
    prefs = {
        "name": "test_prefs",
        "min_dividend_yield": 3.0,
        "max_pe_ratio": 20.0,
        "min_market_cap": 50.0,
        "max_beta": 0.8,
        "preferred_sectors": ["Healthcare", "Utilities"],
    }
    response = client.post("/api/v1/preferences", json=prefs)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_prefs"
    assert data["min_dividend_yield"] == 3.0
    assert data["max_pe_ratio"] == 20.0


def test_update_preferences(client):
    """Test updating existing preferences."""
    # Create initial preferences
    prefs = {"name": "update_test", "min_dividend_yield": 2.0}
    client.post("/api/v1/preferences", json=prefs)

    # Update them
    updated = {"name": "update_test", "min_dividend_yield": 4.0}
    response = client.post("/api/v1/preferences", json=updated)
    assert response.status_code == 200
    data = response.json()
    assert data["min_dividend_yield"] == 4.0


def test_get_named_preferences(client):
    """Test getting preferences by name."""
    # Create named preferences
    prefs = {"name": "my_strategy", "max_pe_ratio": 15.0}
    client.post("/api/v1/preferences", json=prefs)

    # Retrieve them
    response = client.get("/api/v1/preferences?name=my_strategy")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "my_strategy"
    assert data["max_pe_ratio"] == 15.0


def test_delete_preferences(client):
    """Test deleting preferences."""
    # Create preferences
    prefs = {"name": "to_delete", "min_dividend_yield": 1.0}
    client.post("/api/v1/preferences", json=prefs)

    # Delete them
    response = client.delete("/api/v1/preferences/to_delete")
    assert response.status_code == 200


def test_delete_nonexistent_preferences(client):
    """Test deleting non-existent preferences returns 404."""
    response = client.delete("/api/v1/preferences/nonexistent")
    assert response.status_code == 404


# Watchlist tests
def test_get_empty_watchlist(client):
    """Test getting empty watchlist."""
    response = client.get("/api/v1/watchlist")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_add_to_watchlist(client):
    """Test adding a stock to watchlist."""
    item = {"symbol": "AAPL", "notes": "Tech blue chip", "target_price": 200.0}
    response = client.post("/api/v1/watchlist", json=item)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["notes"] == "Tech blue chip"
    assert data["target_price"] == 200.0
    assert data["is_active"] is True


def test_add_duplicate_to_watchlist(client):
    """Test adding duplicate stock updates existing entry."""
    item = {"symbol": "MSFT"}
    client.post("/api/v1/watchlist", json=item)

    # Add again with notes
    updated = {"symbol": "MSFT", "notes": "Updated notes"}
    response = client.post("/api/v1/watchlist", json=updated)
    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Updated notes"


def test_remove_from_watchlist(client):
    """Test removing stock from watchlist."""
    # Add first
    item = {"symbol": "GOOG"}
    client.post("/api/v1/watchlist", json=item)

    # Remove
    response = client.delete("/api/v1/watchlist/GOOG")
    assert response.status_code == 200


def test_remove_nonexistent_from_watchlist(client):
    """Test removing non-existent stock returns 404."""
    response = client.delete("/api/v1/watchlist/INVALID")
    assert response.status_code == 404
