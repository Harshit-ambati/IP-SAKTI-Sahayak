# Knowledge corpus

The corpus contains the authoritative legal and regulatory source records for IP-SAKTI Sahayak:

- [documents.csv](documents.csv): Twenty official source records and their primary URLs across Indian patent/TK law, ASU product classification, Ayurveda Aahara, biodiversity (ABS), and advertising regulations.
- [source_register.csv](source_register.csv): Comprehensive source registry with expanded provenance metadata (issuing authority, jurisdiction, enactment/commencement dates, amendment history, operative version, capture date, checksums, access/reuse status, and reviewer).
- [passages.csv](passages.csv): Thirty-six source-backed passage summaries with precise statutory provision locators, URLs, review status, and audit notes.
- [SOURCE_AUDIT_T01.md](SOURCE_AUDIT_T01.md): Formal provenance and amendment audit note for Task T-01 (Phase 1).
- [SOURCE_AUDIT_T02.md](SOURCE_AUDIT_T02.md): Formal provenance and amendment audit note for Task T-02 (Phase 2).
- [SOURCE_AUDIT_T03.md](SOURCE_AUDIT_T03.md): Formal provenance and amendment audit note for Task T-03 (Phase 3), auditing 20 official instruments, 36 provision passages, biodiversity rules harmonization, and peer review revisions.

These are **real-source data**, not synthetic questions. The CSV holds paraphrased summaries rather than full text of official instruments. Open the source URL to inspect the underlying law or gazette text.

### Verification Status & Milestones

1. **Task T-01 Phase 1 Baseline:**
   - Verified 3 core instruments (`REAL-001`, `REAL-002`, `REAL-003`).
   - Defined initial six provisional routes and decision logic in [thulasi-t01-specification.md](../../docs/work-plan/modules/thulasi-t01-specification.md).

2. **Task T-02 Phase 2 Corpus Extension:**
   - Extended to 12 official sources and 25 passages.
   - Built minimum-question intake protocol in [thulasi-t02-intake-rules.md](../../docs/work-plan/modules/thulasi-t02-intake-rules.md).

3. **Task T-03 Phase 3 Bounded Rules & Biodiversity Harmonization:**
   - Extended corpus to **twenty reviewed official sources** (`REAL-001` through `REAL-020`) and **36 provision-level passages** (`PASS-001` through `PASS-036`).
   - Machine-readable decision rule contract implemented in [decision_rules.json](../rules/decision_rules.json).
   - Detailed specification and 10 reviewed sample rule firings published in [thulasi-t03-decision-rules.md](../../docs/work-plan/modules/thulasi-t03-decision-rules.md).
   - Harmonized *Biological Diversity Rules, 2024* (notified 22 Oct 2024, commenced 21 Dec 2024) with *Biological Diversity Amendment Rules, 2025* (notified 6 May 2025, commencing 1 Nov 2025) and *Biological Diversity Act, 2002* (as amended 2023, effective 1 Apr 2024, distinguishing s. 6(1) foreign approval Form 7 from s. 6(1A) domestic registration Form 8, s. 6(1B) commercialization approval, and s. 7(1) proviso vaid/hakim exemption).
   - Documented omission of Drugs Rules Rule 170 via G.S.R. 360(E) dated 1 July 2024 (`REAL-015`, `PASS-029` marked `omitted_superseded_gsr360e`).
   - Explicit strict TKDL non-confidentiality boundary and uncertain/needs-expert referral pathways.
   - Addressed peer review revisions on FSSAI locators (Reg 3(4) vitamins/minerals/amino acids ban, Reg 13(a) logo), WIPO Articles 5/6, checksum status (`pending_w8_file_ingestion`), and classical routing fallback to Route 7.

*Activation Gate:* Submitted for Harshit's technical review and validation before activation into the production RAG index.
