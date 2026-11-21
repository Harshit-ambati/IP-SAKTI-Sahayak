# Minimum-Question Intake Protocol, Classification Decision Rules, and Evidence Coverage (Task T-02)

- **Task ID:** T-02
- **Module Owner:** Thulasi (Authoritative source corpus, formulation categories and decision rules)
- **Target Window:** Weeks 3–4
- **Status:** Submitted for activation review (Draft PR on `thulasi/t-02-phase-2`)
- **Prior Phase Status:** Task T-01 merged into `main` via PR #1 (merge commit `1a7cae4`)
- **Reviewers:** Harshit (Technical lead / Corpus activation), Deepshika (Multilingual & Terminology)

---

## 1. Executive Summary & Objective

Task T-02 builds upon the initial scope defined in [thulasi-t01-specification.md](thulasi-t01-specification.md) by delivering:
1. **A Minimum-Question Intake Protocol**: A streamlined questionnaire workflow designed to determine the provisional product classification with the minimum number of user questions, complete with missing-fact prompts and fallback behaviors.
2. **Statutorily Grounded Decision Rules**: Complete mapping of intake conditions to verified statutory authorities, distinguishing Classical ASU, Patent or Proprietary (P&P) ASU, Ayurveda Aahara, and Ayurvedic Cosmetics.
3. **Strict Handling of Novel and Phytopharmaceutical Formulations**: Ensuring that novel chemical entities and phytopharmaceutical drugs are never forced into confident AYUSH categories, but are safely routed to professional referral.
4. **Official Evidence Coverage Map**: Documenting which corpus instruments support each intake decision, supported query topic, and legal boundary.
5. **Registry of Exclusions and Evidence Gaps**: Transparently recording out-of-scope regulatory areas and current knowledge corpus limitations.

---

## 2. Minimum-Question Intake Protocol

The intake protocol follows a progressive elimination strategy. Users are asked only the questions necessary to reach a definitive provisional route or safe referral, terminating early whenever disqualifying criteria are met:

```
                            [ Q-USE: Primary Intended Use ]
                                          │
        ┌─────────────────────────────────┼────────────────────────────────┐
        ▼                                 ▼                                ▼
  [ Medicinal ]                      [ Food/Dietary ]                 [ Cosmetic ]
        │                                 │                                │
  [ Q-INGR: Ingredients ]            [ Q-FOOD-TEXT ]                  [ Q-COSM-CLAIM ]
        │                                 │                                │
  [ Q-FORM: Recipe Source ]          [ Q-FOOD-CLAIM ]                      │
        │                                 │                                │
  [ Q-ROUTE: Parenteral? ]           [ Q-FOOD-SYN ]                        ▼
        │                                 │                    Route 6: Ayurvedic Cosmetic
        ▼                                 ▼
   Routes 1, 2, 3, or 4          Route 5: Ayurveda Aahara
```

### Intake Questions & Missing-Fact Prompts

