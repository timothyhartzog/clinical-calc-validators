"""
Test neonatal growth and severity scoring against golden cases.
"""
import json
import pytest
from pathlib import Path

from clinical_validators.neonatal.fenton_growth import (
    fenton_weight_percentile,
    snap_ii_score,
)


@pytest.fixture
def neonatal_golden_cases():
    """Load neonatal golden cases from JSON."""
    cases_file = (
        Path(__file__).parent.parent
        / "golden_cases"
        / "neonatal_golden_cases.json"
    )
    with open(cases_file) as f:
        return json.load(f)


class TestFentonGrowth:
    """Test Fenton growth curve percentile calculations."""

    def test_fenton_32wk_normal(self, neonatal_golden_cases):
        """Test 32-week preterm infant at 50th percentile."""
        case = neonatal_golden_cases["neonatal_calculations"][0]
        assert case["id"] == "FENTON_WEIGHT_PRETERM_32WK_001"

        result = fenton_weight_percentile(
            weight_kg=case["inputs"]["weight_kg"],
            age_weeks=case["inputs"]["age_weeks"],
            sex=case["inputs"]["sex"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify percentile
        assert (
            abs(result.percentile - expected["percentile"])
            / expected["percentile"]
            < tolerance
        ), f"Percentile mismatch: {result.percentile} vs {expected['percentile']}"

        # Verify z-score is close to 0 for 50th percentile
        assert abs(result.z_score - expected["z_score"]) < 0.5

    def test_fenton_28wk_sga(self, neonatal_golden_cases):
        """Test 28-week extremely preterm infant with SGA."""
        case = neonatal_golden_cases["neonatal_calculations"][1]
        assert case["id"] == "FENTON_WEIGHT_PRETERM_28WK_SGA_001"

        result = fenton_weight_percentile(
            weight_kg=case["inputs"]["weight_kg"],
            age_weeks=case["inputs"]["age_weeks"],
            sex=case["inputs"]["sex"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify low percentile (SGA)
        assert (
            abs(result.percentile - expected["percentile"])
            / expected["percentile"]
            < tolerance
        )

        # Verify negative z-score for below average
        assert result.z_score < 0

    def test_fenton_35wk_late_preterm(self, neonatal_golden_cases):
        """Test 35-week late preterm infant."""
        case = neonatal_golden_cases["neonatal_calculations"][2]
        assert case["id"] == "FENTON_WEIGHT_LATE_PRETERM_35WK_001"

        result = fenton_weight_percentile(
            weight_kg=case["inputs"]["weight_kg"],
            age_weeks=case["inputs"]["age_weeks"],
            sex=case["inputs"]["sex"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Should be at 50th percentile
        assert (
            abs(result.percentile - expected["percentile"])
            / expected["percentile"]
            < tolerance
        )

    def test_fenton_40wk_term(self, neonatal_golden_cases):
        """Test term newborn at 40 weeks."""
        case = neonatal_golden_cases["neonatal_calculations"][3]
        assert case["id"] == "FENTON_WEIGHT_TERM_40WK_001"

        result = fenton_weight_percentile(
            weight_kg=case["inputs"]["weight_kg"],
            age_weeks=case["inputs"]["age_weeks"],
            sex=case["inputs"]["sex"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Should be at 50th percentile
        assert (
            abs(result.percentile - expected["percentile"])
            / expected["percentile"]
            < tolerance
        )

    def test_all_fenton_cases(self, neonatal_golden_cases):
        """Test all Fenton growth golden cases."""
        for case in neonatal_golden_cases["neonatal_calculations"]:
            if case["calculation_type"] != "fenton_weight_percentile":
                continue

            result = fenton_weight_percentile(
                weight_kg=case["inputs"]["weight_kg"],
                age_weeks=case["inputs"]["age_weeks"],
                sex=case["inputs"]["sex"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            # Verify percentile with tolerance
            assert (
                abs(result.percentile - expected["percentile"])
                / expected["percentile"]
                < tolerance
            ), f"Failed for case {case['id']}: {result.percentile} vs {expected['percentile']}"


class TestSnapIIScore:
    """Test SNAP-II severity scoring for neonatal mortality prediction."""

    def test_snap_ii_low_risk(self, neonatal_golden_cases):
        """Test stable preterm infant with low mortality risk."""
        case = neonatal_golden_cases["neonatal_calculations"][4]
        assert case["id"] == "SNAP_II_LOW_RISK_001"

        result = snap_ii_score(
            lowest_mean_bp=case["inputs"]["lowest_mean_bp"],
            lowest_temperature=case["inputs"]["lowest_temperature"],
            lowest_ph=case["inputs"]["lowest_ph"],
            lowest_pao2=case["inputs"]["lowest_pao2"],
            seizures=case["inputs"]["seizures"],
            urine_output=case["inputs"]["urine_output"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify score is low
        assert result.total_score <= 10

        # Verify mortality risk is low
        assert (
            abs(
                result.mortality_risk_percent - expected["mortality_risk_percent"]
            )
            / expected["mortality_risk_percent"]
            < tolerance
        )

    def test_snap_ii_high_risk(self, neonatal_golden_cases):
        """Test critically ill infant with high mortality risk."""
        case = neonatal_golden_cases["neonatal_calculations"][5]
        assert case["id"] == "SNAP_II_HIGH_RISK_001"

        result = snap_ii_score(
            lowest_mean_bp=case["inputs"]["lowest_mean_bp"],
            lowest_temperature=case["inputs"]["lowest_temperature"],
            lowest_ph=case["inputs"]["lowest_ph"],
            lowest_pao2=case["inputs"]["lowest_pao2"],
            seizures=case["inputs"]["seizures"],
            urine_output=case["inputs"]["urine_output"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify high mortality risk
        assert (
            abs(
                result.mortality_risk_percent - expected["mortality_risk_percent"]
            )
            / expected["mortality_risk_percent"]
            < tolerance
        )

    def test_snap_ii_moderate_risk(self, neonatal_golden_cases):
        """Test preterm infant with moderate severity."""
        case = neonatal_golden_cases["neonatal_calculations"][6]
        assert case["id"] == "SNAP_II_MODERATE_RISK_001"

        result = snap_ii_score(
            lowest_mean_bp=case["inputs"]["lowest_mean_bp"],
            lowest_temperature=case["inputs"]["lowest_temperature"],
            lowest_ph=case["inputs"]["lowest_ph"],
            lowest_pao2=case["inputs"]["lowest_pao2"],
            seizures=case["inputs"]["seizures"],
            urine_output=case["inputs"]["urine_output"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify moderate mortality risk
        assert (
            abs(
                result.mortality_risk_percent - expected["mortality_risk_percent"]
            )
            / expected["mortality_risk_percent"]
            < tolerance
        )

    def test_all_snap_ii_cases(self, neonatal_golden_cases):
        """Test all SNAP-II golden cases."""
        for case in neonatal_golden_cases["neonatal_calculations"]:
            if case["calculation_type"] != "snap_ii_score":
                continue

            result = snap_ii_score(
                lowest_mean_bp=case["inputs"]["lowest_mean_bp"],
                lowest_temperature=case["inputs"]["lowest_temperature"],
                lowest_ph=case["inputs"]["lowest_ph"],
                lowest_pao2=case["inputs"]["lowest_pao2"],
                seizures=case["inputs"]["seizures"],
                urine_output=case["inputs"]["urine_output"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            # Verify mortality risk with tolerance
            assert (
                abs(
                    result.mortality_risk_percent
                    - expected["mortality_risk_percent"]
                )
                / expected["mortality_risk_percent"]
                < tolerance
            ), f"Failed for case {case['id']}"
