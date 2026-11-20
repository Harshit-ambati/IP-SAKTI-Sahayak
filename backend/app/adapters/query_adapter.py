"""
Query engine adapter interface and SQLite FTS5 implementation (Task Su-02).

Provides a stable query adapter interface bridging the FastAPI service layer
to local evidence retrieval and answer synthesis.

Key architectural invariants:
1. Strict jurisdiction isolation: India queries only search India passages;
   International queries only search International passages.
2. Strict activation gate: Only approved/activated corpus rows (activated = 1)
   can be retrieved for answer synthesis.
3. Answerability gate: Verifies that candidate retrieved passages materially support
   the substantive subject matter of the query, rather than merely sharing generic
   legal/procedural tokens (e.g. 'patent', 'india'). Mixed irrelevant queries cleanly abstain.
4. Synthetic fixture isolation: Synthetic demo passages are NEVER marked as 'supported'
   legal evidence. Responses derived from synthetic fixtures are explicitly labelled mock/demo
   and receive evidence_status='partial'. Normal answer use requiring approved non-synthetic
   evidence (require_approved_evidence=True) abstains if only synthetic fixtures exist.
5. Grounded claims: Every emitted claim's evidence_ids strictly map to retrieved
   and cited passages.
6. Safe abstention: Zero approved evidence matches result in clean abstention
   (status="abstained", evidence_status="insufficient", empty claims).
"""

from abc import ABC, abstractmethod
import math
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
    "it", "its", "this", "that", "these", "those", "have", "has", "had",
}

_PROCEDURAL_TERMS = {
    "patent", "patents", "patentable", "patenting", "patentability", "patented",
    "trademark", "trademarks", "copyright", "copyrights",
    "law", "laws", "act", "acts", "section", "sections", "sec",
    "rule", "rules", "regulation", "regulations", "provision", "provisions",
    "india", "indian", "international", "overview", "wipo", "treaty", "treaties",
    "legal", "statute", "statutory", "query", "question",
    "product", "products", "formula", "formulas", "formulation", "formulations",
    "eligible", "eligibility", "govern", "governed", "governing",
    "applicable", "apply", "requirement", "requirements", "compliance", "comply",
    "approved", "unapproved", "status", "test", "demo", "sample", "example",
}


def _tokenize_query(query: str) -> List[str]:
    """Extracts search terms, filtering stopwords and expanding common legal/patent stems."""
    tokens = re.findall(r"\b[a-zA-Z0-9_-]+\b", query.lower())
    meaningful = [t for t in tokens if t not in _STOPWORDS and len(t) > 1]
    expanded = []
    for t in meaningful:
        expanded.append(f"{t}*")
        if t.endswith("able") and len(t) > 5:
            expanded.append(f"{t[:-4]}*")
        elif t.endswith("ability") and len(t) > 8:
            expanded.append(f"{t[:-7]}*")
        elif t.endswith("ation") and len(t) > 6:
            expanded.append(f"{t[:-5]}*")
    return expanded[:12]


def _extract_substantive_terms(query: str) -> List[str]:
    """Extracts non-procedural substantive subject matter terms from the query."""
    words = re.findall(r"\b[a-zA-Z0-9_-]+\b", query.lower())
    return [w for w in words if w not in _STOPWORDS and w not in _PROCEDURAL_TERMS and len(w) > 2]


def _extract_locators(query: str) -> List[str]:
    """Extracts explicit statutory locators like 3(p), 3(a), 2(b) from query."""
    return re.findall(r"\b\d+\([a-zA-Z0-9]+\)", query.lower())


def _passage_supports_query(
    passage: EvidencePassage,
    substantive_terms: List[str],
    locators: List[str],
) -> bool:
    """
    Answerability Gate: checks if a candidate retrieved passage materially supports
    the substantive question by requiring that a strict majority of substantive terms
    are present in the passage text via stem matching.

    Threshold:
    - 1 term  → 1 must match (all)
    - 2 terms → 1 must match (majority, ceil(2/2))
    - 3 terms → 2 must match (majority, ceil(3/2))
    - 4 terms → 2 must match (majority, ceil(4/2))
    - 5 terms → 3 must match (majority, ceil(5/2))
    - …

    Domain synonym expansion is intentionally excluded: synonym expansion can cause
    false support (e.g. 'traditional' matching for 'drone navigation' queries because
    _DOMAIN_SYNONYMS['traditional'] included 'traditional' itself).  Only direct
    stem matching against passage text is used.
    """
    passage_text = f"{passage.document_title} {passage.locator} {passage.paraphrased_content}".lower()

    # 1. Explicit statutory locator match always supports (e.g. '3(p)' in query)
    for loc in locators:
        if loc in passage.locator.lower():
            return True

    # 2. No substantive terms and no locators — cannot verify answerability
    if not substantive_terms:
        return False

    # 3. Count how many substantive terms have a stem match in the passage text
    matched = sum(
        1 for term in substantive_terms
        if (term[:4] if len(term) >= 5 else term) in passage_text
    )

    # Require a strict majority (ceil(n/2)) to match.
    # This prevents a single coincidental synonym from creating false answerability,
    # while allowing queries where the dominant substantive terms are grounded.
    required = math.ceil(len(substantive_terms) / 2)
    return matched >= required


