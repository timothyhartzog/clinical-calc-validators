"""
Golden case tests for pediatric toxicology assessment module.

Tests cover:
- Acetaminophen toxicity (Rumack-Matthew nomogram)
- Salicylate toxicity
- Iron toxicity
- Drug-induced hepatotoxicity
- Toxic ingestion risk assessment
"""

import json
from pathlib import Path

import pytest

from clinical_validators.pediatric.toxicology import (
    acetaminophen_toxicity_assessment,
    salicylate_toxicity_assessment,
    iron_toxicity_assessment,
    drug_induced_hepatotoxicity_assessment,
    toxic_ingestion_risk_assessment,
)


@pytest.fixture
def toxicology_golden_cases():
    """Load toxicology golden cases from JSON file."""
    cases_file = Path(__file__).parent.parent / "golden_cases" / "toxicology_golden_cases.json"
    with open(cases_file) as f:
        return json.load(f)


# =============================================================================
# ACETAMINOPHEN TOXICITY TESTS
# =============================================================================


class TestAcetaminophenToxicity:
    """Test acetaminophen toxicity assessment."""

    def test_acetaminophen_low_risk(self, toxicology_golden_cases):
        """GOLDEN CASE: Low-risk acetaminophen exposure."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "ACETAMINOPHEN_LOW_RISK_001"
        )
        result = acetaminophen_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.risk_zone == expected["risk_zone"]
        assert result.recommendation == expected["recommendation"]

    def test_acetaminophen_intermediate_risk(self, toxicology_golden_cases):
        """GOLDEN CASE: Intermediate-risk acetaminophen toxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "ACETAMINOPHEN_INTERMEDIATE_RISK_001"
        )
        result = acetaminophen_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.nac_loading_dose_mg_kg == expected["nac_loading_dose_mg_kg"]

    def test_acetaminophen_high_risk(self, toxicology_golden_cases):
        """GOLDEN CASE: High-risk acetaminophen toxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "ACETAMINOPHEN_HIGH_RISK_001"
        )
        result = acetaminophen_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.liver_function_risk == expected["liver_function_risk"]

    def test_acetaminophen_all_cases(self, toxicology_golden_cases):
        """Test all acetaminophen cases."""
        for case in toxicology_golden_cases["toxicology_golden_cases"]:
            if case.get("calculation_type") != "acetaminophen_toxicity_assessment":
                continue
            result = acetaminophen_toxicity_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.toxicity_category == expected["toxicity_category"], f"Failed for {case['id']}"
            assert result.risk_zone == expected["risk_zone"], f"Failed for {case['id']}"

    def test_acetaminophen_invalid_age(self):
        """Test validation of invalid age."""
        with pytest.raises(ValueError, match="Age must be 0-18"):
            acetaminophen_toxicity_assessment(
                age_years=20,
                weight_kg=50,
                plasma_concentration_mcg_ml=50,
                hours_post_ingestion=4,
            )


# =============================================================================
# SALICYLATE TOXICITY TESTS
# =============================================================================


class TestSalicylateToxicity:
    """Test salicylate toxicity assessment."""

    def test_salicylate_mild(self, toxicology_golden_cases):
        """GOLDEN CASE: Mild salicylate toxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "SALICYLATE_MILD_TOXICITY_001"
        )
        result = salicylate_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.acid_base_status == expected["acid_base_status"]

    def test_salicylate_severe(self, toxicology_golden_cases):
        """GOLDEN CASE: Severe salicylate toxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "SALICYLATE_SEVERE_TOXICITY_001"
        )
        result = salicylate_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.dialysis_indicated == expected["dialysis_indicated"]

    def test_salicylate_all_cases(self, toxicology_golden_cases):
        """Test all salicylate cases."""
        for case in toxicology_golden_cases["toxicology_golden_cases"]:
            if case.get("calculation_type") != "salicylate_toxicity_assessment":
                continue
            result = salicylate_toxicity_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.toxicity_category == expected["toxicity_category"], f"Failed for {case['id']}"
            assert result.toxicity_score == expected["toxicity_score"], f"Failed for {case['id']}"

    def test_salicylate_invalid_hours(self):
        """Test validation of invalid hours post-ingestion."""
        with pytest.raises(ValueError, match="Hours post-ingestion"):
            salicylate_toxicity_assessment(
                age_years=10,
                weight_kg=30,
                plasma_salicylate_mg_dl=50,
                hours_post_ingestion=100,
            )


# =============================================================================
# IRON TOXICITY TESTS
# =============================================================================


class TestIronToxicity:
    """Test iron toxicity assessment."""

    def test_iron_low_risk(self, toxicology_golden_cases):
        """GOLDEN CASE: Low-risk iron exposure."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "IRON_LOW_RISK_001"
        )
        result = iron_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.chelation_indicated == expected["chelation_indicated"]

    def test_iron_high_risk(self, toxicology_golden_cases):
        """GOLDEN CASE: High-risk iron toxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "IRON_HIGH_RISK_001"
        )
        result = iron_toxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_category == expected["toxicity_category"]
        assert result.chelation_indicated == expected["chelation_indicated"]
        assert result.deferoxamine_loading_dose_mg_kg == expected["deferoxamine_loading_dose_mg_kg"]

    def test_iron_all_cases(self, toxicology_golden_cases):
        """Test all iron cases."""
        for case in toxicology_golden_cases["toxicology_golden_cases"]:
            if case.get("calculation_type") != "iron_toxicity_assessment":
                continue
            result = iron_toxicity_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.toxicity_category == expected["toxicity_category"], f"Failed for {case['id']}"

    def test_iron_invalid_serum(self):
        """Test validation of negative serum iron."""
        with pytest.raises(ValueError, match="cannot be negative"):
            iron_toxicity_assessment(
                age_years=7,
                weight_kg=23,
                serum_iron_mcg_dl=-10,
                tibc_mcg_dl=350,
                hours_post_ingestion=2,
            )


# =============================================================================
# DRUG-INDUCED HEPATOTOXICITY TESTS
# =============================================================================


class TestDrugInducedHepatotoxicity:
    """Test drug-induced hepatotoxicity assessment."""

    def test_hepatotoxicity_no_injury(self, toxicology_golden_cases):
        """GOLDEN CASE: No drug-induced liver injury."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "HEPATOTOXICITY_NO_INJURY_001"
        )
        result = drug_induced_hepatotoxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_grade == expected["toxicity_grade"]
        assert result.risk_category == expected["risk_category"]

    def test_hepatotoxicity_moderate(self, toxicology_golden_cases):
        """GOLDEN CASE: Moderate drug-induced hepatotoxicity."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "HEPATOTOXICITY_MODERATE_INJURY_001"
        )
        result = drug_induced_hepatotoxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_grade == expected["toxicity_grade"]
        assert result.risk_category == expected["risk_category"]

    def test_hepatotoxicity_severe(self, toxicology_golden_cases):
        """GOLDEN CASE: Severe drug-induced liver injury."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "HEPATOTOXICITY_SEVERE_INJURY_001"
        )
        result = drug_induced_hepatotoxicity_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.toxicity_grade == expected["toxicity_grade"]
        assert result.liver_synthetic_function_impaired == expected["liver_synthetic_function_impaired"]

    def test_hepatotoxicity_all_cases(self, toxicology_golden_cases):
        """Test all hepatotoxicity cases."""
        for case in toxicology_golden_cases["toxicology_golden_cases"]:
            if case.get("calculation_type") != "drug_induced_hepatotoxicity_assessment":
                continue
            result = drug_induced_hepatotoxicity_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.toxicity_grade == expected["toxicity_grade"], f"Failed for {case['id']}"
            assert result.risk_category == expected["risk_category"], f"Failed for {case['id']}"

    def test_hepatotoxicity_invalid_alt(self):
        """Test validation of negative ALT."""
        with pytest.raises(ValueError, match="cannot be negative"):
            drug_induced_hepatotoxicity_assessment(
                age_years=10,
                weight_kg=30,
                alt_iu_l=-50,
                ast_iu_l=40,
                bilirubin_mg_dl=0.8,
            )


