"""
Tests for answer generation endpoint (Task Su-01, Su-02).
Updated after PR #7 review fixes:
- require_approved_evidence now defaults to True in AnswerRequest.
  Demo/synthetic-path tests must pass require_approved_evidence=False explicitly.
- Answerability gate now requires ALL substantive terms (or n-1 for 3+ terms) to match.
"""

from pathlib import Path
from fastapi.testclient import TestClient
from app.db.database import get_db_connection


def test_answer_india_patent_query_success(client: TestClient):
    """
    Demo mode (require_approved_evidence=False): synthetic fixtures are allowed.
    Synthetic fixtures are NEVER marked as 'supported'; evidence_status must be 'partial'.
    """
    payload = {
        "query": "Is a classical Triphala formulation patentable in India?",
        "jurisdiction": "India",
        "language": "en",
        "require_approved_evidence": False,  # explicit demo/synthetic mode
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
    assert any("Section 3" in p for p in data["cited_provisions"]), (
        "Demo-mode answer must cite at least one statutory Section 3 provision."
    )
    assert len(data["limitations"]) > 0


def test_answer_international_query_uses_international_fixture(client: TestClient):
    """
    FIX-1: International answers must cite SYNTH-PASS-INT-001 (not India-only SYNTH-PASS-001)
    and must have evidence_status=partial (not supported).
    Uses require_approved_evidence=False for demo/synthetic path.
    """
    payload = {
        "query": "What international treaties govern patent disclosure of traditional knowledge?",
        "jurisdiction": "International",
        "language": "en",
        "require_approved_evidence": False,  # explicit demo/synthetic mode
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
        "language": "en",
        "require_approved_evidence": False,  # explicit demo/synthetic mode
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
    The status value (answered or abstained) is not privacy-sensitive and is not asserted.
    """
    secret_query = "Confidential classical formulation patent query about SecretIngredientX"
    payload = {
        "query": secret_query,
        "jurisdiction": "India",
        "language": "en",
        "require_approved_evidence": False,  # explicit demo/synthetic mode
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
    # Privacy gate: secret formulation text must never be persisted in audit log
    assert "SecretIngredientX" not in all_audit_text
    assert "Confidential classical formulation" not in all_audit_text


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


def test_answer_mixed_legal_term_with_unsupported_subject_abstains(client: TestClient):
    """
    Answerability Gate Regression: Mixed query with a common procedural legal word
    ('patentable', 'India') plus an unsupported subject ('quantum cryptography')
    must abstain and not generate claims or false 'supported' legal answers.
    """
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


def test_answer_production_mode_abstains_when_only_synthetic_fixtures_exist(client: TestClient):
    """
    Synthetic Gate: Default public API call (require_approved_evidence=True by default)
    excludes synthetic fixtures. If no reviewed non-synthetic evidence exists, the endpoint
    must abstain.
    """
    payload = {
        "query": "Is a classical Triphala formulation patentable in India?",
        "jurisdiction": "India",
        "language": "en",
        # require_approved_evidence omitted — defaults to True (the production default)
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


def test_answer_drone_navigation_with_traditional_term_abstains(client: TestClient):
    """
    BLOCKER-1 Regression: A query whose unsupported primary subject ('drone', 'navigation')
    is not addressed by any indexed passage must abstain, even though the word 'traditional'
    happens to appear as a synonym in the passage text.

    Before the fix, _DOMAIN_SYNONYMS caused 'traditional' to match via synonym expansion and
    the answerability gate returned True for ANY one matching term.
    After the fix, ALL substantive terms must match — 'drone' and 'navigation' are absent
    from indexed provisions, so the gate correctly abstains.
    """
    payload = {
        "query": "Is drone navigation using traditional Indian techniques patentable in India?",
        "jurisdiction": "India",
        "language": "en",
        "require_approved_evidence": False,  # allow synthetic pool, so retrieval can run
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


def test_answer_default_excludes_synthetic_without_explicit_flag(client: TestClient):
    """
    BLOCKER-2 Regression: Calling the public answer endpoint with NO require_approved_evidence
    flag (relying on the default) must exclude synthetic fixtures from the evidence pool.
    If only synthetic fixtures exist in the corpus, the endpoint must abstain.
    This verifies that the system — not the caller — is the safety gate on evidence quality.
    """
    payload = {
        "query": "Is classical Triphala Churna eligible for patent protection in India?",
        "jurisdiction": "India",
        "language": "en",
        # No require_approved_evidence field — must default to True
    }
    response = client.post("/api/v1/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    # With only synthetic fixtures in the corpus, default-mode must abstain
    assert data["status"] == "abstained", (
        "Default public API call must abstain when only synthetic fixtures exist; "
        "the system must not expose synthetic data as approved legal evidence."
    )
    assert data["evidence_status"] == "insufficient"
    assert len(data["claims"]) == 0
    assert not any(
        e.get("is_synthetic") for e in data.get("evidence", [])
    ), "Synthetic passages must never appear in a default-mode public answer."

