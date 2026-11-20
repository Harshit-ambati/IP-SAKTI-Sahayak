"""
Tests for answer generation endpoint (Task Su-01, Su-02).
Updated after PR #7 review fixes:
- Public API contract enforces approved evidence by default; callers cannot relax it.
- Server-side demo mode (ALLOW_SYNTHETIC_DEMO) gates synthetic retrieval.
- Answerability gate enforces that EVERY material subject constraint must be supported
  by retrieved passages, even if a statutory locator or other subject terms match.
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.db.database import get_db_connection


def test_answer_india_patent_query_success_in_demo_mode(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """
    Server-side demo mode (ALLOW_SYNTHETIC_DEMO=True): synthetic fixtures are allowed.
    Synthetic fixtures are NEVER marked as 'supported'; evidence_status must be 'partial'.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "Is traditional knowledge patentable under Section 3(p) in India?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["jurisdiction"] == "India"
    assert data["is_synthetic_fixture"] is True
    # Synthetic demo fixtures are NEVER marked as supported legal evidence
    assert data["evidence_status"] == "partial"
    assert "SYNTHETIC MOCK/DEMO" in data["answer_text"]
    assert len(data["claims"]) > 0
    assert any("Section 3(p)" in p for p in data["cited_provisions"]), (
        "Demo-mode answer must cite Section 3(p) statutory provision."
    )
    assert len(data["limitations"]) > 0


def test_answer_production_mode_with_approved_evidence_success(client: TestClient, test_db_path: Path):
    """
    Production path with approved evidence: Non-synthetic, reviewed approved evidence
    produces evidence_status='supported' and is_synthetic_fixture=False via the public endpoint.
    """
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT OR REPLACE INTO sources (source_id, topic, authority, title, official_url, verification_status, is_synthetic, activated)
            VALUES ('REAL-SRC-001', 'patents', 'IP India', 'The Patents Act 1970', 'https://ipindia.gov.in', 'verified', 0, 1)
            """
        )
        cur.execute(
            """
            INSERT OR REPLACE INTO passages (passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, is_synthetic, activated)
            VALUES ('REAL-PASS-001', 'REAL-SRC-001', 'India', 'IP India', 'The Patents Act 1970', 'Section 3(p)', 'Traditional knowledge and aggregation of known traditional properties are not patentable inventions.', 'https://ipindia.gov.in', 'statute', 'approved', 0, 1)
            """
        )
        conn.commit()

        payload = {
            "query": "Is traditional knowledge patentable in India?",
            "jurisdiction": "India",
            "language": "en",
        }
        response = client.post("/api/v1/answer", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "answered"
        assert data["evidence_status"] == "supported"
        assert data["is_synthetic_fixture"] is False
        assert len(data["claims"]) > 0
        assert any(p["passage_id"] == "REAL-PASS-001" for p in data["evidence"])
        assert any("REAL-PASS-001" in c["evidence_ids"] for c in data["claims"])
    finally:
        cur.execute("DELETE FROM passages WHERE passage_id = 'REAL-PASS-001'")
        cur.execute("DELETE FROM sources WHERE source_id = 'REAL-SRC-001'")
        conn.commit()
        conn.close()


def test_answer_international_query_uses_international_fixture(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """
    FIX-1: International answers must cite SYNTH-PASS-INT-001 (not India-only SYNTH-PASS-001)
    and must have evidence_status=partial (not supported).
    Tested under server-side demo mode.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "What international treaties govern patent disclosure of traditional knowledge?",
        "jurisdiction": "International",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["jurisdiction"] == "International"
    all_evidence_ids = [eid for c in data["claims"] for eid in c["evidence_ids"]]
    assert "SYNTH-PASS-INT-001" in all_evidence_ids, (
        "International answer must cite SYNTH-PASS-INT-001, not an India-only fixture."
    )
    assert "SYNTH-PASS-001" not in all_evidence_ids, (
        "India-only SYNTH-PASS-001 (Patents Act s.3(p)) must NOT appear in International answers."
    )
    assert data["evidence_status"] == "partial", (
        "International answer evidence_status must be 'partial' until full treaty text is indexed."
    )
    assert "WIPO" in data["answer_text"]


