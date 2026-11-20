"""
Query engine adapter interface and SQLite FTS5 implementation (Task Su-02).

Provides a stable query adapter interface bridging the FastAPI service layer
to local evidence retrieval and answer synthesis.

Key architectural invariants:
1. Strict jurisdiction isolation: India queries only search India passages;
   International queries only search International passages.
2. Strict activation gate: Only approved/activated corpus rows (activated = 1)
   can be retrieved for answer synthesis.
3. Grounded claims: Every emitted claim's evidence_ids strictly map to retrieved
   and cited passages.
4. Safe abstention: Zero approved evidence matches result in clean abstention
   (status="abstained", evidence_status="insufficient", empty claims).
"""

from abc import ABC, abstractmethod
import re
import sqlite3
from typing import List, Optional, Tuple
from fastapi import Depends

from ..db.database import get_db
from ..models.schemas import (
    AnswerRequest,
    AnswerResult,
    AnswerStatusEnum,
    EvidencePassage,
    EvidenceStatusEnum,
    JurisdictionEnum,
    LanguageEnum,
    Claim,
    Intake,
)

_STOPWORDS = {
    "is", "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or",
    "what", "how", "where", "when", "why", "which", "who", "under", "about",
    "with", "be", "are", "do", "does", "can", "could", "should", "would",
    "by", "from", "as", "into", "through", "during", "before", "after",
}


def _tokenize_query(query: str) -> List[str]:
    """Extracts search terms, filtering stopwords and expanding common legal/patent stems."""
    tokens = re.findall(r"\b[a-zA-Z0-9_-]+\b", query.lower())
    meaningful = [t for t in tokens if t not in _STOPWORDS and len(t) > 1]
    expanded = []
    for t in meaningful:
        expanded.append(f"{t}*")
        # Add root for common legal/regulatory suffixes
        if t.endswith("able") and len(t) > 5:
            expanded.append(f"{t[:-4]}*")
        elif t.endswith("ability") and len(t) > 8:
            expanded.append(f"{t[:-7]}*")
        elif t.endswith("ation") and len(t) > 6:
            expanded.append(f"{t[:-5]}*")
    return expanded[:12]


class QueryEngineAdapter(ABC):
    """Abstract base class defining the contract for query and retrieval engines."""

    @abstractmethod
    def search_passages(
        self,
        query: str,
        jurisdiction: JurisdictionEnum,
        limit: int = 5,
    ) -> List[EvidencePassage]:
        """Retrieves activated evidence passages matching the query and jurisdiction."""
        pass

    @abstractmethod
    def generate_answer(
        self,
        request: AnswerRequest,
    ) -> AnswerResult:
        """Synthesizes an evidence-grounded answer or cleanly abstains if no evidence is found."""
        pass


