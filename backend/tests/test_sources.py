"""
Tests for sources and evidence passages lookup endpoints (Task Su-01).
Verifies source record retrieval, passage lookup, and 404 responses for unknown IDs.
"""

from fastapi.testclient import TestClient


def test_get_source_by_id_success(client: TestClient):
    response = client.get("/api/v1/sources/SYNTH-SRC-001")
    assert response.status_code == 200
    data = response.json()
    assert data["source_id"] == "SYNTH-SRC-001"
    assert data["topic"] == "patents"
    assert data["authority"] == "IP India (Synthetic Mock)"
    assert data["is_synthetic"] is True


def test_get_source_by_id_not_found(client: TestClient):
    response = client.get("/api/v1/sources/NON_EXISTENT_SOURCE_ID_999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_list_sources(client: TestClient):
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_passage_by_id_success(client: TestClient):
    response = client.get("/api/v1/passages/SYNTH-PASS-001")
    assert response.status_code == 200
    data = response.json()
    assert data["passage_id"] == "SYNTH-PASS-001"
    assert data["source_id"] == "SYNTH-SRC-001"
    assert data["locator"] == "Section 3(p)"
    assert data["is_synthetic"] is True


def test_get_passage_by_id_not_found(client: TestClient):
    response = client.get("/api/v1/passages/NON_EXISTENT_PASSAGE_999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_list_passages(client: TestClient):
    response = client.get("/api/v1/passages")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] >= 1
