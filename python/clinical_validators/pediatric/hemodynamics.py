"""
Pediatric Hemodynamic Calculations

Cardiac output, vascular resistance, perfusion indices, and related
hemodynamic parameters for pediatric patients.

References:
    - American Heart Association. PALS Textbook. 2015.
    - Circulation. 2015;132(16_suppl_2):S444-S482
    - Hazinski MF, et al. Pediatric Advanced Life Support. 2015.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class MeanArterialPressureResult:
    """Result of mean arterial pressure calculation."""
    systolic_bp: float
    diastolic_bp: float
    mean_arterial_pressure: float
    interpretation: str  # "normal", "low", "high", "shock"
    age_months: int
    clinical_note: str


@dataclass
class CardiacOutputResult:
    """Result of cardiac output calculation."""
    heart_rate: float
    stroke_volume_ml: float
    cardiac_output_ml_min: float
    age_months: int
    clinical_note: str


@dataclass
class CardiacIndexResult:
    """Result of cardiac index calculation."""
    cardiac_output_ml_min: float
    body_surface_area_m2: float
    cardiac_index_ml_min_m2: float
    interpretation: str
    clinical_note: str


@dataclass
class VascularResistanceResult:
    """Result of vascular resistance calculation."""
    mean_arterial_pressure: float
    central_venous_pressure: float
    cardiac_output_ml_min: float
    resistance_mmhg_min_ml: float
    resistance_wood_units: float
    body_surface_area_m2: float
    indexed_resistance: float
    interpretation: str


@dataclass
class ShockIndexResult:
    """Result of shock index calculation."""
    heart_rate: float
    systolic_bp: float
    shock_index: float
    interpretation: str  # "normal", "compensated", "uncompensated", "profound"
    clinical_note: str


@dataclass
class BodySurfaceAreaResult:
    """Result of body surface area calculation."""
    weight_kg: float
    height_cm: float
    bsa_m2: float
    bsa_estimate: str  # calculation method used


@dataclass
class CerebralPerfusionPressureResult:
    """Result of cerebral perfusion pressure calculation."""
    mean_arterial_pressure: float
    intracranial_pressure: float
    cerebral_perfusion_pressure: float
    interpretation: str
    clinical_note: str


def mean_arterial_pressure(
    systolic_bp: float,
    diastolic_bp: float,
    age_months: int = None,
) -> MeanArterialPressureResult:
    """
    Calculate mean arterial pressure.

    Mean arterial pressure is the average pressure in arteries during one
    cardiac cycle. It's a better indicator of tissue perfusion than systolic
    or diastolic pressure alone.

    Formula:
        MAP = (SBP + 2×DBP) / 3

    Args:
        systolic_bp: Systolic blood pressure in mmHg (0-300)
        diastolic_bp: Diastolic blood pressure in mmHg (0-200)
        age_months: Age in months for age-appropriate interpretation

    Returns:
        MeanArterialPressureResult with calculated MAP and interpretation

    Raises:
        ValueError: If values out of range or SBP < DBP

    Example:
        >>> result = mean_arterial_pressure(120, 80, age_months=60)
        >>> result.mean_arterial_pressure
        93.33
        >>> result.interpretation
        'normal'

    Clinical Notes:
        - Normal MAP varies significantly by age
        - MAP <50 mmHg indicates inadequate tissue perfusion
        - Used to calculate cerebral perfusion pressure
        - Normal ranges (approximate):
          * Infants (0-12 mo): 50-70 mmHg
          * Toddlers (1-3 yr): 60-75 mmHg
          * School-age (6-12 yr): 65-85 mmHg
          * Adolescents (>12 yr): 70-95 mmHg
    """
    # Input validation
    if systolic_bp < 0 or systolic_bp > 300:
        raise ValueError(f"Systolic BP {systolic_bp} out of range (0-300)")
    if diastolic_bp < 0 or diastolic_bp > 200:
        raise ValueError(f"Diastolic BP {diastolic_bp} out of range (0-200)")
    if systolic_bp < diastolic_bp:
        raise ValueError("Systolic BP cannot be less than diastolic BP")

    # Calculate MAP
    map_value = (systolic_bp + 2 * diastolic_bp) / 3

    # Get age-appropriate normal range
    normal_min, normal_max = _get_normal_map_range(age_months)

    # Interpret
    if map_value < 50:
        interpretation = "shock"
        clinical_note = "CRITICAL: MAP <50 indicates inadequate perfusion"
    elif map_value < normal_min:
        interpretation = "low"
        clinical_note = f"Below normal for age ({normal_min}-{normal_max} mmHg)"
    elif map_value > normal_max:
        interpretation = "high"
        clinical_note = f"Above normal for age ({normal_min}-{normal_max} mmHg)"
    else:
        interpretation = "normal"
        clinical_note = f"Within normal range for age ({normal_min}-{normal_max} mmHg)"

    return MeanArterialPressureResult(
        systolic_bp=systolic_bp,
        diastolic_bp=diastolic_bp,
        mean_arterial_pressure=round(map_value, 2),
        interpretation=interpretation,
        age_months=age_months,
        clinical_note=clinical_note,
    )


def cardiac_output(
    heart_rate: float,
    stroke_volume_ml: float,
    age_months: int = None,
) -> CardiacOutputResult:
    """
    Calculate cardiac output.

    Cardiac output is the volume of blood pumped by the heart per minute.
    CO = HR × SV

    This is fundamental to understanding tissue perfusion and shock states.

    Args:
        heart_rate: Heart rate in beats per minute (0-300)
        stroke_volume_ml: Stroke volume in milliliters (0-150)
        age_months: Age in months for clinical context

    Returns:
        CardiacOutputResult with calculated CO and clinical note

    Raises:
        ValueError: If values out of range

    Example:
        >>> result = cardiac_output(100, 50, age_months=60)
        >>> result.cardiac_output_ml_min
        5000

    Clinical Notes:
        - Normal CO varies significantly by age and body size
        - Better indicator: Cardiac Index (CO/BSA)
        - Critical in sepsis, cardiogenic shock assessment
        - Stroke volume affected by: contractility, preload, afterload
    """
    if heart_rate < 0 or heart_rate > 300:
        raise ValueError(f"Heart rate {heart_rate} out of range (0-300)")
    if stroke_volume_ml < 0 or stroke_volume_ml > 150:
        raise ValueError(f"Stroke volume {stroke_volume_ml} out of range (0-150)")

    co_value = heart_rate * stroke_volume_ml

    return CardiacOutputResult(
        heart_rate=heart_rate,
        stroke_volume_ml=stroke_volume_ml,
        cardiac_output_ml_min=round(co_value, 2),
        age_months=age_months,
        clinical_note="Use Cardiac Index (CO/BSA) for age-adjusted interpretation",
    )


def cardiac_index(
    cardiac_output_ml_min: float,
    body_surface_area_m2: float,
) -> CardiacIndexResult:
    """
    Calculate cardiac index (CO indexed to body surface area).

    Cardiac Index = CO / BSA

    This normalizes cardiac output for body size, allowing age-appropriate
    interpretation across the pediatric spectrum.

    Args:
        cardiac_output_ml_min: Cardiac output in mL/min
        body_surface_area_m2: Body surface area in m²

    Returns:
        CardiacIndexResult with calculated CI and interpretation

    Raises:
        ValueError: If values out of range or BSA is zero

    Example:
        >>> result = cardiac_index(5000, 0.8)
        >>> result.cardiac_index_ml_min_m2
        6250.0

    Clinical Notes:
        - Normal CI across pediatric ages: 3.5-4.5 L/min/m²
        - CI <2.5 indicates reduced cardiac output (cardiogenic shock)
        - Much better than absolute CO for clinical decisions
        - Use with SVR for hemodynamic classification
    """
    if cardiac_output_ml_min < 0:
        raise ValueError(f"Cardiac output {cardiac_output_ml_min} cannot be negative")
    if body_surface_area_m2 <= 0:
        raise ValueError(f"BSA {body_surface_area_m2} must be positive")

    # CI in mL/min/m2, convert to L/min/m2 for clinical interpretation
    ci_value_l_min_m2 = (cardiac_output_ml_min / 1000) / body_surface_area_m2

    # Interpret CI (thresholds in L/min/m2)
    if ci_value_l_min_m2 < 2.5:
        interpretation = "low"
        note = "Reduced cardiac output - investigate cardiogenic shock"
    elif ci_value_l_min_m2 < 3.5:
        interpretation = "borderline"
        note = "At lower end of normal range - monitor closely"
    elif ci_value_l_min_m2 > 4.5:
        interpretation = "high"
        note = "Elevated CI - seen in sepsis, anemia, anxiety"
    else:
        interpretation = "normal"
        note = "Normal cardiac index for age"

    return CardiacIndexResult(
        cardiac_output_ml_min=cardiac_output_ml_min,
        body_surface_area_m2=body_surface_area_m2,
        cardiac_index_ml_min_m2=round(ci_value_l_min_m2, 2),
        interpretation=interpretation,
        clinical_note=note,
    )


def systemic_vascular_resistance(
    mean_arterial_pressure: float,
    central_venous_pressure: float,
    cardiac_output_ml_min: float,
    body_surface_area_m2: float = None,
) -> VascularResistanceResult:
    """
    Calculate systemic vascular resistance (SVR).

    SVR = (MAP - CVP) / CO × 80

    SVR reflects the resistance to flow in systemic vasculature. Low SVR
    (septic shock) or high SVR (cardiogenic shock) helps classify shock.

    Args:
        mean_arterial_pressure: MAP in mmHg
        central_venous_pressure: CVP in mmHg
        cardiac_output_ml_min: CO in mL/min
        body_surface_area_m2: BSA in m² (optional, for indexed calculation)

    Returns:
        VascularResistanceResult with SVR in Wood units and indexed form

    Raises:
        ValueError: If CO is zero or values invalid

    Example:
        >>> result = systemic_vascular_resistance(75, 5, 5000, 0.8)
        >>> result.resistance_mmhg_min_ml
        1120.0

    Clinical Notes:
        - Normal SVR: 15-20 Wood units
        - Low SVR (<10): Septic shock, anaphylaxis
        - High SVR (>20): Cardiogenic shock, vasoconstriction
        - SVR = (MAP-CVP)/CO × 80 in mmHg·min/mL
        - Indexed SVR = SVR × BSA (normal: 1200-1500 mmHg·min·m²/mL)
    """
    if cardiac_output_ml_min <= 0:
        raise ValueError(f"Cardiac output {cardiac_output_ml_min} must be positive")
    if mean_arterial_pressure <= central_venous_pressure:
        raise ValueError("MAP must be greater than CVP for positive SVR")

    # Calculate SVR in Wood units: (MAP - CVP) / CO(L/min)
    # CO is provided in mL/min, convert to L/min
    co_liters_per_min = cardiac_output_ml_min / 1000
    svr_wood = (mean_arterial_pressure - central_venous_pressure) / co_liters_per_min

    # Convert to mmHg·min/mL (1 Wood = 80 mmHg·min/mL)
    svr_mmhg = svr_wood * 80

    # Calculate indexed SVR if BSA provided
    if body_surface_area_m2 is not None and body_surface_area_m2 > 0:
        svr_indexed = svr_wood * body_surface_area_m2
    else:
        svr_indexed = None

    # Interpret
    if svr_wood < 10:
        interpretation = "low (septic shock)"
    elif svr_wood < 15:
        interpretation = "borderline low"
    elif svr_wood > 20:
        interpretation = "high (cardiogenic shock)"
    else:
        interpretation = "normal"

    return VascularResistanceResult(
        mean_arterial_pressure=mean_arterial_pressure,
        central_venous_pressure=central_venous_pressure,
        cardiac_output_ml_min=cardiac_output_ml_min,
        resistance_mmhg_min_ml=round(svr_mmhg, 2),
        resistance_wood_units=round(svr_wood, 2),
        body_surface_area_m2=body_surface_area_m2,
        indexed_resistance=round(svr_indexed, 2) if svr_indexed else None,
        interpretation=interpretation,
    )


def shock_index(
    heart_rate: float,
    systolic_bp: float,
    age_months: int = None,
) -> ShockIndexResult:
    """
    Calculate shock index (HR/SBP).

    SI = HR / SBP

    A simple bedside indicator of compensatory stress. Normal <0.5,
    values >0.9 indicate poor compensation (uncompensated shock).

    Args:
        heart_rate: Heart rate in bpm
        systolic_bp: Systolic blood pressure in mmHg
        age_months: Age in months for context

    Returns:
        ShockIndexResult with SI and clinical interpretation

    Example:
        >>> result = shock_index(120, 100, age_months=60)
        >>> result.shock_index
        1.2
        >>> result.interpretation
        'uncompensated'

    Clinical Notes:
        - SI <0.5: Normal
        - SI 0.5-0.9: Compensated shock
        - SI >0.9: Uncompensated shock
        - Very simple, useful at bedside
        - More useful in older children/adolescents
        - Limit: age-dependent HR/BP ranges affect interpretation
    """
    if systolic_bp <= 0:
        raise ValueError(f"Systolic BP {systolic_bp} must be positive")
    if heart_rate < 0:
        raise ValueError(f"Heart rate {heart_rate} cannot be negative")

    si_value = heart_rate / systolic_bp

    if si_value < 0.5:
        interpretation = "normal"
        note = "Normal compensatory response"
    elif si_value < 0.9:
        interpretation = "compensated"
        note = "Compensated shock - increasing tachycardia relative to BP"
    elif si_value < 1.5:
        interpretation = "uncompensated"
        note = "Uncompensated shock - severe tachycardia with hypotension"
    else:
        interpretation = "profound"
        note = "Profound shock - critical condition"

    return ShockIndexResult(
        heart_rate=heart_rate,
        systolic_bp=systolic_bp,
        shock_index=round(si_value, 2),
        interpretation=interpretation,
        clinical_note=note,
    )


def body_surface_area(
    weight_kg: float,
    height_cm: float = None,
) -> BodySurfaceAreaResult:
    """
    Calculate body surface area.

    BSA is used for many pediatric calculations (cardiac index, drug dosing,
    ventilator settings). Multiple formulas available; Mosteller is most common.

    Formulas:
        - Mosteller: √(height×weight/3600)
        - DuBois: (height^0.725 × weight^0.425) × 0.007184
        - Weight-only (simplified): √(weight/70) for rough estimate

    Args:
        weight_kg: Weight in kilograms (0.5-200)
        height_cm: Height in centimeters (optional)

    Returns:
        BodySurfaceAreaResult with BSA and formula used

    Raises:
        ValueError: If weight/height out of range

    Example:
        >>> result = body_surface_area(20, 115)
        >>> result.bsa_m2
        0.84

    Clinical Notes:
        - Mosteller formula recommended for pediatric use
        - Used for: CI, drug dosing, ventilator parameters
        - If height unknown, weight-only approximation available
        - Extreme values: preemies <0.3 m², obese adolescents >2.0 m²
    """
    if weight_kg < 0.5 or weight_kg > 200:
        raise ValueError(f"Weight {weight_kg} out of range (0.5-200 kg)")

    if height_cm is not None:
        if height_cm < 30 or height_cm > 220:
            raise ValueError(f"Height {height_cm} out of range (30-220 cm)")

        # Mosteller formula: √(height×weight/3600)
        bsa_value = (height_cm * weight_kg / 3600) ** 0.5
        method = "Mosteller (height+weight)"
    else:
        # Simplified weight-only approximation
        bsa_value = (weight_kg / 70) ** 0.5
        method = "Simplified (weight-only)"

    return BodySurfaceAreaResult(
        weight_kg=weight_kg,
        height_cm=height_cm,
        bsa_m2=round(bsa_value, 3),
        bsa_estimate=method,
    )


def cerebral_perfusion_pressure(
    mean_arterial_pressure: float,
    intracranial_pressure: float,
) -> CerebralPerfusionPressureResult:
    """
    Calculate cerebral perfusion pressure.

    CPP = MAP - ICP

    CPP reflects the pressure gradient driving blood flow to the brain.
    Critical in traumatic brain injury and other intracranial emergencies.

    Args:
        mean_arterial_pressure: Mean arterial pressure in mmHg
        intracranial_pressure: Intracranial pressure in mmHg

    Returns:
        CerebralPerfusionPressureResult with CPP and interpretation

    Example:
        >>> result = cerebral_perfusion_pressure(80, 15)
        >>> result.cerebral_perfusion_pressure
        65

    Clinical Notes:
        - Normal ICP: 5-15 mmHg (child)
        - Normal CPP: 50-70 mmHg (child)
        - CPP <40 mmHg: Inadequate cerebral blood flow
        - CPP >100 mmHg: Risk of cerebral edema
        - Used in TBI, post-resuscitation management
        - Maintains CPP >50 is primary goal in severe TBI
    """
    if intracranial_pressure < 0:
        raise ValueError(f"ICP {intracranial_pressure} cannot be negative")

    cpp_value = mean_arterial_pressure - intracranial_pressure

    if cpp_value < 40:
        interpretation = "inadequate"
        note = "CPP <40: Inadequate cerebral perfusion - urgent intervention needed"
    elif cpp_value < 50:
        interpretation = "low"
        note = "CPP <50: Below optimal range"
    elif cpp_value > 100:
        interpretation = "high"
        note = "CPP >100: Risk of increased ICP/cerebral edema"
    else:
        interpretation = "normal"
        note = "CPP 50-70: Optimal cerebral perfusion"

    return CerebralPerfusionPressureResult(
        mean_arterial_pressure=mean_arterial_pressure,
        intracranial_pressure=intracranial_pressure,
        cerebral_perfusion_pressure=cpp_value,
        interpretation=interpretation,
        clinical_note=note,
    )


# Helper functions

def _get_normal_map_range(age_months: int) -> tuple[float, float]:
    """Get age-appropriate normal MAP range in mmHg."""
    if age_months is None:
        return (65, 85)  # Default for older children

    if age_months < 12:
        return (50, 70)  # Infants
    elif age_months < 36:
        return (60, 75)  # Toddlers
    elif age_months < 144:
        return (65, 85)  # School-age (6-12 years)
    else:
        return (70, 95)  # Adolescents (>12 years)
