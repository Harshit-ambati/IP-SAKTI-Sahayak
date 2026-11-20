# Knowledge corpus

The corpus contains the authoritative legal and regulatory source records for IP-SAKTI Sahayak:

- [documents.csv](documents.csv): Seven official source records and their primary URLs.
- [source_register.csv](source_register.csv): Comprehensive source registry with expanded provenance metadata (issuing authority, jurisdiction, enactment/commencement dates, amendment history, operative version, capture date, checksum status, access/reuse status, and reviewer).
- [passages.csv](passages.csv): Fourteen source-backed passage summaries with precise statutory provision locators, URLs, review status, and audit notes.
- [SOURCE_AUDIT_T01.md](SOURCE_AUDIT_T01.md): Formal provenance and amendment audit note for Task T-01.

These are **real-source data**, not synthetic questions. The CSV holds paraphrased summaries rather than full text of official instruments. Open the source URL to inspect the underlying law or gazette text.

### Current Verification Status (Task T-01 Phase 1)

1. **Verified Instruments (`reviewed_t01_pending_activation`):**
   - `REAL-001`: *The Patents Act, 1970* (as amended by Act 38 of 2002 and Act 15 of 2005) — verified for ASU patent exclusions under Section 3(p), Section 3(e), and Section 3(d). Passages: `PASS-002`, `PASS-013`, `PASS-014`.
   - `REAL-002`: *The Drugs and Cosmetics Act, 1940* and *Drugs Rules, 1945* (Ministry of Ayush / CDSCO) — verified for ASU product classification under Section 3(a), First Schedule, Section 3(h), Section 3(aaa), and Rule 2(eb). Passages: `PASS-009`, `PASS-010`, `PASS-011`, `PASS-012`.
   - `REAL-003`: *Food Safety and Standards (Ayurveda Aahara) Regulations, 2022* (FSSAI) — verified for food/supplement boundary, exclusions, statutory ban on vitamins/minerals/amino acids, front-of-pack logo, and disease claims prohibitions under Regulation 2(b), Regulation 3(4), Regulation 8, Regulation 13(a), and Schedule A. Passages: `PASS-003`, `PASS-004`.
   - *Activation Gate:* Submitted for Harshit's technical review and validation before activation into the production RAG index.

2. **Preliminary / Unapproved Records (`preliminary_unverified` / `source_checked_domain_review_pending`):**
   - `REAL-004` & `REAL-005`: Biological Diversity Rules 2024 and 2025 amendments. Preliminary records; require full Gazette text inspection and correlation with the Biological Diversity (Amendment) Act 2023 in Task T-03.
   - `REAL-006`: WIPO GRATK Treaty. Adopted May 2024; pending ratification threshold and domestic legislative analysis in Task T-03. Must not be treated as domestic Indian law.
   - `REAL-007`: TKDL public overview. Informational background only; restricted database contents are strictly excluded.
   - `PASS-001`: Section 3(k) Patents Act (software/algorithms) is flagged as out-of-scope for Ayurvedic formulation classification.
   - `PASS-005` to `PASS-008`: Pending domain review in subsequent milestones.

For decision logic and route definitions, see the [Thulasi T-01 Module Specification](../../docs/work-plan/modules/thulasi-t01-specification.md). For benchmark evaluation protocols, see [benchmark protocol](../benchmark/README.md).
