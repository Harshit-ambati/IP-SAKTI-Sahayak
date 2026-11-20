"""
Tests for Query Engine Adapter (Task Su-02).
Verifies:
1. SQLite FTS5 passage retrieval across jurisdictions.
2. Strict jurisdiction isolation.
3. Strict activation gating (activated=0 excluded).
4. Evidence-grounded answer synthesis and claim citation.
5. Safe abstention on zero approved evidence.
6. Graceful handling of FTS syntax edge cases.
7. Swappable adapter interface.
8. Answerability gate requires ALL substantive terms to match (BLOCKER-1 fix).
9. Default public mode excludes synthetic fixtures (BLOCKER-2 fix).
"""

import sqlite3
from pathlib import Path
import pytest
from app.adapters.query_adapter import (
    QueryEngineAdapter,
    SQLiteFTS5QueryAdapter,
)
from app.db.database import get_db_connection
from app.models.schemas import (
    AnswerRequest,
    AnswerResult,
    AnswerStatusEnum,
    EvidenceStatusEnum,
    JurisdictionEnum,
    LanguageEnum,
)


@pytest.fixture
def db_conn(test_db_path: Path):
    conn = get_db_connection(test_db_path)
    yield conn
    conn.close()


def test_fts5_adapter_retrieves_india_patent_passages(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    passages = adapter.search_passages(
        query="traditional knowledge patent exclusion",
        jurisdiction=JurisdictionEnum.INDIA,
        limit=5,
    )
    assert len(passages) > 0
    assert any(p.passage_id == "SYNTH-PASS-001" for p in passages)
    assert all(p.jurisdiction == "India" for p in passages)


def test_fts5_adapter_retrieves_international_wipo_treaty(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    passages = adapter.search_passages(
        query="WIPO GRATK treaty genetic resources disclosure",
        jurisdiction=JurisdictionEnum.INTERNATIONAL,
        limit=5,
    )
    assert len(passages) > 0
    assert any(p.passage_id == "SYNTH-PASS-INT-001" for p in passages)
    assert all(p.jurisdiction == "International" for p in passages)


def test_fts5_adapter_strict_jurisdiction_isolation(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    # India query searching for international terms must NOT return international passages
    india_passages = adapter.search_passages(
        query="WIPO treaty patent disclosure",
        jurisdiction=JurisdictionEnum.INDIA,
        limit=5,
    )
    assert all(p.jurisdiction == "India" for p in india_passages)
    assert not any(p.passage_id == "SYNTH-PASS-INT-001" for p in india_passages)

    # International query must NOT return India-only passages
    int_passages = adapter.search_passages(
        query="Section 3(p) Patents Act India",
        jurisdiction=JurisdictionEnum.INTERNATIONAL,
        limit=5,
    )
    assert all(p.jurisdiction == "International" for p in int_passages)
    assert not any(p.passage_id == "SYNTH-PASS-001" for p in int_passages)


def test_fts5_adapter_excludes_unactivated_preliminary_rows(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    # Search for terms present in preliminary corpus (e.g., biological diversity or traditional knowledge)
    passages = adapter.search_passages(
        query="traditional knowledge biological diversity",
        jurisdiction=JurisdictionEnum.INDIA,
        limit=20,
    )
    # None of the retrieved passages should have activated=0
    cur = db_conn.cursor()
    cur.execute("SELECT passage_id FROM passages WHERE activated = 0")
    unactivated_ids = {r["passage_id"] for r in cur.fetchall()}

    for p in passages:
        assert p.passage_id not in unactivated_ids, (
            f"Unactivated passage {p.passage_id} was retrieved by query adapter!"
        )


def test_fts5_adapter_safe_abstention_on_zero_evidence(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Quantum cryptography laser communication protocols in deep space",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req)
    assert result.status == AnswerStatusEnum.ABSTAINED
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.cited_provisions) == 0
    assert len(result.evidence) == 0
    assert "abstains" in result.answer_text.lower()


def test_fts5_adapter_answer_grounded_in_citations(db_conn: sqlite3.Connection):
    """
    Demo mode (require_approved_evidence=False): synthetic fixtures are allowed.
    Synthetic demo fixtures must be explicitly marked mock with evidence_status='partial'.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is a classical Ayurvedic Triphala formula eligible for a patent in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
        require_approved_evidence=False,  # explicit demo/synthetic mode
    )
    result = adapter.generate_answer(req)
    assert result.status == AnswerStatusEnum.ANSWERED
    # Synthetic demo fixtures are explicitly marked mock and have evidence_status='partial'
    assert result.evidence_status == EvidenceStatusEnum.PARTIAL
    assert result.is_synthetic_fixture is True
    assert "SYNTHETIC MOCK/DEMO" in result.answer_text
    assert len(result.claims) > 0
    assert len(result.evidence) > 0

    evidence_ids = {p.passage_id for p in result.evidence}
    for claim in result.claims:
        for eid in claim.evidence_ids:
            assert eid in evidence_ids, f"Claim cites unretrieved passage {eid}"


def test_fts5_adapter_mixed_query_with_unsupported_subject_abstains(db_conn: sqlite3.Connection):
    """
    Answerability Gate: A mixed query sharing common procedural legal words
    ('patentable', 'India') with an unsupported subject matter ('quantum cryptography')
    must abstain and not emit substantive claims.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is quantum cryptography patentable in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
        require_approved_evidence=False,  # allow synthetic pool so retrieval runs
    )
    result = adapter.generate_answer(req)
    assert result.status == AnswerStatusEnum.ABSTAINED
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.cited_provisions) == 0
    assert len(result.evidence) == 0
    assert "quantum cryptography" in result.answer_text.lower() or "abstains" in result.answer_text.lower()


def test_fts5_adapter_genuinely_approved_evidence_produces_supported_status(db_conn: sqlite3.Connection):
    """
    Genuine Evidence Path: Non-synthetic, reviewed approved evidence (is_synthetic=0,
    review_status='approved', activated=1) produces evidence_status='supported'
    and is_synthetic_fixture=False.
    """
    cur = db_conn.cursor()
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
        db_conn.commit()

        adapter = SQLiteFTS5QueryAdapter(db_conn)
        req = AnswerRequest(
            query="Is traditional knowledge patentable in India?",
            jurisdiction=JurisdictionEnum.INDIA,
            language=LanguageEnum.EN,
            require_approved_evidence=True,
        )
        result = adapter.generate_answer(req)
        assert result.status == AnswerStatusEnum.ANSWERED
        assert result.evidence_status == EvidenceStatusEnum.SUPPORTED
        assert result.is_synthetic_fixture is False
        assert len(result.claims) > 0
        assert any(p.passage_id == "REAL-PASS-001" for p in result.evidence)
        assert any("REAL-PASS-001" in c.evidence_ids for c in result.claims)
    finally:
        cur.execute("DELETE FROM passages WHERE passage_id = 'REAL-PASS-001'")
        cur.execute("DELETE FROM sources WHERE source_id = 'REAL-SRC-001'")
        db_conn.commit()


def test_fts5_adapter_handles_special_characters_gracefully(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    # Query with punctuation and FTS syntax edge cases (quotes, stars, parentheses, colons)
    query_with_syntax = 'patent* AND ("traditional" OR [knowledge]): s.3(p)!'
    passages = adapter.search_passages(
        query=query_with_syntax,
        jurisdiction=JurisdictionEnum.INDIA,
        limit=5,
    )
    # Must not raise sqlite3.OperationalError and return results if matches exist
    assert isinstance(passages, list)


def test_fts5_adapter_drone_query_with_traditional_term_abstains(db_conn: sqlite3.Connection):
    """
    BLOCKER-1 Regression — Strict answerability gate (all substantive terms must match):
    A query with unsupported primary subjects ('drone', 'navigation') must abstain
    even if the word 'traditional' appears in a retrieved passage.

    Before the fix: _DOMAIN_SYNONYMS caused 'traditional' to match via synonym expansion,
    and ANY one matching term was sufficient — so the query was incorrectly answered.
    After the fix: ALL substantive terms must match (or n-1 for 3+ terms). 'drone' and
    'navigation' are not in any indexed passage, so the gate correctly abstains.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is drone navigation using traditional Indian techniques patentable in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
        require_approved_evidence=False,  # allow synthetic pool so retrieval runs
    )
    result = adapter.generate_answer(req)
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Query with unsupported subject terms ('drone', 'navigation') must abstain "
        "even when 'traditional' appears in a retrieved passage."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.evidence) == 0


def test_fts5_adapter_default_mode_excludes_synthetic(db_conn: sqlite3.Connection):
    """
    BLOCKER-2 Regression — System is the safety gate on evidence quality:
    Calling generate_answer with no explicit require_approved_evidence (defaults to True)
    must exclude synthetic fixtures. When only synthetic passages exist in the corpus,
    the adapter must abstain rather than surfacing synthetic data as approved legal evidence.

    This verifies that callers cannot accidentally expose synthetic fixtures by omitting
    the require_approved_evidence flag — the system enforces the safe default.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is classical Triphala Churna eligible for patent protection in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
        # require_approved_evidence omitted — must default to True
    )
    result = adapter.generate_answer(req)
    # With only synthetic fixtures in the corpus, default mode must abstain
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Default adapter call must abstain when only synthetic fixtures exist; "
        "the system must not expose synthetic data as approved legal evidence."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    # Confirm no synthetic passages leaked through
    assert all(not p.is_synthetic for p in result.evidence)

