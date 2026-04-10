"""
Test hemodynamic calculations against golden cases.
"""
import json
import pytest
from pathlib import Path

from clinical_validators.pediatric.hemodynamics import (
    mean_arterial_pressure,
    cardiac_output,
    cardiac_index,
    systemic_vascular_resistance,
    shock_index,
    body_surface_area,
    cerebral_perfusion_pressure,
)


@pytest.fixture
def hemodynamics_golden_cases():
    """Load hemodynamics golden cases from JSON."""
    cases_file = (
        Path(__file__).parent.parent
        / "golden_cases"
        / "hemodynamics_golden_cases.json"
    )
    with open(cases_file) as f:
        return json.load(f)


class TestMeanArterialPressure:
    """Test MAP calculations."""

    def test_map_normal_6yo(self, hemodynamics_golden_cases):
        """Test normal MAP in school-age child."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][0]
        assert case["id"] == "MAP_NORMAL_6YO_001"

        result = mean_arterial_pressure(
            systolic_bp=case["inputs"]["systolic_bp"],
            diastolic_bp=case["inputs"]["diastolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.mean_arterial_pressure - expected["mean_arterial_pressure"])
            / expected["mean_arterial_pressure"]
            < tolerance
        )
        assert result.interpretation == expected["interpretation"]

    def test_map_infant_low(self, hemodynamics_golden_cases):
        """Test MAP approaching shock in infant with severe dehydration."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][1]
        assert case["id"] == "MAP_INFANT_LOW_001"

        result = mean_arterial_pressure(
            systolic_bp=case["inputs"]["systolic_bp"],
            diastolic_bp=case["inputs"]["diastolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.interpretation == expected["interpretation"]

    def test_map_septic_shock(self, hemodynamics_golden_cases):
        """Test MAP in septic shock."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][2]
        assert case["id"] == "MAP_SEPTIC_SHOCK_001"

        result = mean_arterial_pressure(
            systolic_bp=case["inputs"]["systolic_bp"],
            diastolic_bp=case["inputs"]["diastolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.interpretation == "shock"

    def test_all_map_cases(self, hemodynamics_golden_cases):
        """Test all MAP golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "mean_arterial_pressure":
                continue

            result = mean_arterial_pressure(
                systolic_bp=case["inputs"]["systolic_bp"],
                diastolic_bp=case["inputs"]["diastolic_bp"],
                age_months=case["inputs"].get("age_months"),
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.mean_arterial_pressure - expected["mean_arterial_pressure"])
                / expected["mean_arterial_pressure"]
                < tolerance
            ), f"Failed for case {case['id']}"

    def test_invalid_map_inputs(self):
        """Test MAP error handling."""
        with pytest.raises(ValueError):
            mean_arterial_pressure(systolic_bp=-10, diastolic_bp=60)

        with pytest.raises(ValueError):
            mean_arterial_pressure(systolic_bp=50, diastolic_bp=80)  # SBP < DBP


class TestCardiacOutput:
    """Test cardiac output calculations."""

    def test_co_normal(self, hemodynamics_golden_cases):
        """Test normal CO."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][3]
        assert case["id"] == "CARDIAC_OUTPUT_NORMAL_001"

        result = cardiac_output(
            heart_rate=case["inputs"]["heart_rate"],
            stroke_volume_ml=case["inputs"]["stroke_volume_ml"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.cardiac_output_ml_min == expected["cardiac_output_ml_min"]

    def test_co_tachycardia(self, hemodynamics_golden_cases):
        """Test CO with compensatory tachycardia."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][4]
        assert case["id"] == "CARDIAC_OUTPUT_TACHYCARDIA_001"

        result = cardiac_output(
            heart_rate=case["inputs"]["heart_rate"],
            stroke_volume_ml=case["inputs"]["stroke_volume_ml"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.cardiac_output_ml_min == expected["cardiac_output_ml_min"]

    def test_all_co_cases(self, hemodynamics_golden_cases):
        """Test all CO golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "cardiac_output":
                continue

            result = cardiac_output(
                heart_rate=case["inputs"]["heart_rate"],
                stroke_volume_ml=case["inputs"]["stroke_volume_ml"],
                age_months=case["inputs"].get("age_months"),
            )

            expected = case["expected_output"]
            assert result.cardiac_output_ml_min == expected["cardiac_output_ml_min"]


class TestCardiacIndex:
    """Test cardiac index calculations."""

    def test_ci_normal(self, hemodynamics_golden_cases):
        """Test normal CI."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][5]
        assert case["id"] == "CARDIAC_INDEX_NORMAL_001"

        result = cardiac_index(
            cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
            body_surface_area_m2=case["inputs"]["body_surface_area_m2"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.cardiac_index_ml_min_m2 - expected["cardiac_index_ml_min_m2"])
            / expected["cardiac_index_ml_min_m2"]
            < tolerance
        )
        assert result.interpretation == expected["interpretation"]

    def test_ci_low(self, hemodynamics_golden_cases):
        """Test low CI in cardiogenic shock."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][6]
        assert case["id"] == "CARDIAC_INDEX_LOW_001"

        result = cardiac_index(
            cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
            body_surface_area_m2=case["inputs"]["body_surface_area_m2"],
        )

        expected = case["expected_output"]
        assert result.interpretation == "low"

    def test_all_ci_cases(self, hemodynamics_golden_cases):
        """Test all CI golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "cardiac_index":
                continue

            result = cardiac_index(
                cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
                body_surface_area_m2=case["inputs"]["body_surface_area_m2"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.cardiac_index_ml_min_m2 - expected["cardiac_index_ml_min_m2"])
                / expected["cardiac_index_ml_min_m2"]
                < tolerance
            ), f"Failed for case {case['id']}"


class TestSystemicVascularResistance:
    """Test SVR calculations."""

    def test_svr_normal(self, hemodynamics_golden_cases):
        """Test normal SVR."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][7]
        assert case["id"] == "SVR_NORMAL_001"

        result = systemic_vascular_resistance(
            mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
            central_venous_pressure=case["inputs"]["central_venous_pressure"],
            cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
            body_surface_area_m2=case["inputs"]["body_surface_area_m2"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.resistance_wood_units - expected["resistance_wood_units"])
            / expected["resistance_wood_units"]
            < tolerance
        )
        assert result.interpretation == expected["interpretation"]

    def test_svr_low_sepsis(self, hemodynamics_golden_cases):
        """Test low SVR in sepsis."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][8]
        assert case["id"] == "SVR_LOW_SEPSIS_001"

        result = systemic_vascular_resistance(
            mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
            central_venous_pressure=case["inputs"]["central_venous_pressure"],
            cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
            body_surface_area_m2=case["inputs"]["body_surface_area_m2"],
        )

        expected = case["expected_output"]
        assert "septic" in result.interpretation

    def test_all_svr_cases(self, hemodynamics_golden_cases):
        """Test all SVR golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "systemic_vascular_resistance":
                continue

            result = systemic_vascular_resistance(
                mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
                central_venous_pressure=case["inputs"]["central_venous_pressure"],
                cardiac_output_ml_min=case["inputs"]["cardiac_output_ml_min"],
                body_surface_area_m2=case["inputs"].get("body_surface_area_m2"),
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.resistance_wood_units - expected["resistance_wood_units"])
                / expected["resistance_wood_units"]
                < tolerance
            ), f"Failed for case {case['id']}"


class TestShockIndex:
    """Test shock index calculations."""

    def test_si_normal(self, hemodynamics_golden_cases):
        """Test normal SI."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][9]
        assert case["id"] == "SHOCK_INDEX_NORMAL_001"

        result = shock_index(
            heart_rate=case["inputs"]["heart_rate"],
            systolic_bp=case["inputs"]["systolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.shock_index - expected["shock_index"]) / expected["shock_index"]
            < tolerance
        )

    def test_si_uncompensated(self, hemodynamics_golden_cases):
        """Test SI in profound shock."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][10]
        assert case["id"] == "SHOCK_INDEX_UNCOMPENSATED_001"

        result = shock_index(
            heart_rate=case["inputs"]["heart_rate"],
            systolic_bp=case["inputs"]["systolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.interpretation == "profound"

    def test_all_si_cases(self, hemodynamics_golden_cases):
        """Test all shock index golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "shock_index":
                continue

            result = shock_index(
                heart_rate=case["inputs"]["heart_rate"],
                systolic_bp=case["inputs"]["systolic_bp"],
                age_months=case["inputs"].get("age_months"),
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.shock_index - expected["shock_index"])
                / expected["shock_index"]
                < tolerance
            ), f"Failed for case {case['id']}"


class TestBodySurfaceArea:
    """Test BSA calculations."""

    def test_bsa_mosteller_child(self, hemodynamics_golden_cases):
        """Test Mosteller BSA in school-age child."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][11]
        assert case["id"] == "BSA_MOSTELLER_001"

        result = body_surface_area(
            weight_kg=case["inputs"]["weight_kg"],
            height_cm=case["inputs"]["height_cm"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.bsa_m2 - expected["bsa_m2"]) / expected["bsa_m2"] < tolerance
        )

    def test_bsa_infant(self, hemodynamics_golden_cases):
        """Test BSA in infant."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][12]
        assert case["id"] == "BSA_INFANT_001"

        result = body_surface_area(
            weight_kg=case["inputs"]["weight_kg"],
            height_cm=case["inputs"]["height_cm"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        assert (
            abs(result.bsa_m2 - expected["bsa_m2"]) / expected["bsa_m2"] < tolerance
        )

    def test_all_bsa_cases(self, hemodynamics_golden_cases):
        """Test all BSA golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "body_surface_area":
                continue

            result = body_surface_area(
                weight_kg=case["inputs"]["weight_kg"],
                height_cm=case["inputs"].get("height_cm"),
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.bsa_m2 - expected["bsa_m2"]) / expected["bsa_m2"] < tolerance
            ), f"Failed for case {case['id']}"


class TestCerebralPerfusionPressure:
    """Test CPP calculations."""

    def test_cpp_normal(self, hemodynamics_golden_cases):
        """Test normal CPP."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][13]
        assert case["id"] == "CPP_NORMAL_001"

        result = cerebral_perfusion_pressure(
            mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
            intracranial_pressure=case["inputs"]["intracranial_pressure"],
        )

        expected = case["expected_output"]
        assert result.cerebral_perfusion_pressure == expected["cerebral_perfusion_pressure"]
        assert result.interpretation == expected["interpretation"]

    def test_cpp_inadequate(self, hemodynamics_golden_cases):
        """Test inadequate CPP in severe TBI."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][14]
        assert case["id"] == "CPP_INADEQUATE_001"

        result = cerebral_perfusion_pressure(
            mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
            intracranial_pressure=case["inputs"]["intracranial_pressure"],
        )

        expected = case["expected_output"]
        assert result.interpretation == "inadequate"

    def test_all_cpp_cases(self, hemodynamics_golden_cases):
        """Test all CPP golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            if case["calculation_type"] != "cerebral_perfusion_pressure":
                continue

            result = cerebral_perfusion_pressure(
                mean_arterial_pressure=case["inputs"]["mean_arterial_pressure"],
                intracranial_pressure=case["inputs"]["intracranial_pressure"],
            )

            expected = case["expected_output"]
            assert (
                result.cerebral_perfusion_pressure
                == expected["cerebral_perfusion_pressure"]
            ), f"Failed for case {case['id']}"
