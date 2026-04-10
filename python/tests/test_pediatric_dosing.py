"""
Test suite for pediatric dosing calculations.

Golden cases sourced from AAP Red Book 2024 and peer-reviewed literature.
Tolerance: ±0.5% relative error
"""

import pytest
import json
from pathlib import Path
from clinical_validators.pediatric import dosing, Indication


class TestAmoxicillinDosing:
    """Test amoxicillin weight-based dosing."""

    def test_mild_moderate_5kg_infant(self):
        """GOLDEN CASE: 5 kg infant, mild-moderate infection."""
        result = dosing.amoxicillin_dose(
            weight_kg=5.0,
            age_months=12,
            indication=Indication.MILD_MODERATE
        )
        assert result.dose_mg == 125  # 5 × 25 mg/kg
        assert result.dose_per_kg == 25
        assert result.total_daily_mg == 375  # 125 × 3 doses
        assert result.frequency == "every 8 hours"

    def test_otitis_media_12kg_toddler(self):
        """GOLDEN CASE: 12 kg toddler, acute otitis media (high-dose)."""
        result = dosing.amoxicillin_dose(
            weight_kg=12.0,
            age_months=24,
            indication=Indication.OTITIS_MEDIA
        )
        assert result.dose_mg == 540  # 12 × 45 mg/kg
        assert result.dose_per_kg == 45
        assert result.total_daily_mg == 1620  # 540 × 3 doses
        assert result.frequency == "every 8 hours"

    def test_strep_throat_18kg_child(self):
        """GOLDEN CASE: 18 kg school-age child, strep throat."""
        result = dosing.amoxicillin_dose(
            weight_kg=18.0,
            age_months=72,
            indication=Indication.STREP_THROAT
        )
        # 18 × 12.5 = 225, rounds to 225
        assert result.dose_mg == 225
        assert result.dose_per_kg == 12.5
        assert result.frequency == "every 8 hours"

    def test_severe_infection_25kg_preteen(self):
        """GOLDEN CASE: 25 kg preteen, severe infection."""
        result = dosing.amoxicillin_dose(
            weight_kg=25.0,
            age_months=96,
            indication=Indication.SEVERE
        )
        # 25 × 45 = 1125, but 1125 × 4 = 4500, which exceeds 4000 max
        # So dose is capped to 4000/4 = 1000 mg per dose
        assert result.dose_mg == 1000.0
        assert result.frequency == "every 6 hours"
        assert result.total_daily_mg == 4000  # Capped at max

    def test_invalid_weight_too_high(self):
        """Should reject weight > 50 kg."""
        with pytest.raises(ValueError, match="outside validated range"):
            dosing.amoxicillin_dose(weight_kg=51.0, age_months=120)

    def test_invalid_age_negative(self):
        """Should reject negative age."""
        with pytest.raises(ValueError, match="cannot be negative"):
            dosing.amoxicillin_dose(weight_kg=10.0, age_months=-1)


class TestGentamicinDosing:
    """Test gentamicin extended-interval dosing."""

    def test_6kg_infant_eid(self):
        """GOLDEN CASE: 6 kg infant, extended-interval dosing."""
        result = dosing.gentamicin_dose(
            weight_kg=6.5,
            age_months=4,
            indication=Indication.MILD_MODERATE
        )
        # 6.5 × 7.5 = 48.75, round to 50
        assert result.dose_mg == 50
        assert result.frequency == "once daily"
        assert result.interval_hours == 24

    def test_25kg_child_eid(self):
        """GOLDEN CASE: 25 kg child, extended-interval dosing (max applied)."""
        result = dosing.gentamicin_dose(
            weight_kg=25.0,
            age_months=96,
            indication=Indication.MILD_MODERATE
        )
        # 25 × 7.5 = 187.5, would be capped at 500 mg max
        assert result.dose_mg == 187.5
        assert result.frequency == "once daily"


class TestCefotaximeDosing:
    """Test cefotaxime dosing by indication."""

    def test_mild_moderate_15kg_child(self):
        """GOLDEN CASE: 15 kg child, mild-moderate infection."""
        result = dosing.cefotaxime_dose(
            weight_kg=15.0,
            age_months=36,
            indication=Indication.MILD_MODERATE
        )
        # 15 × 50 = 750
        assert result.dose_mg == 750
        assert result.frequency == "every 8 hours"
        assert result.dose_per_kg == 50

    def test_meningitis_8kg_infant(self):
        """GOLDEN CASE: 8 kg infant, bacterial meningitis (HIGH-DOSE)."""
        result = dosing.cefotaxime_dose(
            weight_kg=8.0,
            age_months=12,
            indication=Indication.MENINGITIS
        )
        # 8 × 50 = 400
        assert result.dose_mg == 400
        assert result.frequency == "every 4 hours"
        assert "meningitis" in result.notes.lower()

    def test_large_child_dose_capped(self):
        """Dose should be capped at 2000 mg per single dose."""
        result = dosing.cefotaxime_dose(
            weight_kg=50.0,
            age_months=144,
            indication=Indication.SEVERE
        )
        # 50 × 50 = 2500, but capped at 2000
        assert result.dose_mg == 2000


class TestGoldenCases:
    """Load and validate against golden cases JSON file."""

    @pytest.fixture(scope="module")
    def golden_cases(self):
        """Load golden cases from JSON."""
        cases_file = Path(__file__).parent.parent / "golden_cases" / "pediatric_golden_cases.json"
        with open(cases_file, 'r') as f:
            return json.load(f)

    def test_all_golden_cases_load(self, golden_cases):
        """Verify golden cases file loads and has expected structure."""
        assert "pediatric_dosing_golden_cases" in golden_cases
        assert len(golden_cases["pediatric_dosing_golden_cases"]) >= 8

    def test_amoxicillin_golden_case(self, golden_cases):
        """Test against AAP Red Book verified amoxicillin case."""
        cases = golden_cases["pediatric_dosing_golden_cases"]
        # Get a specific golden case (strep throat)
        strep_case = next(
            c for c in cases
            if c["drug"] == "Amoxicillin" and c["indication"] == "strep_throat"
        )

        weight = strep_case["inputs"]["weight_kg"]
        age = strep_case["inputs"]["age_months"]
        indication = Indication[strep_case["indication"].upper()]

        result = dosing.amoxicillin_dose(
            weight_kg=weight,
            age_months=age,
            indication=indication
        )

        expected_dose = strep_case["expected_output"]["dose_mg"]
        tolerance = strep_case["tolerance"]

        # Check within tolerance (±0.5%)
        rel_error = abs(result.dose_mg - expected_dose) / expected_dose
        assert rel_error <= tolerance, \
            f"Dose {result.dose_mg} exceeds tolerance {tolerance} vs expected {expected_dose}"
