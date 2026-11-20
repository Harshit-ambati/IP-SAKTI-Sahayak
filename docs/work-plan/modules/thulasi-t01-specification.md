# Thulasi Module Specification: Supported Topics and Classification Decision Rules (Task T-01)

**Task ID:** T-01  
**Module Owner:** Thulasi (Authoritative source corpus, formulation categories and decision rules)  
**Target Window:** Weeks 1–2  
**Status:** Submitted for activation review (Draft PR)  
**Reviewers:** Harshit (Technical lead / Corpus activation), Deepshika (Multilingual & Terminology)  

---

## 1. Executive Summary & Objective

In accordance with [MASTER_PLAN.md](../MASTER_PLAN.md) and [02-thulasi.md](02-thulasi.md), Task T-01 establishes the foundational domain boundary and classification decision rules for IP-SAKTI Sahayak:
1. **Agree supported topics and operational boundaries**: Explicitly delimits what the assistant covers (India patent exclusions, ASU product categories, Ayurveda Aahara, and bounded treaty background) and what is strictly out of scope (foreign country export compliance, legal advice, commercial freedom-to-operate).
2. **Define six provisional classification routes**: Statutorily grounds the six required formulation routes and an explicit unknown/ambiguous fallback route with mandatory referral.
3. **Draft formulation intake questions and decision rules**: Specifies the intake question logic, condition checks, expected provisional routing, statutory provisions, and referral behaviors.
4. **Deliver three verified official instruments and reviewed provision passages**: Grounds the rules in operative statutory text (Patents Act 1970, Drugs and Cosmetics Act 1940, and FSSAI Ayurveda Aahara Regulations 2022) with a companion source audit note ([SOURCE_AUDIT_T01.md](../../data/corpus/SOURCE_AUDIT_T01.md)).

---

## 2. Supported Topics and Scope Boundaries

To prevent legal hallucination and keep workload achievable for a six-member team, the MVP knowledge corpus is strictly bounded to the following six topic domains:

| Topic Code | Domain Description | Governing Official Instruments | MVP Inclusion Scope | Explicit Exclusions / Non-Goals |
|---|---|---|---|---|
| `patents` | Indian Patent Law exclusions relevant to ASU formulations and traditional knowledge | *The Patents Act, 1970* (as amended in 2002 and 2005, Acts 38 of 2002 & 15 of 2005) | Section 3(p) [traditional knowledge aggregation], Section 3(e) [mere admixture], Section 3(d) [new form / known efficacy requirement] | No patentability opinions, validity determinations, or freedom-to-operate (FTO) searches |
| `ayurveda_product_classification` | Indian statutory product categorization for Ayurvedic drugs, cosmetics, and phytopharmaceuticals | *The Drugs and Cosmetics Act, 1940* (Act 23 of 1940) and *Drugs Rules, 1945* (as amended) | Section 3(a) [Classical ASU drug], First Schedule [Authoritative texts], Section 3(h) [Patent or proprietary ASU drug], Section 3(aaa) [Cosmetic], Drugs Rules Rule 2(eb) [Phytopharmaceutical drug] | No clinical trial clearance, GMP certification audits, or commercial licensing guarantees |
| `ayurveda_aahara` | Food and dietary supplement regulatory framework for Ayurvedic recipes and foods | *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022* (FSSAI Gazette 05/09 May 2022) | Regulation 2(b) [Definition and statutory exclusions of drugs/cosmetics], Regulation 3(4) [Statutory ban on vitamins, minerals, amino acids], Regulation 8 [Prohibition against claims to prevent, treat or cure disease], Regulation 13(a) [Front-of-pack logo], Schedule A [Authoritative texts] | Not interchangeable with general nutraceuticals (FSSAI Nutraceutical Regulations 2022). No general food safety licensing advice |
| `biodiversity` | Access and Benefit Sharing (ABS) governance under Indian law | *The Biological Diversity Act, 2002* and *Biological Diversity Rules, 2024 / Amendment Rules 2025* | Preliminary awareness: National Biodiversity Authority (NBA) approval requirements for IPR applications involving Indian biological resources (Section 6) | General guidance only in Phase 1; complete operative rules pending T-03 verification. No commercial ABS fee calculations |
| `traditional_knowledge` | Public overview and defensive protection role of TKDL | Traditional Knowledge Digital Library (TKDL) official public documentation | Public background on prior-art search agreements with patent offices and defensive protection mechanisms | No access to confidential or restricted TKDL database entries; cannot search proprietary formulations |
| `international_treaty` | International intellectual property and genetic resources overview | *WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (GRATK)* (adopted May 2024) | Overview of patent disclosure requirements regarding genetic resources and associated TK; strictly distinguished from domestic Indian legislation | No country-by-country export compliance, foreign national patent office advice, or claims of direct domestic enforceability |