| Question ID | Question Text & Purpose | Permissible Inputs | Missing-Fact Prompt (When input is missing/ambiguous) | Statutory Authority & Locator |
|---|---|---|---|---|
| **`Q-USE`** | *What is the primary intended use of the formulation?* Determines whether product falls under medicine, food, or cosmetic framework. | `medicinal` (treatment/cure/prevention), `food_dietary` (nourishment/supplement), `cosmetic` (cleansing/beautifying), `other` | *"Please specify the primary intended purpose: Is the product meant to treat/prevent a disease, serve as a daily dietary supplement, or provide external cosmetic care?"* | D&C Act 1940 s. 3(a), s. 3(aaa); FSSAI Ayurveda Aahara Reg. 2(b) |
| **`Q-INGR`** | *Are all active ingredients listed in authoritative Ayurvedic classical texts?* (Applicable when `Q-USE == medicinal`). | `all_classical` (100% in First Schedule books), `partial_classical` (contains non-classical plants/minerals), `synthetic_added` (contains synthetic chemicals) | *"Please confirm the source of your active ingredients: Are all botanical/mineral ingredients documented in recognized Ayurvedic texts such as Charaka Samhita or the Ayurvedic Pharmacopoeia of India?"* | D&C Act 1940 s. 3(a), First Schedule; Patents Act s. 3(p) |
| **`Q-FORM`** | *Is the recipe/formula identical to an authoritative classical text, or is it a novel/proprietary combination?* | `exact_classical_recipe`, `proprietary_combination`, `modified_dosage_form` | *"Is the formulation prepared strictly according to an unchanged recipe from an authoritative Ayurvedic book, or have you modified the combination, proportions, or dosage form?"* | D&C Act 1940 s. 3(a), s. 3(h); Drugs Rules r. 158-B |
| **`Q-ROUTE`** | *What is the intended route of administration?* Identifies parenteral contraindication. | `oral`, `topical`, `parenteral` (injectable/IV) | *"How is this medicine administered: orally, applied externally to the skin, or through an injection?"* | D&C Act 1940 s. 3(h); Drugs Rules r. 2(eb) |
| **`Q-FOOD-TEXT`**| *Is the dietary preparation prepared according to authoritative books listed in Schedule A?* | `yes`, `no` | *"Is this food preparation made in accordance with the recipes or principles in authoritative Ayurvedic books listed in Schedule A of the Ayurveda Aahara regulations?"* | FSSAI Ayurveda Aahara Reg. 2(b), Schedule A |
| **`Q-FOOD-CLAIM`**| *Does the food product packaging, labelling, or advertising claim to prevent, treat, or cure any human disease?* | `yes`, `no` | *"Does your product label or marketing material claim to cure, treat, or prevent any human disease?"* | FSSAI Ayurveda Aahara Reg. 8 |
| **`Q-FOOD-SYN`** | *Are any vitamins, minerals, amino acids, or synthetic additives added to the formulation?* | `yes`, `no` | *"Have you added any vitamins, minerals, amino acids, or synthetic nutrients to the product?"* | FSSAI Ayurveda Aahara Reg. 3(4) |
| **`Q-COSM-CLAIM`**| *Does the cosmetic product make therapeutic disease-treatment or prevention claims?* | `yes`, `no` | *"Does this external care product claim to treat or cure skin/hair diseases, or is it strictly for cleansing, grooming, or beautifying?"* | D&C Act 1940 s. 3(aaa) |

---

## 3. Classification Decision Rules (Task T-02)

