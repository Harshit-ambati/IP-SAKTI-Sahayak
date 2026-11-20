"""
Tests for referral export endpoint (Task Su-01).
"""

from fastapi.testclient import TestClient


def test_referral_export_success(client: TestClient):
    payload = {
        "formulation_title": "Synthetic Triphala Extract with Excipients",
        "ingredients": ["Terminalia chebula", "Terminalia bellirica", "Modern Excipient X"],
        "intended_use": "medicinal",
        "claims_disease_treatment": True,
        "claims_disease_cure": True,
        "has_novel_ingredient": True,
        "standardized_fraction": False,
        "external_application_only": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/referral/export", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["packet_id"].startswith("REF-")
    assert "referral intake dossier" in data["query_summary"].lower()
    assert len(data["unresolved_issues"]) >= 2
    assert "disclaimer" in data
