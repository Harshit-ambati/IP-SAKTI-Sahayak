# Minimum-Question Intake Protocol, Classification Decision Rules, and Evidence Coverage (Task T-02)

**Task ID:** T-02  
**Module Owner:** Thulasi (Authoritative source corpus, formulation categories and decision rules)  
**Target Window:** Weeks 3–4  
**Status:** Submitted for activation review (Draft PR on `thulasi/t-02-phase-2`)  
**Reviewers:** Harshit (Technical lead / Corpus activation), Deepshika (Multilingual & Terminology)  

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
| **`Q-ROUTE`** | *What is the route of administration?* Specifically checks for parenteral administration (injections/IV). | `oral`, `topical`, `nasal/ocular`, `parenteral` (injection/IV) | *"How is this product administered (e.g., orally, applied to the skin)? Note: Injectable formulations cannot be licensed as Ayurvedic medicines."* | D&C Act 1940 s. 3(h); Drugs Rules r. 2(eb); FSSAI Reg. 2(b) |
| **`Q-PHYTO`** | *Is the formulation a purified, standardized plant extract with defined bioactive compounds?* | `standardized_fraction_4plus` (purified fraction, >= 4 bioactives), `crude_extract_or_powder` | *"Is this product a purified standardized fraction characterized by at least four bioactive chemical markers, or is it a traditional crude extract/formulation?"* | Drugs Rules 1945 Rule 2(eb), Schedule Y |
| **`Q-FOOD-TEXT`** | *Is the recipe or ingredient described in authoritative Ayurvedic books recognized for food?* (Applicable when `Q-USE == food_dietary`). | `schedule_a_text`, `modern_novel_food`, `unknown` | *"Is this food product based on recipes or ingredients described in classical Ayurvedic texts recognized under Schedule A of the Ayurveda Aahara Regulations?"* | FSSAI Ayurveda Aahara Regs 2022, Reg. 2(b) & Schedule A |
| **`Q-FOOD-CLAIM`**| *Does the food product packaging or marketing claim to prevent, treat, or cure any human disease?* | `claims_disease_cure == TRUE`, `claims_disease_cure == FALSE` | *"Does the product make any claims to treat, cure, or prevent human diseases? (Ayurveda Aahara regulations strictly prohibit disease-cure claims)."* | FSSAI Ayurveda Aahara Regs 2022, Reg. 8 |
| **`Q-FOOD-SYN`**  | *Are any synthetic vitamins, minerals, amino acids, or isolated chemical additives added?* | `synthetic_nutrients_added == TRUE`, `synthetic_nutrients_added == FALSE` | *"Does this food product contain synthetic vitamins, minerals, or amino acids? (Ayurveda Aahara permits only naturally occurring nutrients)."* | FSSAI Ayurveda Aahara Regs 2022, Reg. 2(b)(v) |
| **`Q-COSM-CLAIM`**| *Does the cosmetic product make any therapeutic, curative, or medicinal claims?* (Applicable when `Q-USE == cosmetic`). | `medicinal_claims == TRUE`, `cosmetic_only == TRUE` | *"Is the product intended solely for external cleansing/beautification, or does it claim therapeutic treatment for skin/hair diseases?"* | D&C Act 1940 s. 3(aaa), s. 3(b) |

---

## 3. Classification Decision Rules Matrix

The table below defines the complete decision rules, minimum condition set, resulting provisional classification, governing statutory authority, and automated referral triggers:

