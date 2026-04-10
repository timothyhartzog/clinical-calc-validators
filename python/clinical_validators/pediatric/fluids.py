"""
Pediatric Fluid and Electrolyte Calculations

Maintenance fluid requirements, deficit replacement, and electrolyte dosing.

References:
    - Holliday MA, Segar WE. The maintenance need for water in parenteral fluid therapy.
      Pediatrics. 1957
    - AAP Textbook of Pediatric Advanced Life Support. 2016
    - Lexi-Drugs pediatric dosing
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MaintenanceFluidResult:
    """Result of maintenance fluid calculation."""
    weight_kg: float
    age_months: int

    # Daily requirements
    total_daily_ml: float
    hourly_rate_ml: float

    # Breakdown
    fluid_phase_1_kg: float  # ml/kg for first 10 kg
    fluid_phase_2_kg: float  # ml/kg for kg 10-20
    fluid_phase_3_kg: float  # ml/kg for kg >20

    # Electrolytes
    sodium_meq_daily: float
    potassium_meq_daily: float
    chloride_meq_daily: float

    method: str
    source: str


def holliday_segar_maintenance(weight_kg: float, age_months: int) -> MaintenanceFluidResult:
    """
    Calculate pediatric maintenance fluid requirements using Holliday-Segar formula.

    This is the standard formula for calculating daily maintenance water and
    electrolyte requirements in children.

    Formula:
        First 10 kg: 100 mL/kg/day
        Next 10 kg (11-20): 50 mL/kg/day
        Each kg >20: 20 mL/kg/day

    Args:
        weight_kg: Patient weight in kilograms
        age_months: Patient age in months

    Returns:
        MaintenanceFluidResult with daily and hourly rates

    Clinical pearls:
        - Add 10-15 mL/kg for each 1°C of fever above 38.5°C
        - Adjust for GI losses (vomiting, diarrhea)
        - Adjust for increased metabolic rate
        - Monitor urine output (goal: 0.5-1 mL/kg/hr)

    Example:
        - 10 kg child: 100 × 10 = 1000 mL/day (100 mL/kg)
        - 20 kg child: (100 × 10) + (50 × 10) = 1500 mL/day (75 mL/kg average)
        - 30 kg child: (100 × 10) + (50 × 10) + (20 × 10) = 1700 mL/day

    References:
        Holliday MA, Segar WE. Pediatrics. 1957;19(5):823-832
        https://doi.org/10.1542/peds.19.5.823
    """

    if weight_kg <= 0:
        raise ValueError("Weight must be positive")

    if age_months < 0:
        raise ValueError("Age cannot be negative")

    # Calculate fluid requirements by weight
    total_daily_ml = 0.0

    if weight_kg <= 10:
        # First 10 kg: 100 mL/kg/day
        fluid_phase_1_kg = 100
        fluid_phase_2_kg = 0
        fluid_phase_3_kg = 0
        total_daily_ml = weight_kg * 100

    elif weight_kg <= 20:
        # First 10 kg + next up to 10 kg
        fluid_phase_1_kg = 100
        fluid_phase_2_kg = 50
        fluid_phase_3_kg = 0
        total_daily_ml = (10 * 100) + ((weight_kg - 10) * 50)

    else:
        # First 10 kg + second 10 kg + remaining
        fluid_phase_1_kg = 100
        fluid_phase_2_kg = 50
        fluid_phase_3_kg = 20
        total_daily_ml = (10 * 100) + (10 * 50) + ((weight_kg - 20) * 20)

    # Hourly rate (24-hour infusion)
    hourly_rate_ml = total_daily_ml / 24.0

    # Electrolyte requirements
    # Standard: 1 mEq Na+/mL maintenance fluid, 1 mEq K+/mL maintenance fluid
    # Typical fluids: 0.9% NaCl + 20 mEq KCl in 1 liter D5 1/2 NS
    sodium_meq_daily = total_daily_ml * 0.001 * 1000 / 1000  # ~1 mEq per 1 mL
    potassium_meq_daily = total_daily_ml * 0.001 * 1000 / 1000  # ~1 mEq per 1 mL
    chloride_meq_daily = sodium_meq_daily  # Matches sodium

    # More practical: typical maintenance IV fluids contain
    # D5 1/2 NS with 20 mEq/L KCl
    sodium_meq_daily = (total_daily_ml / 1000) * 77  # 0.9% saline = 154 mEq/L; 1/2 NS = 77 mEq/L
    potassium_meq_daily = (total_daily_ml / 1000) * 20  # 20 mEq/L KCl
    chloride_meq_daily = (total_daily_ml / 1000) * 77

    return MaintenanceFluidResult(
        weight_kg=weight_kg,
        age_months=age_months,
        total_daily_ml=total_daily_ml,
        hourly_rate_ml=hourly_rate_ml,
        fluid_phase_1_kg=fluid_phase_1_kg,
        fluid_phase_2_kg=fluid_phase_2_kg,
        fluid_phase_3_kg=fluid_phase_3_kg,
        sodium_meq_daily=sodium_meq_daily,
        potassium_meq_daily=potassium_meq_daily,
        chloride_meq_daily=chloride_meq_daily,
        method="Holliday-Segar",
        source="Holliday MA, Segar WE. Pediatrics. 1957"
    )


def deficit_fluid_replacement(
    weight_kg: float,
    dehydration_percent: float,
    fluid_type: str = "isotonic"
) -> dict:
    """
    Calculate fluid deficit replacement for dehydrated child.

    Args:
        weight_kg: Patient weight in kilograms
        dehydration_percent: Percent dehydration (3-5%, 6-9%, 10%+)
        fluid_type: "isotonic" (most common), "hypotonic", "hypertonic"

    Returns:
        Dictionary with:
        - deficit_ml: Total deficit to replace
        - phase_1_ml: Rapid rehydration bolus (usually 20 mL/kg)
        - phase_2_ml: Remaining deficit over 2-4 hours
        - electrolyte_replacement: Salt requirements

    Example:
        10 kg child, 8% dehydration (mild-moderate)
        Deficit = 10 kg × 8% = 800 mL
        - Bolus: 200 mL (20 mL/kg) over 15-30 min
        - Remaining: 600 mL over 2-4 hours

    References:
        AAP Textbook of Pediatric Advanced Life Support
    """

    if weight_kg <= 0:
        raise ValueError("Weight must be positive")

    if dehydration_percent <= 0 or dehydration_percent > 15:
        raise ValueError("Dehydration percent should be 1-15%")

    # Calculate deficit
    deficit_ml = weight_kg * dehydration_percent * 10  # kg × % × 10 = mL

    # Phase 1: Rapid bolus (20 mL/kg IV over 15-30 min)
    phase_1_ml = weight_kg * 20
    phase_1_ml = min(phase_1_ml, deficit_ml)  # Can't exceed total deficit

    # Phase 2: Remaining deficit over 2-4 hours
    phase_2_ml = deficit_ml - phase_1_ml

    # Electrolyte replacement depends on fluid type
    if fluid_type == "isotonic":
        # Use 0.9% saline (isotonic)
        # Typical replacement: 0.9% NaCl (154 mEq/L)
        electrolyte_na = (deficit_ml / 1000) * 154
    elif fluid_type == "hypotonic":
        # 0.45% saline (hypotonic)
        # Use cautiously - risk of hyponatremia
        electrolyte_na = (deficit_ml / 1000) * 77
    else:  # hypertonic
        # 3% saline (hypertonic) - for severe hyponatremia
        electrolyte_na = (deficit_ml / 1000) * 513

    return {
        "deficit_ml": deficit_ml,
        "phase_1_bolus_ml": phase_1_ml,
        "phase_1_time_minutes": 20,  # 15-30 min typical
        "phase_2_remaining_ml": phase_2_ml,
        "phase_2_duration_hours": 2,  # 2-4 hours typical
        "sodium_mEq_to_replace": electrolyte_na,
        "fluid_type": fluid_type,
        "method": "AAP Rehydration Protocol"
    }


def maintenance_plus_deficit(
    weight_kg: float,
    age_months: int,
    dehydration_percent: float
) -> dict:
    """
    Calculate total fluid requirement (maintenance + deficit).

    Used to determine total daily fluid rate for hospitalized child with
    ongoing dehydration.

    Args:
        weight_kg: Patient weight in kilograms
        age_months: Patient age in months
        dehydration_percent: Percent dehydration (3-10%)

    Returns:
        Dictionary with maintenance + deficit breakdown
    """

    maintenance = holliday_segar_maintenance(weight_kg, age_months)
    deficit = deficit_fluid_replacement(weight_kg, dehydration_percent)

    # Total over 24-48 hours
    total_daily_ml = maintenance.total_daily_ml + deficit["phase_1_bolus_ml"]

    # If replacing remaining deficit over 24 hours
    total_with_deficit_24h = maintenance.total_daily_ml + deficit["deficit_ml"]

    return {
        "maintenance_daily_ml": maintenance.total_daily_ml,
        "maintenance_hourly_ml": maintenance.hourly_rate_ml,
        "deficit_total_ml": deficit["deficit_ml"],
        "deficit_phase_1_bolus_ml": deficit["phase_1_bolus_ml"],
        "deficit_phase_2_remaining_ml": deficit["phase_2_remaining_ml"],
        "total_24h_ml": total_daily_ml,
        "hourly_rate_including_deficit_ml": total_with_deficit_24h / 24,
        "sodium_daily_meq": maintenance.sodium_meq_daily + deficit["sodium_mEq_to_replace"],
        "notes": "Typical approach: bolus deficit in 1-2 hours, spread remaining over 24-48 hours with ongoing maintenance"
    }
