"""
Classification route for formulation intake (Task Su-01).

Fixes applied per Harshit's review (PR #3 Changes Requested):
- FIX-2a: Rule 06 (cosmetic) no longer fires on intended_use="cosmetic" alone without
  external_application_only=True. Classification on cosmetic route requires BOTH.
- FIX-2b: Rule 02 (patent_proprietary) no longer fires on intended_use="medicinal" alone
  when any mandatory fact is missing or intended_use is unspecified. Missing classical
  reference with medicinal use now demands clarification before assigning a confident route.
- FIX-2c: intended_use="unspecified" now always falls to unknown_ambiguous.
"""

from fastapi import APIRouter
from ...models.schemas import (
    Intake,
    ClassificationResult,
    ProvisionalRouteEnum,
)

router = APIRouter(prefix="/api/v1", tags=["Classification"])

_KNOWN_INTENDED_USES = {"medicinal", "food_dietary", "cosmetic"}


@router.post(
    "/classify",
    response_model=ClassificationResult,
    summary="Formulation Intake Classification (Su-01 Mock Skeleton)",
    description=(
        "Accepts formulation intake, validates input fields, and returns a provisional "
        "classification route. In Su-01, returns explicit synthetic mock results "
        "matching the six statutory routes defined in MASTER_PLAN.md. "
        "Missing or conflicting facts always return unknown_ambiguous with clarifying questions."
    ),
)
def classify_formulation(intake: Intake) -> ClassificationResult:
    """
    Evaluates intake conditions against statutory decision rules (RULE-01 to RULE-07).

    Safety-first ordering:
      Contradictions → missing facts → phytopharmaceutical → novel → cosmetic
      → aahara → classical → proprietary → unknown_ambiguous fallback.

    FIX-2c: unspecified intended_use immediately triggers unknown_ambiguous.
    FIX-2a: cosmetic requires external_application_only=True (not intended_use alone).
    FIX-2b: medicinal without classical text reference triggers clarification, not confident route.
    """

    # --- Gate 1: Missing mandatory fields (Pydantic already enforces non-empty title/ingredients) ---
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

    # --- Gate 2: FIX-2c — unspecified intended_use always triggers clarification ---
    if intake.intended_use not in _KNOWN_INTENDED_USES:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_uncertain",
            governing_provisions=["Master Plan Safety Gate"],
            missing_facts=[
                f"intended_use '{intake.intended_use}' is not one of the recognised categories "
                "(medicinal, food_dietary, cosmetic). Please clarify the intended purpose."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Gate 3: Contradiction — external cosmetic claiming disease treatment/cure ---
    if intake.external_application_only and (intake.claims_disease_treatment or intake.claims_disease_cure):
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_rule_conflict",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(aaa) & Section 3(h)"],
            missing_facts=[
                "Contradiction: Product marked as external topical cosmetic but also claims disease "
                "treatment or cure. Cosmetics cannot claim therapeutic efficacy under Section 3(aaa). "
                "Reclassify as a medicinal drug or remove therapeutic claims."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Gate 4: Contradiction — Ayurveda Aahara claiming disease cure ---
    if intake.intended_use == "food_dietary" and intake.claims_disease_cure:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_rule_conflict",
            governing_provisions=["FSSAI Ayurveda Aahara Regulations 2022, Regulation 8"],
            missing_facts=[
                "Contradiction: Ayurveda Aahara food products are strictly prohibited from claiming "
                "prevention, treatment or cure of human disease under Regulation 8. "
                "Remove curative claims or reclassify as a medicinal drug."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Gate 5: Contradiction — food_dietary + external_application_only ---
    if intake.intended_use == "food_dietary" and intake.external_application_only:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_rule_conflict",
            governing_provisions=["FSSAI Ayurveda Aahara Regulations 2022, Regulation 2(b)"],
            missing_facts=[
                "Contradiction: intended_use is food_dietary (ingested) but external_application_only is True (topical). "
                "Food products cannot be external application only. Please clarify the formulation route of administration."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Rule 04: Phytopharmaceutical Drug ---
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

    # --- Rule 03: Novel / Non-classical ASU Drug ---
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

    # --- Rule 06: Cosmetic ---
    # FIX-2a: requires BOTH external_application_only=True AND intended_use="cosmetic".
    # Previously only checked one condition, which could misclassify ambiguous medicinal+external cases.
    if intake.external_application_only and intake.intended_use == "cosmetic":
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.COSMETIC,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(aaa)"],
            missing_facts=[],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Ambiguity: cosmetic intended_use without external_application_only ---
    if intake.intended_use == "cosmetic" and not intake.external_application_only:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_uncertain",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(aaa)"],
            missing_facts=[
                "Cosmetic classification requires confirmation that the product is for external "
                "topical use only (external_application_only=True). Please clarify route of administration."
            ],
            referral_required=True,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Rule 05: Ayurveda Aahara ---
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

    # --- Rule 01: Classical ASU Drug ---
    if intake.classical_text_reference and not intake.has_novel_ingredient and intake.intended_use == "medicinal":
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

    # --- Rule 02: Patent or Proprietary ASU Drug ---
    # Explicitly declared as proprietary/branded ASU drug, without classical text reference,
    # and without novel synthetic chemicals or standardized fraction.
    if (
        intake.intended_use == "medicinal"
        and intake.is_proprietary_branded
        and not intake.classical_text_reference
        and not intake.has_novel_ingredient
        and not intake.standardized_fraction
    ):
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.PATENT_PROPRIETARY,
            confidence_label="synthetic_mock_rule_match",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(h)"],
            missing_facts=[],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Ambiguity: medicinal without classical text reference or proprietary declaration ---
    # Missing text reference alone is surfaced as a clarification question, not silently assigned a route.
    if intake.intended_use == "medicinal" and not intake.classical_text_reference:
        return ClassificationResult(
            provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
            confidence_label="synthetic_mock_uncertain",
            governing_provisions=["Drugs and Cosmetics Act 1940, Section 3(h)"],
            missing_facts=[
                "To determine whether the formulation is a Classical ASU Drug (Section 3(a)) or a "
                "Patent/Proprietary ASU Medicine (Section 3(h)), please provide: "
                "(1) the classical authoritative text reference, if applicable; "
                "(2) whether this is a novel proprietary formula not listed in classical texts."
            ],
            referral_required=False,
            disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
            is_synthetic_fixture=True,
        )

    # --- Fallback: Unknown / Ambiguous ---
    return ClassificationResult(
        provisional_route=ProvisionalRouteEnum.UNKNOWN_AMBIGUOUS,
        confidence_label="synthetic_mock_uncertain",
        governing_provisions=["Master Plan Safety Gate"],
        missing_facts=["Insufficient facts to determine statutory route. Please provide intended use and ingredient details."],
        referral_required=True,
        disclaimer="Provisional classification only; does not constitute legal or regulatory approval.",
        is_synthetic_fixture=True,
    )