| Rule ID | Classification Route | Trigger Condition Expression | Emitted Route | Primary Statutory Authority | Corpus Locators | Explanation & Guidance |
|---|---|---|---|---|---|---|
| **`RULE-T02-01`** | Classical ASU Drug | `Q-USE == "medicinal"` AND `Q-INGR == "all_classical"` AND `Q-FORM == "exact_classical_recipe"` AND `Q-ROUTE != "parenteral"` | **Route 1: Classical ASU** | D&C Act 1940 s. 3(a), Drugs Rules r. 158-B(I) | `REAL-002`, s. 3(a); `REAL-009`, r. 158-B(I); `PASS-009`, `PASS-017` | Formulations manufactured exclusively per formulae in First Schedule treatises qualify for classical licensing. Licensing application must cite specific classical treatise. |
| **`RULE-T02-02`** | Patent or Proprietary ASU Medicine | `Q-USE == "medicinal"` AND `Q-INGR == "all_classical"` AND `Q-FORM in ["proprietary_combination", "modified_dosage_form"]` AND `Q-ROUTE != "parenteral"` | **Route 2: Patent or Proprietary ASU** | D&C Act 1940 s. 3(h), Drugs Rules r. 158-B(II) | `REAL-002`, s. 3(h); `REAL-009`, r. 158-B(II); `PASS-010`, `PASS-018` | Contains only ingredients mentioned in First Schedule texts but prepared in proprietary ratios. Requires safety proof and published literature under Rule 158-B(II). Strictly excludes parenteral route. |
| **`RULE-T02-03`** | Phytopharmaceutical Drug | `Q-USE == "medicinal"` AND `has_purified_standardized_fraction == TRUE` AND `minimum_four_bioactive_markers == TRUE` AND `Q-ROUTE != "parenteral"` | **Route 4: Phytopharmaceutical (Referral)** | Drugs Rules 1945 r. 2(eb), Schedule Y Appendix I/IA | `REAL-002`, r. 2(eb); `REAL-012`, GSR 918(E); `PASS-012`, `PASS-022` | Regulated under modern CDSCO allopathic framework. Requires extensive animal toxicology, standardisation, and human clinical trials under Schedule Y. Emits referral notice. |
| **`RULE-T02-04`** | Novel / Non-Classical Formulation | `Q-USE == "medicinal"` AND (`Q-INGR in ["partial_classical", "synthetic_added"]` OR `contains_novel_botanical == TRUE`) | **Route 3: Novel / Referral** | D&C Act 1940 s. 3(a), s. 3(h); Patents Act s. 3(p) | `REAL-001`, s. 3(p); `REAL-002`, s. 3(h); `PASS-002`, `PASS-010` | Formulations introducing non-classical botanicals or synthetic actives cannot be licensed under standard ASU drug pathways. Referred to regulatory experts for new drug or AYUSH dual-license review. |
| **`RULE-T02-05`** | Ayurveda Aahara | `Q-USE == "food_dietary"` AND `Q-FOOD-TEXT == "yes"` AND `Q-FOOD-CLAIM == "no"` AND `Q-FOOD-SYN == "no"` | **Route 5: Ayurveda Aahara** | FSSAI Ayurveda Aahara Regs 2022, Reg. 2(b), 3(4), 8, 13(a) | `REAL-003`, Reg. 2(b), 3(4), 8, 13(a); `PASS-003`, `PASS-004`, `PASS-024` | Qualifies as Ayurveda Aahara food supplement. Must display official front-of-pack logo under Reg 13(a). Disqualified if vitamins/minerals/amino acids are added (Reg 3(4)) or if human disease prevention/treatment/cure claims are made (Reg 8). |
| **`RULE-T02-06`** | Ayurvedic Cosmetic | `Q-USE == "cosmetic"` AND `Q-COSM-CLAIM == "no"` AND `applied_to_human_body == TRUE` | **Route 6: Ayurvedic Cosmetic** | D&C Act 1940 s. 3(aaa) | `REAL-002`, s. 3(aaa); `PASS-011` | Topical application for cleansing, beautifying, or altering appearance without disease claims. If therapeutic claims are made, must route to Route 1 or 2 drug framework. |
| **`RULE-T02-07`** | Missing Data / Ambiguity Fallback | `any_required_input_is_missing_or_ambiguous == TRUE` | **Route 7: Unknown / Clarification** | Master Plan Safety Policy | N/A | When required facts are missing, the system never guesses or auto-classifies. Emits targeted missing-fact prompt to user. |

---

## 4. Representative Product Scenarios & Edge Cases

### Scenario 1: Classical Churna (Route 1)
- **User Inputs:** `Q-USE = medicinal`, `Q-INGR = all_classical`, `Q-FORM = exact_classical_recipe` (Saraswatarishta per Charaka Samhita), `Q-ROUTE = oral`.
- **System Outcome:** Classified as **Route 1: Classical ASU Drug**.
- **Evidence Emitted:** `REAL-002` (s. 3(a)), `REAL-009` (r. 158-B(I)), `PASS-009`, `PASS-017`.
- **Guidance:** Applicant must identify the First Schedule authoritative treatise in application; no separate clinical efficacy trial is required by SLA.

### Scenario 2: Polyherbal Tablet Formulation (Route 2)
- **User Inputs:** `Q-USE = medicinal`, `Q-INGR = all_classical` (Ashwagandha, Shatavari, Gokshura), `Q-FORM = proprietary_combination` (novel proprietary ratio in compressed tablet form), `Q-ROUTE = oral`.
- **System Outcome:** Classified as **Route 2: Patent or Proprietary (P&P) ASU Medicine**.
- **Evidence Emitted:** `REAL-002` (s. 3(h)), `REAL-009` (r. 158-B(II)), `PASS-010`, `PASS-018`.
- **Guidance:** Must provide published safety literature and proof of effectiveness to State Licensing Authority under Rule 158-B(II). Cannot be administered parenterally.

