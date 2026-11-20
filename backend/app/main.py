"""
Main FastAPI Application Entrypoint for IP-SAKTI Sahayak.
Backend service owned by Suresh (Phase 1 / Task Su-01).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import PROJECT_NAME, VERSION, CORS_ORIGINS
from .db.database import init_database, get_db_connection
from .db.init_db import seed_fixtures, seed_real_corpus_if_available
from .api.routes import (
    health_router,
    classify_router,
    answer_router,
    sources_router,
    referral_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle:
    Initializes SQLite tables and seeds baseline fixtures if needed.
    """
    init_database()
    conn = get_db_connection()
    try:
        # Check if sources table is empty; if so, seed fixtures
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM sources;")
        if cur.fetchone()[0] == 0:
            seed_fixtures(conn)
            seed_real_corpus_if_available(conn)
    finally:
        conn.close()
    yield


app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=(
        "IP-SAKTI Sahayak Backend API.\n\n"
        "Provides validated endpoints for formulation classification, evidence retrieval, "
        "source lookup, citation verification, and user referral export.\n\n"
        "**Phase 2 (Su-02)**: Real query engine integration via stable retrieval adapter."
    ),
    lifespan=lifespan,
)

# CORS middleware for Akshay's frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)
app.include_router(classify_router)
app.include_router(answer_router)
app.include_router(sources_router)
app.include_router(referral_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "service": PROJECT_NAME,
        "version": VERSION,
        "phase": "Su-02: Query Engine Integration",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
        "status": "operational",
    }