### System-Wide Abstention and Exclusions
Under no circumstances shall IP-SAKTI Sahayak:
- Provide legal counsel or formal patent prosecution filings.
- Assert that international treaties (such as WIPO GRATK) alter domestic Indian requirements prior to national enabling legislation.
- Grant definitive classification when user input omits active ingredients, administration mode, or intended use.

---

## 3. The Six Provisional Classification Routes

Under Indian law, product categorization governs the regulatory authority, licensing route, permissible claims, and patent exclusions. The system implements six provisional routes plus a mandatory ambiguous/referral route:

```
                          [User Formulation Query]
                                     |
              +----------------------+----------------------+
              |                                             |
     [Intended as Medicine?]                       [Food or Cosmetic?]
              |                                             |
     +--------+--------+                           +--------+--------+
     |                 |                           |                 |
[Classical]     [Proprietary/Novel]         [Ayurveda Aahara]   [Cosmetic]
     |                 |                           |                 |
  Route 1       +------+------+                 Route 5           Route 6
(D&C s.3(a))   |             |               (FSSAI Regs)     (D&C s.3(aaa))
             Route 2       Route 3 / 4
          (D&C s.3(h))    (Novel / Phyto)
```

1. **Route 1: Classical Ayurvedic Medicine (Shastriya)**
   - *Statutory Basis:* *Drugs and Cosmetics Act, 1940*, Section 3(a).
   - *Core Criterion:* Manufactured exclusively in accordance with formulae described in the authoritative books specified in the First Schedule to the Act.
   - *Key Consequence:* Eligible for classical ASU licensing; exempt from novel clinical trial data under Rule 158-B; excluded from patentability under Patents Act Section 3(p) as traditional knowledge.

2. **Route 2: Patent or Proprietary Ayurvedic Medicine**
   - *Statutory Basis:* *Drugs and Cosmetics Act, 1940*, Section 3(h).
   - *Core Criterion:* Contains only ingredients mentioned in the authoritative books of the First Schedule, but the combination, proportion, or processing is not in the classical formulae. Excludes parenteral administration.
   - *Key Consequence:* Requires proof of safety and effectiveness under Rule 158-B; patentability requires addressing Section 3(p) (traditional knowledge) and Section 3(e) (mere admixture), where demonstrating synergistic effect is an examination consideration under IP India Guidelines rather than a statutory guarantee.

3. **Route 3: Novel / Non-Classical Formulation**
   - *Statutory Basis:* Outside ASU definitions; governed by general new drug provisions (*Drugs and Cosmetics Act, 1940*, Chapter IV / New Drugs and Clinical Trials Rules, 2019).
   - *Core Criterion:* Contains synthetic active compounds, novel chemical entities, or non-classical botanicals claiming therapeutic efficacy.
   - *Key Consequence:* Must be routed away from Ayush State Licensing Authorities to CDSCO allopathic/new drug approvals; patentability assessed under general patent criteria (Sections 2(1)(j), 3(d), 3(e)).

4. **Route 4: Phytopharmaceutical Drug**
   - *Statutory Basis:* *Drugs Rules, 1945*, Rule 2(eb) (inserted via Gazette G.S.R. 918(E) dated 30 November 2015).
   - *Core Criterion:* Purified and standardized fraction with defined minimum of four bioactive or phytochemical compounds of an extract of a medicinal plant; non-parenteral.
   - *Key Consequence:* Evaluated under CDSCO phytopharmaceutical regulatory framework (Schedule Y / New Drugs Rules) with preclinical and clinical trial data.

5. **Route 5: Ayurveda Aahara**
   - *Statutory Basis:* *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022*, Regulation 2(b).
   - *Core Criterion:* Food prepared in accordance with recipes, ingredients, or processes in authoritative books listed in Schedule A. Strictly excludes Ayurvedic drugs and cosmetics (Regulation 2(b)). Must not contain added vitamins, minerals, or amino acids (Regulation 3(4)). Must carry the Ayurveda Aahara front-of-pack logo (Regulation 13(a)), carry the oral-consumption warning (Regulation 13(f)), and must not claim to prevent, treat or cure disease (Regulation 8).
   - *Key Consequence:* Regulated under FSSAI, not Ayush or CDSCO; cannot make medicinal prevention, treatment, or cure claims.

