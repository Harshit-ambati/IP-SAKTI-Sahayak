"""
Pytest configuration and fixtures for IP-SAKTI Sahayak backend tests.
Uses an isolated in-memory or temporary SQLite test database.
"""

import os
# Suppress LangChain / LangSmith background network tracing during tests
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TEST_TRACKING"] = "false"
os.environ["LANGCHAIN_CALLBACKS_BACKGROUND"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

import sys
import tempfile
from pathlib import Path
from typing import Generator
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app
from app.db.database import get_db, init_database, get_db_connection
from app.db.init_db import seed_fixtures


@pytest.fixture(scope="session")
def test_db_path() -> Generator[Path, None, None]:
    """
    Creates a temporary SQLite file for the test session.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        temp_path = Path(tf.name)
    
    # Initialize schema and load synthetic fixtures
    init_database(temp_path)
    conn = get_db_connection(temp_path)
    seed_fixtures(conn)
    conn.close()

    yield temp_path

    # Cleanup
    if temp_path.exists():
        try:
            temp_path.unlink()
        except Exception:
            pass


@pytest.fixture
def client(test_db_path: Path) -> Generator[TestClient, None, None]:
    """
    Provides a FastAPI TestClient configured to use the isolated test database.
    """
    def override_get_db():
        conn = get_db_connection(test_db_path)
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
