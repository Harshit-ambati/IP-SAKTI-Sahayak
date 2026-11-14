"""
Health check endpoints for IP-SAKTI Sahayak.
Provides service liveness, database status, and FTS5 verification.
"""

from datetime import datetime, timezone
from fastapi import APIRouter
from ...config import PROJECT_NAME, VERSION
from ...db.database import check_db_health
from ...models.schemas import HealthStatus

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthStatus, summary="Basic service health check")
@router.get("/api/v1/health", response_model=HealthStatus, summary="API v1 service health check")
def get_health() -> HealthStatus:
    """
    Returns service health status, version, and SQLite database connectivity.
    """
    db_status = check_db_health()
    return HealthStatus(
        status="healthy" if db_status.get("status") == "connected" else "degraded",
        service=PROJECT_NAME,
        version=VERSION,
        database=db_status.get("status", "unknown"),
        fts5_supported=db_status.get("fts5_supported", False),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
