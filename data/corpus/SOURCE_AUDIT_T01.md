# Corpus Source Audit Note: Task T-01 (Phase 1)

- **Date of Audit:** 14 November 2026 (Updated 15 November 2026; Re-audited 21 November 2026)
- **Auditor / Reviewer:** Thulasi (Authoritative source corpus, formulation categories and decision rules)
- **Deliverable:** T-01 Phase 1 Official Source Verification & Initial Reviewed Provision Rows
- **Target Repository:** `https://github.com/Harshit-ambati/IP-SAKTI-Sahayak`
- **Review Requests:** Harshit (Provenance verification & RAG activation), Deepshika (Legal-term preservation & glossaries)

---

## 1. Scope & Audit Purpose

Under [MASTER_PLAN.md](../../docs/work-plan/MASTER_PLAN.md) (Section 5) and [02-thulasi.md](../../docs/work-plan/modules/02-thulasi.md), all knowledge corpus records must undergo rigorous provenance, amendment, and locator verification before activation into the production RAG index.

The seven document records in `documents.csv` and eight paraphrases in `passages.csv` were committed as preliminary starter rows on 1 November 2026. This audit note records the **Phase 1 formal verification of three exact official instruments** (`REAL-001`, `REAL-002`, `REAL-003`) and their operative provisions, explicitly marks unknown or unverified metadata honestly, and documents why remaining rows (`REAL-004` through `REAL-007`) remain preliminary.

---

## 2. Verified Official Instruments (Phase 1)

### Instrument 1: REAL-001 — The Patents Act, 1970
- **Official Title:** The Patents Act, 1970 (Act No. 39 of 1970) as amended.
- **Issuing Authority:** Controller General of Patents, Designs and Trade Marks (CGPDTM / IP India), Ministry of Commerce and Industry, Government of India; and Legislative Department, Ministry of Law and Justice (India Code).
- **Jurisdiction:** India.
- **Instrument Type:** Primary Legislation (Statute).
- **Official Primary URLs:**
  - Official India Code Repository: `https://www.indiacode.nic.in/bitstream/123456789/1392/1/A1970-39.pdf`
  - IP India Acts Portal: `https://ipindia.gov.in/acts-patents.htm`
- **Key Dates:**
  - *Enactment Date:* 19 September 1970.
  - *Commencement Date:* 20 April 1972 (via S.O. 197(E) & 201(E)).
  - *Key Statutory Amendments:*
    - Patents (Amendment) Act, 2002 (Act No. 38 of 2002): inserted Section 3(p) w.e.f. 20 May 2003 (S.O. 561(E)).
    - Patents (Amendment) Act, 2005 (Act No. 15 of 2005): substituted Section 3(d) w.e.f. 1 January 2005.
    - Patents (Amendment) Rules, 2024: Gazette G.S.R. 190(E) dated 15 March 2024 (procedural rules; does not alter substantive s. 3 statutory exclusions).
- **Operative Version Status:** Currently operative statute. Section 3 exclusions remain in force.
- **Access & Reuse Conditions:** Public official legislative enactment of the Parliament of India. Open access and non-commercial public reproduction under Section 52(1)(q) of the Indian *Copyright Act, 1957* (reproduction of legislative enactments).
- **Capture / Inspection Date:** 14 November 2026.
- **Checksum & Provenance Gate Status:**
  - Text streams verified against official India Code canonical PDF (`A1970-39.pdf`).
  - Recorded as `pending_w8_file_ingestion` in `source_register.csv` pending captured PDF file ingestion into the repository pipeline in Week 8.
- **Operative Provisions Verified:**
  - **Section 3(p):** Excludes from patentability "an invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components".
  - **Section 3(e):** Excludes "a substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof or a process for producing such substance". (Examined under IP India Guidelines where demonstrating synergistic effect is an evidentiary consideration, not a statutory guarantee).
  - **Section 3(d):** Excludes "the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance". (Must include the statutory limitation 'for a known substance').
- **Audit Decision:** Verified for intake and classification rule grounding. Submitted as `reviewed_t01_pending_activation`.

---