class QueryEngineAdapter(ABC):
    """Abstract base class defining the contract for query and retrieval engines."""

    @abstractmethod
    def search_passages(
        self,
        query: str,
        jurisdiction: JurisdictionEnum,
        limit: int = 5,
        require_approved_evidence: bool = False,
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
        require_approved_evidence: bool = False,
    ) -> List[EvidencePassage]:
        """
        Executes full-text retrieval on passages_fts joined with passages table.
        Strictly enforces:
        - p.jurisdiction = jurisdiction.value
        - p.activated = 1 (preliminary corpus rows are excluded)
        - If require_approved_evidence=True: p.is_synthetic = 0 AND p.review_status = 'approved'
        """
        terms = _tokenize_query(query)
        if not terms:
            return []

        fts_expression = " OR ".join(terms)
        passages: List[EvidencePassage] = []

        synthetic_filter = "AND p.is_synthetic = 0 AND p.review_status = 'approved'" if require_approved_evidence else ""

        try:
            cur = self.conn.cursor()
            cur.execute(
                f"""
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
                  {synthetic_filter}
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
            passages = self._fallback_like_search(terms, jurisdiction, limit, require_approved_evidence)

        return passages

    def _fallback_like_search(
        self,
        terms: List[str],
        jurisdiction: JurisdictionEnum,
        limit: int = 5,
        require_approved_evidence: bool = False,
    ) -> List[EvidencePassage]:
        """Graceful fallback search when FTS syntax encounters special characters."""
        cur = self.conn.cursor()
        clean_terms = [t.rstrip("*") for t in terms[:4]]
        if not clean_terms:
            return []

        like_clauses = " OR ".join(["p.paraphrased_content LIKE ? OR p.document_title LIKE ?" for _ in clean_terms])
        synthetic_filter = "AND p.is_synthetic = 0 AND p.review_status = 'approved'" if require_approved_evidence else ""

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
              {synthetic_filter}
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
        Enforces:
        - Answerability Gate: mixed queries with common legal words + unsupported subjects abstain.
        - Strict evidence gate: synthetic fixtures are never marked as 'supported' legal evidence.
        - require_approved_evidence=True abstains if only synthetic fixtures are available.
        """
        provisional_class = (
            request.intake.provisional_route
            if request.intake and hasattr(request.intake, "provisional_route")
            else None
        )

        # 1. Retrieve candidates from index.
        # The public API ALWAYS requires approved non-synthetic evidence.
        # `request.require_approved_evidence` is kept on AnswerRequest for
        # explicit unit-test / demo override only; the production default is True.
        raw_passages = self.search_passages(
            query=request.query,
            jurisdiction=request.jurisdiction,
            limit=5,
            require_approved_evidence=request.require_approved_evidence,
        )

        # 2. Case: Zero passages found in DB
        if not raw_passages:
            reason = (
                f"No reviewed, non-synthetic approved evidence is available in the indexed corpus for this "
                f"question under {request.jurisdiction.value} jurisdiction. Synthetic test fixtures are excluded "
                "from production answers per safety policy. The system abstains."
                if request.require_approved_evidence
                else (
                    f"No approved statutory or regulatory evidence was found in the indexed corpus "
                    f"for the query under {request.jurisdiction.value} jurisdiction. To prevent "
                    "hallucination and ensure legal safety, the system abstains from answering without "
                    "verified source provisions."
                )
            )
            return AnswerResult(
                status=AnswerStatusEnum.ABSTAINED,
                jurisdiction=request.jurisdiction,
                language=request.language,
                provisional_class=provisional_class,
                answer_text=reason,
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
                is_synthetic_fixture=False if request.require_approved_evidence else True,
            )

        # 3. Answerability Gate: Check whether retrieved passages support the substantive query
        substantive_terms = _extract_substantive_terms(request.query)
        locators = _extract_locators(request.query)

        supported_passages = [
            p for p in raw_passages
            if _passage_supports_query(p, substantive_terms, locators)
        ]

        # Mixed query rejection: query has substantive terms, but NONE are addressed by retrieved passages
        if substantive_terms and not supported_passages:
            unsupported_subjects = ", ".join(f"'{t}'" for t in substantive_terms[:3])
            return AnswerResult(
                status=AnswerStatusEnum.ABSTAINED,
                jurisdiction=request.jurisdiction,
                language=request.language,
                provisional_class=provisional_class,
                answer_text=(
                    f"The inquiry concerns subject matter ({unsupported_subjects}) for which no supporting "
                    f"statutory provisions or approved evidence exist in the indexed corpus under {request.jurisdiction.value} "
                    f"jurisdiction. While general or procedural patent provisions exist, they do not address this "
                    "specific subject. The system abstains from generating substantive claims to prevent ungrounded legal advice."
                ),
                assumptions=[
                    f"Query contains substantive subject terms ({unsupported_subjects}) absent from retrieved provisions.",
                    "Answerability gate prevents lexical overlap on procedural words from creating false support.",
                ],
                claims=[],
                cited_provisions=[],
                evidence=[],
                limitations=[
                    "Abstained: Retrieved passages do not address the query's material subject.",
                    "Procedural term overlap alone does not establish legal answerability.",
                ],
                evidence_status=EvidenceStatusEnum.INSUFFICIENT,
                corpus_version="v0.2-fts5-adapter",
                model_version="fts5-retrieval-adapter-v1",
                is_synthetic_fixture=any(p.is_synthetic for p in raw_passages),
            )

        # 4. Synthesize Answer from Supported Passages
        claims: List[Claim] = []
        cited_provisions: List[str] = []
        synthesis_points: List[str] = []

        for p in supported_passages:
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

        is_synthetic = any(p.is_synthetic for p in supported_passages)

        if is_synthetic:
            # Synthetic fixtures are NEVER marked as SUPPORTED legal evidence
            evidence_status = EvidenceStatusEnum.PARTIAL
            header = (
                "[SYNTHETIC MOCK/DEMO - NOT PRODUCTION EVIDENCE]\n"
                "Notice: The following citations are synthetic testing fixtures and do not constitute approved "
                "statutory provisions. These mock citations illustrate retrieval format only:\n\n"
            )
            limitations = [
                "MOCK DEMO NOTICE: This response is derived from synthetic Phase 1 fixtures for skeleton testing.",
                "Synthetic fixtures are NOT approved legal evidence and cannot be relied upon for regulatory or legal decisions.",
                "Informational guidance only; not formal legal advice, patent certification, or regulatory clearance.",
            ]
        else:
            # Genuinely approved non-synthetic evidence
            if request.jurisdiction == JurisdictionEnum.INTERNATIONAL:
                evidence_status = EvidenceStatusEnum.PARTIAL
                header = (
                    "[INTERNATIONAL JURISDICTION - APPROVED MULTILATERAL EVIDENCE]\n"
                    "At the international level, multilateral treaties establish traditional knowledge "
                    "and genetic resource disclosure principles:\n\n"
                )
            else:
                evidence_status = EvidenceStatusEnum.SUPPORTED
                header = (
                    "[INDIA JURISDICTION - APPROVED STATUTORY EVIDENCE]\n"
                    "Under the Indian statutory framework, the following approved provisions were retrieved:\n\n"
                )
            limitations = [
                "Informational guidance only; not formal legal advice, patent certification, or regulatory clearance.",
                "Statutory interpretation depends on official gazette notifications and court precedents.",
                "Synthesized from reviewed, non-synthetic approved passages via the Su-02 retrieval adapter.",
            ]

        answer_text = header + "\n\n".join(synthesis_points)

        assumptions = [
            f"Query matched {len(supported_passages)} activated statutory evidence passage(s) in local index.",
            "Evidence is constrained strictly to the selected jurisdiction.",
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
            evidence=supported_passages,
            limitations=limitations,
            evidence_status=evidence_status,
            corpus_version="v0.2-fts5-adapter",
            model_version="fts5-retrieval-adapter-v1",
            is_synthetic_fixture=is_synthetic,
        )


def get_query_adapter(
    conn: sqlite3.Connection = Depends(get_db),
) -> QueryEngineAdapter:
    """FastAPI dependency provider for the active query engine adapter."""
    return SQLiteFTS5QueryAdapter(conn)
