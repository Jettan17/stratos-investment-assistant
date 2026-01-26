"""Tests for health check endpoint."""


def test_health_check(client):
    """Test that health check returns OK status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_redirects_to_docs(client):
    """Test that root path provides API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "Stratos" in data["name"]
