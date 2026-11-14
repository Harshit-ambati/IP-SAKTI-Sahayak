"""
Classification route for formulation intake (Task Su-01).
Implements input validation and explicit mock responses across the six provisional routes.
"""

from fastapi import APIRouter
from ...models.schemas import (
    Intake,
    ClassificationResult,
    ProvisionalRouteEnum,
)

router = APIRouter(prefix="/api/v1", tags=["Classification"])


@router.post(
    "/classify",
    response_model=ClassificationResult,
    summary="Formulation Intake Classification (Su-01 Mock Skeleton)",
    description=(
        "Accepts formulation intake, validates input fields, and returns a provisional "
        "classification route. In Su-01, returns explicit synthetic mock results "
        "matching the six statutory routes defined in MASTER_PLAN.md."
    ),
)
def classify_formulation(intake: Intake) -> ClassificationResult:
    """
    Evaluates intake conditions against statutory decision rules (RULE-01 to RULE-07)
    and returns an explicit synthetic mock outcome.
    """
    # Rule 07: Ambiguous / Missing Facts / Contradictory Claims
    if not intake.formulation_title.strip() or len(intake.ingredients) == 0:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_uncertain",
            governing_provisions=["Master Plan Safety Gate"],
            missing_facts=["Formulation title and at least one valid ingredient are mandatory."],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Contradiction: Cosmetic claiming disease treatment/cure
    if intake.external_application_only and (intake.claims_disease_treatment or intake.claims_disease_cure):
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_rule_conflict",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(aaa) & Section 3(h)"],
            missing_facts=[
                "Contradiction: Product marked as external cosmetic but claims disease cure/treatment. "
                "Cosmetics cannot claim therapeutic efficacy under Section 3(aaa)."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Contradiction: Ayurveda Aahara claiming disease cure
    if intake.intended_use == "food_dietary" and intake.claims_disease_cure:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_rule_conflict",
            governing_provisions=["FSSAI Ayurveda Aahara Regulations 2022, Regulation 8"],
            missing_facts=[
                "Contradiction: Ayurveda Aahara food products are strictly prohibited from claiming "
                "prevention, treatment or cure of human disease under Regulation 8."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 04: Phytopharmaceutical Drug
    if intake.standardized_fraction and intake.intended_use == "medicinal":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.PHYTOPHARMACEUTICAL,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs Rules 1945, Rule 2(eb)"],
            missing_facts=[],
            referral_required=True,  # Mandatory referral to CDSCO new drug pathway
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 03: Novel / Non-classical ASU Drug
    if intake.has_novel_ingredient and intake.intended_use == "medicinal":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.NOVEL_NON_CLASSICAL,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(h)"],
            missing_facts=["Safety and clinical trial evidence required for novel non-classical ingredients."],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 06: Cosmetic
    if intake.external_application_only or intake.intended_use == "cosmetic":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.COSMETIC,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(aaa)"],
            missing_facts=[],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 05: Ayurveda Aahara
    if intake.intended_use == "food_dietary":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.AYURVEDA_AAHARA,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["FSSAI Ayurveda Aahara Regulations 2022, Regulation 2(b) & Regulation 8"],
            missing_facts=[],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 01: Classical ASU Drug
    if intake.classical_text_reference and not intake.has_novel_ingredient:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.CLASSICAL_GENERIC,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=[
                "Drugs and Cosmetics Act 1940, Section 3(a)",
                "First Schedule Authoritative Books",
            ],
            missing_facts=[],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Rule 02: Patent or Proprietary ASU Drug (Default medicinal when classical text is absent)
    if intake.intended_use == "medicinal":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.PATENT_PROPRIETARY,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(h)"],
            missing_facts=["Specify authoritative text if claiming classical status."],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # Fallback to Unknown / Ambiguous
    return ClassificationResult(
        provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
        confidence_label="synthetic_mock_uncertain",
        governing_provisions=["Master Plan Safety Gate"],
        missing_facts=["Insufficient facts to determine statutory route. Please provide classical reference or intended use."],
        referral_required=True,
        disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
        is_synthetic_fixture=True,
    )