### Instrument 2: REAL-002 — The Drugs and Cosmetics Act, 1940 & Drugs Rules, 1945
- **Official Title:** The Drugs and Cosmetics Act, 1940 (Act No. 23 of 1940) and The Drugs Rules, 1945 (as amended).
- **Issuing Authority:** Ministry of Ayush; and Central Drugs Standard Control Organization (CDSCO), Directorate General of Health Services, Ministry of Health and Family Welfare, Government of India.
- **Jurisdiction:** India.
- **Instrument Type:** Primary Legislation & Subordinate Statutory Rules.
- **Official Primary URLs:**
  - Ministry of Ayush official legal compilation: `https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf`
  - India Code Repository: `https://www.indiacode.nic.in/handle/123456789/2414`
- **Key Dates:**
  - *Enactment Date:* 10 April 1940.
  - *Commencement Date:* 10 April 1940 (Rules commenced 1945).
  - *Key Statutory Amendments:*
    - The Drugs and Cosmetics (Amendment) Act, 1964 (Act No. 13 of 1964): introduced Chapter IVA and statutory definitions for Ayurvedic, Siddha, and Unani drugs (w.e.f. 1 February 1969).
    - The Drugs and Cosmetics (Amendment) Act, 1982 (Act No. 68 of 1982): introduced Section 3(aaa) defining cosmetic.
    - Gazette G.S.R. 918(E) dated 30 November 2015: inserted Rule 2(eb) and Schedule Y phytopharmaceutical regulatory regime.
- **Operative Version Status:** Currently operative.
- **Access & Reuse Conditions:** Public statutory enactment and subordinate rules published under authority of the Government of India. Open public access; non-commercial public reproduction under Section 52(1)(q) of the *Copyright Act, 1957*.
- **Capture / Inspection Date:** 14 November 2026.
- **Checksum & Provenance Gate Status:**
  - Text streams verified against Ministry of Ayush compilation.
  - Recorded as `pending_w8_file_ingestion` in `source_register.csv` pending captured PDF file ingestion in Week 8.
- **Operative Provisions Verified:**
  - **Section 3(a):** Defines *Ayurvedic, Siddha or Unani drug* as medicines manufactured exclusively in accordance with formulae in First Schedule authoritative books. Grounds Route 1 (Classical ASU).
  - **Section 3(h):** Defines *Patent or proprietary medicine* in relation to ASU systems as formulations containing only ingredients mentioned in First Schedule authoritative books, but not included in authoritative formulae; excludes parenterals. Grounds Route 2 (Patent or Proprietary ASU).
  - **Section 3(aaa):** Defines *Cosmetic* as articles intended for cleansing, beautifying, promoting attractiveness, or altering appearance. Grounds Route 6 (Ayurvedic Cosmetic).
  - **Drugs Rules, Rule 2(eb):** Defines *Phytopharmaceutical drug* as purified/standardized fraction of medicinal plant extract with minimum 4 bioactive markers; non-parenteral. Grounds Route 4 (Phytopharmaceutical referral).
- **Audit Decision:** Verified for intake and classification rule grounding. Submitted as `reviewed_t01_pending_activation`.

---

### Instrument 3: REAL-003 — Food Safety and Standards (Ayurveda Aahara) Regulations, 2022
- **Official Title:** Food Safety and Standards (Ayurveda Aahara) Regulations, 2022.
- **Issuing Authority:** Food Safety and Standards Authority of India (FSSAI), Ministry of Health and Family Welfare, Government of India.
- **Jurisdiction:** India.
- **Instrument Type:** Subordinate Statutory Regulation.
- **Official Primary URL:** `https://fssai.gov.in/upload/notifications/2022/05/62789a20b54bdGazette_Notification_Ayurveda_Aahara_09_05_2022.pdf`
- **Key Dates:**
  - *Enactment Date:* 5 May 2022 (Gazette notification No. 200, uploaded 9 May 2022).
  - *Commencement Date:* 5 May 2022; compliance enforced from 1 November 2022; transition clarity orders extended up to 25 July 2025.
  - *Amendments:* Clarification directives (F. No. Stds/SP-05/A-1.2022-Part(1)).
- **Operative Version Status:** Currently operative.
- **Access & Reuse Conditions:** Official Gazette of India notification. Open access public regulatory text; non-commercial public reproduction under Section 52(1)(q) of the *Copyright Act, 1957*.
- **Capture / Inspection Date:** 14 November 2026.
- **Checksum & Provenance Gate Status:**
  - Text streams verified against official FSSAI Gazette notification.
  - Recorded as `pending_w8_file_ingestion` in `source_register.csv` pending captured PDF file ingestion in Week 8.