6. **Route 6: Ayurvedic Cosmetic**
   - *Statutory Basis:* *Drugs and Cosmetics Act, 1940*, Section 3(aaa).
   - *Core Criterion:* Applied externally to the human body for cleansing, beautifying, promoting attractiveness, or altering appearance; non-parenteral.
   - *Key Consequence:* Must not claim therapeutic or medicinal prevention/cure effects; governed by cosmetic licensing standards.

7. **Route 7: Unknown / Clarification / Referral Route (System Safeguard)**
   - *Mandatory Fallback:* Triggered whenever the user query omits essential classification facts (e.g., intended use, ingredient origin, administration mode) or inputs conflicting attributes. Missing classical text citations must route here for clarification rather than defaulting to proprietary status.

---

## 4. Minimum Intake Logic & Decision Rules (T-01)

| Rule ID | Intake Condition / Question Evaluated | Logic / Condition Expression | Resulting Route | Governing Provision | Source ID & Locator | Ambiguity / Fallback Action |
|---|---|---|---|---|---|---|
| **RULE-01** | What is the intended primary use of the formulation? | `intended_use == "medicinal"` AND `ingredients_all_classical == TRUE` AND `formula_in_first_schedule == TRUE` AND `claims_disease_treatment == TRUE` | **Route 1: Classical Ayurvedic Medicine** | D&C Act 1940, Section 3(a), First Schedule | `REAL-002`, s. 3(a) | If text citation is missing, prompt for specific First Schedule text citation; if absent, route to Route 7 (Unknown / Clarification / Referral) rather than defaulting to proprietary route, because missing classical evidence is an evidentiary gap requiring expert clarification, not affirmative proof of proprietary medicine. |
| **RULE-02** | Are all ingredients in First Schedule texts, but the combination or form is proprietary? | `intended_use == "medicinal"` AND `ingredients_all_classical == TRUE` AND `formula_in_first_schedule == FALSE` AND `parenteral == FALSE` | **Route 2: Patent or Proprietary Ayurvedic Medicine** | D&C Act 1940, Section 3(h) | `REAL-002`, s. 3(h) | If any ingredient is non-classical or unlisted, trigger RULE-03. If parenteral, reject immediately. |
| **RULE-03** | Does the formulation contain synthetic substances or non-classical botanicals claiming therapeutic effect? | `intended_use == "medicinal"` AND (`has_synthetic_active == TRUE` OR `ingredients_all_classical == FALSE`) AND `phytopharmaceutical_criteria == FALSE` | **Route 3: Novel / Non-Classical Formulation** | D&C Act 1940, general non-ASU provisions | `REAL-002`, general; safe referral | Automatic abstention on ASU licensing; generate referral packet to CDSCO/allopathic patent attorney. |
| **RULE-04** | Is the product a purified, standardized plant fraction with defined bioactive markers? | `intended_use == "medicinal"` AND `standardized_fraction == TRUE` AND `bioactive_markers_count >= 4` AND `parenteral == FALSE` | **Route 4: Phytopharmaceutical Drug** | Drugs Rules 1945, Rule 2(eb) | `REAL-002`, r. 2(eb) | Mandatory referral to CDSCO new drug regulatory framework. |
| **RULE-05** | Is the product intended as food/supplement based on classical recipes, without disease cure claims? | `intended_use == "food_dietary"` AND `recipe_in_schedule_a == TRUE` AND `synthetic_nutrients_added == FALSE` AND `claims_disease_cure == FALSE` | **Route 5: Ayurveda Aahara** | FSSAI Regs 2022, Reg. 2(b), Reg. 3(4), Reg. 8 & Reg. 13(a) | `REAL-003`, reg. 2(b), reg. 3(4), reg. 8, reg. 13(a) | If disease cure/treatment claimed, flag violation of Reg. 8 (prevent, treat or cure prohibition); if synthetic vitamins, minerals, or amino acids added, violate Reg. 3(4) and exclude under Reg. 2(b) and refer to Route 7. |
| **RULE-06** | Is the product applied externally for cleansing/beautifying without therapeutic claims? | `intended_use == "cosmetic"` AND `external_application_only == TRUE` AND `claims_disease_treatment == FALSE` | **Route 6: Ayurvedic Cosmetic** | D&C Act 1940, Section 3(aaa) | `REAL-002`, s. 3(aaa) | If medicinal/cure claims are made, re-evaluate under drug rules (RULE-01 or RULE-02). |
| **RULE-07** | Are formulation ingredients, intended use, or processing details missing or conflicting? | `missing_mandatory_facts == TRUE` OR `conflicting_intake_inputs == TRUE` | **Route 7: Unknown / Clarification / Referral** | Master Plan Safety & Abstention Policy | `REAL-001`, `REAL-002`, `REAL-003` | Prompt for missing facts; generate structured referral packet; do not output confident classification. |
| **RULE-08** | Is the user querying Indian patentability for an Ayurvedic formulation? | `query_type == "patentability_india"` AND `is_traditional_knowledge_or_aggregation == TRUE` | **Patent Exclusion Notice** | Patents Act 1970, Section 3(p) & Section 3(e) | `REAL-001`, s. 3(p), s. 3(e) | Explain statutory exclusions under 3(p) (traditional knowledge) and 3(e) (mere admixture); note that under IP India examination guidelines for AYUSH-related inventions, demonstrating synergistic effect is an examination consideration when assessing whether a combination is more than a mere aggregation of known properties, but does not constitute an automatic statutory exception or guaranteed grant of patentability. |

