"""
Test fluids calculations against golden cases.
"""
import json
import pytest
from pathlib import Path

from clinical_validators.pediatric.fluids import (
    holliday_segar_maintenance,
    deficit_fluid_replacement,
)


@pytest.fixture
def fluids_golden_cases():
    """Load fluids golden cases from JSON."""
    cases_file = (
        Path(__file__).parent.parent
        / "golden_cases"
        / "fluids_golden_cases.json"
    )
    with open(cases_file) as f:
        return json.load(f)


class TestMaintenanceFluid:
    """Test maintenance fluid calculations."""

    def test_maintenance_infant_7kg(self, fluids_golden_cases):
        """Test 6-month-old 7kg infant maintenance."""
        case = fluids_golden_cases["fluid_calculations"][0]
        assert case["id"] == "MAINTENANCE_INFANT_7KG_001"

        result = holliday_segar_maintenance(
            weight_kg=case["inputs"]["weight_kg"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify daily rate
        assert (
            abs(result.total_daily_ml - expected["total_daily_ml"])
            / expected["total_daily_ml"]
            < tolerance
        )

        # Verify hourly rate
        assert (
            abs(result.hourly_rate_ml - expected["hourly_rate_ml"])
            / expected["hourly_rate_ml"]
            < tolerance
        )

        # Verify electrolytes
        assert (
            abs(result.sodium_meq_daily - expected["sodium_meq_daily"])
            / expected["sodium_meq_daily"]
            < tolerance
        )

    def test_maintenance_toddler_14kg(self, fluids_golden_cases):
        """Test 2-year-old 14kg toddler maintenance (two-phase formula)."""
        case = fluids_golden_cases["fluid_calculations"][1]
        assert case["id"] == "MAINTENANCE_TODDLER_14KG_001"

        result = holliday_segar_maintenance(
            weight_kg=case["inputs"]["weight_kg"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Should trigger two-phase formula
        assert result.total_daily_ml == expected["total_daily_ml"]

        # Verify phases are correct
        assert result.fluid_phase_1_kg == 100.0  # 10 * 100
        assert result.fluid_phase_2_kg == 50.0  # 4 * 50

    def test_maintenance_school_age_30kg(self, fluids_golden_cases):
        """Test 8-year-old 30kg school-age child (three-phase formula)."""
        case = fluids_golden_cases["fluid_calculations"][2]
        assert case["id"] == "MAINTENANCE_SCHOOL_AGE_30KG_001"

        result = holliday_segar_maintenance(
            weight_kg=case["inputs"]["weight_kg"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]

        # Should trigger three-phase formula
        assert result.total_daily_ml == expected["total_daily_ml"]

        # Verify all three phases
        assert result.fluid_phase_1_kg == 1000.0  # 10 * 100
        assert result.fluid_phase_2_kg == 500.0  # 10 * 50
        assert result.fluid_phase_3_kg == 200.0  # 10 * 20

    def test_maintenance_newborn_4kg(self, fluids_golden_cases):
        """Test 3-day-old 4kg newborn maintenance."""
        case = fluids_golden_cases["fluid_calculations"][3]
        assert case["id"] == "MAINTENANCE_NEWBORN_4KG_001"

        result = holliday_segar_maintenance(
            weight_kg=case["inputs"]["weight_kg"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.total_daily_ml == expected["total_daily_ml"]

    def test_all_maintenance_cases(self, fluids_golden_cases):
        """Test all maintenance fluid golden cases."""
        for case in fluids_golden_cases["fluid_calculations"]:
            if case["calculation_type"] != "holliday_segar_maintenance":
                continue

            result = holliday_segar_maintenance(
                weight_kg=case["inputs"]["weight_kg"],
                age_months=case["inputs"]["age_months"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            # Verify daily rate with tolerance
            assert (
                abs(result.total_daily_ml - expected["total_daily_ml"])
                / expected["total_daily_ml"]
                < tolerance
            ), f"Failed for case {case['id']}"


class TestDeficitFluid:
    """Test deficit fluid replacement calculations."""

    def test_deficit_mild_dehydration_10kg(self, fluids_golden_cases):
        """Test mild (5%) dehydration in 10kg child."""
        case = fluids_golden_cases["fluid_calculations"][4]
        assert case["id"] == "DEFICIT_MILD_DEHYDRATION_10KG_001"

        result = deficit_fluid_replacement(
            weight_kg=case["inputs"]["weight_kg"],
            dehydration_percent=case["inputs"]["dehydration_percent"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify total deficit
        assert (
            abs(result.deficit_total_ml - expected["deficit_total_ml"])
            / expected["deficit_total_ml"]
            < tolerance
        )

        # Verify phase 1 bolus
        assert (
            abs(result.phase_1_bolus_ml - expected["phase_1_bolus_ml"])
            / expected["phase_1_bolus_ml"]
            < tolerance
        )

    def test_deficit_moderate_dehydration_15kg(self, fluids_golden_cases):
        """Test moderate (10%) dehydration in 15kg child."""
        case = fluids_golden_cases["fluid_calculations"][5]
        assert case["id"] == "DEFICIT_MODERATE_DEHYDRATION_15KG_001"

        result = deficit_fluid_replacement(
            weight_kg=case["inputs"]["weight_kg"],
            dehydration_percent=case["inputs"]["dehydration_percent"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify total deficit
        assert (
            abs(result.deficit_total_ml - expected["deficit_total_ml"])
            / expected["deficit_total_ml"]
            < tolerance
        )

    def test_all_deficit_cases(self, fluids_golden_cases):
        """Test all deficit fluid golden cases."""
        for case in fluids_golden_cases["fluid_calculations"]:
            if case["calculation_type"] != "deficit_fluid_replacement":
                continue

            result = deficit_fluid_replacement(
                weight_kg=case["inputs"]["weight_kg"],
                dehydration_percent=case["inputs"]["dehydration_percent"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            # Verify deficit calculation with tolerance
            assert (
                abs(result.deficit_total_ml - expected["deficit_total_ml"])
                / expected["deficit_total_ml"]
                < tolerance
            ), f"Failed for case {case['id']}"