| Rule ID | Minimum Condition Set | Resulting Route | Governing Provision | Cited Corpus Locators | Action on Incomplete / Ambiguous Data |
|---|---|---|---|---|---|
| **`RULE-T02-01`** | `Q-USE == "medicinal"` AND `Q-INGR == "all_classical"` AND `Q-FORM == "exact_classical_recipe"` AND `Q-ROUTE != "parenteral"` | **Route 1: Classical Ayurvedic Medicine** | D&C Act 1940, Section 3(a), First Schedule; Drugs Rules 1945, Rule 158-B(I) | `REAL-002`, s. 3(a); `REAL-009`, r. 158-B(I) | If book citation missing, issue missing-fact prompt for First Schedule text name; if unavailable, demote to `RULE-T02-02`. |
| **`RULE-T02-02`** | `Q-USE == "medicinal"` AND `Q-INGR == "all_classical"` AND (`Q-FORM == "proprietary_combination"` OR `Q-FORM == "modified_dosage_form"`) AND `Q-ROUTE != "parenteral"` | **Route 2: Patent or Proprietary (P&P) Ayurvedic Medicine** | D&C Act 1940, Section 3(h); Drugs Rules 1945, Rule 158-B(II) | `REAL-002`, s. 3(h); `REAL-009`, r. 158-B(II) | If parenteral, trigger automatic rejection. If safety/literature data missing, advise of Rule 158-B proof requirements. |
| **`RULE-T02-03`** | `Q-USE == "medicinal"` AND (`Q-INGR == "partial_classical"` OR `Q-INGR == "synthetic_added"`) AND `Q-PHYTO != "standardized_fraction_4plus"` | **Route 3: Novel / Non-Classical Formulation (Mandatory Referral)** | D&C Act 1940, general non-ASU provisions; New Drugs Rules 2019 | `REAL-002`, general; safe referral policy | **Strict Non-Forcing:** Assistant must NOT force product into ASU licensing. Issue warning that formulation falls outside AYUSH and output professional referral packet. |
| **`RULE-T02-04`** | `Q-USE == "medicinal"` AND `Q-PHYTO == "standardized_fraction_4plus"` AND `Q-ROUTE != "parenteral"` | **Route 4: Phytopharmaceutical Drug (Mandatory Referral)** | Drugs Rules 1945, Rule 2(eb), Rule 122E, Schedule Y | `REAL-002`, r. 2(eb); `REAL-012`, Schedule Y | **Strict Non-Forcing:** Inform user of CDSCO regulatory framework (clinical trials/toxicology required). Do not classify as AYUSH proprietary medicine; issue referral packet. |
| **`RULE-T02-05`** | `Q-USE == "food_dietary"` AND `Q-FOOD-TEXT == "schedule_a_text"` AND `Q-FOOD-CLAIM == FALSE` AND `Q-FOOD-SYN == FALSE` AND `Q-ROUTE != "parenteral"` | **Route 5: Ayurveda Aahara** | FSSAI Ayurveda Aahara Regs 2022, Reg. 2(b), Reg. 8 | `REAL-003`, reg. 2(b), reg. 8; `REAL-011`, order 2025 | If disease cure claimed, issue violation notice under Reg. 8; if synthetic vitamins added, reject under Reg. 2(b) and refer to general nutraceuticals. |
| **`RULE-T02-06`** | `Q-USE == "cosmetic"` AND `Q-ROUTE == "topical"` AND `Q-COSM-CLAIM == "cosmetic_only"` | **Route 6: Ayurvedic Cosmetic** | D&C Act 1940, Section 3(aaa) | `REAL-002`, s. 3(aaa) | If medicinal/disease cure claims made, re-route to `Q-USE == "medicinal"`. |
| **`RULE-T02-07`** | Any required intake fact missing, contradictory, or user responds "unknown" | **Route 7: Unknown / Clarification / Referral** | Master Plan Safety & Abstention Protocol | `REAL-001`, `REAL-002`, `REAL-003` | Output specific missing-fact prompt. If unresolvable, provide structured referral packet. Never hallucinate or default to confident classification. |
| **`RULE-T02-08`** | User query relates to Indian patentability of Ayurvedic formulation | **Patent Scrutiny & Exclusion Notice** | Patents Act 1970, Section 3(p), Section 3(e), Section 3(d); CGPDTM Guidelines 2012 | `REAL-001`, s. 3(p), s. 3(e); `REAL-010`, para 4.1 | Disclose Section 3(p) (traditional knowledge aggregation) and 3(e) (mere admixture); explain that unexpected synergistic effect supported by comparative data is required to overcome 3(e). |
| **`RULE-T02-09`** | User query involves biological material obtained from India for IPR application | **Biodiversity / NBA Prior Approval Notice** | Biological Diversity Act 2002, Section 6 (as amended 2023) | `REAL-008`, s. 6(1), s. 6(1A) | Alert user that Section 6(1) mandates prior approval of National Biodiversity Authority before filing patent applications in or outside India. |