# =============================================================================
# TOXIC INGESTION RISK TESTS
# =============================================================================


class TestToxicIngestionRisk:
    """Test toxic ingestion risk assessment."""

    def test_acetaminophen_low_dose(self, toxicology_golden_cases):
        """GOLDEN CASE: Low-dose acetaminophen ingestion."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "TOXIC_INGESTION_ACETAMINOPHEN_LOW_DOSE_001"
        )
        result = toxic_ingestion_risk_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert result.antidote_available == expected["antidote_available"]

    def test_iron_high_dose(self, toxicology_golden_cases):
        """GOLDEN CASE: High-dose iron ingestion."""
        case = next(
            c for c in toxicology_golden_cases["toxicology_golden_cases"]
            if c["id"] == "TOXIC_INGESTION_IRON_HIGH_DOSE_001"
        )
        result = toxic_ingestion_risk_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert result.disposition == expected["disposition"]

    def test_toxic_ingestion_all_cases(self, toxicology_golden_cases):
        """Test all toxic ingestion cases."""
        for case in toxicology_golden_cases["toxicology_golden_cases"]:
            if case.get("calculation_type") != "toxic_ingestion_risk_assessment":
                continue
            result = toxic_ingestion_risk_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.risk_category == expected["risk_category"], f"Failed for {case['id']}"
            assert result.substance_type == expected["substance_type"], f"Failed for {case['id']}"

    def test_toxic_ingestion_invalid_age(self):
        """Test validation of invalid age."""
        with pytest.raises(ValueError, match="Age must be 0-18"):
            toxic_ingestion_risk_assessment(
                age_years=25,
                weight_kg=60,
                substance="acetaminophen",
                reported_dose_mg=5000,
            )
