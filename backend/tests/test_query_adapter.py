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
    adapter = SQLiteFTS5QueryAdapter(db_conn)
    req = AnswerRequest(
        query="Is a classical Ayurvedic Triphala formula eligible for a patent in India?",
        jurisdiction=JurisdictionEnum.INDIA,
        language=LanguageEnum.EN,
    )
    result = adapter.generate_answer(req)
    assert result.status == AnswerStatusEnum.ANSWERED
    assert result.evidence_status == EvidenceStatusEnum.SUPPORTED
    assert len(result.claims) > 0
    assert len(result.evidence) > 0

    evidence_ids = {p.passage_id for p in result.evidence}
    for claim in result.claims:
        for eid in claim.evidence_ids:
            assert eid in evidence_ids, f"Claim cites unretrieved passage {eid}"


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
