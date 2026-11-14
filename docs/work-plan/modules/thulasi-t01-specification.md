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
| `ayurveda_aahara` | Food and dietary supplement regulatory framework for Ayurvedic recipes and foods | *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022* (FSSAI Gazette 05/09 May 2022) | Regulation 2(b) [Definition and statutory exclusions of drugs/cosmetics], Regulation 8 [Labelling, logo, disease prevention/cure claim prohibition], Schedule A [Authoritative texts] | Not interchangeable with general nutraceuticals (FSSAI Nutraceutical Regulations 2022). No general food safety licensing advice |
| `biodiversity` | Access and Benefit Sharing (ABS) governance under Indian law | *The Biological Diversity Act, 2002* and *Biological Diversity Rules, 2024 / Amendment Rules 2025* | Preliminary awareness: National Biodiversity Authority (NBA) approval requirements for IPR applications involving Indian biological resources (Section 6) | General guidance only in Phase 1; complete operative rules pending T-03 verification. No commercial ABS fee calculations |
| `traditional_knowledge` | Public overview and defensive protection role of TKDL | Traditional Knowledge Digital Library (TKDL) official public documentation | Public background on prior-art search agreements with patent offices and defensive protection mechanisms | No access to confidential or restricted TKDL database entries; cannot search proprietary formulations |
| `international_treaty` | International intellectual property and genetic resources overview | *WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (GRATK)* (adopted May 2024) | Overview of patent disclosure requirements regarding genetic resources and associated TK; strictly distinguished from domestic Indian legislation | No country-by-country export compliance, foreign national patent office advice, or claims of direct domestic enforceability |

### System-Wide Operational Rules
1. **Information vs. Legal Advice**: The system delivers cited regulatory information, not legal or regulatory advice. Output notices must explicitly state this boundary.
2. **Jurisdiction Isolation**: India queries retrieve solely Indian statutory instruments; international queries retrieve WIPO/treaty overviews. Crossing jurisdictions within a single query is strictly blocked.
3. **Safe Abstention & Referral**: When user input is incomplete, ambiguous, or describes novel synthetic substances outside ASU texts, the system must not guess or force a category; it must output an explicit referral packet.

---

## 3. Six Provisional Classification Routes (+ Referral Pathway)

Every intake scenario is mapped to one of six provisional routes or routed to an explicit clarification/referral outcome:

```
                                  [ Formulation Intake ]
                                             │
             ┌───────────────────────────────┴───────────────────────────────┐
      [ Intended Use? ]                                              [ Incomplete / Ambiguous ]
       ├── Medicinal (Diagnosis/Cure/Prevention)                                    │
       │    ├── 100% ingredients & formula in First Schedule text?                  ▼
       │    │    ├── YES  ──► Route 1: Classical / Generic Ayurvedic Medicine  [ Route 7: Unknown / Referral ]
       │    │    └── NO   ──► All ingredients in First Schedule, but formula novel/proprietary?
       │    │                  ├── YES ──► Route 2: Patent or Proprietary (P&P) Ayurvedic Medicine
       │    │                  └── NO  ──► Standardized fraction (4+ bioactives, plant part)?
       │    │                               ├── YES ──► Route 4: Phytopharmaceutical Drug (Referral)
       │    │                               └── NO  ──► Route 3: Novel / Non-Classical Formulation (Referral)
       ├── Food / Dietary Supplement / Nutrition
       │    └── Recipe/ingredients in Schedule A of Ayurveda Aahara Regs & NO disease cure claims?
       │         ├── YES ──► Route 5: Ayurveda Aahara (Food)
       │         └── NO  ──► Route 7: Ambiguous / Referral
       └── Cleansing / Beautifying / External Application (No medicinal claims)
            └── Route 6: Ayurvedic Cosmetic
```