def test_answer_india_answer_does_not_cite_international_passages(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """India-jurisdiction answers must not cite international-only passages."""
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "How are classical Ayurvedic drugs defined under Indian law?",
        "jurisdiction": "India",
        "language": "en",
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
    """
    Privacy check: query text, formulation title, and secret ingredients must NEVER
    appear in audit_events, regardless of whether the query is answered or abstained.
    """
    secret_query = "Confidential traditional knowledge patent query about SecretIngredientX under Section 3(p)"
    payload = {
        "query": secret_query,
        "jurisdiction": "India",
        "language": "en",
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
    assert "SecretIngredientX" not in all_audit_text
    assert "Confidential traditional knowledge" not in all_audit_text


def test_answer_unsupported_query_abstains_cleanly(client: TestClient):
    """Zero approved statutory evidence yields clean abstention with empty claims (Task Su-02)."""
    payload = {
        "query": "Superconducting quantum computing orbital hardware protocol",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained"
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert len(data["cited_provisions"]) == 0
    assert "abstains" in data["answer_text"].lower()


def test_answer_mixed_legal_term_with_unsupported_subject_abstains(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """
    Answerability Gate Regression: Mixed query with a common procedural legal word
    ('patentable', 'India') plus an unsupported subject ('quantum cryptography')
    must abstain and not generate claims or false 'supported' legal answers.
    Tested even when demo pool is active.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "Is quantum cryptography patentable in India?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained"
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert len(data["cited_provisions"]) == 0
    assert len(data["evidence"]) == 0
    assert "quantum cryptography" in data["answer_text"].lower() or "abstains" in data["answer_text"].lower()


def test_answer_unsupported_drone_navigation_under_matching_section_locator_abstains(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    """
    Answerability Gate Regression (Finding 1):
    Query: 'Is drone navigation patentable under Section 3(p)?'
    With Section 3(p) in the active retrieval pool (demo mode), the locator matches Section 3(p),
    but the material subject terms ('drone', 'navigation') are completely unsupported by the passage.
    The answerability gate must reject candidate passages and force clean abstention.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "Is drone navigation patentable under Section 3(p)?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained", (
        "Query with unsupported subject terms ('drone', 'navigation') must abstain "
        "even when the query specifies a matching statutory locator like Section 3(p)."
    )
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert len(data["cited_provisions"]) == 0
    assert len(data["evidence"]) == 0


def test_answer_unsupported_drone_with_matching_traditional_knowledge_terms_abstains(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    """
    Answerability Gate Regression (Finding 1):
    Query: 'Is drone traditional knowledge patentable in India?'
    Even though 'traditional' and 'knowledge' match Section 3(p), the material subject
    constraint 'drone' is not addressed by any passage in the pool.
    Unsupported material subject constraints must force abstention rather than producing
    false legal advice.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "Is drone traditional knowledge patentable in India?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained", (
        "Query with unsupported subject constraint 'drone' must abstain "
        "even when other subject terms ('traditional', 'knowledge') match a passage."
    )
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert len(data["cited_provisions"]) == 0
    assert len(data["evidence"]) == 0


def test_answer_drone_navigation_with_traditional_term_abstains(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    """
    Answerability Gate Regression: A query with unsupported primary subjects ('drone', 'navigation')
    must abstain even when 'traditional' appears in a retrieved passage.
    """
    monkeypatch.setattr("app.config.ALLOW_SYNTHETIC_DEMO", True)
    monkeypatch.setattr("app.api.routes.answer.ALLOW_SYNTHETIC_DEMO", True)
    payload = {
        "query": "Is drone navigation using traditional Indian techniques patentable in India?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained", (
        "Query with unsupported subject terms ('drone', 'navigation') must abstain "
        "even when 'traditional' appears in a retrieved passage."
    )
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert len(data["evidence"]) == 0


def test_answer_public_request_cannot_relax_evidence_gate_by_sending_false(client: TestClient):
    """
    Evidence Gate Regression (Finding 2):
    An ordinary public request cannot relax the evidence gate by passing require_approved_evidence=false.
    The public API contract does not permit caller overrides; the route enforces approved evidence.
    With only synthetic fixtures in the database, the public endpoint must cleanly abstain.
    """
    payload = {
        "query": "Is traditional knowledge patentable under Section 3(p)?",
        "jurisdiction": "India",
        "language": "en",
        "require_approved_evidence": False,  # caller attempts to bypass
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained", (
        "Ordinary public request must abstain when only synthetic fixtures exist; "
        "caller cannot relax the evidence gate by passing require_approved_evidence=False."
    )
    assert data["evidence_status"] == "insufficient"
    assert data["is_synthetic_fixture"] is False
    assert len(data["claims"]) == 0
    assert len(data["evidence"]) == 0
    assert not any(
        e.get("is_synthetic") for e in data.get("evidence", [])
    ), "Synthetic passages must never appear in an ordinary public answer."


def test_answer_production_mode_abstains_when_only_synthetic_fixtures_exist(client: TestClient):
    """
    Synthetic Gate: Default public API call excludes synthetic fixtures.
    If no reviewed non-synthetic evidence exists, the endpoint must abstain.
    """
    payload = {
        "query": "Is traditional knowledge patentable in India?",
        "jurisdiction": "India",
        "language": "en",
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "abstained"
    assert data["evidence_status"] == "insufficient"
    assert data["is_synthetic_fixture"] is False
    assert len(data["claims"]) == 0
    assert len(data["evidence"]) == 0
    assert "synthetic" in data["answer_text"].lower() or "abstains" in data["answer_text"].lower()
