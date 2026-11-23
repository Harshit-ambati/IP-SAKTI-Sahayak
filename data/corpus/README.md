# Knowledge corpus

The corpus contains the authoritative legal and regulatory source records for IP-SAKTI Sahayak:

- [documents.csv](documents.csv): Official source records (expanded to 12 instruments in Task T-02) and their primary URLs.
- [source_register.csv](source_register.csv): Comprehensive source registry with expanded provenance metadata (issuing authority, jurisdiction, enactment/commencement dates, amendment history, operative version, capture date, checksum status, access/reuse status, and reviewer).
- [passages.csv](passages.csv): Twenty-five source-backed passage summaries with precise statutory provision locators, URLs, review status, and audit notes.
- [SOURCE_AUDIT_T01.md](SOURCE_AUDIT_T01.md): Formal provenance and amendment audit note for Task T-01 (Merged in PR #1, commit `1a7cae4`).
- [SOURCE_AUDIT_T02.md](SOURCE_AUDIT_T02.md): Formal provenance and amendment audit note for Task T-02.

These are **real-source data**, not synthetic questions. The CSV holds paraphrased summaries rather than full text of official instruments. Open the source URL to inspect the underlying law or gazette text.

### Current Verification Status (Task T-02 Phase 2)

1. **Verified Instruments (`reviewed_t02_pending_activation`):**
   - `REAL-001`: *The Patents Act, 1970* (as amended by Act 38 of 2002 and Act 15 of 2005) — verified for ASU patent exclusions under Section 3(p), Section 3(e), and Section 3(d). Passages: `PASS-002`, `PASS-013`, `PASS-014`.
   - `REAL-002`: *The Drugs and Cosmetics Act, 1940* and *Drugs Rules, 1945* (Ministry of Ayush / CDSCO) — verified for ASU product classification under Section 3(a), First Schedule (54 treatises), Section 3(h), Section 3(aaa), and Rule 2(eb). Passages: `PASS-009`, `PASS-010`, `PASS-011`, `PASS-012`, `PASS-023`.
   - `REAL-003`: *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022* (FSSAI) — verified for food/supplement boundary, exclusions of drugs/cosmetics, statutory ban on adding vitamins/minerals/amino acids (covering all sources), front-of-pack logo, and prohibition against claims in labelling, advertising or presentation to prevent, treat or cure human disease under Regulation 2(b), Regulation 3(4), Regulation 8, Regulation 13(a), and Schedule A. Passages: `PASS-003`, `PASS-004`, `PASS-024`.
   - `REAL-004`: *Biological Diversity Rules, 2024* (National Biodiversity Authority) — verified for commencement date (21 Dec 2024 per NBA FAQ), Form 7 and Form 8 procedural workflows under Rule 1(2). Passage: `PASS-005`.
   - `REAL-005`: *Biological Diversity Amendment Rules, 2025* (National Biodiversity Authority) — verified for commencement date (1 Nov 2025 per NBA FAQ) and updated ABS fee schedules and operational Form 7/8 filings. Passage: `PASS-006`.
   - `REAL-006`: *WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge* (WIPO) — verified for Article 3 (mandatory patent disclosure), Article 5 (sanctions/remedies), and Article 6 (information systems and databases); bounded strictly as international treaty context with no direct domestic legal obligation. Passages: `PASS-007`, `PASS-025`.
   - `REAL-007`: *TKDL Public Overview* (CSIR / Ministry of Ayush) — verified defensive protection framework and patent office access agreements; restricted database contents are strictly excluded. Passage: `PASS-008`.
   - `REAL-008`: *The Biological Diversity Act, 2002* (as amended by Biological Diversity Amendment Act, 2023) — verified Section 6 amendments effective 1 Apr 2024: Section 6(1) foreign entity NBA approval (Form 7); Section 6(1A) domestic entity NBA registration (Form 8); Section 6(1B) commercialisation approval; Section 6(2) benefit sharing determination; Section 7(1) proviso vaid/hakim exemption. Passages: `PASS-015`, `PASS-016`.
   - `REAL-009`: *Drugs Rules, 1945 — Rule 158-B* (Ministry of Ayush) — verified classical ASU licensing citation requirements under Rule 158-B(I) and patent or proprietary ASU medicine safety/literature proof under Rule 158-B(II). Passages: `PASS-017`, `PASS-018`.
   - `REAL-010`: *Guidelines for Examination of Patent Applications on Traditional Knowledge, 2012* (Office of CGPDTM) — verified Section 3(p)/3(e) assessment criteria (synergy evaluated as an examination consideration with comparative data) and mandatory TKDL prior-art searches. Passages: `PASS-019`, `PASS-020`.
   - `REAL-011`: *FSSAI Order on Category A Ayurveda Aahara (25 July 2025)* (FSSAI) — verified Category A classical recipe list and FBO inclusion representation procedure. Passage: `PASS-021`.
   - `REAL-012`: *Drugs Rules, 1945 — Phytopharmaceuticals GSR 918(E)* (CDSCO / Ministry of Health) — verified regulatory burden, minimum 4 bioactive/phytochemical marker requirement under Rule 2(eb), and Schedule Y clinical trial/toxicology requirements. Passage: `PASS-022`.
   - *Activation Gate:* Submitted for Harshit's technical review and validation before activation into the production RAG index.

2. **Preliminary / Out-of-Scope Records:**
   - `PASS-001`: Section 3(k) Patents Act (software/algorithms) is flagged as out-of-scope for Ayurvedic formulation classification.
   - Subsequent phase instruments (e.g. BD Act Section 10 biological disclosure, Form 1 declarations, DMR Act, etc.) are scheduled for Task T-03.

For decision logic and route definitions, see the [Thulasi T-01 Module Specification](../../docs/work-plan/modules/thulasi-t01-specification.md) and [Thulasi T-02 Intake Rules](../../docs/work-plan/modules/thulasi-t02-intake-rules.md). For benchmark evaluation protocols, see [benchmark protocol](../benchmark/README.md).
