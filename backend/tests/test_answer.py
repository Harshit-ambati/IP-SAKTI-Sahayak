"""
Tests for answer generation endpoint (Task Su-01).
Verifies claim-evidence structure, synthetic mock outputs, field validation, and privacy audit logging.
"""

from pathlib import Path
from fastapi.testclient import TestClient
from app.db.database import get_db_connection


def test_answer_india_patent_query_success(client: TestClient):
    payload = {
        "query": "Is a classical Triphala formulation patentable in India?",
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["jurisdiction"] == "India"
    assert data["is_synthetic_fixture"] is True
    assert len(data["claims"]) > 0
    assert len(data["claims"][0]["evidence_ids"]) > 0
    assert any("Section 3(p)" in p for p in data["cited_provisions"])
    assert len(data["limitations"]) > 0
    assert "informational" in data["limitations"][0].lower()


def test_answer_international_query_success(client: TestClient):
    payload = {
        "query": "What international treaties govern patent disclosure of traditional knowledge?",
        "jurisdiction": "International",
        "language": "en"
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["jurisdiction"] == "International"
    assert "WIPO" in data["answer_text"]
    assert any("WIPO" in p for p in data["cited_provisions"])


def test_answer_malformed_short_query_fails_validation(client: TestClient):
    payload = {
        "query": "hi",  # min_length=3
        "jurisdiction": "India"
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 422


def test_answer_privacy_audit_logging(client: TestClient, test_db_path: Path):
    secret_query = "Confidential formulation patent query about SecretIngredientX"
    payload = {
        "query": secret_query,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200

    # Inspect audit_events table in test database
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute("SELECT audit_id, request_id, route, jurisdiction, evidence_ids, status FROM audit_events ORDER BY timestamp DESC LIMIT 1;")
    row = cur.fetchone()
    conn.close()

    assert row is not None
    assert row["jurisdiction"] == "India"
    assert row["status"] == "answered"

    # Strict Privacy Check: ensure the query text and secret formulation did NOT enter audit_events
    cur_full = get_db_connection(test_db_path).cursor()
    cur_full.execute("SELECT * FROM audit_events;")
    all_audit_text = str(cur_full.fetchall())
    assert "SecretIngredientX" not in all_audit_text
    assert "Confidential formulation" not in all_audit_text
