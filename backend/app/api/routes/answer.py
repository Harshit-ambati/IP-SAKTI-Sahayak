"""
Answer generation endpoint for IP-SAKTI Sahayak (Task Su-02).
Integrates the retrieval engine through the stable QueryEngineAdapter interface.

Features:
- Dynamically retrieves activated statutory evidence passages via SQLite FTS5.
- Enforces strict jurisdiction isolation (India vs International).
- Excludes preliminary unactivated corpus rows (activated = 0).
- Employs safe abstention when no approved evidence matches the inquiry.
- Logs privacy-preserving audit events without recording confidential queries.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from ...adapters.query_adapter import QueryEngineAdapter, get_query_adapter
from ...config import AUDIT_LOG_ENABLED, ALLOW_SYNTHETIC_DEMO
from ...db.database import get_db
from ...models.schemas import (
    AnswerRequest,
    AnswerResult,
)

router = APIRouter(prefix="/api/v1", tags=["Answer"])


@router.post(
    "/answer",
    response_model=AnswerResult,
    summary="Generate Cited Legal/Regulatory Answer (Su-02 Engine Integration)",
    description=(
        "Accepts a query, selected jurisdiction, and optional intake payload. "
        "Retrieves approved evidence passages via the stable query engine adapter and "
        "synthesizes an evidence-grounded AnswerResult with claims, passage citations, "
        "and statutory provisions. Cleanly abstains if no approved evidence is found. "
        "Strictly isolates India and International jurisdictions, and records zero-knowledge audit logs."
    ),
)
def generate_answer(
    request: AnswerRequest,
    query_adapter: QueryEngineAdapter = Depends(get_query_adapter),
    conn: sqlite3.Connection = Depends(get_db),
) -> AnswerResult:
    """
    Executes answer generation via the configured QueryEngineAdapter.
    Enforces approved evidence gate: callers cannot relax or override this.
    Only server-side ALLOW_SYNTHETIC_DEMO configuration can permit synthetic demo retrieval.
    Records a privacy-preserving audit event without user secret formulation data.
    """
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # Enforce approved evidence gate: callers cannot relax or override this.
    # Only server-side ALLOW_SYNTHETIC_DEMO configuration can permit synthetic demo retrieval.
    require_approved = not ALLOW_SYNTHETIC_DEMO

    # Delegate retrieval and synthesis to the stable query adapter
    result = query_adapter.generate_answer(
        request,
        require_approved_evidence=require_approved,
    )

    # Privacy-Compliant Audit Event Logging
    # MUST NOT log user query text, full formulation, or confidential ingredients.
    if AUDIT_LOG_ENABLED:
        try:
            audit_id = str(uuid.uuid4())
            evidence_ids_str = json.dumps([c.evidence_ids for c in result.claims])
            versions_str = json.dumps({"corpus": result.corpus_version, "model": result.model_version})
            route_str = str(result.provisional_class.value if result.provisional_class else "direct_query")

            conn.execute(
                """
                INSERT INTO audit_events (
                    audit_id, request_id, timestamp, route, jurisdiction, evidence_ids, versions, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    request_id,
                    timestamp,
                    route_str,
                    request.jurisdiction.value,
                    evidence_ids_str,
                    versions_str,
                    result.status.value,
                )
            )
            conn.commit()
        except Exception:
            pass

    return result
