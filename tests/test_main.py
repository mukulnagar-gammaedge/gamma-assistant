import pytest


class TestHealth:
    """Test health check endpoints"""

    def test_root_endpoint(self, client):
        """Test that root endpoint returns API running message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "API running"

    def test_root_endpoint_returns_json(self, client):
        """Test that root endpoint returns valid JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
