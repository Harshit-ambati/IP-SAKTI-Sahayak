"""
Tests for answer generation endpoint (Task Su-01).
Updated after PR #3 review fixes.
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
    assert any("Section 3(p)" in p for p in data["cited_provisions"])
    assert len(data["limitations"]) > 0


def test_answer_international_query_uses_international_fixture(client: TestClient):
    """
    FIX-1: International answers must cite SYNTH-PASS-INT-001 (not India-only SYNTH-PASS-001)
    and must have evidence_status=partial (not supported).
    """
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
    # FIX-1: Must use international fixture, not India-only SYNTH-PASS-001
    all_evidence_ids = [eid for c in data["claims"] for eid in c["evidence_ids"]]
    assert "SYNTH-PASS-INT-001" in all_evidence_ids, (
        "International answer must cite SYNTH-PASS-INT-001, not an India-only fixture."
    )
    assert "SYNTH-PASS-001" not in all_evidence_ids, (
        "India-only SYNTH-PASS-001 (Patents Act s.3(p)) must NOT appear in International answers."
    )
    # FIX-1: International answers are partial (full treaty text not yet indexed)
    assert data["evidence_status"] == "partial", (
        "International answer evidence_status must be 'partial' until full treaty text is indexed."
    )
    assert "WIPO" in data["answer_text"]


def test_answer_india_answer_does_not_cite_international_passages(client: TestClient):
    """India-jurisdiction answers must not cite international-only passages."""
    payload = {
        "query": "How is a classical Ayurvedic drug classified under Indian law?",
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["jurisdiction"] == "India"
    all_evidence_ids = [eid for c in data["claims"] for eid in c["evidence_ids"]]
    assert "SYNTH-PASS-INT-001" not in all_evidence_ids, (
        "India-jurisdiction answers must not cite international passages."
    )


def test_answer_malformed_short_query_fails_validation(client: TestClient):
    payload = {"query": "hi", "jurisdiction": "India"}  # min_length=3
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

    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT audit_id, request_id, route, jurisdiction, evidence_ids, status FROM audit_events ORDER BY timestamp DESC LIMIT 1;"
    )
    row = cur.fetchone()

    # Strict Privacy Check: query text must NOT be in audit_events
    cur.execute("SELECT * FROM audit_events;")
    all_audit_text = str(cur.fetchall())
    conn.close()

    assert row is not None
    assert row["jurisdiction"] == "India"
    assert row["status"] == "answered"
    assert "SecretIngredientX" not in all_audit_text
    assert "Confidential formulation" not in all_audit_text