---

## 4. Evidence Coverage Map

The table below maps the 11 reviewed official corpus instruments to the supported topics, classification routes, and system boundaries:

| Source ID | Official Instrument Title | Issuing Authority | Operative Provisions Covered | Supported Topics & Classification Routes | Verification & Status |
|---|---|---|---|---|---|
| `REAL-001` | *The Patents Act, 1970* (as amended) | IP India / Legislative Dept | Section 3(p), Section 3(e), Section 3(d) | Indian patent exclusions for ASU formulations; Section 3(p) TK aggregation, 3(e) mere admixture | `reviewed_t02_pending_activation` |
| `REAL-002` | *The Drugs and Cosmetics Act, 1940* | Ministry of Ayush / CDSCO | Section 3(a), First Schedule, Section 3(h), Section 3(aaa), Rule 2(eb) | Route 1 (Classical ASU), Route 2 (P&P ASU), Route 6 (Cosmetic), Route 4 (Phytopharmaceutical) | `reviewed_t02_pending_activation` |
| `REAL-003` | *FSSAI Ayurveda Aahara Regulations, 2022* | FSSAI | Regulation 2(b), Regulation 8, Schedule A | Route 5 (Ayurveda Aahara definition, exclusions of drugs/cosmetics, claims prohibition) | `reviewed_t02_pending_activation` |
| `REAL-004` | *Biological Diversity Rules, 2024* | National Biodiversity Authority | Rule 1(2), Rule 14 | Biodiversity governance; commencement and IPR application procedures | `reviewed_t02_pending_activation` |
| `REAL-005` | *Biological Diversity Amendment Rules, 2025* | National Biodiversity Authority | Gazette amendment provisions | Updates to fee schedules and operational procedures for ABS | `reviewed_t02_pending_activation` |
| `REAL-006` | *WIPO GRATK Treaty (Adopted May 2024)* | WIPO | Article 3, Article 5 | International patent disclosure overview; strictly bounded as non-domestic legal text | `reviewed_t02_pending_activation` |
| `REAL-007` | *TKDL Public Overview* | CSIR / Ministry of Ayush | Public overview, access agreement terms | Defensive protection context; non-confidential prior art search agreements | `reviewed_t02_pending_activation` |
| `REAL-008` | *The Biological Diversity Act, 2002* (as amended 2023) | Ministry of Environment / NBA | Section 6(1), Section 6(1A) | Mandatory prior NBA approval before applying for IPR on Indian biological resources | `reviewed_t02_pending_activation` |
| `REAL-009` | *Drugs Rules, 1945 — Rule 158-B* | Ministry of Ayush | Rule 158-B(I), Rule 158-B(II) | Evidentiary requirements for licensing: classical book citation vs safety/literature proof for P&P | `reviewed_t02_pending_activation` |
| `REAL-010` | *CGPDTM Guidelines on TK Patent Applications (2012)* | Office of CGPDTM (IP India) | Paragraph 4.1, Paragraph 4.2 | Administrative examination criteria for s. 3(p)/3(e) exclusions and TKDL prior art screening | `reviewed_t02_pending_activation` |
| `REAL-011` | *FSSAI Implementation Order (25 July 2025)* | FSSAI | Clarification on Ayurveda Aahara enforcement | Enforcement timelines, logo licensing, distinction from general dietary supplements | `reviewed_t02_pending_activation` |
| `REAL-012` | *Drugs Rules, 1945 — Phytopharmaceuticals (GSR 918(E))*| CDSCO / Health Ministry | Rule 2(eb), Schedule Y Appendix I/IA | Route 4: CDSCO regulatory requirements for phytopharmaceutical new drugs | `reviewed_t02_pending_activation` |

---

## 5. Exclusions and Evidence Gaps Registry

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
