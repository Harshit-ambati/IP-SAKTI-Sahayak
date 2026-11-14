"""
Source and Passage lookup routes for IP-SAKTI Sahayak (Task Su-01).
Allows retrieving official source records and verified passages by citation ID.
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


@router.get(
    "/sources/{source_id}",
    response_model=SourceRecord,
    summary="Get Source Document by ID",
    description="Looks up an official or synthetic source record by its unique source_id.",
)
def get_source_by_id(
    source_id: str,
    conn: sqlite3.Connection = Depends(get_db),
) -> SourceRecord:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT source_id, topic, authority, title, official_url, format, role, priority, verification_status, review_note, is_synthetic
        FROM sources
        WHERE source_id = ?
        """,
        (source_id,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source record with ID '{source_id}' not found.",
        )

    return SourceRecord(
        source_id=row["source_id"],
        topic=row["topic"],
        authority=row["authority"],
        title=row["title"],
        official_url=row["official_url"],
        format=row["format"],
        role=row["role"],
        priority=row["priority"],
        verification_status=row["verification_status"],
        review_note=row["review_note"],
        is_synthetic=bool(row["is_synthetic"]),
    )


@router.get(
    "/sources",
    response_model=SourceListResponse,
    summary="List Source Documents",
    description="Returns a paginated list of registered official and synthetic source documents.",
)
def list_sources(
    topic: Optional[str] = Query(None, description="Optional topic filter"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    conn: sqlite3.Connection = Depends(get_db),
) -> SourceListResponse:
    cur = conn.cursor()
    if topic:
        cur.execute("SELECT count(*) FROM sources WHERE topic = ?", (topic,))
        total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT source_id, topic, authority, title, official_url, format, role, priority, verification_status, review_note, is_synthetic
            FROM sources
            WHERE topic = ?
            ORDER BY source_id ASC
            LIMIT ? OFFSET ?
            """,
            (topic, limit, offset)
        )
    else:
        cur.execute("SELECT count(*) FROM sources")
        total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT source_id, topic, authority, title, official_url, format, role, priority, verification_status, review_note, is_synthetic
            FROM sources
            ORDER BY source_id ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )

    rows = cur.fetchall()
    items = [
        SourceRecord(
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
        for r in rows
    ]
    return SourceListResponse(total=total, items=items)


@router.get(
    "/passages/{passage_id}",
    response_model=EvidencePassage,
    summary="Get Evidence Passage by ID",
    description="Looks up an authoritative provision passage excerpt by its passage_id.",
)
def get_passage_by_id(
    passage_id: str,
    conn: sqlite3.Connection = Depends(get_db),
) -> EvidencePassage:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
        FROM passages
        WHERE passage_id = ?
        """,
        (passage_id,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence passage with ID '{passage_id}' not found.",
        )

    return EvidencePassage(
        passage_id=row["passage_id"],
        source_id=row["source_id"],
        jurisdiction=row["jurisdiction"],
        authority=row["authority"],
        document_title=row["document_title"],
        locator=row["locator"],
        paraphrased_content=row["paraphrased_content"],
        source_url=row["source_url"],
        source_type=row["source_type"],
        review_status=row["review_status"],
        review_note=row["review_note"],
        is_synthetic=bool(row["is_synthetic"]),
    )


@router.get(
    "/passages",
    response_model=PassageListResponse,
    summary="List Evidence Passages",
    description="Returns a paginated list of indexed evidence passages.",
)
def list_passages(
    source_id: Optional[str] = Query(None, description="Optional parent source_id filter"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    conn: sqlite3.Connection = Depends(get_db),
) -> PassageListResponse:
    cur = conn.cursor()
    if source_id:
        cur.execute("SELECT count(*) FROM passages WHERE source_id = ?", (source_id,))
        total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
            FROM passages
            WHERE source_id = ?
            ORDER BY passage_id ASC
            LIMIT ? OFFSET ?
            """,
            (source_id, limit, offset)
        )
    else:
        cur.execute("SELECT count(*) FROM passages")
        total = cur.fetchone()[0]
        cur.execute(
            """
            SELECT passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic
            FROM passages
            ORDER BY passage_id ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )

    rows = cur.fetchall()
    items = [
        EvidencePassage(
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
        for r in rows
    ]
    return PassageListResponse(total=total, items=items)