---

## 5. First Reviewed Official Source Records & Operative Provisions

Three exact official instruments have been verified and submitted for Harshit's activation review. Full provenance and checksum details are recorded in [SOURCE_AUDIT_T01.md](../../data/corpus/SOURCE_AUDIT_T01.md) and [source_register.csv](../../data/corpus/source_register.csv).

1. **REAL-001: The Patents Act, 1970 (Act 39 of 1970)**
   - *Authority*: Controller General of Patents, Designs and Trade Marks (IP India), Ministry of Commerce and Industry.
   - *Key Provisions Reviewed*: Section 3(p), Section 3(e), Section 3(d).
   - *Amendment History*: Act 38 of 2002 (inserted Section 3(p) w.e.f. 20 May 2003); Act 15 of 2005 (substituted Section 3(d) w.e.f. 1 January 2005).
   - *Corpus Locators*: `PASS-002` (s. 3(p)), `PASS-013` (s. 3(e)), `PASS-014` (s. 3(d)).

2. **REAL-002: The Drugs and Cosmetics Act, 1940 (Act 23 of 1940) & Drugs Rules, 1945**
   - *Authority*: Ministry of Ayush & CDSCO, Ministry of Health and Family Welfare.
   - *Key Provisions Reviewed*: Section 3(a), Section 3(h), Section 3(aaa), and Drugs Rules Rule 2(eb).
   - *Amendment History*: Act 13 of 1964 (inserted Chapter IVA relating to ASU drugs w.e.f. 1 Feb 1969); Gazette G.S.R. 918(E) dated 30 Nov 2015 (introduced Phytopharmaceutical drug definitions).
   - *Corpus Locators*: `PASS-009` (s. 3(a)), `PASS-010` (s. 3(h)), `PASS-011` (s. 3(aaa)), `PASS-012` (r. 2(eb)).

3. **REAL-003: Food Safety and Standards (Ayurveda Aahara) Regulations, 2022**
   - *Authority*: Food Safety and Standards Authority of India (FSSAI).
   - *Key Provisions Reviewed*: Regulation 2(b) (definition and mandatory exclusions of drugs/cosmetics), Regulation 3(4) (statutory prohibition against added vitamins, minerals, amino acids), Regulation 8 (prohibition against claims to prevent, treat or cure disease), Regulation 13(a) (front-of-pack logo), Regulation 13(f) (oral consumption warning), and Schedule A (authoritative texts).
   - *Amendment History*: Gazette Extraordinary, Part III, Sec. 4, No. 200, dated 5 May 2022 (uploaded 9 May 2022); operative compliance w.e.f. 1 Nov 2022.
   - *Corpus Locators*: `PASS-003` (reg. 2(b) & reg. 3(4)), `PASS-004` (reg. 8 & reg. 13(a)).

---

## 6. Review Gates and Integration Handoff

- **Corpus Activation (Harshit)**: The reviewed source records and provision passages are submitted on branch `thulasi/t-01-phase-1`. Under the Master Plan decision matrix, Harshit must validate schema compatibility, provision-aware chunking, and activate these rows for RAG index ingestion.
- **Terminology Review (Deepshika)**: Deepshika will review English and Hindi glossaries to ensure statutory terms (*Classical ASU*, *Patent or Proprietary*, *Ayurveda Aahara*, *Traditional Knowledge*, *Mere Admixture*) maintain 100% conceptual and locator parity.
- **Downstream Consumers**:
  - *Suresh (Backend)*: Consume rule table logic for endpoint contract `/api/v1/classify` and stub fixtures.
  - *Sabeena (Benchmarks)*: Ground the initial 20 synthetic benchmark scenarios in the six provisional routes defined herein.
  - *Akshay (Frontend)*: Implement the guided intake form matching the conditions in RULE-01 through RULE-07.