### Scenario 3: Standardized Herbal Fraction with 4 Markers (Route 4)
- **User Inputs:** `Q-USE = medicinal`, `Q-INGR = partial_classical`, extract containing 4 isolated and standardized phytochemical markers (curcuminoids fraction), `Q-ROUTE = oral`.
- **System Outcome:** Safely routed to **Route 4: Phytopharmaceutical Drug (Referral)**.
- **Evidence Emitted:** `REAL-002` (r. 2(eb)), `REAL-012` (GSR 918(E)), `PASS-012`, `PASS-022`.
- **Guidance:** This is not an AYUSH drug. Requires CDSCO new drug application, Schedule Y clinical trials, and toxicological profiling.

### Scenario 4: Herbal Tea with Added Vitamins (Route 5 Edge Case)
- **User Inputs:** `Q-USE = food_dietary`, `Q-FOOD-TEXT = yes` (Tulsi-Ginger recipe from classical texts), `Q-FOOD-CLAIM = no`, `Q-FOOD-SYN = yes` (added Vitamin C for immunity fortification).
- **System Outcome:** Disqualified from Route 5; routed to **Route 7: Referral / Clarification**.
- **Evidence Emitted:** `REAL-003` (Reg. 3(4), Reg. 2(b)), `PASS-003`.
- **Guidance:** Adding vitamins, minerals, or amino acids violates Regulation 3(4) of FSSAI Ayurveda Aahara Regulations. Product must either remove added vitamins or seek licensing under FSSAI Nutraceutical Regulations 2022.

### Scenario 5: Herbal Tea with Disease Prevention Claims (Route 5 Edge Case)
- **User Inputs:** `Q-USE = food_dietary`, `Q-FOOD-TEXT = yes`, `Q-FOOD-SYN = no`, `Q-FOOD-CLAIM = yes` (packaging claims *"Prevents viral infections and treats respiratory cough"*).
- **System Outcome:** Disqualified from Route 5; routed to **Route 7: Referral / Clarification**.
- **Evidence Emitted:** `REAL-003` (Reg. 8, Reg. 2(b)), `PASS-004`.
- **Guidance:** Claiming to prevent, treat, or cure human disease violates Regulation 8 of Ayurveda Aahara Regulations. Therapeutic claims require licensing as an Ayurvedic drug under Section 3(a) or 3(h) of Drugs and Cosmetics Act.

---

## 5. Official Evidence Coverage Map (Task T-02)