### Route 1: Classical / Generic Ayurvedic Medicine
- **Statutory Authority**: *Drugs and Cosmetics Act, 1940*, Section 3(a), read with the First Schedule.
- **Definition**: Medicines intended for internal or external use for the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurveda specified in the First Schedule.
- **Key Intake Criteria**:
  - Ingredients, proportions, method of preparation, and indication are strictly identical to an authoritative book listed in the First Schedule (e.g., Charaka Samhita, Sushruta Samhita, Ayurvedic Formulary of India).
  - No synthetic active pharmaceutical ingredients (APIs) or unauthorized excipients.
- **Regulatory & IP Implications**:
  - Requires standard State AYUSH manufacturing license under Classical ASU rules.
  - **Patentability in India**: Excluded under Section 3(p) of the Patents Act, 1970 (public domain traditional knowledge).

### Route 2: Patent or Proprietary (P&P) Ayurvedic Medicine
- **Statutory Authority**: *Drugs and Cosmetics Act, 1940*, Section 3(h), read with Section 3(a) and the First Schedule.
- **Definition**: In relation to Ayurvedic systems of medicine, a formulation containing only such ingredients mentioned in the formulae described in the authoritative books of Ayurveda specified in the First Schedule, but does not include a medicine administered by parenteral route and also a formulation included in the classical authoritative books specified in clause (a).
- **Key Intake Criteria**:
  - All active ingredients are individually cited in First Schedule authoritative texts.
  - The combination, proportions, dosage form, or processing is proprietary or not found as a combined classical recipe.
  - Route of administration is strictly non-parenteral (no injections/IV).
- **Regulatory & IP Implications**:
  - Requires AYUSH State Licensing Authority approval under Patent & Proprietary category, with required safety/proof of concept data.
  - **Patentability in India**: Subject to strict scrutiny under Section 3(p) (aggregation of known properties of traditionally known components) and Section 3(e) (mere admixture). Requires demonstrable non-obvious synergistic technical effect.

### Route 3: Novel / Non-Classical Formulation (Mandatory Referral Route)
- **Statutory Authority**: Falls outside classical ASU definitions under *Drugs and Cosmetics Act, 1940*, Section 3(a) and Section 3(h).
- **Definition**: Formulations incorporating non-classical botanicals, synthetic chemical compounds, unlisted minerals, or novel drug delivery mechanisms not recognized in ASU authoritative texts, but claiming medicinal/therapeutic properties.
- **Key Intake Criteria**:
  - Contains ingredients not listed in First Schedule ASU texts, or uses synthetic chemical additives as active agents.
- **System Action**:
  - **Automatic Safe Referral**: The assistant cannot validate or approve novel non-classical drugs. It issues an explicit notice that the product falls outside standard AYUSH licensing and provides a downloadable professional referral packet.

### Route 4: Phytopharmaceutical Drug (Mandatory Referral Route)
- **Statutory Authority**: *Drugs Rules, 1945*, Rule 2(eb), Rule 122E, and Schedule Y / Appendix I/IA (introduced via Gazette notification G.S.R. 918(E) dated 30 November 2015).
- **Definition**: Purified and standardized fraction with defined minimum four bioactive or phytochemical compounds of an extract of a medicinal plant or its part, for internal or external use in humans or animals for diagnosis, treatment, mitigation or prevention of disease, but does not include parenteral administration.
- **Key Intake Criteria**:
  - Highly purified and standardized fraction (not crude powder or traditional kwath/taila).
  - Minimum 4 characterized chemical bioactives/biomarkers.
- **System Action**:
  - **Automatic Referral**: Regulated under CDSCO (Central Drugs Standard Control Organization) modern drug regulatory pathway (new drug approval, non-clinical toxicity, and clinical trials). The assistant informs the user of CDSCO jurisdiction and directs them to regulatory specialists.

