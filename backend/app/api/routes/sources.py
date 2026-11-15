"""
Source and Passage lookup routes for IP-SAKTI Sahayak (Task Su-01).

Activation gate: only rows with activated=1 are returned from public endpoints.
  - Synthetic fixtures (is_synthetic=1, activated=1): visible for testing.
  - Preliminary real corpus rows (is_synthetic=0, activated=0): staged locally only;
    NOT returned until Thulasi's review and Harshit's corpus activation gate is passed.
"""

import sqlite3
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ...db.database import get_db
from ...models.schemas import (
    SourceRecord,
    SourceListResponse,
    EvidencePassage,
    PassageListResponse,
)

router = APIRouter(prefix="/api/v1", tags=["Sources & Evidence"])

# Activation gate: only rows with activated=1 are served from public endpoints.
_ACTIVATION_FILTER = "activated = 1"


def _row_to_source(r: sqlite3.Row) -> SourceRecord:
    return SourceRecord(
        source_id=r["source_id"],
        topic=r["topic"],
        authority=r["authority"],
        title=r["title"],
        official_url=r["official_url"],
        format=r["format"],
        role=r["role"],
        priority=r["priority"],
        verification_status=r["verification_status"],
        review_note=r["review_note"],
        is_synthetic=bool(r["is_synthetic"]),
    )


def _row_to_passage(r: sqlite3.Row) -> EvidencePassage:
    return EvidencePassage(
        passage_id=r["passage_id"],
        source_id=r["source_id"],
        jurisdiction=r["jurisdiction"],
        authority=r["authority"],
        document_title=r["document_title"],
        locator=r["locator"],
        paraphrased_content=r["paraphrased_content"],
        source_url=r["source_url"],
        source_type=r["source_type"],
        review_status=r["review_status"],
        review_note=r["review_note"],
        is_synthetic=bool(r["is_synthetic"]),
    )


@router.get(
    "/sources/{source_id}",
    response_model=SourceRecord,
    summary="Get Source Document by ID",
    description=(
        "Looks up an activated source record by its unique source_id. "
        "Preliminary corpus rows (activated=0) are not returned; use the internal admin path."
    ),
)
def get_source_by_id(
    source_id: str,
    conn: sqlite3.Connection = Depends(get_db),
) -> SourceRecord:
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT source_id, topic, authority, title, official_url, format, role, priority,
               verification_status, review_note, is_synthetic
        FROM sources
        WHERE source_id = ? AND {_ACTIVATION_FILTER}
        """,
        (source_id,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source record with ID '{source_id}' not found or not yet activated.",
        )
    return _row_to_source(row)


@router.get(
    "/sources",
    response_model=SourceListResponse,
    summary="List Activated Source Documents",
    description=(
        "Returns a paginated list of activated source documents. "
        "Preliminary corpus rows (activated=0) are excluded until Harshit's corpus activation gate is passed."
    ),
)
def list_sources(
    topic: Optional[str] = Query(None, description="Optional topic filter"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    conn: sqlite3.Connection = Depends(get_db),
) -> SourceListResponse:
    cur = conn.cursor()
    if topic:
        cur.execute(
            f"SELECT count(*) FROM sources WHERE topic = ? AND {_ACTIVATION_FILTER}",
            (topic,)
        )
        total = cur.fetchone()[0]
        cur.execute(
            f"""
            SELECT source_id, topic, authority, title, official_url, format, role, priority,
                   verification_status, review_note, is_synthetic
            FROM sources
            WHERE topic = ? AND {_ACTIVATION_FILTER}
            ORDER BY source_id ASC
            LIMIT ? OFFSET ?
            """,
            (topic, limit, offset)
        )
    else:
        cur.execute(f"SELECT count(*) FROM sources WHERE {_ACTIVATION_FILTER}")
        total = cur.fetchone()[0]
        cur.execute(
            f"""
            SELECT source_id, topic, authority, title, official_url, format, role, priority,
                   verification_status, review_note, is_synthetic
            FROM sources
            WHERE {_ACTIVATION_FILTER}
            ORDER BY source_id ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )

    rows = cur.fetchall()
    return SourceListResponse(total=total, items=[_row_to_source(r) for r in rows])


@router.get(
    "/passages/{passage_id}",
    response_model=EvidencePassage,
    summary="Get Evidence Passage by ID",
    description=(
        "Looks up an activated provision passage by its passage_id. "
        "Preliminary corpus rows (activated=0) are not returned."
    ),
)
def get_passage_by_id(
    passage_id: str,
    conn: sqlite3.Connection = Depends(get_db),
) -> EvidencePassage:
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT passage_id, source_id, jurisdiction, authority, document_title, locator,
               paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
        FROM passages
        WHERE passage_id = ? AND {_ACTIVATION_FILTER}
        """,
        (passage_id,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence passage with ID '{passage_id}' not found or not yet activated.",
        )
    return _row_to_passage(row)


@router.get(
    "/passages",
    response_model=PassageListResponse,
    summary="List Activated Evidence Passages",
    description=(
        "Returns a paginated list of activated evidence passages. "
        "Preliminary corpus rows (activated=0) are excluded until Harshit's corpus activation gate is passed."
    ),
)
def list_passages(
    source_id: Optional[str] = Query(None, description="Optional parent source_id filter"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    conn: sqlite3.Connection = Depends(get_db),
) -> PassageListResponse:
    cur = conn.cursor()
    if source_id:
        cur.execute(
            f"SELECT count(*) FROM passages WHERE source_id = ? AND {_ACTIVATION_FILTER}",
            (source_id,)
        )
        total = cur.fetchone()[0]
        cur.execute(
            f"""
            SELECT passage_id, source_id, jurisdiction, authority, document_title, locator,
                   paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
            FROM passages
            WHERE source_id = ? AND {_ACTIVATION_FILTER}
            ORDER BY passage_id ASC
            LIMIT ? OFFSET ?
            """,
            (source_id, limit, offset)
        )
    else:
        cur.execute(f"SELECT count(*) FROM passages WHERE {_ACTIVATION_FILTER}")
        total = cur.fetchone()[0]
        cur.execute(
            f"""
            SELECT passage_id, source_id, jurisdiction, authority, document_title, locator,
                   paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
            FROM passages
            WHERE {_ACTIVATION_FILTER}
            ORDER BY passage_id ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )

    rows = cur.fetchall()
    return PassageListResponse(total=total, items=[_row_to_passage(r) for r in rows])