- **Operative Provisions Verified:**
  - **Regulation 2(b):** Defines *Ayurveda Aahara* as food prepared in accordance with authoritative books in Schedule A; explicitly excludes Ayurvedic drugs, proprietary medicines, and cosmetics. (Mandatory non-parenteral warning 'FOR ORAL CONSUMPTION ONLY, NOT FOR PARENTERAL USE' is enacted separately under Regulation 13(f)).
  - **Regulation 3(4):** Strictly prohibits the addition of vitamins, minerals, or amino acids to Ayurveda Aahara formulations (an unqualified statutory bar covering all added nutrients, regardless of whether synthetic or naturally sourced).
  - **Regulation 8:** Strictly prohibits any claim in labelling, advertising or presentation that Ayurveda Aahara prevents, treats or cures any human disease (covering all three statutory limbs: prevent, treat, or cure; strictly confined to human disease).
  - **Regulation 13(a):** Mandates front-of-pack display of the official Ayurveda Aahara logo on the principal display panel.
  - **Schedule A:** Lists authoritative classical texts recognized for Ayurveda Aahara recipes.
- **Audit Decision:** Verified for intake and classification rule grounding. Submitted as `reviewed_t01_pending_activation`.

---

## 3. Unapproved & Preliminary Starter Rows Retained Honestly

The remaining four rows in `documents.csv` and six passage rows in `passages.csv` are maintained as **preliminary and unactivated**:

| Source ID | Title | Current Status | Technical Reason for Deferral | Target Resolution Milestone |
|---|---|---|---|---|
| `REAL-004` | Biological Diversity Rules, 2024 | Preliminary (`official_url_checked_2026-11-01`) | Substantive ABS rules must be cross-verified against Biological Diversity (Amendment) Act 2023. | Task T-03 (W5–6) |
| `REAL-005` | Biological Diversity Amendment Rules, 2025 | Preliminary (`linked_from_official_rules_page_2026-11-01`) | Portal download timed out during initial crawler inspection; manual verification scheduled for T-03. | Task T-03 (W5–6) |
| `REAL-006` | WIPO GRATK Treaty (adopted May 2024) | Preliminary (`official_url_checked_2026-11-01`) | No direct domestic legal enforceability in India until national ratification and enabling legislation. Scope must remain bounded to international treaty overview. | Task T-03 (W5–6) |
| `REAL-007` | TKDL public overview | Preliminary (`official_url_checked_2026-11-01`) | Public webpage describing bilateral patent office search access agreements. Restricted database contents are completely unavailable. Serves as background context only; cannot be cited for patent validity of specific formulations. | Task T-03 (W5–6) |

### Audit of Existing Preliminary Passages (`passages.csv`)
- **PASS-001 (REAL-001, Section 3(k)):** Addresses computer programmes per se and algorithms. Kept preliminary. Marked as out-of-scope for Ayurvedic formulation classification; will not be included in formulation routing indexes.
- **PASS-002 (REAL-001, Section 3(p)):** Verified and updated to `reviewed_t01_pending_activation`.
- **PASS-003 (REAL-003, Regulation 2(b) & Regulation 3(4)):** Verified and updated to `reviewed_t01_pending_activation`. Paraphrase narrowed strictly to Regulation 2(b) product exclusions (drugs, proprietary medicines, cosmetics) and Regulation 3(4) statutory ban on added vitamins, minerals, or amino acids. Parenteral warning is properly attributed to Regulation 13(f).
- **PASS-004 (REAL-003, Regulation 8 & Regulation 13(a)):** Verified and updated to `reviewed_t01_pending_activation`. Paraphrase narrowed strictly to Regulation 8's Gazette text: prohibiting claims in labelling, advertising, or presentation to prevent, treat or cure any human disease, and Regulation 13(a) front-of-pack logo requirement.
- **PASS-005 & PASS-006 (REAL-004 & REAL-005):** Kept as `source_checked_domain_review_pending`. Do not activate until Gazette PDF verification in T-03.
- **PASS-007 & PASS-008 (REAL-006 & REAL-007):** Kept as `source_checked_domain_review_pending` (background overview only).

