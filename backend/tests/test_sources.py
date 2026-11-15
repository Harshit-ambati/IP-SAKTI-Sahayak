"""
Tests for sources and evidence passages lookup endpoints (Task Su-01).
Updated after PR #3 review fixes: preliminary corpus rows (activated=0) must NOT appear.
"""

from pathlib import Path
from fastapi.testclient import TestClient
from app.db.database import get_db_connection


def test_get_source_by_id_success(client: TestClient):
    response = client.get("/api/v1/sources/SYNTH-SRC-001")
    assert response.status_code == 200
    data = response.json()
    assert data["source_id"] == "SYNTH-SRC-001"
    assert data["topic"] == "patents"
    assert data["is_synthetic"] is True


def test_get_source_by_id_not_found(client: TestClient):
    response = client.get("/api/v1/sources/NON_EXISTENT_SOURCE_ID_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_sources_returns_only_activated(client: TestClient, test_db_path: Path):
    """
    FIX-3: Preliminary corpus rows (activated=0, is_synthetic=0) must NOT appear in /sources.
    Only activated=1 rows (synthetic test fixtures) should be returned.
    """
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

    # All returned items must be activated (synthetic fixtures only in phase 1)
    for item in data["items"]:
        assert item["is_synthetic"] is True, (
            f"Source {item['source_id']} is not synthetic but appeared in public endpoint. "
            "Preliminary corpus rows must be gated by activated=1."
        )

    # Verify that real preliminary corpus sources (REAL-*) are NOT in the public response
    source_ids = [item["source_id"] for item in data["items"]]
    real_ids = [sid for sid in source_ids if sid.startswith("REAL-")]
    assert len(real_ids) == 0, (
        f"Preliminary corpus rows {real_ids} appeared in public /sources endpoint. "
        "These must be gated behind activated=1."
    )


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
    assert "not found" in response.json()["detail"].lower()


def test_list_passages_returns_only_activated(client: TestClient):
    """
    FIX-3: Preliminary corpus passages (activated=0) must NOT appear in /passages.
    """
    response = client.get("/api/v1/passages")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

    # All returned items must be synthetic (the only activated=1 rows in phase 1)
    for item in data["items"]:
        assert item["is_synthetic"] is True, (
            f"Passage {item['passage_id']} is not synthetic but appeared in public endpoint."
        )

    passage_ids = [item["passage_id"] for item in data["items"]]
    real_ids = [pid for pid in passage_ids if pid.startswith("PASS-")]
    assert len(real_ids) == 0, (
        f"Preliminary corpus passages {real_ids} appeared in public /passages endpoint."
    )


def test_international_passage_retrievable_by_id(client: TestClient):
    """The dedicated international fixture must be accessible by ID."""
    response = client.get("/api/v1/passages/SYNTH-PASS-INT-001")
    assert response.status_code == 200
    data = response.json()
    assert data["jurisdiction"] == "International"
    assert data["is_synthetic"] is True
