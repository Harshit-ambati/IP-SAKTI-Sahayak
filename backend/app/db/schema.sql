-- IP-SAKTI Sahayak SQLite Database Schema
-- Su-01 Data Skeleton: Sources, Passages, FTS5 Search, and Privacy-Compliant Audit Log

-- 1. Official and Synthetic Sources
-- activated = 1: eligible for public lookup endpoints (synthetic test fixtures or Thulasi-approved real records)
-- activated = 0: stored locally but NOT returned from public /sources or /passages endpoints (preliminary corpus rows)
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    authority TEXT NOT NULL,
    title TEXT NOT NULL,
    official_url TEXT NOT NULL,
    format TEXT NOT NULL DEFAULT 'html',
    role TEXT NOT NULL DEFAULT 'primary',
    priority TEXT NOT NULL DEFAULT 'required',
    verification_status TEXT NOT NULL,
    review_note TEXT,
    is_synthetic INTEGER NOT NULL DEFAULT 0,
    activated INTEGER NOT NULL DEFAULT 0
);

-- 2. Evidence Passages
-- activated = 1: eligible for public lookup endpoints
-- activated = 0: stored locally but NOT returned from public /passages endpoints
CREATE TABLE IF NOT EXISTS passages (
    passage_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    jurisdiction TEXT NOT NULL,
    authority TEXT NOT NULL,
    document_title TEXT NOT NULL,
    locator TEXT NOT NULL,
    paraphrased_content TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'statute',
    review_status TEXT NOT NULL,
    review_note TEXT,
    is_synthetic INTEGER NOT NULL DEFAULT 0,
    activated INTEGER NOT NULL DEFAULT 0
);

-- 3. FTS5 Virtual Table for Hybrid/Full-Text Search
CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(
    passage_id UNINDEXED,
    document_title,
    locator,
    paraphrased_content,
    jurisdiction,
    content='passages',
    content_rowid='rowid'
);

-- Triggers to keep FTS5 synchronized with passages table
CREATE TRIGGER IF NOT EXISTS passages_ai AFTER INSERT ON passages BEGIN
    INSERT INTO passages_fts(rowid, passage_id, document_title, locator, paraphrased_content, jurisdiction)
    VALUES (new.rowid, new.passage_id, new.document_title, new.locator, new.paraphrased_content, new.jurisdiction);
END;

CREATE TRIGGER IF NOT EXISTS passages_ad AFTER DELETE ON passages BEGIN
    INSERT INTO passages_fts(passages_fts, rowid, passage_id, document_title, locator, paraphrased_content, jurisdiction)
    VALUES('delete', old.rowid, old.passage_id, old.document_title, old.locator, old.paraphrased_content, old.jurisdiction);
END;

CREATE TRIGGER IF NOT EXISTS passages_au AFTER UPDATE ON passages BEGIN
    INSERT INTO passages_fts(passages_fts, rowid, passage_id, document_title, locator, paraphrased_content, jurisdiction)
    VALUES('delete', old.rowid, old.passage_id, old.document_title, old.locator, old.paraphrased_content, old.jurisdiction);
    INSERT INTO passages_fts(rowid, passage_id, document_title, locator, paraphrased_content, jurisdiction)
    VALUES (new.rowid, new.passage_id, new.document_title, new.locator, new.paraphrased_content, new.jurisdiction);
END;

-- 4. Privacy-Compliant Audit Log
-- Enforces zero-knowledge logging of formulation secrets:
-- ONLY records request_id, timestamp, route, jurisdiction, evidence_ids, versions, and status.
CREATE TABLE IF NOT EXISTS audit_events (
    audit_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    route TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    evidence_ids TEXT NOT NULL,
    versions TEXT NOT NULL,
    status TEXT NOT NULL
);