class SQLiteFTS5QueryAdapter(QueryEngineAdapter):
    """Concrete query engine adapter backed by SQLite FTS5 index and relational database."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def search_passages(
        self,
        query: str,
        jurisdiction: JurisdictionEnum,
        limit: int = 5,
    ) -> List[EvidencePassage]:
        """
        Executes full-text retrieval on passages_fts joined with passages table.
        Strictly enforces:
        - p.jurisdiction = jurisdiction.value
        - p.activated = 1 (preliminary corpus rows are excluded)
        """
        terms = _tokenize_query(query)
        if not terms:
            return []

        fts_expression = " OR ".join(terms)
        passages: List[EvidencePassage] = []

        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                SELECT p.passage_id, p.source_id, p.jurisdiction, p.authority,
                       p.document_title, p.locator, p.paraphrased_content,
                       p.source_url, p.source_type, p.review_status,
                       p.review_note, p.is_synthetic, p.activated,
                       bm25(passages_fts) as rank
                FROM passages_fts
                JOIN passages p ON p.rowid = passages_fts.rowid
                WHERE passages_fts MATCH ?
                  AND p.jurisdiction = ?
                  AND p.activated = 1
                ORDER BY rank
                LIMIT ?
                """,
                (fts_expression, jurisdiction.value, limit),
            )
            rows = cur.fetchall()
            for r in rows:
                passages.append(
                    EvidencePassage(
                        passage_id=r["passage_id"],
                        source_id=r["source_id"],
                        jurisdiction=r["jurisdiction"],
                        authority=r["authority"],
                        document_title=r["document_title"],
                        locator=r["locator"],
                        paraphrased_content=r["paraphrased_content"],
                        source_url=r["source_url"],
                        source_type=r["source_type"],
                        review_status=r["review_status"],
                        review_note=r["review_note"],
                        is_synthetic=bool(r["is_synthetic"]),
                    )
                )
        except sqlite3.OperationalError:
            # Fallback to token LIKE if FTS syntax edge case occurs
            passages = self._fallback_like_search(terms, jurisdiction, limit)

        return passages

    def _fallback_like_search(
        self,
        terms: List[str],
        jurisdiction: JurisdictionEnum,
        limit: int = 5,
    ) -> List[EvidencePassage]:
        """Graceful fallback search when FTS syntax encounters special characters."""
        cur = self.conn.cursor()
        clean_terms = [t.rstrip("*") for t in terms[:4]]
        if not clean_terms:
            return []

        like_clauses = " OR ".join(["p.paraphrased_content LIKE ? OR p.document_title LIKE ?" for _ in clean_terms])
        params = []
        for ct in clean_terms:
            params.extend([f"%{ct}%", f"%{ct}%"])
        params.extend([jurisdiction.value, limit])

        sql = f"""
            SELECT p.passage_id, p.source_id, p.jurisdiction, p.authority,
                   p.document_title, p.locator, p.paraphrased_content,
                   p.source_url, p.source_type, p.review_status,
                   p.review_note, p.is_synthetic, p.activated
            FROM passages p
            WHERE ({like_clauses})
              AND p.jurisdiction = ?
              AND p.activated = 1
            LIMIT ?
        """
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        return [
            EvidencePassage(
                passage_id=r["passage_id"],
                source_id=r["source_id"],
                jurisdiction=r["jurisdiction"],
                authority=r["authority"],
                document_title=r["document_title"],
                locator=r["locator"],
                paraphrased_content=r["paraphrased_content"],
                source_url=r["source_url"],
                source_type=r["source_type"],
                review_status=r["review_status"],
                review_note=r["review_note"],
                is_synthetic=bool(r["is_synthetic"]),
            )
            for r in rows
        ]

    def generate_answer(
        self,
        request: AnswerRequest,
    ) -> AnswerResult:
        """
        Retrieves matching approved evidence passages and synthesizes a grounded response.
        Enforces clean abstention if no matching approved passages exist.
        """
        passages = self.search_passages(
            query=request.query,
            jurisdiction=request.jurisdiction,
            limit=5,
        )

        provisional_class = (
            request.intake.provisional_route
            if request.intake and hasattr(request.intake, "provisional_route")
            else None
        )

        # --- Case 1: Zero evidence found -> Clean Abstention ---
        if not passages:
            return AnswerResult(
                status=AnswerStatusEnum.ABSTAINED,
                jurisdiction=request.jurisdiction,
                language=request.language,
                provisional_class=provisional_class,
                answer_text=(
                    f"No approved statutory or regulatory evidence was found in the indexed corpus "
                    f"for the query under {request.jurisdiction.value} jurisdiction. To prevent "
                    "hallucination and ensure legal safety, the system abstains from answering without "
                    "verified source provisions. Please consult an IP attorney or refer to official gazettes."
                ),
                assumptions=[
                    "No matching passages with activated=1 status exist for this inquiry.",
                    "Strict safety gate prevents ungrounded legal assertions.",
                ],
                claims=[],
                cited_provisions=[],
                evidence=[],
                limitations=[
                    "Abstained due to absence of verified statutory evidence.",
                    "Informational guidance only; does not constitute formal legal counsel.",
                ],
                evidence_status=EvidenceStatusEnum.INSUFFICIENT,
                corpus_version="v0.2-fts5-adapter",
                model_version="fts5-retrieval-adapter-v1",
                is_synthetic_fixture=True,
            )

        # --- Case 2: Matching Evidence Found -> Evidence-Grounded Answer ---
        claims: List[Claim] = []
        cited_provisions: List[str] = []
        synthesis_points: List[str] = []

        for idx, p in enumerate(passages, start=1):
            claim_id = f"CLAIM-{p.passage_id}"
            claims.append(
                Claim(
                    claim_id=claim_id,
                    claim_text=p.paraphrased_content,
                    evidence_ids=[p.passage_id],
                )
            )
            provision_locator = f"{p.document_title}, {p.locator}"
            if provision_locator not in cited_provisions:
                cited_provisions.append(provision_locator)
            synthesis_points.append(f"- Under {p.document_title} ({p.locator}): {p.paraphrased_content}")

        if request.jurisdiction == JurisdictionEnum.INTERNATIONAL:
            evidence_status = EvidenceStatusEnum.PARTIAL
            header = (
                "[INTERNATIONAL JURISDICTION - RETRIEVED STATUTORY EVIDENCE]\n"
                "At the international level, multilateral treaties establish traditional knowledge "
                "and genetic resource disclosure principles:\n\n"
            )
        else:
            evidence_status = EvidenceStatusEnum.SUPPORTED
            header = (
                "[INDIA JURISDICTION - RETRIEVED STATUTORY EVIDENCE]\n"
                "Under Indian statutory framework, the following relevant provisions were retrieved:\n\n"
            )

        answer_text = header + "\n\n".join(synthesis_points)

        assumptions = [
            f"Query matched {len(passages)} activated statutory evidence passage(s) in local index.",
            "Evidence is constrained strictly to the selected jurisdiction.",
        ]

        limitations = [
            "Informational guidance only; not formal legal advice, patent certification, or regulatory clearance.",
            "Statutory interpretation depends on official gazette notifications and court precedents.",
            "Synthesized from activated passages via the Su-02 retrieval adapter.",
        ]

        return AnswerResult(
            status=AnswerStatusEnum.ANSWERED,
            jurisdiction=request.jurisdiction,
            language=request.language,
            provisional_class=provisional_class,
            answer_text=answer_text,
            assumptions=assumptions,
            claims=claims,
            cited_provisions=cited_provisions,
            evidence=passages,
            limitations=limitations,
            evidence_status=evidence_status,
            corpus_version="v0.2-fts5-adapter",
            model_version="fts5-retrieval-adapter-v1",
            is_synthetic_fixture=any(p.is_synthetic for p in passages),
        )


def get_query_adapter(
    conn: sqlite3.Connection = Depends(get_db),
) -> QueryEngineAdapter:
    """FastAPI dependency provider for the active query engine adapter."""
    return SQLiteFTS5QueryAdapter(conn)
