"""
Pediatric Growth Calculations

CDC growth chart percentiles and z-scores for children 2-19 years.
References:
    - CDC Growth Charts: https://www.cdc.gov/growthcharts/
    - Kuczmarski et al. Vital Health Stat 11. 2002
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GrowthPercentile:
    """Result of a growth percentile calculation."""
    metric: str  # "height", "weight", "bmi"
    value: float
    unit: str
    age_years: float
    age_months: int
    sex: str  # "male", "female"
    percentile: float  # 0-100
    z_score: float
    interpretation: str  # "underweight", "normal", "overweight", "obese"
    source: str


def bmi_from_weight_height(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI from weight and height.

    BMI = weight_kg / (height_m)^2
    """
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Weight and height must be positive")

    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)


def weight_percentile_2_19y(weight_kg: float, age_years: float, sex: str) -> GrowthPercentile:
    """
    Estimate weight percentile for children 2-19 years using CDC data.

    Uses simplified LMS method (lambda-mu-sigma) approximation.
    See: Kuczmarski et al. 2002

    Args:
        weight_kg: Weight in kilograms
        age_years: Age in years (2-19)
        sex: "male" or "female"

    Returns:
        GrowthPercentile with estimated percentile rank

    Note:
        This is a simplified approximation. For clinical use,
        refer to official CDC growth charts or specialized software.
    """

    if age_years < 2 or age_years > 19:
        raise ValueError("Age must be between 2-19 years")

    if weight_kg <= 0:
        raise ValueError("Weight must be positive")

    # Simplified percentile lookup (actual CDC uses LMS tables)
    # These are approximate reference values for 50th percentile
    reference_weights = {
        "male": {
            2: 12.5, 3: 14.5, 4: 16.5, 5: 18.5, 6: 20.5,
            7: 23, 8: 25.5, 9: 28.5, 10: 31.5, 11: 34.5,
            12: 37.5, 13: 40.5, 14: 44, 15: 47.5, 16: 50.5,
            17: 52.5, 18: 53.5, 19: 54
        },
        "female": {
            2: 12, 3: 14, 4: 16, 5: 17.5, 6: 19.5,
            7: 22, 8: 24.5, 9: 27, 10: 30.5, 11: 33.5,
            12: 36.5, 13: 40, 14: 42, 15: 43.5, 16: 44.5,
            17: 45, 18: 45, 19: 45
        }
    }

    sex_lower = sex.lower()
    if sex_lower not in reference_weights:
        raise ValueError(f"Sex must be 'male' or 'female', got '{sex}'")

    age_int = int(age_years)
    if age_int not in reference_weights[sex_lower]:
        age_int = 10 if age_int < 10 else 18

    reference = reference_weights[sex_lower].get(age_int, 25)

    # Simplified percentile calculation
    # In reality, this would use LMS transformation
    percentile = min(99, max(1, 50 + (weight_kg - reference) / reference * 25))
    z_score = (weight_kg - reference) / (reference * 0.15)

    # Interpret percentile
    if percentile < 5:
        interpretation = "underweight"
    elif percentile < 85:
        interpretation = "normal"
    elif percentile < 95:
        interpretation = "overweight"
    else:
        interpretation = "obese"

    return GrowthPercentile(
        metric="weight",
        value=weight_kg,
        unit="kg",
        age_years=age_years,
        age_months=int(age_years * 12),
        sex=sex,
        percentile=percentile,
        z_score=z_score,
        interpretation=interpretation,
        source="CDC Growth Charts (simplified approximation)"
    )


def bmi_percentile_2_19y(bmi: float, age_years: float, sex: str) -> GrowthPercentile:
    """
    Estimate BMI percentile for children 2-19 years using CDC data.

    Categories:
    - Underweight: <5th percentile
    - Healthy weight: 5th-<85th percentile
    - Overweight: 85th-<95th percentile
    - Obese: ≥95th percentile
    """

    if age_years < 2 or age_years > 19:
        raise ValueError("Age must be between 2-19 years")

    if bmi <= 0:
        raise ValueError("BMI must be positive")

    # Simplified BMI reference values (50th percentile)
    reference_bmi = {
        "male": {
            2: 16.3, 3: 15.9, 4: 15.6, 5: 15.3, 6: 15.2,
            7: 15.2, 8: 15.4, 9: 15.7, 10: 16.2, 11: 16.8,
            12: 17.5, 13: 18.2, 14: 19, 15: 19.8, 16: 20.5,
            17: 21, 18: 21.5, 19: 22
        },
        "female": {
            2: 16.2, 3: 15.7, 4: 15.4, 5: 15.1, 6: 15,
            7: 15, 8: 15.2, 9: 15.6, 10: 16.2, 11: 16.9,
            12: 17.6, 13: 18.3, 14: 18.9, 15: 19.4, 16: 19.7,
            17: 20, 18: 20.1, 19: 20.2
        }
    }

    sex_lower = sex.lower()
    if sex_lower not in reference_bmi:
        raise ValueError(f"Sex must be 'male' or 'female', got '{sex}'")

    age_int = int(age_years)
    reference = reference_bmi[sex_lower].get(age_int, 18)

    # Simplified percentile
    percentile = min(99, max(1, 50 + (bmi - reference) / reference * 30))
    z_score = (bmi - reference) / (reference * 0.12)

    # Categorize
    if percentile < 5:
        interpretation = "underweight"
    elif percentile < 85:
        interpretation = "normal"
    elif percentile < 95:
        interpretation = "overweight"
    else:
        interpretation = "obese"

    return GrowthPercentile(
        metric="bmi",
        value=bmi,
        unit="kg/m²",
        age_years=age_years,
        age_months=int(age_years * 12),
        sex=sex,
        percentile=percentile,
        z_score=z_score,
        interpretation=interpretation,
        source="CDC Growth Charts (simplified approximation)"
    )
