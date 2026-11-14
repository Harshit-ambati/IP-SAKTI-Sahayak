"""
Answer generation endpoint for IP-SAKTI Sahayak (Task Su-01).
Implements input validation, privacy-compliant audit logging, and explicit mock responses.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from ...config import AUDIT_LOG_ENABLED
from ...db.database import get_db
from ...models.schemas import (
    AnswerRequest,
    AnswerResult,
    AnswerStatusEnum,
    EvidenceStatusEnum,
    JurisdictionEnum,
    Claim,
)

router = APIRouter(prefix="/api/v1", tags=["Answer"])


@router.post(
    "/answer",
    response_model=AnswerResult,
    summary="Generate Cited Legal/Regulatory Answer (Su-01 Mock Skeleton)",
    description=(
        "Accepts a query, selected jurisdiction, and optional intake payload. "
        "Validates input fields and returns a structured AnswerResult with claims, "
        "evidence IDs, cited provisions, and limitations. Logs minimal audit events without secrets."
    ),
)
def generate_answer(
    request: AnswerRequest,
    conn: sqlite3.Connection = Depends(get_db),
) -> AnswerResult:
    """
    Returns an explicit synthetic mock answer conforming to the agreed Master Plan contract.
    Records a privacy-preserving audit event.
    """
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # Route and evidence mapping for mock answer
    if request.jurisdiction == JurisdictionEnum.INTERNATIONAL:
        # International treaty overview (WIPO GRATK) mock
        status = AnswerStatusEnum.ANSWERED
        evidence_status = EvidenceStatusEnum.SUPPORTED
        answer_text = (
            "[SYNTHETIC MOCK ANSWER - INTERNATIONAL] At the international level, the WIPO Treaty "
            "on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (GRATK), "
            "adopted in May 2024, establishes a mandatory patent disclosure requirement. Applicants "
            "must disclose the country of origin or indigenous source when an invention is based on "
            "genetic resources or traditional knowledge. This treaty does not automatically confer domestic "
            "enforceability; individual contracting party ratification is required."
        )
        assumptions = [
            "Query relates to multilateral WIPO treaty framework.",
            "Country-specific export compliance is excluded per MVP scope."
        ]
        claims = [
            Claim(
                claim_id="SYNTH-CLAIM-INT-01",
                claim_text="The WIPO GRATK Treaty establishes a patent disclosure requirement for genetic resources and associated TK.",
                evidence_ids=["SYNTH-PASS-001"]  # In real engine, mapped to PASS-007
            )
        ]
        cited_provisions = ["WIPO GRATK Treaty 2024, Overview"]
        provisional_class = None

    elif "patent" in request.query.lower() or "patentable" in request.query.lower() or "3(p)" in request.query.lower():
        # Patent exclusion under Section 3(p) mock
        status = AnswerStatusEnum.ANSWERED
        evidence_status = EvidenceStatusEnum.SUPPORTED
        answer_text = (
            "[SYNTHETIC MOCK ANSWER - INDIA PATENTS] Under Indian patent law, classical Ayurvedic "
            "formulations and known herbal combinations are generally excluded from patentability. "
            "Specifically, Section 3(p) of the Patents Act, 1970 excludes inventions which in effect "
            "are traditional knowledge or an aggregation or duplication of known properties of traditionally "
            "known components. Only non-obvious synergistic formulations with measurable technical advancement "
            "over known traditional combinations may overcome Section 3(e) admixture objections."
        )
        assumptions = [
            "Formulation ingredients are known in classical Ayurvedic pharmacopoeia.",
            "No synergistic efficacy data demonstrating unexpected therapeutic effect was provided."
        ]
        claims = [
            Claim(
                claim_id="SYNTH-CLAIM-PAT-01",
                claim_text="Traditional knowledge and aggregations of known traditional components are non-patentable subject matter.",
                evidence_ids=["SYNTH-PASS-001"]
            ),
            Claim(
                claim_id="SYNTH-CLAIM-PAT-02",
                claim_text="Classical ASU medicines manufactured strictly per First Schedule texts are categorized as Classical ASU Drugs.",
                evidence_ids=["SYNTH-PASS-002"]
            )
        ]
        cited_provisions = [
            "The Patents Act 1970, Section 3(p)",
            "The Patents Act 1970, Section 3(e)",
            "Drugs and Cosmetics Act 1940, Section 3(a)"
        ]
        provisional_class = request.intake.provisional_route if request.intake else None

    elif "aahara" in request.query.lower() or "food" in request.query.lower() or "dietary" in request.query.lower():
        # Ayurveda Aahara mock
        status = AnswerStatusEnum.ANSWERED
        evidence_status = EvidenceStatusEnum.SUPPORTED
        answer_text = (
            "[SYNTHETIC MOCK ANSWER - AYURVEDA AAHARA] Under the Food Safety and Standards (Ayurveda Aahara) "
            "Regulations, 2022, Ayurveda Aahara encompasses food prepared in accordance with recipes or processes "
            "described in authoritative Ayurvedic books. Crucially, Regulation 8 prohibits any labelling or "
            "advertising from claiming prevention, treatment, or cure of human diseases."
        )
        assumptions = [
            "Product is intended as dietary food/supplement, not a medicinal drug.",
            "No synthetic vitamins or chemical minerals added."
        ]
        claims = [
            Claim(
                claim_id="SYNTH-CLAIM-AAH-01",
                claim_text="Ayurveda Aahara products are strictly prohibited from making disease prevention or cure claims.",
                evidence_ids=["SYNTH-PASS-003"]
            )
        ]
        cited_provisions = [
            "FSSAI Ayurveda Aahara Regulations 2022, Regulation 2(b)",
            "FSSAI Ayurveda Aahara Regulations 2022, Regulation 8"
        ]
        provisional_class = request.intake.provisional_route if request.intake else None

    else:
        # General informational answer
        status = AnswerStatusEnum.ANSWERED
        evidence_status = EvidenceStatusEnum.PARTIAL
        answer_text = (
            "[SYNTHETIC MOCK ANSWER - GENERAL] For Ayurveda-based formulations in India, regulatory classification "
            "depends strictly on the source authoritative text, manufacturing process, and intended use. "
            "Classical formulations fall under Section 3(a) of the Drugs and Cosmetics Act, 1940, while proprietary "
            "formulations fall under Section 3(h). Inventions based on traditional knowledge are barred from "
            "patents under Section 3(p) of the Patents Act, 1970."
        )
        assumptions = ["General inquiry without specific single product formulation dossier."]
        claims = [
            Claim(
                claim_id="SYNTH-CLAIM-GEN-01",
                claim_text="Classical Ayurvedic formulations are governed by Section 3(a) of the D&C Act 1940.",
                evidence_ids=["SYNTH-PASS-002"]
            )
        ]
        cited_provisions = ["Drugs and Cosmetics Act 1940, Section 3(a)"]
        provisional_class = request.intake.provisional_route if request.intake else None

    limitations = [
        "Informational guidance only; not formal legal advice, patent certification, or regulatory clearance.",
        "Statutory interpretation depends on official gazette notifications and court precedents.",
        "This response is derived from synthetic Phase 1 fixtures for skeleton testing."
    ]

    result = AnswerResult(
        status=status,
        jurisdiction=request.jurisdiction,
        language=request.language,
        provisional_class=provisional_class,
        answer_text=answer_text,
        assumptions=assumptions,
        claims=claims,
        cited_provisions=cited_provisions,
        limitations=limitations,
        evidence_status=evidence_status,
        corpus_version="v0.1-synthetic-su01",
        model_version="mock-stub-v1",
        is_synthetic_fixture=True,
    )

    # Privacy-Compliant Audit Event Logging
    # MUST NOT log user's query text, full formulation, or confidential ingredients
    if AUDIT_LOG_ENABLED:
        try:
            audit_id = str(uuid.uuid4())
            evidence_ids_str = json.dumps([c.evidence_ids for c in claims])
            versions_str = json.dumps({"corpus": "v0.1-synthetic-su01", "model": "mock-stub-v1"})
            route_str = str(provisional_class.value if provisional_class else "direct_query")
            
            conn.execute(
                """
                INSERT INTO audit_events (
                    audit_id, request_id, timestamp, route, jurisdiction, evidence_ids, versions, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    request_id,
                    timestamp,
                    route_str,
                    request.jurisdiction.value,
                    evidence_ids_str,
                    versions_str,
                    status.value,
                )
            )
            conn.commit()
        except Exception:
            # Audit logging failure should not break the response path in dev skeleton
            pass

    return result
