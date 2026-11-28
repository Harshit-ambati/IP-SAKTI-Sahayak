# IP-SAKTI Sahayak - Backend Service & Data Skeleton

**Module Owner:** Suresh  
**Phase / Task:** Su-01 (Weeks 1–2: API and Data Skeleton)  
**Status:** Implemented & Verified against Phase 1 Gate Requirements  
**Requested Reviewers:**  
- Harshit (Technical lead / Architecture, response contracts & security)  
- Akshay (Frontend module owner / Client compatibility & fixture integration)  

---

## 1. Overview & Architectural Stack

In accordance with [MASTER_PLAN.md](../../docs/work-plan/MASTER_PLAN.md) (Section 5) and [04-suresh.md](../../docs/work-plan/modules/04-suresh.md), Task **Su-01** provides the initial backend API and database skeleton:
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) (0.128.0) with [Uvicorn](https://www.uvicorn.org/) ASGI server.
- **Data Validation & Contracts:** [Pydantic v2](https://docs.pydantic.dev/) (2.13.4) enforcing strict schema validation and error responses (HTTP 422).
- **Database & Retrieval Storage:** [SQLite with FTS5](https://www.sqlite.org/fts5.html) virtual table support for exact-term and keyword indexing.
- **Privacy Architecture:** Zero-knowledge audit logging enforcing that user formulation secrets, ingredient lists, or raw query text are never persisted in routine logs or databases.
- **Synthetic Test Fixtures:** Dedicated, visibly marked synthetic mock datasets (`backend/fixtures/synthetic_fixtures.json`) providing mock endpoints for Akshay's UI flow before real RAG engine integration in Su-02.

---

## 2. Directory Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application definition and lifecycle
│   ├── config.py               # Environment configuration and privacy defaults
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # GET /health, GET /api/v1/health
│   │       ├── classify.py     # POST /api/v1/classify (provisional route evaluation)
│   │       ├── answer.py       # POST /api/v1/answer (evidence-constrained mock responses)
│   │       ├── sources.py      # GET /api/v1/sources, GET /api/v1/passages
│   │       └── referral.py     # POST /api/v1/referral/export (downloadable referral packet)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLite connection pool & FTS5 health checker
│   │   ├── schema.sql          # DDL tables: sources, passages, passages_fts, audit_events
│   │   └── init_db.py          # Database setup and fixture loader script
│   └── models/
│       ├── __init__.py
│       └── schemas.py          # Frozen Master Plan schemas (Intake, ClassificationResult, etc.)
├── fixtures/
│   └── synthetic_fixtures.json # Visibly synthetic mock dataset for testing
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Isolated SQLite test database fixture
│   ├── test_health.py          # Health check endpoint tests
│   ├── test_classify.py        # Input validation & 6 provisional routes tests
│   ├── test_answer.py          # Mock answer synthesis & privacy audit tests
│   ├── test_sources.py         # Source and passage lookup tests
│   ├── test_referral.py        # Referral packet export tests
│   └── test_db.py              # SQLite schema, FTS5 search & privacy tests
├── requirements.txt            # Python dependencies
└── README.md                   # This documentation
```

---

## 3. Installation & Run Commands

### 3.1 Prerequisites
- Python 3.10+ (Tested on Python 3.14.2)
- Pip

### 3.2 Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3.3 Initialize the Local Database
Initializes the SQLite schema (`backend/data/ipsakti_dev.db`), compiles FTS5 triggers, and loads baseline synthetic test fixtures:
```powershell
# Windows PowerShell
python backend/app/db/init_db.py

# Linux / macOS
python backend/app/db/init_db.py
```

### 3.4 Run the Backend Development Server
```powershell
# Windows PowerShell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Or from inside backend directory:
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive OpenAPI documentation will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3.5 Execute Automated Test Suite
Run the 24 automated unit and integration tests:
```powershell
# Windows PowerShell
python -m pytest backend/tests -v

# Linux / macOS
pytest backend/tests -v
```

---

## 4. Endpoint Specifications & Contracts

### 4.1 Health Check: `GET /health` and `GET /api/v1/health`
Checks backend liveness and SQLite FTS5 database readiness.
```json
{
  "status": "healthy",
  "service": "IP-SAKTI Sahayak API",
  "version": "0.1.0-su01",
  "database": "connected",
  "fts5_supported": true,
  "timestamp": "2026-11-15T02:18:27Z"
}
```

### 4.2 Intake Classification: `POST /api/v1/classify`
Validates input fields (`formulation_title`, `ingredients`, `intended_use`, etc.) and returns an explicit provisional route. Contradictory inputs (e.g. cosmetics claiming disease cure) safely return `unknown_ambiguous` with clarifying questions.

**Sample Request:**
```json
{
  "formulation_title": "Synthetic Triphala Churna Sample",
  "ingredients": ["Terminalia chebula", "Terminalia bellirica", "Phyllanthus emblica"],
  "classical_text_reference": "Charaka Samhita",
  "processing_method": "Churna",
  "intended_use": "medicinal",
  "claims_disease_treatment": true,
  "claims_disease_cure": false,
  "has_novel_ingredient": false,
  "standardized_fraction": false,
  "external_application_only": false,
  "jurisdiction": "India",
  "language": "en"
}
```

**Sample Response:**
```json
{
  "provisional_route": "classical_generic",
  "confidence_label": "synthetic_mock_rule_match",
  "governing_provisions": [
    "Drugs and Cosmetics Act 1940, Section 3(a)",
    "First Schedule Authoritative Books"
  ],
  "missing_facts": [],
  "referral_required": false,
  "disclaimer": "Provisional classification only; does not constitute legal or regulatory approval.",
  "is_synthetic_fixture": true
}
```

### 4.3 Cited Answer: `POST /api/v1/answer`
Validates legal query and jurisdiction. Returns structured answer with explicit evidence IDs, cited provisions, assumptions, limitations, and synthetic status flags.

**Sample Request:**
```json
{
  "query": "Is a classical Triphala formulation patentable in India?",
  "jurisdiction": "India",
  "language": "en"
}
```

**Sample Response:**
```json
{
  "status": "answered",
  "jurisdiction": "India",
  "language": "en",
  "provisional_class": null,
  "answer_text": "[SYNTHETIC MOCK ANSWER - INDIA PATENTS] Under Indian patent law, classical Ayurvedic formulations and known herbal combinations are generally excluded from patentability. Specifically, Section 3(p) of the Patents Act, 1970 excludes inventions which in effect are traditional knowledge...",
  "assumptions": [
    "Formulation ingredients are known in classical Ayurvedic pharmacopoeia.",
    "No synergistic efficacy data demonstrating unexpected therapeutic effect was provided."
  ],
  "claims": [
    {
      "claim_id": "SYNTH-CLAIM-PAT-01",
      "claim_text": "Traditional knowledge and aggregations of known traditional components are non-patentable subject matter.",
      "evidence_ids": ["SYNTH-PASS-001"]
    }
  ],
  "cited_provisions": [
    "The Patents Act 1970, Section 3(p)",
    "The Patents Act 1970, Section 3(e)",
    "Drugs and Cosmetics Act 1940, Section 3(a)"
  ],
  "limitations": [
    "Informational guidance only; not formal legal advice, patent certification, or regulatory clearance.",
    "This response is derived from synthetic Phase 1 fixtures for skeleton testing."
  ],
  "evidence_status": "supported",
  "corpus_version": "v0.1-synthetic-su01",
  "model_version": "mock-stub-v1",
  "is_synthetic_fixture": true
}
```

### 4.4 Source & Passage Lookup: `GET /api/v1/sources/{source_id}` & `GET /api/v1/passages/{passage_id}`
Allows frontend cards and citation popups to resolve exact source documents and statutory locators. Unknown IDs return HTTP 404 with clean descriptive errors.

### 4.5 Referral Packet Export: `POST /api/v1/referral/export`
Generates a user-controlled referral packet containing intake facts, statutory provisions, and unresolved issues for export to a professional attorney or Ayush practitioner. No automated third-party messages are transmitted.

### 4.6 H-02 local provision lookup

From the repository root, stage the corpus in a fresh temporary database and run:

```powershell
$env:IPSAKTI_DB_PATH = Join-Path ([IO.Path]::GetTempPath()) ("sahayak-h02-" + [guid]::NewGuid() + ".db")
python -B -m backend.app.db.init_db
python -B -m backend.app.provision_lookup --db $env:IPSAKTI_DB_PATH --jurisdiction India PASS-002
```

The lookup uses the backend's existing SQLite FTS5 index, with one indexed row per passage. It accepts a passage ID, a provision locator, or a literal phrase in an indexed title, locator or paraphrase. Choose `India` or `international_overview`. It opens the database read-only and returns an H-01 answer object. A single eligible match returns the reviewed paraphrase, passage ID, official URL and locator. Multiple matches ask for a passage ID. No matches return `abstained` with empty claims and evidence. Use a precise provision lookup rather than a product eligibility question.

Both the source and passage must be active and real, and the passage must have explicit `approved` status. The merged T-02 records are pending activation, so the example above abstains. The cited path is verified with isolated test records until Thulasi and Harshit clear provisions for activation. The local command does not change the general answer endpoint, which is handled by Su-02.

---

## 5. Security & Privacy Safeguards

1. **Zero-Knowledge Formulation Logging:**
   The `audit_events` table only persists:
   - `request_id`, `timestamp`, `route`, `jurisdiction`, `evidence_ids`, `versions`, `status`.
   Raw questions, formulation titles, and ingredient lists are strictly excluded from routine logs.
2. **Persistent User Case Storage Disabled:**
   `ENABLE_PERSISTENT_CASE_STORAGE` defaults to `False`. No user case or formulation is permanently stored.
3. **Visibly Synthetic Fixtures:**
   All mock fixtures have explicit `is_synthetic: true` flags, synthetic IDs (`SYNTH-SRC-001`, `SYNTH-PASS-001`), and warning notices to prevent confusion with real verified legal evidence.
