"""
Golden case tests for pediatric oncology assessment module.

Tests cover:
- Tumor risk stratification
- CTCAE toxicity scoring
- Cardiotoxicity risk assessment
- Hematologic recovery monitoring
- Neutropenia infection risk
"""

import json
from pathlib import Path

import pytest

from clinical_validators.pediatric.oncology import (
    tumor_risk_stratification,
    ctcae_toxicity_scoring,
    cardiotoxicity_risk_assessment,
    hematologic_recovery_assessment,
    neutropenia_infection_risk,
)


@pytest.fixture
def oncology_golden_cases():
    """Load oncology golden cases from JSON file."""
    cases_file = Path(__file__).parent.parent / "golden_cases" / "oncology_golden_cases.json"
    with open(cases_file) as f:
        return json.load(f)


# =============================================================================
# TUMOR RISK STRATIFICATION TESTS
# =============================================================================


class TestTumorRiskStratification:
    """Test tumor risk stratification."""

    def test_risk_stratification_low(self, oncology_golden_cases):
        """GOLDEN CASE: Low-risk lymphoma."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "RISK_STRATIFICATION_LOW_001"
        )
        result = tumor_risk_stratification(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_group == expected["risk_group"]
        assert result.risk_score == expected["risk_score"]
        assert result.recommended_intensity == expected["recommended_intensity"]

    def test_risk_stratification_intermediate(self, oncology_golden_cases):
        """GOLDEN CASE: Intermediate-risk leukemia."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "RISK_STRATIFICATION_INTERMEDIATE_001"
        )
        result = tumor_risk_stratification(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_group == expected["risk_group"]
        assert result.risk_score == expected["risk_score"]

    def test_risk_stratification_high(self, oncology_golden_cases):
        """GOLDEN CASE: High-risk neuroblastoma."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "RISK_STRATIFICATION_HIGH_001"
        )
        result = tumor_risk_stratification(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_group == expected["risk_group"]

    def test_risk_stratification_veryhigh(self, oncology_golden_cases):
        """GOLDEN CASE: Very high-risk Ph+ ALL."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "RISK_STRATIFICATION_VERYHIGH_001"
        )
        result = tumor_risk_stratification(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_group == expected["risk_group"]
        assert result.risk_score == expected["risk_score"]

    def test_risk_stratification_all_cases(self, oncology_golden_cases):
        """Test all risk stratification cases."""
        for case in oncology_golden_cases["oncology_golden_cases"]:
            if case.get("calculation_type") != "tumor_risk_stratification":
                continue
            result = tumor_risk_stratification(**case["inputs"])
            expected = case["expected_output"]
            assert result.risk_group == expected["risk_group"], f"Failed for {case['id']}"
            assert result.risk_score == expected["risk_score"], f"Failed for {case['id']}"

    def test_risk_stratification_invalid_age(self):
        """Test validation of invalid age."""
        with pytest.raises(ValueError, match="Age must be 0-18"):
            tumor_risk_stratification(
                age_years=25,
                tumor_type="leukemia",
                stage=1,
                grade=1,
                cytogenetics_risk="favorable",
                other_risk_factors=0,
            )


# =============================================================================
# CTCAE TOXICITY SCORING TESTS
# =============================================================================


class TestCTCAEToxicity:
    """Test CTCAE toxicity scoring."""

    def test_ctcae_no_toxicity(self, oncology_golden_cases):
        """GOLDEN CASE: No adverse events."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CTCAE_NOTOXICITY_001"
        )
        result = ctcae_toxicity_scoring(**case["inputs"])
        expected = case["expected_output"]
        assert result.overall_max_grade == expected["overall_max_grade"]
        assert result.hematologic_grade == expected["hematologic_grade"]

    def test_ctcae_grade2(self, oncology_golden_cases):
        """GOLDEN CASE: Grade 2 moderate toxicity."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CTCAE_GRADE2_001"
        )
        result = ctcae_toxicity_scoring(**case["inputs"])
        expected = case["expected_output"]
        assert result.overall_max_grade == expected["overall_max_grade"]

    def test_ctcae_grade3(self, oncology_golden_cases):
        """GOLDEN CASE: Grade 3 severe toxicity."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CTCAE_GRADE3_001"
        )
        result = ctcae_toxicity_scoring(**case["inputs"])
        expected = case["expected_output"]
        assert result.overall_max_grade == expected["overall_max_grade"]

    def test_ctcae_all_cases(self, oncology_golden_cases):
        """Test all CTCAE cases."""
        for case in oncology_golden_cases["oncology_golden_cases"]:
            if case.get("calculation_type") != "ctcae_toxicity_scoring":
                continue
            result = ctcae_toxicity_scoring(**case["inputs"])
            expected = case["expected_output"]
            assert result.overall_max_grade == expected["overall_max_grade"], f"Failed for {case['id']}"

    def test_ctcae_invalid_age(self):
        """Test validation of invalid age."""
        with pytest.raises(ValueError, match="Age must be 0-18"):
            ctcae_toxicity_scoring(
                age_years=20,
                chemotherapy_agents=["doxorubicin"],
                days_since_treatment=10,
                laboratory_values={},
                clinical_symptoms={},
            )


# =============================================================================
# CARDIOTOXICITY RISK TESTS
# =============================================================================


class TestCardiotoxicityRisk:
    """Test cardiotoxicity risk assessment."""

    def test_cardiotoxicity_low(self, oncology_golden_cases):
        """GOLDEN CASE: Low-risk cardiotoxicity."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CARDIOTOXICITY_LOW_001"
        )
        result = cardiotoxicity_risk_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert abs(result.estimated_toxicity_probability_percent - expected["estimated_toxicity_probability_percent"]) < 1.0

    def test_cardiotoxicity_intermediate(self, oncology_golden_cases):
        """GOLDEN CASE: Intermediate-risk with trastuzumab."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CARDIOTOXICITY_INTERMEDIATE_001"
        )
        result = cardiotoxicity_risk_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]

    def test_cardiotoxicity_high(self, oncology_golden_cases):
        """GOLDEN CASE: High-risk with previous toxicity."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "CARDIOTOXICITY_HIGH_001"
        )
        result = cardiotoxicity_risk_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert result.recommended_cardioprotection == expected["recommended_cardioprotection"]

    def test_cardiotoxicity_all_cases(self, oncology_golden_cases):
        """Test all cardiotoxicity cases."""
        for case in oncology_golden_cases["oncology_golden_cases"]:
            if case.get("calculation_type") != "cardiotoxicity_risk_assessment":
                continue
            result = cardiotoxicity_risk_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.risk_category == expected["risk_category"], f"Failed for {case['id']}"

    def test_cardiotoxicity_invalid_dose(self):
        """Test validation of invalid dose."""
        with pytest.raises(ValueError, match="Anthracycline dose"):
            cardiotoxicity_risk_assessment(
                age_years=10,
                cumulative_anthracycline_dose_mg_m2=600,
                trastuzumab_exposure_months=None,
                baseline_ejection_fraction_percent=60,
                baseline_shortening_fraction_percent=None,
                previous_cardiotoxicity=False,
                family_history_cardiomyopathy=False,
                other_cardiac_drugs=[],
            )


