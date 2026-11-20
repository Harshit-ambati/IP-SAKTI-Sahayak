"""
Domain schemas and API contract models for IP-SAKTI Sahayak.
Frozen week-2 contract models per docs/work-plan/MASTER_PLAN.md:
Intake, ClassificationResult, SourceRecord, EvidencePassage, AnswerResult, ReferralPacket.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class JurisdictionEnum(str, Enum):
    INDIA = "India"
    INTERNATIONAL = "International"


class LanguageEnum(str, Enum):
    EN = "en"
    HI = "hi"
    KN = "kn"
    TA = "ta"
    TE = "te"


class ProvisionalRouteEnum(str, Enum):
    CLASSICAL_GENERIC = "classical_generic"
    PATENT_PROPRIETARY = "patent_proprietary"
    NOVEL_NON_CLASSICAL = "novel_non_classical"
    PHYTOPHARMACEUTICAL = "phytopharmaceutical"
    AYURVEDA_AAHARA = "ayurveda_aahara"
    COSMETIC = "cosmetic"
    UNKNOWN_AMBIGUOUS = "unknown_ambiguous"


class AnswerStatusEnum(str, Enum):
    CLARIFY = "clarify"
    ANSWERED = "answered"
    ABSTAINED = "abstained"
    REFERRAL = "referral"


class EvidenceStatusEnum(str, Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient"


# --- 1. Intake Schema ---

class Intake(BaseModel):
    """
    Intake form payload submitted by the user or client interface.
    Captures formulation details without saving sensitive identity or unconsented data.
    """
    intake_id: Optional[str] = Field(
        default=None,
        description="Optional client-side session identifier (no personal data)."
    )
    formulation_title: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Name or title of the formulation or query subject."
    )
    ingredients: List[str] = Field(
        ...,
        min_length=1,
        description="List of ingredients, plant parts, or excipients."
    )
    classical_text_reference: Optional[str] = Field(
        default=None,
        description="Name of classical text (e.g. Charaka Samhita, Sushruta Samhita) if applicable."
    )
    processing_method: Optional[str] = Field(
        default=None,
        description="Method of preparation (e.g. Asava, Arishta, Taila, standardized extract)."
    )
    intended_use: str = Field(
        default="medicinal",
        description="Intended use: medicinal, food_dietary, cosmetic, or unspecified."
    )
    claims_disease_treatment: bool = Field(
        default=False,
        description="Whether therapeutic or curative claims are made."
    )
    claims_disease_cure: bool = Field(
        default=False,
        description="Whether prevention, treatment, or cure of human disease is claimed."
    )
    has_novel_ingredient: bool = Field(
        default=False,
        description="Whether modern chemical excipients, synthetic vitamins, or novel plants are added."
    )
    standardized_fraction: bool = Field(
        default=False,
        description="Whether a purified standardized fraction with >=4 bioactive markers is used."
    )
    is_proprietary_branded: bool = Field(
        default=False,
        description="Whether the formulation is an explicitly branded proprietary ASU drug not based on classical texts."
    )
    external_application_only: bool = Field(
        default=False,
        description="Whether formulation is strictly for external topical use for cleansing/beautifying."
    )
    jurisdiction: JurisdictionEnum = Field(
        default=JurisdictionEnum.INDIA,
        description="Selected legal jurisdiction."
    )
    language: LanguageEnum = Field(
        default=LanguageEnum.EN,
        description="Selected language."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "intake_id": "SYNTH-INTAKE-001",
                "formulation_title": "Synthetic Triphala Churna Sample",
                "ingredients": ["Terminalia chebula", "Terminalia bellirica", "Phyllanthus emblica"],
                "classical_text_reference": "Charaka Samhita, Chikitsasthana",
                "processing_method": "Churna (fine powder)",
                "intended_use": "medicinal",
                "claims_disease_treatment": True,
                "claims_disease_cure": False,
                "has_novel_ingredient": False,
                "standardized_fraction": False,
                "external_application_only": False,
                "jurisdiction": "India",
                "language": "en"
            }
        }
    )


# --- 2. Classification Result ---

class ClassificationResult(BaseModel):
    """
    Provisional classification outcome derived from decision rules.
    Statutorily grounds the 6 provisional routes and explicit unknown fallback.
    """
    provisional_route: ProvisionalRouteEnum = Field(
        ...,
        description="Identified provisional route."
    )
    confidence_label: str = Field(
        default="provisional_rule_based",
        description="Confidence label (explicitly provisional; never legal certification)."
    )
    governing_provisions: List[str] = Field(
        default_factory=list,
        description="Statutory provisions governing this route."
    )
    missing_facts: List[str] = Field(
        default_factory=list,
        description="Missing facts or clarifying questions if route is ambiguous."
    )
    referral_required: bool = Field(
        default=False,
        description="Whether human professional referral is mandatory."
    )
    disclaimer: str = Field(
        default="Provisional classification only; does not constitute legal or regulatory approval.",
        description="Mandatory legal disclaimer."
    )
    is_synthetic_fixture: bool = Field(
        default=True,
        description="Visible synthetic flag for mock/testing phase."
    )


# --- 3. Source & Evidence Schemas ---

class SourceRecord(BaseModel):
    """
    Official source document metadata matching data/corpus/documents.csv.
    """
    source_id: str = Field(..., description="Unique source identifier (e.g. REAL-001 or SYNTH-SRC-001).")
    topic: str = Field(..., description="Topic code (patents, ayurveda_product_classification, etc.).")
    authority: str = Field(..., description="Issuing authority (IP India, Ministry of Ayush, FSSAI, etc.).")
    title: str = Field(..., description="Document or Act title.")
    official_url: str = Field(..., description="Official verification URL.")
    format: str = Field(default="html", description="Document format (html, pdf).")
    role: str = Field(default="primary", description="Corpus role (primary, background).")
    priority: str = Field(default="required", description="Priority level (required, optional).")
    verification_status: str = Field(..., description="Verification status.")
    review_note: Optional[str] = Field(default=None, description="Notes on operative provisions/amendments.")
    is_synthetic: bool = Field(default=False, description="Flag indicating synthetic fixture.")


class EvidencePassage(BaseModel):
    """
    Provision passage excerpt matching data/corpus/passages.csv.
    """
    passage_id: str = Field(..., description="Unique passage identifier (e.g. PASS-001 or SYNTH-PASS-001).")
    source_id: str = Field(..., description="Foreign key to source_id.")
    jurisdiction: str = Field(..., description="Jurisdiction (India, International).")
    authority: str = Field(..., description="Issuing authority.")
    document_title: str = Field(..., description="Title of parent document.")
    locator: str = Field(..., description="Exact provision locator (e.g. Section 3(p), Regulation 2(b)).")
    paraphrased_content: str = Field(..., description="Statutory paraphrase or text.")
    source_url: str = Field(..., description="Official URL.")
    source_type: str = Field(default="statute", description="Type (statute, regulation, treaty).")
    review_status: str = Field(..., description="Review status.")
    review_note: Optional[str] = Field(default=None, description="Review notes.")
    is_synthetic: bool = Field(default=False, description="Flag indicating synthetic fixture.")


# --- 4. Answer Request & Result ---

class Claim(BaseModel):
    """
    Material claim made in an answer, linked to specific evidence IDs.
    """
    claim_id: str = Field(..., description="Claim identifier.")
    claim_text: str = Field(..., description="Statement of fact or legal provision summary.")
    evidence_ids: List[str] = Field(..., description="List of passage_ids supporting this claim.")


class AnswerRequest(BaseModel):
    """
    Request payload to generate an answer.
    """
    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User query or legal question."
    )
    jurisdiction: JurisdictionEnum = Field(
        default=JurisdictionEnum.INDIA,
        description="Jurisdiction filter (India or International)."
    )
    language: LanguageEnum = Field(
        default=LanguageEnum.EN,
        description="Language code (en, hi, etc.)."
    )
    intake: Optional[Intake] = Field(
        default=None,
        description="Optional accompanying formulation intake."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "Is a classical Triphala churna eligible for a product patent in India?",
                "jurisdiction": "India",
                "language": "en"
            }
        }
    )


class AnswerResult(BaseModel):
    """
    Structured answer constrained to retrieved evidence passages.
    """
    status: AnswerStatusEnum = Field(
        ...,
        description="Outcome status: answered, clarify, abstained, referral."
    )
    jurisdiction: JurisdictionEnum = Field(
        ...,
        description="Active jurisdiction."
    )
    language: LanguageEnum = Field(
        ...,
        description="Active language."
    )
    provisional_class: Optional[ProvisionalRouteEnum] = Field(
        default=None,
        description="Provisional formulation classification if determined."
    )
    answer_text: str = Field(
        ...,
        description="Constrained synthesis answering the query."
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Explicit assumptions made in evaluating the query."
    )
    claims: List[Claim] = Field(
        default_factory=list,
        description="Claims with explicit evidence ID citations."
    )
    cited_provisions: List[str] = Field(
        default_factory=list,
        description="List of cited statutory provision locators."
    )
    limitations: List[str] = Field(
        default_factory=list,
        description="Caveats and non-legal advice limitations."
    )
    evidence_status: EvidenceStatusEnum = Field(
        ...,
        description="Evidence status: supported, partial, insufficient."
    )
    corpus_version: str = Field(
        default="v0.1-synthetic",
        description="Version of corpus used."
    )
    model_version: str = Field(
        default="mock-stub-v1",
        description="Version of model or stub used."
    )
    is_synthetic_fixture: bool = Field(
        default=True,
        description="Visible synthetic flag: true for phase 1 mock responses."
    )


# --- 5. Referral Packet ---

class ReferralPacket(BaseModel):
    """
    User-controlled referral packet for export to a qualified IP attorney or Ayush expert.
    """
    packet_id: str = Field(..., description="Unique packet identifier.")
    query_summary: str = Field(..., description="Summary of query and facts.")
    provisional_route: Optional[ProvisionalRouteEnum] = Field(default=None)
    jurisdiction: JurisdictionEnum = Field(default=JurisdictionEnum.INDIA)
    assumptions: List[str] = Field(default_factory=list)
    cited_provisions: List[str] = Field(default_factory=list)
    unresolved_issues: List[str] = Field(default_factory=list)
    export_timestamp: str = Field(..., description="ISO 8601 timestamp.")
    disclaimer: str = Field(
        default="This packet was prepared by IP-SAKTI Sahayak as an informational summary. It does not constitute formal legal counsel.",
        description="Legal disclaimer."
    )


# --- 6. Health & Auxiliary Responses ---

class HealthStatus(BaseModel):
    """
    Service health status.
    """
    status: str = Field(default="healthy")
    service: str = Field(default="ip-sakti-backend")
    version: str = Field(default="0.1.0-su01")
    database: str = Field(..., description="Database connection status.")
    fts5_supported: bool = Field(default=True, description="SQLite FTS5 support status.")
    timestamp: str = Field(..., description="Server timestamp.")


class SourceListResponse(BaseModel):
    """
    Paginated source list response.
    """
    total: int
    items: List[SourceRecord]


class PassageListResponse(BaseModel):
    """
    Paginated passage list response.
    """
    total: int
    items: List[EvidencePassage]


class AuditEventRecord(BaseModel):
    """
    Minimal audit log entry adhering to strict privacy rules:
    NO user formulation text or secret ingredients are recorded.
    """
    audit_id: str
    request_id: str
    timestamp: str
    route: str
    jurisdiction: str
    evidence_ids: List[str]
    versions: str
    status: str
