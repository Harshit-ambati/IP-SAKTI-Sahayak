# Knowledge corpus

The corpus has two populated CSVs:

- [documents.csv](documents.csv): seven official source records and their URLs.
- [passages.csv](passages.csv): eight source-backed, paraphrased records with locators and review notes.

These are **real-source data**, not synthetic questions. The passage summaries are preliminary and marked `source_checked_domain_review_pending`. They are suitable for corpus-format development and source navigation; they are **not approved as legal-answer evidence** until the named provisions, amendments, applicability and wording receive domain review. The CSV holds paraphrases rather than full text of the official instruments. Open the source URL to inspect the underlying law or guidance.

Thulasi should extend the dataset one official document and provision at a time. Each new row needs a stable ID, exact jurisdiction and locator, current source URL, instrument/version status, review decision and reviewer. For citations, the app must show the source and provision; the reviewed summary can help retrieval but must not replace checking the actual source. Keep India and international records separate.

The corpus is still incomplete for the proposed MVP. The Ayush compilation and the 2024/2025 biodiversity rules are listed in `documents.csv` but need more reviewed provision rows. Add Patents Rules amendments, the amended Biological Diversity Act, relevant product definitions and current FSSAI material before enabling the associated answer topics. The TKDL row represents only its public overview.

The [benchmark protocol](../benchmark/README.md) describes the separate, source-grounded evaluation dataset the team must create. The earlier twelve unreviewed synthetic fixture prompts and empty templates were removed from the repository because they could be mistaken for completed data.
