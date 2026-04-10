"""
Test severity scores calculations against golden cases.
"""
import json
import pytest
from pathlib import Path

from clinical_validators.pediatric.scores import (
    apgar_score,
    news_pediatric,
)


@pytest.fixture
def scores_golden_cases():
    """Load scores golden cases from JSON."""
    cases_file = (
        Path(__file__).parent.parent
        / "golden_cases"
        / "scores_golden_cases.json"
    )
    with open(cases_file) as f:
        return json.load(f)


class TestApgarScore:
    """Test APGAR score calculations."""

    def test_apgar_1min_excellent(self, scores_golden_cases):
        """Test perfect 10-point 1-minute APGAR."""
        case = scores_golden_cases["score_calculations"][0]
        assert case["id"] == "APGAR_1MIN_EXCELLENT_001"

        result = apgar_score(
            appearance=case["inputs"]["appearance"],
            pulse=case["inputs"]["pulse"],
            grimace=case["inputs"]["grimace"],
            activity=case["inputs"]["activity"],
            respiration=case["inputs"]["respiration"],
            time_minutes=case["inputs"]["time_minutes"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.interpretation == expected["interpretation"]
        assert result.time_minutes == 1

    def test_apgar_1min_concerning(self, scores_golden_cases):
        """Test concerning 6-point 1-minute APGAR."""
        case = scores_golden_cases["score_calculations"][1]
        assert case["id"] == "APGAR_1MIN_CONCERNING_001"

        result = apgar_score(
            appearance=case["inputs"]["appearance"],
            pulse=case["inputs"]["pulse"],
            grimace=case["inputs"]["grimace"],
            activity=case["inputs"]["activity"],
            respiration=case["inputs"]["respiration"],
            time_minutes=case["inputs"]["time_minutes"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.interpretation == expected["interpretation"]

    def test_apgar_1min_severe(self, scores_golden_cases):
        """Test severe 0-point 1-minute APGAR."""
        case = scores_golden_cases["score_calculations"][2]
        assert case["id"] == "APGAR_1MIN_SEVERE_001"

        result = apgar_score(
            appearance=case["inputs"]["appearance"],
            pulse=case["inputs"]["pulse"],
            grimace=case["inputs"]["grimace"],
            activity=case["inputs"]["activity"],
            respiration=case["inputs"]["respiration"],
            time_minutes=case["inputs"]["time_minutes"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.interpretation == expected["interpretation"]

    def test_apgar_5min_recovery(self, scores_golden_cases):
        """Test 5-minute APGAR showing recovery."""
        case = scores_golden_cases["score_calculations"][3]
        assert case["id"] == "APGAR_5MIN_RECOVERY_001"

        result = apgar_score(
            appearance=case["inputs"]["appearance"],
            pulse=case["inputs"]["pulse"],
            grimace=case["inputs"]["grimace"],
            activity=case["inputs"]["activity"],
            respiration=case["inputs"]["respiration"],
            time_minutes=case["inputs"]["time_minutes"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.interpretation == expected["interpretation"]
        assert result.time_minutes == 5

    def test_all_apgar_cases(self, scores_golden_cases):
        """Test all APGAR score golden cases."""
        for case in scores_golden_cases["score_calculations"]:
            if case["calculation_type"] != "apgar_score":
                continue

            result = apgar_score(
                appearance=case["inputs"]["appearance"],
                pulse=case["inputs"]["pulse"],
                grimace=case["inputs"]["grimace"],
                activity=case["inputs"]["activity"],
                respiration=case["inputs"]["respiration"],
                time_minutes=case["inputs"]["time_minutes"],
            )

            expected = case["expected_output"]
            assert result.total_score == expected["total_score"], (
                f"Score mismatch for {case['id']}: "
                f"expected {expected['total_score']}, got {result.total_score}"
            )
            assert result.interpretation == expected["interpretation"], (
                f"Interpretation mismatch for {case['id']}"
            )


class TestNewsScore:
    """Test National Early Warning Score calculations."""

    def test_news_low_risk(self, scores_golden_cases):
        """Test stable child with low NEWS score."""
        case = scores_golden_cases["score_calculations"][4]
        assert case["id"] == "NEWS_LOW_RISK_001"

        result = news_pediatric(
            respiration_rate=case["inputs"]["respiration_rate"],
            oxygen_saturation=case["inputs"]["oxygen_saturation"],
            temperature=case["inputs"]["temperature"],
            systolic_bp=case["inputs"]["systolic_bp"],
            heart_rate=case["inputs"]["heart_rate"],
            consciousness=case["inputs"]["consciousness"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.risk_level == expected["risk_level"]

    def test_news_medium_risk(self, scores_golden_cases):
        """Test child with moderate vital sign abnormalities."""
        case = scores_golden_cases["score_calculations"][5]
        assert case["id"] == "NEWS_MEDIUM_RISK_001"

        result = news_pediatric(
            respiration_rate=case["inputs"]["respiration_rate"],
            oxygen_saturation=case["inputs"]["oxygen_saturation"],
            temperature=case["inputs"]["temperature"],
            systolic_bp=case["inputs"]["systolic_bp"],
            heart_rate=case["inputs"]["heart_rate"],
            consciousness=case["inputs"]["consciousness"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.risk_level == expected["risk_level"]

    def test_news_high_risk(self, scores_golden_cases):
        """Test critically ill child requiring escalation."""
        case = scores_golden_cases["score_calculations"][6]
        assert case["id"] == "NEWS_HIGH_RISK_001"

        result = news_pediatric(
            respiration_rate=case["inputs"]["respiration_rate"],
            oxygen_saturation=case["inputs"]["oxygen_saturation"],
            temperature=case["inputs"]["temperature"],
            systolic_bp=case["inputs"]["systolic_bp"],
            heart_rate=case["inputs"]["heart_rate"],
            consciousness=case["inputs"]["consciousness"],
        )

        expected = case["expected_output"]
        assert result.total_score == expected["total_score"]
        assert result.risk_level == expected["risk_level"]

    def test_all_news_cases(self, scores_golden_cases):
        """Test all NEWS score golden cases."""
        for case in scores_golden_cases["score_calculations"]:
            if case["calculation_type"] != "news_pediatric":
                continue

            result = news_pediatric(
                respiration_rate=case["inputs"]["respiration_rate"],
                oxygen_saturation=case["inputs"]["oxygen_saturation"],
                temperature=case["inputs"]["temperature"],
                systolic_bp=case["inputs"]["systolic_bp"],
                heart_rate=case["inputs"]["heart_rate"],
                consciousness=case["inputs"]["consciousness"],
            )

            expected = case["expected_output"]
            assert result.total_score == expected["total_score"], (
                f"Score mismatch for {case['id']}: "
                f"expected {expected['total_score']}, got {result.total_score}"
            )
            assert result.risk_level == expected["risk_level"], (
                f"Risk level mismatch for {case['id']}"
            )
