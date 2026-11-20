"""
Query engine adapters for IP-SAKTI Sahayak (Task Su-02).
Provides an abstract adapter interface and concrete SQLite FTS5 implementation
for evidence retrieval, answer synthesis, and safe abstention.
"""

from .query_adapter import (
    QueryEngineAdapter,
    SQLiteFTS5QueryAdapter,
    get_query_adapter,
)

__all__ = [
    "QueryEngineAdapter",
    "SQLiteFTS5QueryAdapter",
    "get_query_adapter",
]
