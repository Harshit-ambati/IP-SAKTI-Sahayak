# Knowledge corpus

The corpus contains the authoritative legal and regulatory source records for IP-SAKTI Sahayak:

- [documents.csv](documents.csv): Twelve official source records and their primary URLs across Indian patent/TK law, ASU product classification, Ayurveda Aahara, and biodiversity.
- [source_register.csv](source_register.csv): Comprehensive source registry with expanded provenance metadata (issuing authority, jurisdiction, enactment/commencement dates, amendment history, operative version, capture date, checksums, access/reuse status, and reviewer).
- [passages.csv](passages.csv): Twenty-five source-backed passage summaries with precise statutory provision locators, URLs, review status, and audit notes.
- [SOURCE_AUDIT_T01.md](SOURCE_AUDIT_T01.md): Formal provenance and amendment audit note for Task T-01 (Phase 1).
- [SOURCE_AUDIT_T02.md](SOURCE_AUDIT_T02.md): Formal provenance and amendment audit note for Task T-02 (Phase 2), auditing 12 official instruments and 25 provision passages.

These are **real-source data**, not synthetic questions. The CSV holds paraphrased summaries rather than full text of official instruments. Open the source URL to inspect the underlying law or gazette text.

### Verification Status & Milestones

1. **Task T-01 Phase 1 Baseline:**
   - 3 primary instruments verified: `REAL-001` (Patents Act 1970), `REAL-002` (Drugs and Cosmetics Act 1940), and `REAL-003` (FSSAI Ayurveda Aahara Regulations 2022).
   - Six provisional routes and initial intake decision rules specified in [thulasi-t01-specification.md](../../docs/work-plan/modules/thulasi-t01-specification.md).

2. **Task T-02 Phase 2 Corpus Extension:**
   - Extended corpus to **twelve reviewed official sources** (`REAL-001` through `REAL-012`), all audited under status `reviewed_t02_pending_activation`.
   - Priority areas expanded:
     - *Product definitions & licensing proof:* `REAL-002`, `REAL-009` (Rule 158-B ASU licensing guidelines), and `REAL-012` (Drugs Rules GSR 918(E) Phytopharmaceuticals).
     - *Indian Patent & Traditional Knowledge:* `REAL-001`, `REAL-008` (Biological Diversity Act s. 6), `REAL-010` (CGPDTM Patent Examination Guidelines on TK), `REAL-007` (TKDL public framework), and `REAL-006` (WIPO GRATK Treaty overview).
     - *Ayurveda Aahara regulations & orders:* `REAL-003` and `REAL-011` (FSSAI Order dated 25-07-2025).
     - *Biodiversity Rules:* `REAL-004` (BD Rules 2024) and `REAL-005` (BD Amendment Rules 2025).
   - Passage count increased to 25 verified records (`PASS-001` through `PASS-025`).
   - Delivered minimum-question intake protocol, missing-fact prompts, and decision rules in [thulasi-t02-intake-rules.md](../../docs/work-plan/modules/thulasi-t02-intake-rules.md).

*Activation Gate:* Submitted for Harshit's technical review and validation before activation into the production RAG index.
