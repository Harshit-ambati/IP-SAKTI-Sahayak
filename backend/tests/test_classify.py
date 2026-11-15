"""
Tests for formulation intake classification endpoint (Task Su-01).
Updated after PR #3 review fixes.
"""

from fastapi.testclient import TestClient


def test_classify_classical_generic_success(client: TestClient):
    payload = {
        "formulation_title": "Synthetic Triphala Churna Sample",
        "ingredients": ["Terminalia chebula", "Terminalia bellirica", "Phyllanthus emblica"],
        "classical_text_reference": "Charaka Samhita",
        "processing_method": "Churna",
        "intended_use": "medicinal",
        "claims_disease_treatment": True,
        "claims_disease_cure": False,
        "has_novel_ingredient": False,
        "standardized_fraction": False,
        "external_application_only": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "classical_generic"
    assert data["is_synthetic_fixture"] is True
    assert "Section 3(a)" in data["governing_provisions"][0]
    assert data["referral_required"] is False
    assert "disclaimer" in data


def test_classify_ayurveda_aahara_success(client: TestClient):
    payload = {
        "formulation_title": "Synthetic Herbal Chyawanprash Food Bar",
        "ingredients": ["Emblica officinalis", "Sesamum indicum oil", "Honey"],
        "intended_use": "food_dietary",
        "claims_disease_treatment": False,
        "claims_disease_cure": False,
        "has_novel_ingredient": False,
        "standardized_fraction": False,
        "external_application_only": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "ayurveda_aahara"
    assert any("Regulation 2(b)" in p for p in data["governing_provisions"])


def test_classify_cosmetic_requires_both_flags(client: TestClient):
    """FIX-2a: cosmetic route requires BOTH external_application_only=True AND intended_use=cosmetic."""
    payload = {
        "formulation_title": "Synthetic Kumkumadi Skin Radiance Oil",
        "ingredients": ["Crocus sativus", "Sandalwood oil"],
        "intended_use": "cosmetic",
        "external_application_only": True,  # Both flags required
        "claims_disease_treatment": False,
        "claims_disease_cure": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "cosmetic"
    assert any("Section 3(aaa)" in p for p in data["governing_provisions"])


def test_classify_cosmetic_intended_use_without_external_flag_is_ambiguous(client: TestClient):
    """FIX-2a: cosmetic intended_use alone without external_application_only=True returns unknown_ambiguous."""
    payload = {
        "formulation_title": "Synthetic Ambiguous Cosmetic Cream",
        "ingredients": ["Herbal Base"],
        "intended_use": "cosmetic",
        "external_application_only": False,  # Missing; should trigger clarification
        "claims_disease_treatment": False,
        "claims_disease_cure": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "unknown_ambiguous"
    assert len(data["missing_facts"]) > 0
    assert "external" in data["missing_facts"][0].lower()


def test_classify_phytopharmaceutical_success(client: TestClient):
    payload = {
        "formulation_title": "Synthetic Purified Fraction Extract Q",
        "ingredients": ["Standardized fraction of Withania somnifera"],
        "intended_use": "medicinal",
        "standardized_fraction": True,
        "claims_disease_treatment": True,
        "claims_disease_cure": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "phytopharmaceutical"
    assert data["referral_required"] is True


def test_classify_contradictory_cosmetic_cure_claims(client: TestClient):
    """FIX-2a: external cosmetic + disease treatment/cure = unknown_ambiguous."""
    payload = {
        "formulation_title": "Synthetic Contradictory Cosmetic Cream",
        "ingredients": ["Herbal Base"],
        "intended_use": "cosmetic",
        "external_application_only": True,
        "claims_disease_treatment": True,  # Contradiction
        "claims_disease_cure": True,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "unknown_ambiguous"
    assert data["referral_required"] is True
    assert len(data["missing_facts"]) > 0


def test_classify_medicinal_without_classical_text_is_ambiguous(client: TestClient):
    """FIX-2b: medicinal without classical text reference returns unknown_ambiguous for clarification."""
    payload = {
        "formulation_title": "Synthetic Unnamed Herbal Medicine",
        "ingredients": ["Unknown Herb A", "Unknown Herb B"],
        "intended_use": "medicinal",
        "classical_text_reference": None,  # Missing — must clarify before assigning a route
        "claims_disease_treatment": True,
        "claims_disease_cure": False,
        "has_novel_ingredient": False,
        "standardized_fraction": False,
        "external_application_only": False,
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "unknown_ambiguous"
    assert len(data["missing_facts"]) > 0
    assert any("authoritative text" in f.lower() or "classical" in f.lower() for f in data["missing_facts"])


def test_classify_unspecified_intended_use_is_ambiguous(client: TestClient):
    """FIX-2c: unspecified intended_use always returns unknown_ambiguous."""
    payload = {
        "formulation_title": "Synthetic Unknown Product",
        "ingredients": ["Herb A"],
        "intended_use": "unspecified",
        "jurisdiction": "India",
        "language": "en"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provisional_route"] == "unknown_ambiguous"
    assert data["referral_required"] is True
    assert any("unspecified" in f or "intended_use" in f.lower() for f in data["missing_facts"])


def test_classify_malformed_missing_required_fields(client: TestClient):
    payload = {"intended_use": "medicinal"}  # Missing ingredients and title
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_classify_empty_ingredients_fails_validation(client: TestClient):
    payload = {
        "formulation_title": "Empty Ingredients Test",
        "ingredients": [],  # Violates min_length=1
        "intended_use": "medicinal"
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 422
