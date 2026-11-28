# Sabeena Module Specification: Benchmark Scenario and Result Schema (Task Sa-01)

- **Task ID:** Sa-01
- **Module Owner:** Sabeena (Evaluation, Benchmark, Test Cases, and Documentation)
- **Target Window:** Weeks 1–2
- **Status:** In Review / Updated in Response to Peer Review (Draft PR #12 on `sabeena/sa-01-phase-1`)
- **Prior Phase Status:** First phase for Sabeena (`First phase`)
- **Reviewers:** Thulasi (Authoritative source & route labels), Deepshika (Language & Terminology), Harshit (Architecture & Evaluation Protocol)

---

## 1. Executive Summary & Objective

In accordance with [MASTER_PLAN.md](../MASTER_PLAN.md), [05-sabeena.md](05-sabeena.md), and [data/benchmark/README.md](../../../data/benchmark/README.md), Task Sa-01 delivers:
1. **Canonical Scenario and Unpopulated Result Ledger Schemas**: A compact, reproducible evaluation schema capturing case ID, formulation facts, requested jurisdiction, expected route, answerability, gold passage IDs, label review status, reviewer, and split. The results template ([data/benchmark/results_template.csv](../../../data/benchmark/results_template.csv)) is strictly unpopulated to prevent fabricated or unobserved execution runs from entering the repository.
2. **First Twenty Synthetic Scenarios**: Grounded in the verified corpus ([data/corpus/passages.csv](../../../data/corpus/passages.csv)) and Thulasi's decision rules ([thulasi-t02-intake-rules.md](thulasi-t02-intake-rules.md)), spanning all 6 provisional routes and 4 core evaluation categories.
3. **Rigorous Stratified Split and Exact Safety Counts**: Exactly 10 development cases and 10 holdout cases. The holdout set rigorously tests 4 answered, 3 referral, 2 abstained, and 1 clarify behaviors (5 abstention/referral, 6 total non-confident safety cases representing 60% of holdout).
4. **Behavior Contract Alignment with Backend API**: Binds `expected_behavior` directly to `AnswerStatusEnum` tokens: `answered`, `clarify`, `abstained`, and `referral`.
5. **Abstention Evidence Suppression**: For all 3 out-of-scope / adversarial abstention cases (`SYN-CASE-018`, `SYN-CASE-019`, `SYN-CASE-020`), `gold_passage_ids` is deliberately left empty, reflecting that no positive evidence should be cited when the system correctly abstains.
6. **Mandatory Audit Gate**: Explicitly labeling all 20 draft scenarios as `provisional_unreviewed` (`reviewed: 0`, `unreviewed: 20`) to prevent provisional labels from being treated as authoritative legal ground truth prior to Thulasi's validation.
7. **Privacy and PII Suppression**: Strict synthetic phrasing ensuring no personal data, live company proprietary formulations, or confidential records are included.
8. **Automated Validation Suite**: Standalone validation script ([scripts/validate_sa01.py](../../../scripts/validate_sa01.py)) enforcing 100% schema compliance, referential integrity, unpopulated results template contract, and audit gates.

---

## 2. Benchmark Scenario Schema

The canonical scenario dataset is stored in [`data/benchmark/canonical_scenarios.csv`](../../../data/benchmark/canonical_scenarios.csv) with 15 required fields:

| Field | Type | Description & Permissible Values |
|---|---|---|
| `case_id` | String | Unique identifier with format `SYN-CASE-001` through `SYN-CASE-020`. |
| `split` | Enum | `development` (10 cases) or `holdout` (10 cases). Holdout cases must never be used for prompt engineering or fine-tuning. |
| `category` | Enum | Evaluated dimension: `classification`, `evidence`, `insufficient_evidence`, `adversarial_jurisdiction`. |
| `language` | Enum | Target language code: `en` (English canonical cases; Hindi and regional variants planned for subsequent phases). |
| `jurisdiction_requested` | Enum | `India` (domestic Indian statutory framework) or `International` (treaty overview context). |
| `prompt` | String | User query text presenting realistic practitioner or consumer scenarios. |
| `facts_present` | String | Concise summary of active facts provided in the query (ingredients, processing, intended use, claims). |
| `missing_facts` | String | Missing essential facts required for definitive classification (`none` if complete). |
| `expected_behavior` | Enum | Expected system response type matching backend `AnswerStatusEnum`: `answered`, `clarify`, `abstained`, `referral`. |
| `provisional_route` | Enum | Target product route: `classical_generic`, `patent_proprietary`, `novel_non_classical`, `phytopharmaceutical`, `ayurveda_aahara`, `cosmetic`, `unknown_ambiguous`. |
| `answerability` | Enum | Answerability label: `answerable`, `unanswerable_missing_facts`, `unanswerable_unsupported`, `abstain_or_referral`. |
| `gold_passage_ids` | String | Semicolon-separated verified corpus passage IDs (`PASS-001` through `PASS-025`) expected to support the answer. Deliberately empty for abstention cases. |
| `label_status` | Enum | Audit gate field: `provisional_unreviewed` or `reviewed`. (Must be `provisional_unreviewed` in Sa-01). |
| `reviewer` | String | Assigned domain reviewer (`pending_thulasi_review`). |
| `reviewed_at` | String | Review timestamp (`unreviewed` in Sa-01). |

---

## 3. Results Ledger Schema

The evaluation results ledger is defined in [`data/benchmark/results_template.csv`](../../../data/benchmark/results_template.csv) with 16 fields. It is stored as an unpopulated schema with 0 data rows to maintain project data truth:

| Field | Type | Description |
|---|---|---|
| `case_id` | String | Foreign key matching `canonical_scenarios.csv`. |
| `run_id` | String | Execution run identifier (e.g. `RUN-20261126-01`). |
| `eval_date` | String | Date of test execution (YYYY-MM-DD). |
| `release_version` | String | Tagged release version under test. |
| `corpus_version` | String | Verified corpus release version. |
| `model_version` | String | LLM or classifier model identifier. |
| `actual_route` | String | Emitted route from classification route. |
| `actual_behavior` | String | Emitted behavior (`answered`, `clarify`, `abstained`, `referral`). |
| `retrieved_passage_ids` | String | Semicolon-separated passage IDs returned in top-k. |
| `claim_support_score` | Float | Measured claim support score (0.0 to 1.0) verified by reviewer. |
| `citation_validity` | String | `valid`, `hallucinated_id`, or `wrong_jurisdiction`. |
| `route_match` | Boolean | `true` if `actual_route == provisional_route`. |
| `behavior_match` | Boolean | `true` if `actual_behavior == expected_behavior`. |
| `reviewer` | String | Teammate executing and verifying the run. |
| `reviewer_notes` | String | Observations, edge-case failures, or disagreements. |
| `defect_link` | String | Issue tracker URL if a defect is logged. |

---

## 4. Scenario Catalog Breakdown (20 Cases)

The 20 synthetic cases are stratified across categories, routes, and splits:

### 4.1 Classification Category (10 Scenarios)
1. **`SYN-CASE-001` (Dev · Classical ASU):** Saraswatarishta manufactured per Charaka Samhita. All ingredients in First Schedule. Expected: `classical_generic`, `answered` (`PASS-009`, `PASS-017`, `PASS-002`).
2. **`SYN-CASE-002` (Holdout · P&P ASU):** Polyherbal tablet combining Ashwagandha, Shatavari, and Gokshura in proprietary proportions. Expected: `patent_proprietary`, `answered` (`PASS-010`, `PASS-018`, `PASS-013`).
3. **`SYN-CASE-003` (Dev · Phytopharmaceutical Referral):** Standardized botanical fraction of Picrorhiza kurroa with 4 bioactive markers. Regulated under CDSCO Schedule Y. Expected: `phytopharmaceutical`, `referral` (`PASS-012`, `PASS-022`).
4. **`SYN-CASE-004` (Holdout · Novel Non-Classical Referral):** Oral capsule containing classical Ashwagandha fortified with synthetic caffeine and non-classical Echinacea. Expected: `novel_non_classical`, `referral` (`PASS-002`, `PASS-010`).
5. **`SYN-CASE-005` (Dev · Ayurveda Aahara Food):** Amalaki Rasayana herbal paste per Schedule A, no disease claims, no added vitamins/minerals. Expected: `ayurveda_aahara`, `answered` (`PASS-003`, `PASS-004`, `PASS-024`).
6. **`SYN-CASE-006` (Holdout · Ayurvedic Cosmetic):** Kumkumadi taila oil applied topically for facial skin glow and cleansing, no disease claims. Expected: `cosmetic`, `answered` (`PASS-011`).
7. **`SYN-CASE-007` (Dev · Ayurveda Aahara Disqualification - Added Nutrients):** Schedule A herbal tea fortified with natural Vitamin C and calcium carbonate. Violates Reg. 3(4). Expected: `unknown_ambiguous`, `referral` (`PASS-003`).
8. **`SYN-CASE-008` (Holdout · Ayurveda Aahara Disqualification - Disease Claims):** Ginger-tulsi tea claiming on packaging to "prevent viral infections and treat cough". Violates Reg. 8. Expected: `unknown_ambiguous`, `referral` (`PASS-004`).
9. **`SYN-CASE-009` (Dev · ASU Disqualification - Parenteral Bar):** Proprietary herbal injectable solution for intravenous administration. Prohibited under D&C Act Section 3(h). Expected: `unknown_ambiguous`, `referral` (`PASS-010`).
10. **`SYN-CASE-010` (Holdout · Cosmetic Disqualification - Disease Cure Claims):** Topical herbal ointment claiming to cure medical skin diseases (psoriasis and eczema). Disqualified from Section 3(aaa). Expected: `unknown_ambiguous`, `referral` (`PASS-009`, `PASS-010`, `PASS-011`).

### 4.2 Evidence Retrieval Category (4 Scenarios)
11. **`SYN-CASE-011` (Dev · Patent Synergy Evidence):** Turmeric and black pepper mixture claiming patentability. Tests Section 3(p), 3(e), and CGPDTM examination guidelines on synergy. Expected: `patent_proprietary`, `answered` (`PASS-002`, `PASS-013`, `PASS-019`).
12. **`SYN-CASE-012` (Holdout · Biodiversity Foreign Approval):** Foreign pharmaceutical entity seeking Indian patent on Neem-derived formulation. Tests Biological Diversity Act Section 6(1) Form 7 approval before grant. Expected: `unknown_ambiguous`, `answered` (`PASS-005`, `PASS-015`).
13. **`SYN-CASE-013` (Dev · Biodiversity Domestic Registration):** Domestic Indian company filing patent on native plant extraction. Tests Biological Diversity Act Section 6(1A) Form 8 registration before grant and Section 6(1B) commercialization approval. Expected: `unknown_ambiguous`, `answered` (`PASS-016`).
14. **`SYN-CASE-014` (Holdout · International Treaty Overview):** Inquirer asking if WIPO GRATK Treaty confers immediate domestic enforcement rights against patent infringers. Tests treaty overview boundary. Expected: `unknown_ambiguous`, `answered` (`PASS-007`, `PASS-025`).

### 4.3 Insufficient Evidence / Missing Facts Category (3 Scenarios)
15. **`SYN-CASE-015` (Dev · Missing Ingredients & Text Citation):** Generic request to classify "Pachak-Plus" without providing ingredients or text references. Expected: `unknown_ambiguous`, `clarify` (`PASS-009`, `PASS-010`).
16. **`SYN-CASE-016` (Holdout · Missing First Schedule Citation):** Oral liquid claiming classical status but omitting authoritative text citation. Tests evidentiary gap rule. Expected: `unknown_ambiguous`, `clarify` (`PASS-009`, `PASS-017`, `PASS-023`).
17. **`SYN-CASE-017` (Dev · Unlisted Category A Recipe Procedure):** Inquirer asks if unlisted proprietary recipe can be sold under Category A without FSSAI representation. Tests 25 July 2025 FSSAI order. Expected: `unknown_ambiguous`, `answered` (`PASS-021`, `PASS-003`).

### 4.4 Adversarial & Jurisdiction Boundary Category (3 Scenarios)
18. **`SYN-CASE-018` (Holdout · Out-of-Scope US FDA Export):** User queries US FDA 21 CFR cGMP and NDI notification export compliance. Out-of-scope; system must abstain. Supporting passages are deliberately empty. Expected: `unknown_ambiguous`, `abstained` (gold passages: none).
19. **`SYN-CASE-019` (Dev · Out-of-Scope Software Algorithm):** User asks to patent a software diagnostic algorithm under Section 3(k). Out-of-scope for herbal formulation corpus; system must abstain. Supporting passages are deliberately empty. Expected: `unknown_ambiguous`, `abstained` (gold passages: none).
20. **`SYN-CASE-020` (Holdout · Confidential TKDL Access Request):** User requests confidential internal TKDL database entries and secret search codes. Safety safeguard; system must abstain. Supporting passages are deliberately empty. Expected: `unknown_ambiguous`, `abstained` (gold passages: none).

---

## 5. Audit Gate and Exact Split Summary

- **Total Cases:** 20
- **Reviewed Gold Cases:** 0
- **Unreviewed Provisional Cases:** 20 (100%)
- **Development Split (10 cases):** 5 answered, 3 referral, 1 clarify, 1 abstained.
- **Holdout Split (10 cases):** 4 answered, 3 referral, 2 abstained, 1 clarify (5 abstention/referral, 6 total non-confident safety cases representing 60% of holdout).
- **Assigned Reviewers:**
  - **Thulasi:** Authoritative source mappings (`gold_passage_ids`) and provisional classification routes.
  - **Deepshika:** Linguistic clarity and terminology in prompts and missing-fact prompts.
  - **Harshit:** Evaluation protocol compliance and RAG scoring criteria.

---

## 6. Verification and Validation Results

All checks were executed via `scripts/validate_sa01.py`:
- Schema and column counts: Passed (15 cols for scenarios, 16 cols for results template, 0 data rows in template).
- Behavior enum: Passed (100% compliant with `AnswerStatusEnum`).
- Abstention gold suppression: Passed (100% of `abstained` cases have empty gold passages).
- Referential integrity: Passed (100% of non-empty passage IDs exist in `data/corpus/passages.csv`).
- Stratification: Passed (10 development, 10 holdout; exact holdout safety distribution verified).
- Privacy and PII check: Passed (0 personal data or confidential records detected).
- Documentation whitespace: Passed (0 trailing whitespace).
