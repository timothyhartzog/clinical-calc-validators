"""
Neonatal Growth Calculations - Fenton 2013

Growth charts for preterm and term infants.
Fenton curves are the standard for neonatal growth assessment.

References:
    - Fenton TR. A new growth chart for preterm infants.
      Arch Dis Child Fetal Neonatal Ed. 2013;98(5):F394-F398
    - Growth Charts: https://www.ajnr.org/content/fentongrowthchart
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class FentonGrowthResult:
    """Result of Fenton growth assessment."""
    metric: str  # "weight", "length", "head_circumference"
    value: float
    unit: str
    age_weeks: float  # gestational age in weeks (22-50)
    age_days: int
    sex: str  # "male", "female"

    percentile: float  # 3, 10, 25, 50, 75, 90, 97
    z_score: float
    interpretation: str

    source: str


def fenton_weight_percentile(weight_kg: float, age_weeks: float, sex: str) -> FentonGrowthResult:
    """
    Estimate weight percentile using Fenton 2013 curves.

    Fenton curves are for infants from 22-50 weeks postmenstrual age (PMA).
    PMA = gestational age + postnatal age

    Args:
        weight_kg: Weight in kilograms
        age_weeks: Postmenstrual age in weeks (22-50)
        sex: "male" or "female"

    Returns:
        FentonGrowthResult with percentile estimate

    Example:
        32-week preterm infant weighing 1.5 kg at birth
        age_weeks = 32
        weight_kg = 1.5

    Reference:
        Fenton TR. Arch Dis Child Fetal Neonatal Ed. 2013
    """

    if age_weeks < 22 or age_weeks > 50:
        raise ValueError("Postmenstrual age must be 22-50 weeks")

    if weight_kg <= 0:
        raise ValueError("Weight must be positive")

    # Simplified Fenton reference values (50th percentile approximations)
    # In practice, use official Fenton growth chart software or tables
    reference_weights = {
        "male": {
            24: 0.55, 26: 0.75, 28: 1.0, 30: 1.3, 32: 1.6,
            34: 2.0, 36: 2.4, 38: 2.8, 40: 3.3, 42: 3.8,
            44: 4.2, 46: 4.6, 48: 4.9, 50: 5.1
        },
        "female": {
            24: 0.52, 26: 0.70, 28: 0.95, 30: 1.25, 32: 1.55,
            34: 1.9, 36: 2.3, 38: 2.7, 40: 3.1, 42: 3.5,
            44: 3.9, 46: 4.3, 48: 4.6, 50: 4.8
        }
    }

    sex_lower = sex.lower()
    if sex_lower not in reference_weights:
        raise ValueError(f"Sex must be 'male' or 'female'")

    age_int = int(age_weeks)
    if age_int not in reference_weights[sex_lower]:
        # Interpolate between nearest weeks
        if age_int < 24:
            age_int = 24
        elif age_int > 50:
            age_int = 50
        else:
            # Find closest reference point
            available = sorted(reference_weights[sex_lower].keys())
            if age_int < 24:
                age_int = 24
            elif age_int > 50:
                age_int = 50
            else:
                # Use closest available
                age_int = min(available, key=lambda x: abs(x - age_int))

    reference = reference_weights[sex_lower].get(age_int, 2.5)

    # Simplified percentile calculation
    percentile = min(97, max(3, 50 + (weight_kg - reference) / reference * 40))

    # Z-score approximation
    z_score = (weight_kg - reference) / (reference * 0.15)

    # Interpretation
    if percentile >= 90:
        interpretation = "Above average growth"
    elif percentile >= 10:
        interpretation = "Normal growth"
    else:
        interpretation = "Growth restriction - assess for causes"

    return FentonGrowthResult(
        metric="weight",
        value=weight_kg,
        unit="kg",
        age_weeks=age_weeks,
        age_days=int(age_weeks * 7),
        sex=sex,
        percentile=percentile,
        z_score=z_score,
        interpretation=interpretation,
        source="Fenton TR. Arch Dis Child. 2013 (simplified approximation)"
    )


@dataclass
class SnapIIResult:
    """Result of SNAP-II score calculation."""
    total_score: int
    components: dict
    mortality_risk_percent: float
    interpretation: str


def snap_ii_score(
    lowest_mean_bp: int,
    lowest_temperature_c: float,
    lowest_ph: float,
    lowest_pao2: float,
    seizures: bool = False,
    urine_output_ml_kg_hr: float = 1.0
) -> SnapIIResult:
    """
    Calculate SNAP-II (Score for Neonatal Acute Physiology II).

    SNAP-II predicts mortality risk in critically ill neonates.
    Used in NICU for severity assessment and outcomes prediction.

    Components (each scored 0-100):
    - Mean arterial pressure (lowest in first 24 hours)
    - Temperature (lowest in first 24 hours)
    - pH (lowest in first 24 hours)
    - PaO2 (lowest in first 24 hours)
    - Seizures (yes/no)
    - Urine output

    Args:
        lowest_mean_bp: Lowest mean arterial pressure (mmHg)
        lowest_temperature_c: Lowest temperature (°C)
        lowest_ph: Lowest pH
        lowest_pao2: Lowest PaO2 on any FiO2
        seizures: Whether seizures occurred
        urine_output_ml_kg_hr: Urine output (mL/kg/hr)

    Returns:
        SnapIIResult with score and mortality risk

    Reference:
        Richardson DK et al. J Pediatr. 2001;138(5):644-649

    Clinical use:
        SNAP-II is used to:
        - Predict mortality risk
        - Risk-adjust outcomes
        - Compare NICU performance
    """

    # Scoring thresholds (simplified)
    bp_score = 0
    if lowest_mean_bp < 30:
        bp_score = 18
    elif lowest_mean_bp < 40:
        bp_score = 11
    elif lowest_mean_bp < 50:
        bp_score = 6
    elif lowest_mean_bp > 85:
        bp_score = 4

    temp_score = 0
    if lowest_temperature_c < 35:
        temp_score = 15
    elif lowest_temperature_c < 36:
        temp_score = 8
    elif lowest_temperature_c > 39.5:
        temp_score = 5

    ph_score = 0
    if lowest_ph < 7.0:
        ph_score = 32
    elif lowest_ph < 7.1:
        ph_score = 16
    elif lowest_ph < 7.2:
        ph_score = 8
    elif lowest_ph > 7.35:
        ph_score = 3

    pao2_score = 0
    if lowest_pao2 < 40:
        pao2_score = 22
    elif lowest_pao2 < 60:
        pao2_score = 16
    elif lowest_pao2 < 80:
        pao2_score = 6
    elif lowest_pao2 > 150:
        pao2_score = 2

    seizure_score = 12 if seizures else 0

    urine_score = 0
    if urine_output_ml_kg_hr < 0.5:
        urine_score = 10
    elif urine_output_ml_kg_hr < 1.0:
        urine_score = 5

    total_score = bp_score + temp_score + ph_score + pao2_score + seizure_score + urine_score

    # Mortality risk approximation (actual calculation uses LOGIT model)
    mortality_risk = min(99, max(1, 100 / (1 + 2.718 ** (3.8 - total_score * 0.08))))

    if mortality_risk < 10:
        interpretation = "Low mortality risk"
    elif mortality_risk < 30:
        interpretation = "Moderate mortality risk"
    else:
        interpretation = "High mortality risk - intensive monitoring"

    return SnapIIResult(
        total_score=total_score,
        components={
            "mean_bp": bp_score,
            "temperature": temp_score,
            "ph": ph_score,
            "pao2": pao2_score,
            "seizures": seizure_score,
            "urine_output": urine_score,
        },
        mortality_risk_percent=mortality_risk,
        interpretation=interpretation
    )