| Source ID | Official Document Title | Issuing Authority | Key Statutory Locators | Supported System Routes & Functions | Verification Status |
|---|---|---|---|---|---|
| `REAL-001` | *The Patents Act, 1970* | IP India / Legislative Dept | Section 3(p), Section 3(e), Section 3(d) | Traditional knowledge patent exclusions, mere admixture exclusions, new use exclusions | `reviewed_t02_pending_activation` |
| `REAL-002` | *The Drugs and Cosmetics Act, 1940* | Ministry of Ayush / CDSCO | Section 3(a), First Schedule, Section 3(h), Section 3(aaa), Rule 2(eb) | Route 1 (Classical ASU), Route 2 (P&P ASU), Route 6 (Cosmetic), Route 4 (Phytopharmaceutical) | `reviewed_t02_pending_activation` |
| `REAL-003` | *FSSAI Ayurveda Aahara Regulations, 2022* | FSSAI | Regulation 2(b), Regulation 3(4), Regulation 8, Regulation 13(a), Regulation 13(f), Schedule A | Route 5 (Ayurveda Aahara definition, exclusions of drugs/cosmetics/synthetic nutrients, human disease claims prohibition, logo mandate, oral warning) | `reviewed_t02_pending_activation` |
| `REAL-004` | *Biological Diversity Rules, 2024* | National Biodiversity Authority | Rule 1(2), Form 7, Form 8 | Biodiversity governance; notified 22 Oct 2024, commencement 21 Dec 2024 per NBA FAQ; Form 7/Form 8 IPR procedures | `reviewed_t02_pending_activation` |
| `REAL-005` | *Biological Diversity Amendment Rules, 2025* | National Biodiversity Authority | Rule amendment provisions | Updates to fee schedules and operational Form 7/Form 8 procedures for ABS; notified 6 May 2025, commencement 1 Nov 2025 per NBA FAQ | `reviewed_t02_pending_activation` |
| `REAL-006` | *WIPO GRATK Treaty (Adopted May 2024)* | WIPO | Article 3, Article 5, Article 6 | International patent disclosure overview; Article 5 remedies, Article 6 information systems; strictly bounded as non-domestic legal text | `reviewed_t02_pending_activation` |
| `REAL-007` | *TKDL Public Overview* | CSIR / Ministry of Ayush | Public overview, access agreement terms | Defensive protection context; non-confidential prior art search agreements | `reviewed_t02_pending_activation` |
| `REAL-008` | *The Biological Diversity Act, 2002* (as amended 2023) | Ministry of Environment / NBA | Section 6(1), Section 6(1A), Section 6(1B), Section 6(2), Section 7(1) proviso | Section 6 amendments effective 1 Apr 2024: NBA approval before grant for s. 3(2) foreign entities (s. 6(1), Form 7); NBA registration before grant (s. 6(1A), Form 8) and approval before commercialization (s. 6(1B)) for s. 7 domestic entities; vaid/hakim routine commercial exemption (s. 7(1) proviso) | `reviewed_t02_pending_activation` |
| `REAL-009` | *Drugs Rules, 1945 — Rule 158-B* | Ministry of Ayush | Rule 158-B(I), Rule 158-B(II) | Evidentiary requirements for licensing: classical book citation vs safety/literature proof for P&P | `reviewed_t02_pending_activation` |
| `REAL-010` | *CGPDTM Guidelines on TK Patent Applications (2012)* | Office of CGPDTM (IP India) | Paragraph 4.1, Paragraph 4.2 | Administrative examination criteria for s. 3(p)/3(e) exclusions and TKDL prior art screening | `reviewed_t02_pending_activation` |
| `REAL-011` | *FSSAI Implementation Order (25 July 2025)* | FSSAI | Clarification on Ayurveda Aahara enforcement | Enforcement timelines, logo licensing, distinction from general dietary supplements | `reviewed_t02_pending_activation` |
| `REAL-012` | *Drugs Rules, 1945 — Phytopharmaceuticals (GSR 918(E))*| CDSCO / Health Ministry | Rule 2(eb), Schedule Y Appendix I/IA | Route 4: CDSCO regulatory requirements for phytopharmaceutical new drugs | `reviewed_t02_pending_activation` |

---

## 6. Exclusions and Evidence Gaps Registry

To prevent legal over-reach and maintain transparency, the following exclusions and evidence gaps are formally recorded:

### Explicitly Excluded Domains (Out-of-Scope)
1. **Foreign Country-Specific Export Compliance**: The system does NOT evaluate compliance with the US FDA, EU EMA, UK MHRA, or individual foreign import regimes. Users are directed to international overviews or export councils.
2. **Freedom-to-Operate (FTO) & Infringement Searches**: The system cannot perform commercial patent clearance searches or guarantee that an Ayurvedic formulation is free from patent infringement.
3. **Automated Regulatory Approval Guarantees**: Classifications are provisional informational assessments; they do not substitute for formal State Licensing Authority or FSSAI license grant.
4. **General Nutraceutical Framework**: Ayurveda Aahara is distinct from general nutraceuticals, health supplements, or foods for special medical purposes (FSSAI Nutraceutical Regulations 2022). General nutraceuticals are out of scope.

### Current Evidence Gaps in Corpus
1. **Schedule 1 Text Transcripts**: The corpus contains references to the 54 authoritative classical books listed in the First Schedule to the Drugs and Cosmetics Act, but does not index the full text of all classical treatises. Formulation verification relies on user declaration of text reference.
2. **State-Specific AYUSH Licensing Portals**: Procedural licensing rules vary marginally across State AYUSH departments; the corpus models central statutory criteria only.
3. **National Biodiversity Authority (NBA) Specific SBB Benefit-Sharing Rates**: While Section 6 approval mandates are verified, local State Biodiversity Board (SBB) commercial ABS fee schedules are variable and require direct NBA consultation.
