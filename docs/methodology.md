# Data collection and research methodology

## Purpose and research question

IP-SAKTI Sahayak will test whether guided formulation classification, jurisdiction filtering and citation checks improve the support and safety of answers to a bounded set of Ayurveda IP and regulatory questions. The system provides information and points to original sources. It does not determine patentability, product approval or legal compliance.

Research question: **On a fixed set of source-grounded questions, how does a classification-guided, citation-checked assistant compare with a basic retrieval-augmented generation baseline in evidence retrieval, claim support, appropriate abstention and jurisdiction separation?**

## Data collection

1. **Knowledge corpus.** Thulasi chooses supported topics, discovers official sources and records each in [source_register.csv](../data/sources/source_register.csv). A discovery page is not a legal citation. Choose the exact operative instrument and provision; check amendments, commencement, authority, access/reuse and extraction quality. Record each approved passage in a copy of [provisions.template.csv](../data/sources/provisions.template.csv). A second teammate reviews a sample from each batch before activation.
2. **Research literature.** Search scholarly databases with a recorded query for legal RAG, source verification, multilingual legal AI, hallucination and abstention. Record database, query, date, inclusion/exclusion decisions and full-text availability. Keep this literature table separate from the legal corpus. If writing a scoping review, report using [PRISMA-ScR](https://www.prisma-statement.org/scoping).
3. **Evaluation scenarios.** Sabeena develops synthetic cases with Thulasi's expected evidence and Deepshika's reviewed language variants. Freeze development and holdout splits before tuning. Use only development results to choose thresholds or prompts.
4. **User feedback.** With consent, ask a small number of participants to attempt supported tasks and report comprehension. Store anonymized summaries and avoid collecting sensitive formulations. Usability ratings do not establish legal accuracy.

## Processing and experiment

Extract provision-level passages; retain source IDs, locators, dates and versions. Implement keyword retrieval as a baseline, then compare it with hybrid retrieval. Run the same frozen cases through a basic RAG answer path and the classification-guided, citation-checked path using the same corpus and generation model. Keep India and international evidence in separate filters.

Measure classification macro-F1 with class counts, evidence recall at five, material-claim support, citation-ID validity, abstention precision and recall, jurisdiction mixing, multilingual citation parity and comprehension. Report denominators, confidence intervals where useful, raw failures, reviewer qualifications and model/corpus versions. Claim support requires human review of the cited passage; a valid URL alone does not prove support.

## Release conditions

Thulasi signs off corpus provenance and routing labels; Harshit signs off technical evaluation; Deepshika signs off reviewed language fixtures; Sabeena keeps the results ledger. If a source becomes stale or a consequential unsupported claim appears, quarantine the affected topic and rerun its tests. Publish actual results only after evaluation.

The [work plan](work-plan/MASTER_PLAN.md) contains the 16-week milestones and quantitative targets. This starter package supplies structure and examples, not completed data collection or measured outcomes.