---

## 4. Newly Submitted Reviewed Passage Rows (Phase 1)

The following six new passage rows have been extracted with precise provision locators, verified against official texts, and submitted to `passages.csv` under status `reviewed_t01_pending_activation`:

1. **`PASS-009`** (Source: `REAL-002`, Locator: `Section 3(a)`):
   - *Statutory Text Content:* "Ayurvedic, Siddha or Unani drug includes all medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, and manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic, Siddha and Unani systems of medicine specified in the First Schedule."
2. **`PASS-010`** (Source: `REAL-002`, Locator: `Section 3(h)`):
   - *Statutory Text Content:* "Patent or proprietary medicine in relation to Ayurvedic, Siddha or Unani systems means a formulation containing only such ingredients mentioned in the formulae described in the authoritative books specified in the First Schedule, but does not include a medicine administered by parenteral route and also a formulation included in the authoritative books specified in clause (a)."
3. **`PASS-011`** (Source: `REAL-002`, Locator: `Section 3(aaa)`):
   - *Statutory Text Content:* "Cosmetic means any article intended to be rubbed, poured, sprinkled or sprayed on, or introduced into, or otherwise applied to the human body or any part thereof for cleansing, beautifying, promoting attractiveness, or altering the appearance."
4. **`PASS-012`** (Source: `REAL-002`, Locator: `Drugs Rules 1945, Rule 2(eb)`):
   - *Statutory Text Content:* "Phytopharmaceutical drug means purified and standardized fraction with defined minimum four bioactive or phytochemical compounds of an extract of a medicinal plant or its part, for internal or external use of human beings or animals for diagnosis, treatment, mitigation or prevention of any disease or disorder, but does not include administration by parenteral route."
5. **`PASS-013`** (Source: `REAL-001`, Locator: `Section 3(e)`):
   - *Statutory Text Content:* "A substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof or a process for producing such substance is not an invention within the meaning of this Act."
6. **`PASS-014`** (Source: `REAL-001`, Locator: `Section 3(d)`):
   - *Statutory Text Content:* "The mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant is not an invention." (Includes explicit statutory limitation 'for a known substance').

---

## 5. Classification Routing and Evidentiary Fallback Audit

In accordance with peer review findings:
1. **Evidentiary Fallback (RULE-01):** When an applicant claims a classical Ayurvedic medicine but cannot provide an authoritative book citation listed in the First Schedule, the system must **never** default or demote the product to Patent or Proprietary medicine (Route 2). Missing classical evidence is an evidentiary gap requiring clarification or expert referral (Route 7: `needs_expert_referral`), not proof that the product qualifies as a proprietary formulation.
2. **Ayurveda Aahara Boundaries (RULE-05):** Products carrying added vitamins, minerals, or amino acids (irrespective of synthetic or natural source) violate Regulation 3(4) and are excluded from Ayurveda Aahara under Regulation 2(b). Claims in labelling, advertising, or presentation to prevent, treat, or cure human disease violate Regulation 8 (strictly three limbs: prevent, treat, or cure; confined to human disease). Front-of-pack display of the logo is required under Regulation 13(a), and oral-only consumption is mandated under Regulation 13(f).
3. **Patentability Examination Framing (RULE-08):** Section 3(e) excludes mere admixtures resulting in the aggregation of component properties. Under IP India's *Guidelines for Examination of Patent Applications in the Field of Pharmaceuticals and Ayush*, demonstrating synergistic effect is an examination consideration when assessing whether a combination is more than a mere aggregation of known properties, but does not constitute an automatic statutory exception or guaranteed grant of patentability.

---

## 6. Metadata Integrity Statement & Honest Disclosure

In compliance with the project guidelines:
1. No statutory provisions, amendment dates, or official source approvals have been invented or assumed.
2. The checksum status for preliminary instruments is recorded as `pending_w8_file_ingestion` until full local raw PDF files are ingested and SHA-256 hashes computed in Week 8.
3. Substantive answer generation must **not** claim legal advice or formal regulatory clearance; all answers must carry the mandatory non-legal disclaimer.
4. Activation of these rows into the RAG chunk index is held pending Harshit's technical review and validation.