# =============================================================================
# HEMATOLOGIC RECOVERY TESTS
# =============================================================================


class TestHematologicRecovery:
    """Test hematologic recovery assessment."""

    def test_hematologic_recovery_nadir(self, oncology_golden_cases):
        """GOLDEN CASE: Expected nadir phase."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "HEMATOLOGIC_RECOVERY_NADIR_001"
        )
        result = hematologic_recovery_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.recovery_phase == expected["recovery_phase"]
        assert result.neutropenia_severity == expected["neutropenia_severity"]

    def test_hematologic_recovery_with_gcsf(self, oncology_golden_cases):
        """GOLDEN CASE: Recovery phase with G-CSF."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "HEMATOLOGIC_RECOVERY_WITH_GCSF_001"
        )
        result = hematologic_recovery_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.recovery_phase == expected["recovery_phase"]
        assert result.infection_risk_level == expected["infection_risk_level"]

    def test_hematologic_recovery_recovered(self, oncology_golden_cases):
        """GOLDEN CASE: Recovered state."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "HEMATOLOGIC_RECOVERY_RECOVERED_001"
        )
        result = hematologic_recovery_assessment(**case["inputs"])
        expected = case["expected_output"]
        assert result.recovery_phase == expected["recovery_phase"]
        assert result.estimated_recovery_days == expected["estimated_recovery_days"]

    def test_hematologic_recovery_all_cases(self, oncology_golden_cases):
        """Test all hematologic recovery cases."""
        for case in oncology_golden_cases["oncology_golden_cases"]:
            if case.get("calculation_type") != "hematologic_recovery_assessment":
                continue
            result = hematologic_recovery_assessment(**case["inputs"])
            expected = case["expected_output"]
            assert result.recovery_phase == expected["recovery_phase"], f"Failed for {case['id']}"

    def test_hematologic_recovery_invalid_days(self):
        """Test validation of invalid days."""
        with pytest.raises(ValueError, match="Days since chemotherapy"):
            hematologic_recovery_assessment(
                age_years=10,
                chemotherapy_regimen="standard",
                baseline_wbc_k_ul=5,
                baseline_platelets_k_ul=200,
                current_wbc_k_ul=1,
                current_platelets_k_ul=100,
                days_since_chemotherapy=-5,
                g_csf_support=False,
                infection_present=False,
            )


# =============================================================================
# NEUTROPENIA INFECTION RISK TESTS
# =============================================================================


class TestNeutropeniaInfectionRisk:
    """Test neutropenia infection risk."""

    def test_neutropenia_low_risk(self, oncology_golden_cases):
        """GOLDEN CASE: Low infection risk."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "NEUTROPENIA_LOW_RISK_001"
        )
        result = neutropenia_infection_risk(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert result.hospitalization_threshold_met == expected["hospitalization_threshold_met"]

    def test_neutropenia_moderate_risk(self, oncology_golden_cases):
        """GOLDEN CASE: Moderate infection risk."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "NEUTROPENIA_MODERATE_RISK_001"
        )
        result = neutropenia_infection_risk(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]

    def test_neutropenia_high_risk(self, oncology_golden_cases):
        """GOLDEN CASE: High infection risk with fever."""
        case = next(
            c for c in oncology_golden_cases["oncology_golden_cases"]
            if c["id"] == "NEUTROPENIA_HIGH_RISK_001"
        )
        result = neutropenia_infection_risk(**case["inputs"])
        expected = case["expected_output"]
        assert result.risk_category == expected["risk_category"]
        assert result.hospitalization_threshold_met == expected["hospitalization_threshold_met"]

    def test_neutropenia_all_cases(self, oncology_golden_cases):
        """Test all neutropenia cases."""
        for case in oncology_golden_cases["oncology_golden_cases"]:
            if case.get("calculation_type") != "neutropenia_infection_risk":
                continue
            result = neutropenia_infection_risk(**case["inputs"])
            expected = case["expected_output"]
            assert result.risk_category == expected["risk_category"], f"Failed for {case['id']}"

    def test_neutropenia_invalid_anc(self):
        """Test validation of invalid ANC."""
        with pytest.raises(ValueError, match="ANC must be"):
            neutropenia_infection_risk(
                age_years=10,
                absolute_neutrophil_count_k_ul=15,
                days_of_neutropenia=5,
                chemotherapy_intensity="standard",
                fever_present=False,
                mucositis_grade=0,
                indwelling_catheter=False,
                previous_infections=0,
                nutritional_status="well_nourished",
            )