### Route 5: Ayurveda Aahara (Food / Dietary Supplement)
- **Statutory Authority**: *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022*, Regulation 2(b) & Regulation 8.
- **Definition**: Food prepared in accordance with the recipes or ingredients or processes described in the authoritative books of Ayurveda listed in Schedule A of the 2022 Regulations.
- **Mandatory Exclusions under Reg. 2(b)**:
  - Cannot be an Ayurvedic drug or proprietary Ayurvedic medicine under the Drugs and Cosmetics Act.
  - Cannot be administered parenterally.
  - Cannot contain synthetic vitamins, minerals, amino acids, or narcotic/psychotropic substances.
- **Labelling & Claims Constraints under Reg. 8**:
  - Strictly prohibits any claim to prevent, treat, mitigate or cure any human disease or disorder.
  - Must display the official Ayurveda Aahara logo and advisory statements.
- **Regulatory Distinction**:
  - Regulated under FSSAI, not Ministry of Ayush drug licensing. Not interchangeable with generic nutraceuticals or health supplements.

### Route 6: Ayurvedic Cosmetic
- **Statutory Authority**: *Drugs and Cosmetics Act, 1940*, Section 3(aaa) and Part XIII/XV of *Drugs Rules, 1945*.
- **Definition**: Any article intended to be rubbed, poured, sprinkled or sprayed on, or introduced into, or otherwise applied to the human body for cleansing, beautifying, promoting attractiveness, or altering appearance, incorporating Ayurvedic ingredients.
- **Key Intake Criteria**:
  - Topical / external application only.
  - Intended solely for cosmetic effect (cleansing, appearance, beautification).
  - Strictly no therapeutic, medicinal, or disease-cure claims.
- **Regulatory Implication**:
  - Licensed under cosmetic regulations; separate from drug or food licensing.

### Route 7: Unknown / Ambiguous / Insufficient Facts (Clarification & Referral)
- **Trigger**: User provides incomplete formulation details, conflicting intended use (e.g. food that claims to cure cancer), unverified ingredients, or ambiguous administration routes.
- **System Action**:
  - Requests targeted clarification on missing mandatory fields (ingredients, authoritative text reference, intended use, route of administration).
  - If ambiguity persists, issues a structured referral packet for human professional consultation.

---

## 4. Draft Decision Rules Specification

The following decision rules govern the intake classification logic. Each rule maps directly to a verified statutory provision locator:

| Rule ID | Intake Condition / Question Evaluated | Logic / Condition Expression | Resulting Route | Governing Provision | Source ID & Locator | Ambiguity / Fallback Action |
|---|---|---|---|---|---|---|
| **RULE-01** | What is the intended primary use of the formulation? | `intended_use == "medicinal"` AND `ingredients_all_classical == TRUE` AND `formula_in_first_schedule == TRUE` AND `claims_disease_treatment == TRUE` | **Route 1: Classical Ayurvedic Medicine** | D&C Act 1940, Section 3(a), First Schedule | `REAL-002`, s. 3(a) | If text name missing, prompt for specific First Schedule text; if absent, route to RULE-02. |
| **RULE-02** | Are all ingredients in First Schedule texts, but the combination or form is proprietary? | `intended_use == "medicinal"` AND `ingredients_all_classical == TRUE` AND `formula_in_first_schedule == FALSE` AND `parenteral == FALSE` | **Route 2: Patent or Proprietary Ayurvedic Medicine** | D&C Act 1940, Section 3(h) | `REAL-002`, s. 3(h) | If any ingredient is non-classical or unlisted, trigger RULE-03. If parenteral, reject immediately. |
| **RULE-03** | Does the formulation contain synthetic substances or non-classical botanicals claiming therapeutic effect? | `intended_use == "medicinal"` AND (`has_synthetic_active == TRUE` OR `ingredients_all_classical == FALSE`) AND `phytopharmaceutical_criteria == FALSE` | **Route 3: Novel / Non-Classical Formulation** | D&C Act 1940, general non-ASU provisions | `REAL-002`, general; safe referral | Automatic abstention on ASU licensing; generate referral packet to CDSCO/allopathic patent attorney. |
| **RULE-04** | Is the product a purified, standardized plant fraction with defined bioactive markers? | `intended_use == "medicinal"` AND `standardized_fraction == TRUE` AND `bioactive_markers_count >= 4` AND `parenteral == FALSE` | **Route 4: Phytopharmaceutical Drug** | Drugs Rules 1945, Rule 2(eb) | `REAL-002`, r. 2(eb) | Mandatory referral to CDSCO new drug regulatory framework. |
| **RULE-05** | Is the product intended as food/supplement based on classical recipes, without disease cure claims? | `intended_use == "food_dietary"` AND `recipe_in_schedule_a == TRUE` AND `synthetic_nutrients_added == FALSE` AND `claims_disease_cure == FALSE` | **Route 5: Ayurveda Aahara** | FSSAI Regs 2022, Reg. 2(b) & Reg. 8 | `REAL-003`, reg. 2(b), reg. 8 | If disease cure claimed, flag violation of Reg. 8; if synthetic vitamins added, exclude under Reg. 2(b) and refer. |
| **RULE-06** | Is the product applied externally for cleansing/beautifying without therapeutic claims? | `intended_use == "cosmetic"` AND `external_application_only == TRUE` AND `claims_disease_treatment == FALSE` | **Route 6: Ayurvedic Cosmetic** | D&C Act 1940, Section 3(aaa) | `REAL-002`, s. 3(aaa) | If medicinal/cure claims are made, re-evaluate under drug rules (RULE-01 or RULE-02). |
| **RULE-07** | Are formulation ingredients, intended use, or processing details missing or conflicting? | `missing_mandatory_facts == TRUE` OR `conflicting_intake_inputs == TRUE` | **Route 7: Unknown / Clarification / Referral** | Master Plan Safety & Abstention Policy | `REAL-001`, `REAL-002`, `REAL-003` | Prompt for missing facts; generate structured referral packet; do not output confident classification. |
| **RULE-08** | Is the user querying Indian patentability for an Ayurvedic formulation? | `query_type == "patentability_india"` AND `is_traditional_knowledge_or_aggregation == TRUE` | **Patent Exclusion Notice** | Patents Act 1970, Section 3(p) & Section 3(e) | `REAL-001`, s. 3(p), s. 3(e) | Explain statutory exclusions under 3(p) and 3(e); state clearly that only surprising non-obvious synergy can overcome 3(e). |

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
   - *Key Provisions Reviewed*: Regulation 2(b) (definition and mandatory exclusions), Regulation 8 (claims prohibition and logo).
   - *Amendment History*: Gazette Extraordinary, Part III, Sec. 4, No. 200, dated 5 May 2022 (uploaded 9 May 2022); operative compliance w.e.f. 1 Nov 2022.
   - *Corpus Locators*: `PASS-003` (reg. 2(b)), `PASS-004` (reg. 8).

---

## 6. Review Gates and Integration Handoff

- **Corpus Activation (Harshit)**: The reviewed source records and provision passages are submitted on branch `thulasi/t-01-phase-1`. Under the Master Plan decision matrix, Harshit must validate schema compatibility, provision-aware chunking, and activate these rows for RAG index ingestion.
- **Terminology Review (Deepshika)**: Deepshika will review English and Hindi glossaries to ensure statutory terms (*Classical ASU*, *Patent or Proprietary*, *Ayurveda Aahara*, *Traditional Knowledge*, *Mere Admixture*) maintain 100% conceptual and locator parity.
- **Downstream Consumers**:
  - *Suresh (Backend)*: Consume rule table logic for endpoint contract `/api/v1/classify` and stub fixtures.
  - *Sabeena (Benchmarks)*: Ground the initial 20 synthetic benchmark scenarios in the six provisional routes defined herein.
  - *Akshay (Frontend)*: Implement the guided intake form matching the conditions in RULE-01 through RULE-07.
