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
8. Answerability gate enforces that all material subject constraints must match (Finding 1).
9. Default mode excludes synthetic fixtures without explicit server-side override (Finding 2).
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
        require_approved_evidence=False,  # allow synthetic fixtures for retrieval test
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
        require_approved_evidence=False,  # allow synthetic fixtures for retrieval test
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
        require_approved_evidence=False,
    )
    assert all(p.jurisdiction == "India" for p in india_passages)
    assert not any(p.passage_id == "SYNTH-PASS-INT-001" for p in india_passages)

    # International query must NOT return India-only passages
    int_passages = adapter.search_passages(
        query="Section 3(p) Patents Act India",
        jurisdiction=JurisdictionEnum.INTERNATIONAL,
        limit=5,
        require_approved_evidence=False,
    )
    assert all(p.jurisdiction == "International" for p in int_passages)
    assert not any(p.passage_id == "SYNTH-PASS-001" for p in int_passages)


def test_fts5_adapter_excludes_unactivated_preliminary_rows(db_conn: sqlite3.Connection):
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    passages = adapter.search_passages(
        query="traditional knowledge biological diversity",
        jurisdiction=JurisdictionEnum.INDIA,
        limit=20,
        require_approved_evidence=False,
    )
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
        query="Is traditional knowledge patentable under Section 3(p) in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req, require_approved_evidence=False)
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
    )
    result = adapter.generate_answer(req, require_approved_evidence=False)
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
        )
        result = adapter.generate_answer(req, require_approved_evidence=True)
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
    query_with_syntax = 'patent* AND ("traditional" OR [knowledge]): s.3(p)!'
    passages = adapter.search_passages(
        query=query_with_syntax,
        jurisdiction=JurisdictionEnum.INDIA,
        limit=5,
        require_approved_evidence=False,
    )
    assert isinstance(passages, list)


def test_fts5_adapter_unsupported_drone_navigation_under_matching_locator_abstains(db_conn: sqlite3.Connection):
    """
    Answerability Gate Regression (Finding 1):
    Query: 'Is drone navigation patentable under Section 3(p)?'
    With Section 3(p) in the retrieved pool, locator matches 3(p), but 'drone' and 'navigation'
    are unsupported. The adapter must reject the passage and abstain.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is drone navigation patentable under Section 3(p)?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req, require_approved_evidence=False)
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Query with unsupported subject terms ('drone', 'navigation') must abstain "
        "even when a matching statutory locator like Section 3(p) is present."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.evidence) == 0


def test_fts5_adapter_unsupported_drone_with_matching_traditional_terms_abstains(db_conn: sqlite3.Connection):
    """
    Answerability Gate Regression (Finding 1):
    Query: 'Is drone traditional knowledge patentable in India?'
    Even though 'traditional' and 'knowledge' match Section 3(p), the material subject
    constraint 'drone' is not addressed by any passage in the pool.
    The adapter must force abstention.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is drone traditional knowledge patentable in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req, require_approved_evidence=False)
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Query with unsupported subject constraint 'drone' must abstain "
        "even when other subject terms ('traditional', 'knowledge') match a passage."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.evidence) == 0


def test_fts5_adapter_drone_query_with_traditional_term_abstains(db_conn: sqlite3.Connection):
    """
    Answerability Gate Regression: A query with unsupported primary subjects ('drone', 'navigation')
    must abstain even when 'traditional' appears in a retrieved passage.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is drone navigation using traditional Indian techniques patentable in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req, require_approved_evidence=False)
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Query with unsupported subject terms ('drone', 'navigation') must abstain "
        "even when 'traditional' appears in a retrieved passage."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert len(result.evidence) == 0


def test_fts5_adapter_default_mode_excludes_synthetic(db_conn: sqlite3.Connection):
    """
    Finding 2 Regression — System is the safety gate on evidence quality:
    Calling generate_answer with default require_approved_evidence=True must exclude synthetic fixtures.
    When only synthetic passages exist in the corpus, the adapter must abstain rather than
    surfacing synthetic data as approved legal evidence.
    """
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is traditional knowledge patentable under Section 3(p) in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req)  # default require_approved_evidence=True
    assert result.status == AnswerStatusEnum.ABSTAINED, (
        "Default adapter call must abstain when only synthetic fixtures exist; "
        "the system must not expose synthetic data as approved legal evidence."
    )
    assert result.evidence_status == EvidenceStatusEnum.INSUFFICIENT
    assert len(result.claims) == 0
    assert all(not p.is_synthetic for p in result.evidence)
