# Corpus Source Audit Note: Task T-01 (Phase 1)

**Date of Audit:** 14 November 2026  
**Auditor / Reviewer:** Thulasi (Authoritative source corpus, formulation categories and decision rules)  
**Deliverable:** T-01 Phase 1 Official Source Verification & Initial Reviewed Provision Rows  
**Target Repository:** `https://github.com/Harshit-ambati/IP-SAKTI-Sahayak`  
**Review Requests:** Harshit (Provenance verification & RAG activation), Deepshika (Legal-term preservation & glossaries)  

---

## 1. Scope & Audit Purpose

Under the [MASTER_PLAN.md](../../docs/work-plan/MASTER_PLAN.md) (Section 5) and [02-thulasi.md](../../docs/work-plan/modules/02-thulasi.md), all knowledge corpus records must undergo rigorous provenance, amendment, and locator verification before activation into the production RAG index.

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
- **Integrity / Checksum:**
  - Inspected India Code canonical PDF (`A1970-39.pdf`): SHA-256 computed on official PDF text stream for Section 3 provisions; verification against official gazette text confirmed.
- **Operative Provisions Verified:**
  - **Section 3(p):** Excludes from patentability "an invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components".
  - **Section 3(e):** Excludes "a substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof or a process for producing such substance".
  - **Section 3(d):** Excludes "the mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance".
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
    - Drugs and Cosmetics (Amendment) Act, 1964 (Act No. 13 of 1964): inserted Chapter IVA ("Provisions relating to Ayurvedic, Siddha and Unani Drugs") and First Schedule w.e.f. 1 February 1969.
    - Drugs and Cosmetics (Amendment) Act, 1982 (Act No. 68 of 1982): amended Section 3(h) ASU patent or proprietary definition w.e.f. 1 February 1983.
    - Gazette G.S.R. 918(E) dated 30 November 2015: inserted Rule 2(eb), Rule 122E amendments, and Schedule Y provisions creating the regulatory category of "Phytopharmaceutical drug".
- **Operative Version Status:** Currently operative statute and subordinate rules. Governs all manufacture and sale of ASU medicines and cosmetics in India.
- **Access & Reuse Conditions:** Public official legislative and regulatory text of the Government of India. Free public access under Section 52(1)(q) of the Indian *Copyright Act, 1957*.
- **Capture / Inspection Date:** 14 November 2026.
- **Integrity / Checksum:**
  - Inspected Ministry of Ayush official compilation PDF (`Drugs-and-Cosmetics-Act-Rules.pdf`): text locators for Section 3(a), 3(h), 3(aaa), First Schedule, and Rule 2(eb) matched and verified against Gazette extraordinary notifications.
- **Operative Provisions Verified:**
  - **Section 3(a):** Definition of "Ayurvedic, Siddha or Unani drug": all medicines for internal/external use in diagnosis, treatment, mitigation or prevention of disease in humans or animals manufactured exclusively according to formulae in First Schedule authoritative books.
  - **First Schedule:** Statutory inventory of recognized authoritative texts (AFI, API, Charaka Samhita, Sushruta Samhita, etc.).
  - **Section 3(h):** Definition of "patent or proprietary medicine" in relation to ASU: formulation containing only ingredients mentioned in First Schedule authoritative books, but not in classical formulae; excludes parenteral administration.
  - **Section 3(aaa):** Definition of "cosmetic": articles applied to the body for cleansing, beautifying, promoting attractiveness, or altering appearance.
  - **Drugs Rules, 1945, Rule 2(eb):** Definition of "Phytopharmaceutical drug": purified and standardized fraction with defined minimum 4 bioactive/phytochemical compounds of an extract of a medicinal plant/part, non-parenteral, regulated under CDSCO framework.
- **Audit Decision:** Verified for intake and classification rule grounding. Submitted as `reviewed_t01_pending_activation`.

---

### Instrument 3: REAL-003 — Food Safety and Standards (Ayurveda Aahara) Regulations, 2022
- **Official Title:** Food Safety and Standards (Ayurveda Aahara) Regulations, 2022.
- **Issuing Authority:** Food Safety and Standards Authority of India (FSSAI), Ministry of Health and Family Welfare, Government of India.
- **Jurisdiction:** India.
- **Instrument Type:** Subordinate Statutory Regulations (Gazette Notification).
- **Official Primary URLs:**
  - FSSAI Official Gazette PDF: `https://fssai.gov.in/upload/notifications/2022/05/62789a20b54bdGazette_Notification_Ayurveda_Aahara_09_05_2022.pdf`
  - FSSAI Clarification Order (2025): `https://www.fssai.gov.in/upload/uploadfiles/files/Order%20dated%2025-07-2025%20enclosing%20Ayurveda%20Aahara.pdf`
- **Key Dates:**
  - *Notification Date:* 5 May 2022 (F. No. Stds/SP-05/A-1.2022; published in Gazette of India Extraordinary, Part III, Sec. 4, No. 200, dated 5 May 2022; uploaded to portal 9 May 2022).
  - *Commencement Date:* Date of publication in the Official Gazette (5 May 2022).
  - *Mandatory Compliance Date:* 1 November 2022 (subject to subsequent FSSAI enforcement transition orders up to July 2025).
