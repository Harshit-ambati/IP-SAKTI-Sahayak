# Benchmark dataset protocol and scenario catalog

This directory contains the canonical evaluation scenarios, test protocols, and result ledger templates for **IP-SAKTI Sahayak** under Task Sa-01 (owned by Sabeena).

> **Current Review Status (Task Sa-01 Phase 1):**
> - **Total Canonical Cases Drafted:** 20
> - **Reviewed Gold Cases:** 0
> - **Provisional Unreviewed Cases:** 20 (All legal expectations labeled provisional pending Thulasi's authoritative domain check)
> - **Review Pending:** Thulasi for statutory provisions & routes, Deepshika for language fidelity, Harshit for evaluation protocol.

---

## 1. Directory Structure

- [`canonical_scenarios.csv`](canonical_scenarios.csv): The first twenty synthetic but realistic scenarios covering supported topics across 4 categories and 6 provisional routes.
- [`results_template.csv`](results_template.csv): Standardized result recording ledger schema (unpopulated template with zero fabricated test runs) for future model evaluations.
- [`../../docs/work-plan/modules/sabeena-sa01-benchmark-spec.md`](../../docs/work-plan/modules/sabeena-sa01-benchmark-spec.md): Formal scenario and result schema specification, split composition, and case-by-case analysis.

---

## 2. Canonical Scenario Schema (`canonical_scenarios.csv`)

| Field Name | Type | Permissible Values / Description |
|---|---|---|
| `case_id` | String | Stable unique scenario identifier (`SYN-CASE-001` through `SYN-CASE-020`). |
| `split` | Enum | `development` (10 cases) or `holdout` (10 cases). Holdout cases are strictly reserved for un-tuned evaluation. |
| `category` | Enum | `classification` (10), `evidence` (4), `insufficient_evidence` (3), `adversarial_jurisdiction` (3). |
| `language` | Enum | `en` (English; Hindi `hi` and regional variants scheduled for later phases). |
| `jurisdiction_requested` | Enum | `India` or `International` (treaty overview context). |
| `prompt` | String | Synthetic user question, realistic but strictly free of personal data or proprietary formulations. |
| `facts_present` | String | Key formulation and factual elements supplied in the intake prompt. |
| `missing_facts` | String | Critical missing conditions that should prevent affirmative classification or trigger clarification. |
| `expected_behavior` | Enum | System response contract matching API `AnswerStatusEnum`: `answered`, `clarify`, `abstained`, `referral`. |
| `provisional_route` | Enum | `classical_generic`, `patent_proprietary`, `novel_non_classical`, `phytopharmaceutical`, `ayurveda_aahara`, `cosmetic`, `unknown_ambiguous`. |
| `answerability` | Enum | `answerable`, `unanswerable_missing_facts`, `unanswerable_unsupported`, `abstain_or_referral`. |
| `gold_passage_ids` | String | Semicolon-separated verified corpus passage IDs (`PASS-001` through `PASS-025`). Blank for abstention cases where positive evidence is deliberately suppressed. |
| `label_status` | Enum | `provisional_unreviewed` (prevents treating draft labels as ground truth). |
| `reviewer` | String | Assigned peer reviewer (`pending_thulasi_review`). |
| `reviewed_at` | String | `unreviewed` until signed off by domain owner. |

---

## 3. Results Ledger Schema (`results_template.csv`)

The results ledger provides the official scoring format for future model evaluation runs. It contains zero pre-populated runs to prevent unobserved test data:

| Field Name | Type | Description |
|---|---|---|
| `case_id` | String | Foreign key matching `canonical_scenarios.csv`. |
| `run_id` | String | Execution run identifier. |
| `eval_date` | String | ISO 8601 date of evaluation run. |
| `release_version` | String | System software release tag under test. |
| `corpus_version` | String | Verified corpus release version. |
| `model_version` | String | LLM / classifier model identifier. |
| `actual_route` | String | Route emitted by the classifier. |
| `actual_behavior` | String | System behavior emitted (`answered`, `clarify`, `abstained`, `referral`). |
| `retrieved_passage_ids` | String | Semicolon-separated passage IDs retrieved in top-k. |
| `claim_support_score` | Float | Fraction of material claims supported by retrieved passages (0.0 to 1.0). |
| `citation_validity` | String | `valid`, `hallucinated_id`, or `wrong_jurisdiction`. |
| `route_match` | Boolean | Whether `actual_route == provisional_route`. |
| `behavior_match` | Boolean | Whether `actual_behavior == expected_behavior`. |
| `reviewer` | String | Teammate executing and verifying the run. |
| `reviewer_notes` | String | Observations, edge-case failures, or disagreements. |
| `defect_link` | String | Issue tracker link if a defect was identified. |

---

## 4. Stratified Split and Exact Composition

| Split | Category | Count | Expected Behavior Breakdown | Evaluated Scenarios |
|---|---|:---:|---|---|
| **Development** | `classification` | 5 | 2 answered, 3 referral | `SYN-CASE-001` (Classical ASU), `003` (Phytopharmaceutical), `005` (Aahara), `007` (Aahara Nutrients Bar), `009` (Parenteral Bar) |
| | `evidence` | 2 | 2 answered | `SYN-CASE-011` (Patent Synergy), `013` (BD Act Domestic Form 8) |
| | `insufficient_evidence` | 2 | 1 clarify, 1 answered | `SYN-CASE-015` (Missing Facts), `017` (Category A Unlisted Procedure) |
| | `adversarial_jurisdiction` | 1 | 1 abstained | `SYN-CASE-019` (Software s. 3(k) Out-of-Scope; gold passages empty) |
| **Development Total** | | **10** | **5 answered, 3 referral, 1 clarify, 1 abstained** | |
| **Holdout** | `classification` | 5 | 2 answered, 3 referral | `SYN-CASE-002` (P&P ASU), `004` (Novel Non-Classical), `006` (Cosmetic), `008` (Aahara Disease Claims Bar), `010` (Cosmetic Medical Claims Bar) |
| | `evidence` | 2 | 2 answered | `SYN-CASE-012` (BD Act Foreign Form 7), `014` (WIPO GRATK Treaty Overview) |
| | `insufficient_evidence` | 1 | 1 clarify | `SYN-CASE-016` (Missing First Schedule Citation) |
| | `adversarial_jurisdiction` | 2 | 2 abstained | `SYN-CASE-018` (US FDA Export Out-of-Scope; gold passages empty), `020` (Confidential TKDL Access Safeguard; gold passages empty) |
| **Holdout Total** | | **10** | **4 answered, 3 referral, 2 abstained, 1 clarify** | **5 abstention/referral, 6 total non-confident safety cases (60% of holdout)** |
| **Grand Total** | | **20** | **9 answered, 6 referral, 3 abstained, 2 clarify** | **100% unreviewed provisional; 0 reviewed** |

---

## 5. Review & Verification Workflow

Run the Sa-01 benchmark validation script to verify schema conformity, API behavior enum alignment, empty gold passages on abstention, and unreviewed counts:
```bash
python scripts/validate_sa01.py
```
