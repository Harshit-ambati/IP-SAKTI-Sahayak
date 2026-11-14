# Corpus Source Audit Note: Task T-03 (Phase 3)

**Date of Audit:** 14 November 2026  
**Auditor / Reviewer:** Thulasi (Authoritative source corpus, formulation categories and decision rules)  
**Deliverable:** T-03 Formal Provenance Audit of Twenty Official Instruments, 35 Provision Passages, Biodiversity Rules Harmonization, and Rule Verification Log  
**Target Repository:** `https://github.com/Harshit-ambati/IP-SAKTI-Sahayak`  
**Review Requests:** Harshit (Technical lead / Corpus activation & rule contracts), Deepshika (Multilingual & Terminology)  

---

## 1. Scope & Audit Purpose

Under [MASTER_PLAN.md](../../docs/work-plan/MASTER_PLAN.md) (Section 5) and [02-thulasi.md](../../docs/work-plan/modules/02-thulasi.md), Task T-03 expands the verified knowledge corpus to **twenty useful official source records** (`REAL-001` through `REAL-020`) and establishes the bounded decision rules for:
- Indian Patent / Traditional Knowledge screening (*Patents Act, 1970* Sections 3(p), 3(e), 3(d), 10(4)(d)(ii); *CGPDTM Guidelines, 2012*).
- Biological resource and Access & Benefit Sharing (ABS) governance (*Biological Diversity Act, 2002* as amended 2023; *Biological Diversity Rules, 2024* read in conjunction with the *Biological Diversity Amendment Rules, 2025*).
- Product route classification and safe expert referrals (*Drugs and Cosmetics Act, 1940*, *Drugs Rules, 1945*, *FSSAI Ayurveda Aahara Regulations, 2022*, and *FSSAI 2025 Order*).
- Strict confidentiality boundaries for the Traditional Knowledge Digital Library (TKDL).

---

## 2. Twenty Verified Official Source Records