- **Operative Version Status:** Currently operative subordinate regulation under the Food Safety and Standards Act, 2006.
- **Access & Reuse Conditions:** Official statutory subordinate legislation published in the Gazette of India. Open public access; Government public document.
- **Capture / Inspection Date:** 14 November 2026.
- **Integrity / Checksum:**
  - Inspected FSSAI Gazette publication (`62789a20b54bdGazette_Notification_Ayurveda_Aahara_09_05_2022.pdf`): full text verified across Regulations 1 through 13 and Schedules A through D.
- **Operative Provisions Verified:**
  - **Regulation 2(b):** Definition of "Ayurveda Aahara": food prepared in accordance with recipes or ingredients or processes described in authoritative books of Ayurveda listed in Schedule A. Explicitly excludes Ayurvedic drugs or proprietary Ayurvedic medicines under Drugs and Cosmetics Act 1940 and rules, cosmetics, and parenteral administration.
  - **Regulation 3(4):** Prohibition on added nutrients: Strictly prohibits the addition of vitamins, minerals or amino acids to Ayurveda Aahara.
  - **Regulation 8:** Claims prohibition: Strictly prohibits claiming prevention, treatment, mitigation or cure of any human disease or disorder in advertising or packaging.
  - **Regulation 13(a):** Front-of-pack logo: Mandates displaying the specified Ayurveda Aahara logo on the principal display panel on front of pack along with advisory statements.
  - **Schedule A:** Recognizes classical Ayurveda authoritative texts for foods and recipes.
- **Audit Decision:** Verified for intake and classification rule grounding. Submitted as `reviewed_t01_pending_activation`.

---

## 3. Status Audit of Preliminary Corpus Records

The remaining four document records and four passage rows remain **preliminary** and **unapproved for substantive legal answers** until verified in subsequent tasks:

| Source ID | Title / Description | Current Status in Repo | Auditor Finding & Next Action | Planned Verification Milestone |
|---|---|---|---|---|
| `REAL-004` | Biological Diversity Rules 2024 (NBA) | Preliminary (`official_url_checked_2026-11-01`) | Portal link checked; commencement after 60 days from notification noted. Must be verified alongside 2025 amendments and Biological Diversity (Amendment) Act 2023 before activation. | Task T-03 (W5–6) |
| `REAL-005` | Biological Diversity Amendment Rules 2025 (NBA) | Preliminary (`linked_from_official_rules_page_2026-11-01`) | Official download link timed out during initial automated crawler inspection. Requires manual retrieval of official Gazette PDF from NBA / eGazette portal. | Task T-03 (W5–6) |
| `REAL-006` | WIPO GRATK Treaty text | Preliminary (`official_url_checked_2026-11-01`) | Treaty adopted 24 May 2024 at WIPO Diplomatic Conference. Does not have direct domestic legal enforceability in India until national ratification and enabling legislation. Scope must remain bounded to international treaty overview. | Task T-03 (W5–6) |
| `REAL-007` | TKDL public overview | Preliminary (`official_url_checked_2026-11-01`) | Public webpage describing bilateral patent office search access agreements. Restricted database contents are completely unavailable. Serves as background context only; cannot be cited for patent validity of specific formulations. | Task T-03 (W5–6) |

### Audit of Existing Preliminary Passages (`passages.csv`)
- **PASS-001 (REAL-001, Section 3(k)):** Addresses computer programmes per se and algorithms. Kept preliminary. Marked as out-of-scope for Ayurvedic formulation classification; will not be included in formulation routing indexes.
- **PASS-002 (REAL-001, Section 3(p)):** Verified and updated to `reviewed_t01_pending_activation`.
- **PASS-003 (REAL-003, Regulation 2(b)):** Verified and updated to `reviewed_t01_pending_activation`.
- **PASS-004 (REAL-003, Regulation 8):** Verified and updated to `reviewed_t01_pending_activation`.
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
   - *Statutory Text Content:* "The mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance or the mere discovery of any new property or new use for a known substance or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant is not an invention."

---

## 5. Metadata Integrity Statement & Honest Disclosure

In compliance with the project guidelines:
1. No statutory provisions, amendment dates, or official source approvals have been invented or assumed.
2. Where exact Gazette publication timestamps or dynamic checksums for web portals vary across mirror sites, they are explicitly catalogued as verified against the primary India Code and official Ministry portals on 14 November 2026.
3. Substantive answer generation must **not** claim legal advice or formal regulatory clearance; all answers must carry the mandatory non-legal disclaimer.
4. In `source_register.csv`, checksums are marked as `pending_w8_file_ingestion` in the `checksum_status` column rather than placeholder hash strings, honestly reflecting that physical binary capture and SHA-256 computation will occur upon local document ingestion at Week 8.
5. Activation of these rows into the RAG chunk index is held pending Harshit's technical review and validation.
