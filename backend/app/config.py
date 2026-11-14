import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DEFAULT_DB_PATH = BASE_DIR / "data" / "ipsakti_dev.db"
DB_PATH = Path(os.getenv("IPSAKTI_DB_PATH", str(DEFAULT_DB_PATH)))

# Service Metadata
API_V1_STR = "/api/v1"
PROJECT_NAME = "IP-SAKTI Sahayak API"
VERSION = "0.1.0-su01"

# Privacy & Storage Policy Defaults (Enforced by Master Plan & Module 04)
# Persistent user case storage is DISABLED by default.
ENABLE_PERSISTENT_CASE_STORAGE = os.getenv("ENABLE_PERSISTENT_CASE_STORAGE", "false").lower() == "true"
AUDIT_LOG_ENABLED = os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true"

# CORS origins for Akshay's frontend
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