| Source ID | Official Instrument Title | Issuing Authority | Jurisdiction | Instrument Type | Official Primary URL | Key Dates & Amendments | Operative Status | Access & Reuse Conditions | Status |
|---|---|---|---|---|---|---|---|---|---|
| `REAL-001` | *The Patents Act, 1970* | IP India / Legislative Dept | India | Primary Statute | `https://www.indiacode.nic.in/bitstream/123456789/1392/1/A1970-39.pdf` | Enacted: 1970-09-19; Commenced: 1972-04-20; Acts 38 of 2002 & 15 of 2005 | Operative | Public domain legislative enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-002` | *The Drugs and Cosmetics Act, 1940* | Ministry of Ayush / CDSCO | India | Primary Statute | `https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf` | Enacted: 1940-04-10; Act 13 of 1964; GSR 918(E) (2015) | Operative | Public domain statutory enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-003` | *Ayurveda Aahara Regulations, 2022* | FSSAI | India | Subordinate Regulation | `https://fssai.gov.in/upload/notifications/2022/05/62789a20b54bdGazette_Notification_Ayurveda_Aahara_09_05_2022.pdf` | Notified: 2022-05-05; Commenced: 2022-05-05; Mandatory: 2022-11-01; Reg 2(b), Reg 3(4), Reg 8, Reg 13(a) | Operative | Public domain subordinate legislation (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-004` | *Biological Diversity Rules, 2024* | National Biodiversity Authority | India | Subordinate Statutory Rules | `https://nbaindia.nic.in/sites/default/files/2026-05/BD_Rules.pdf` | Notified: 2024; Commenced: 2024-12-21 per NBA FAQ; IPR filing procedures | Operative | Public domain subordinate legislation (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-005` | *Biological Diversity Amendment Rules, 2025* | National Biodiversity Authority | India | Subordinate Statutory Rules | `https://nbaindia.nic.in/sites/default/files/2026-05/AmendmentBD_Rules.pdf` | Notified: 2025; Commenced: 2025-11-01 per NBA FAQ; operational fee schedules and Form III updates | Operative | Public domain subordinate legislation (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-006` | *WIPO GRATK Treaty (Adopted May 2024)* | WIPO | International Overview | Multilateral Treaty | `https://www.wipo.int/wipolex/en/treaties/textdetails/19849` | Adopted: 2024-05-24; entry into force requires 15 ratifications | Adopted text | Public official multilateral treaty text | `reviewed_t03_pending_activation` |
| `REAL-007` | *TKDL Public Overview* | CSIR & Ministry of Ayush | India | Institutional Guidance | `https://www.tkdl.res.in/tkdl/langdefault/common/Abouttkdl.asp` | Established: 2001; bilateral patent search agreements; confidential files excluded | Active framework | Public institutional overview | `reviewed_t03_pending_activation` |
| `REAL-008` | *Biological Diversity Act, 2002 (amended 2023)* | National Biodiversity Authority | India | Primary Statute | `https://www.indiacode.nic.in/handle/123456789/2046` | Enacted: 2003-02-05; Act 10 of 2023 (w.e.f. 2023-08-01, s. 6(1), s. 6(2), s. 6(1A)) | Operative | Public domain legislative enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-009` | *Drugs Rules, 1945 — Rule 158-B* | Ministry of Ayush | India | Subordinate Statutory Rules | `https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf` | Notified: GSR 560(E) dated 2005-08-10; licensing proof criteria | Operative | Public domain statutory rules (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-010` | *CGPDTM Guidelines on TK Patents (2012)* | Office of CGPDTM (IP India) | India | Administrative Guidelines | `https://ipindia.gov.in/writereaddata/Portal/IPOGuidelines/1_37_1_guidelines-for-examination-of-patent-applications-traditional-knowledge.pdf` | Issued: 2012-10-29; s. 3(p)/3(e) administrative assessment | Operative guidance | Public official administrative guidelines | `reviewed_t03_pending_activation` |
| `REAL-011` | *FSSAI Ayurveda Aahara Implementation Order (2025)* | FSSAI | India | Administrative Order | `https://www.fssai.gov.in/upload/uploadfiles/files/Order%20dated%2025-07-2025%20enclosing%20Ayurveda%20Aahara.pdf` | Issued: 2025-07-25 (F. No. Stds/SP-05/A-1.2022-Part(1)) | Operative | Public official administrative order | `reviewed_t03_pending_activation` |
| `REAL-012` | *Drugs Rules, 1945 — Phytopharmaceuticals GSR 918(E)* | CDSCO / Health Ministry | India | Subordinate Statutory Rules | `https://cdsco.gov.in/opencms/export/sites/CDSCO_WEB/pdf-page/GSR-918E.pdf` | Notified: 2015-11-30; Rule 2(eb), Schedule Y Appendix I/IA | Operative | Public domain statutory rules (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-013` | *Patents Act, 1970 — Section 10 Biological Disclosure* | IP India / Legislative Dept | India | Primary Statute | `https://www.indiacode.nic.in/bitstream/123456789/1392/1/A1970-39.pdf` | Section 10(4)(d)(ii) inserted by Act 38 of 2002 w.e.f. 2003-05-20 | Operative | Public domain legislative enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-014` | *Patents Rules, 2003 (amended up to 2024 GSR 190(E))* | Office of CGPDTM | India | Subordinate Statutory Rules | `https://ipindia.gov.in/writereaddata/Portal/Images/pdf/Patents_Amendment_Rules_2024.pdf` | Rule 13 Form 1 declaration; GSR 190(E) dated 2024-03-15 | Operative | Public domain statutory rules (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-015` | *Drugs Rules, 1945 — Rule 170 ASU Advertising GSR 851(E)*| Ministry of Ayush | India | Subordinate Statutory Rules | `https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf` | GSR 851(E) dated 2018-12-21; prior approval & misleading ad ban | Operative | Public domain statutory rules (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-016` | *Drugs and Magic Remedies Act, 1954* | Ministry of Health | India | Primary Statute | `https://www.indiacode.nic.in/handle/123456789/1473` | Enacted: 1954-04-30; Sections 3 and 4 disease cure ad ban | Operative | Public domain legislative enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |
| `REAL-017` | *NBA ABS Regulations, 2014 GSR 886(E)* | National Biodiversity Authority | India | Subordinate Statutory Regulations | `https://nbaindia.nic.in/sites/default/files/2026-05/ABS_Regulations_2014.pdf` | GSR 886(E) dated 2014-11-21; benefit sharing formula (0.1%-0.5%) | Operative | Public subordinate regulations (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-018` | *FSSAI Advertising and Claims Regulations, 2018* | FSSAI | India | Subordinate Regulation | `https://fssai.gov.in/upload/notifications/2019/07/5d1db96860c23Gazette_Notification_Advertising_Claims_03_07_2019.pdf` | Notified: 2018-11-19; Regulation 4 non-medicinal food claims | Operative | Public subordinate regulations (Gazette of India) | `reviewed_t03_pending_activation` |
| `REAL-019` | *CDSCO Guidance on Phytopharmaceuticals (2018)* | CDSCO | India | Administrative Guidance | `https://cdsco.gov.in/opencms/export/sites/CDSCO_WEB/pdf-page/guidance_phytopharmaceutical.pdf` | Issued: 2018-05-10; botanical multi-marker standardization data | Operative guidance | Public administrative guidance (CDSCO) | `reviewed_t03_pending_activation` |
| `REAL-020` | *PPV&FR Act, 2001 — Section 39 (Farmers' Rights)* | PPV&FR Authority | India | Primary Statute | `https://www.indiacode.nic.in/handle/123456789/1908` | Enacted: 2001-10-30; Section 39 plant variety rights vs patents | Operative | Public domain legislative enactment (Section 52(1)(q) Indian Copyright Act) | `reviewed_t03_pending_activation` |

---

## 3. Provision-Level Passage Ledger (Passages PASS-001 through PASS-036)

All 36 provision passages currently indexed in `data/corpus/passages.csv` have been verified against official source documents:
- `PASS-001` to `PASS-025`: Fully verified and audited in Phases 1 & 2 (including corrected `PASS-003` for Reg 3(4), `PASS-004` for Reg 13(a), `PASS-005`/`PASS-006` for NBA FAQ dates, `PASS-015`/`PASS-016` for Section 6(1)/6(2) compliance bifurcation, and `PASS-025` for WIPO Article 6 information systems).
- `PASS-026`: *Patents Act, 1970* Section 10(4)(d)(ii) — Mandatory disclosure of biological material source and geographical origin in patent specifications.
- `PASS-027`: *Patents Rules, 2003* Rule 13 & Form 1 — Procedural declaration regarding Indian biological material and status of NBA permission.
- `PASS-028`: *Patents Rules, 2003* Rule 131 — Form 27 commercial working statements as amended by 2024 Rules.
- `PASS-029`: *Drugs Rules, 1945* Rule 170 — Advertising approval and unique identification number requirements for ASU medicines.
- `PASS-030`: *Drugs and Magic Remedies Act, 1954* Section 3 — Statutory prohibition on advertising drugs for treatment of Schedule diseases (cancer, diabetes, etc.).
- `PASS-031`: *Drugs and Magic Remedies Act, 1954* Section 4 — Prohibition on false impressions and misleading drug advertisements.
- `PASS-032`: *NBA ABS Regulations, 2014* Regulations 3 & 4 — Economic benefit-sharing percentage formulas (0.1% to 0.5% ex-factory sales) for commercial biological resource utilization.
- `PASS-033`: *FSSAI Claims Regulations, 2018* Regulation 4 — General food claims standards prohibiting therapeutic or disease prevention claims.
- `PASS-034`: *CDSCO Phytopharmaceutical Guidance, 2018* Section 3 — Taxonomic authentication and chromatographic multi-marker standardization standards.
- `PASS-035`: *PPV&FR Act, 2001* Section 39 — Farmers' rights to save, use, and share seed; boundary distinguishing plant variety protection from patent monopolies.
- `PASS-036`: *WIPO GRATK Treaty (2024)* Article 5 — Sanctions and remedies for failure to comply with patent disclosure requirements regarding genetic resources and associated traditional knowledge.

---

## 4. Formal Review Log & Handoff

- **Log Entry 4 (2026-11-14, Task T-03):** Completed formal provenance audit of 20 official instruments and 35 provision passages. Integrated machine-readable JSON rule contract (`data/rules/decision_rules.json`).
- **Log Entry 5 (2026-11-15, Peer Review Revisions):** Addressed Harshit's peer-review feedback:
  1. *Biodiversity Approval Rule & Section 6:* Refined `RULE-ABS-01` and `RULE-T02-09` to distinguish Section 3(2) foreign entities (mandatory NBA approval before patent grant, s. 6(1)) from Section 7 domestic Indian entities (mandatory NBA registration before patent grant and approval before commercialization, s. 6(2)). Updated `PASS-015` and `PASS-016` accordingly.
  2. *Biodiversity Dates:* Corrected commencement dates to 2024-12-21 (2024 Rules) and 2025-11-01 (2025 Amendment Rules) per NBA FAQ in `source_register.csv`, `documents.csv`, and `passages.csv`.
  3. *Ayurveda Aahara Provision Locators:* Assigned synthetic nutrients ban to Regulation 3(4) (not 2(b)); front-of-pack logo mandate to Regulation 13(a) (not 8); retained Regulation 8 for disease claims prohibition.
  4. *WIPO Treaty Locators:* Corrected information systems locator from Article 5 to Article 6 in `PASS-025`, and added `PASS-036` covering Article 5 (sanctions and remedies).
  5. *Checksum Integrity:* Renamed `checksum_sha256` to `checksum_status` in `source_register.csv`, marking rows as `pending_w8_file_ingestion` to honestly indicate that physical captured binary hashes will be generated during local snapshot ingestion in Week 8.
  6. *Routing Fallback Risk:* Corrected `RULE-CLS-01` and `RULE-T02-01` so that missing classical text citations route to Route 7 clarification / expert referral (`needs_expert_referral`), never defaulting or demoting to proprietary medicine.
- **TKDL Exclusion Check:** Re-verified that no private or restricted TKDL formulation dossiers are stored or accessible.
- **Teammate Review Conducted:**
  - `Harshit (Technical Lead)`: Audited machine-readable rule schema (`data/rules/decision_rules.json`), scenario locators, and patent/ABS multi-statute interaction.
  - `Deepshika (Terminology)`: Audited statutory terminology consistency across classical ASU, P&P ASU, Ayurveda Aahara, and cosmetic routes.
  - `Sabeena (Benchmarks)`: Validated sample scenario outcomes against the benchmark protocol ledger.

