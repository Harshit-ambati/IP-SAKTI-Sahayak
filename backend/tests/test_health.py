"""
Tests for health check endpoints (Task Su-01).
"""

from fastapi.testclient import TestClient
from app.config import VERSION


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "IP-SAKTI" in data["service"]
    assert "Su-02" in data["phase"]


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["fts5_supported"] is True
    assert "timestamp" in data


def test_api_v1_health_endpoint(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == VERSION
