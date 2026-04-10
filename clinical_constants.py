"""
Clinical Constants and Reference Values

All values sourced from peer-reviewed literature and official guidelines.
"""

# ============================================================================
# PEDIATRIC AGE DEFINITIONS
# ============================================================================

AGE_CATEGORIES = {
    "newborn": {"min_days": 0, "max_days": 28, "description": "0-28 days"},
    "infant": {"min_days": 28, "max_days": 365, "description": "1-12 months"},
    "toddler": {"min_days": 365, "max_days": 1095, "description": "1-3 years"},
    "preschool": {"min_days": 1095, "max_days": 1825, "description": "3-5 years"},
    "school_age": {"min_days": 1825, "max_days": 4380, "description": "5-12 years"},
    "adolescent": {"min_days": 4380, "max_days": 6570, "description": "12-18 years"},
}

# ============================================================================
# NEONATAL TEMPERATURE CLASSIFICATIONS
# Blackburn, S. T. (2018). Maternal, Fetal, & Neonatal Physiology (6th ed.)
# ============================================================================

NEONATAL_TEMP_CLASSIFICATION = {
    "hypothermia": {"min": 0, "max": 36.4, "celsius": "0-36.4°C"},
    "moderate_hypothermia": {"min": 32, "max": 36.4, "celsius": "32-36.4°C"},
    "severe_hypothermia": {"min": 0, "max": 32, "celsius": "<32°C"},
    "normothermia": {"min": 36.5, "max": 37.5, "celsius": "36.5-37.5°C"},
    "hyperthermia": {"min": 37.6, "max": 42, "celsius": ">37.6°C"},
}

# ============================================================================
# NEONATAL NEUTRAL THERMAL ZONE (NTZ) REFERENCE TEMPERATURES
# Scopes & Wolf (1966), values recalculated for incubator air temps
# Used to define environmental temperature needs by postnatal age/weight
# ============================================================================

# Neutral Thermal Zone (NTZ) by age and weight
# Temperature in °C for naked infant in still air
NTZ_COEFFICIENTS = {
    # Day 1 NTZ by birth weight
    "day_1": {
        "1000g": 35.0, "1500g": 34.5, "2000g": 34.0, "2500g": 33.5, "3000g": 33.0,
    },
    # Day 3-5 NTZ by birth weight
    "day_3_5": {
        "1000g": 34.5, "1500g": 34.0, "2000g": 33.5, "2500g": 33.0, "3000g": 32.5,
    },
    # Day 7-28 NTZ by birth weight (stable infants)
    "day_7_28": {
        "1000g": 33.5, "1500g": 33.0, "2000g": 32.5, "2500g": 32.0, "3000g": 31.5,
    },
}

# ============================================================================
# VENTILATOR INITIAL SETTINGS
# Adapted from Keszler et al. (2012) Cleveland Clinic critical care handbook
# ============================================================================

VENTILATOR_INITIAL_SETTINGS = {
    "conventional": {
        "description": "Conventional pressure-controlled ventilation",
        "rate_range": {"min": 20, "max": 60, "default": 40},
        "pip_range": {"min": 12, "max": 30, "default": 16},
        "peep_range": {"min": 4, "max": 8, "default": 5},
        "inspiratory_time_range": {"min": 0.25, "max": 0.35, "default": 0.25},
    },
    "hfov": {
        "description": "High-frequency oscillatory ventilation",
        "frequency_hz": 10,
        "amplitude_range": {"min": 20, "max": 50},
        "mean_airway_pressure": {"min": 8, "max": 15},
    },
}

# ============================================================================
# HOLLIDAY-SEGAR MAINTENANCE FLUIDS
# Classic calculation: first 10 kg @ 100 mL/kg, next 10 kg @ 50 mL/kg, >20 kg @ 20 mL/kg
# References:
#   - Holliday, M.A., & Segar, W.E. (1957). "Metabolic rate and body size"
#   - Modern pediatrics now often uses "4-2-1" rule (see comments)
# ============================================================================

def calculate_holliday_segar_maintenance(weight_kg: float) -> float:
    """
    Calculate daily maintenance fluid requirement using Holliday-Segar formula.
    
    Args:
        weight_kg: Weight in kilograms
        
    Returns:
        Daily fluid requirement in mL
        
    Formula:
        First 10 kg:    100 mL/kg
        Next 10 kg:     50 mL/kg  
        Each additional kg: 20 mL/kg
        
    Example:
        - 5 kg infant: 5 × 100 = 500 mL/day
        - 15 kg child: (10 × 100) + (5 × 50) = 1250 mL/day
        - 25 kg child: (10 × 100) + (10 × 50) + (5 × 20) = 1600 mL/day
    """
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
    
    if weight_kg <= 10:
        return weight_kg * 100
    elif weight_kg <= 20:
        return 1000 + (weight_kg - 10) * 50
    else:
        return 1500 + (weight_kg - 20) * 20

# Alternative "4-2-1" rule (often used in modern practice)
# First 10 kg: 4 mL/kg/hour
# Next 10 kg: 2 mL/kg/hour
# Each additional kg: 1 mL/kg/hour
def calculate_4_2_1_maintenance(weight_kg: float) -> float:
    """Alternative modern maintenance fluid calculation (4-2-1 rule)."""
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
    
    hourly = 0
    if weight_kg <= 10:
        hourly = weight_kg * 4
    elif weight_kg <= 20:
        hourly = 40 + (weight_kg - 10) * 2
    else:
        hourly = 60 + (weight_kg - 20) * 1
    
    return hourly * 24  # Convert to daily

# ============================================================================
# PEDIATRIC HEMODYNAMIC PARAMETERS
# Adapted from Task Force on Hemodynamic Monitoring (AAP, PALS)
# ============================================================================

HEMODYNAMIC_REFERENCE = {
    "blood_pressure": {
        "newborn": {"systolic": {"min": 50, "max": 70}, "diastolic": {"min": 25, "max": 45}},
        "infant": {"systolic": {"min": 80, "max": 100}, "diastolic": {"min": 55, "max": 65}},
        "toddler": {"systolic": {"min": 95, "max": 105}, "diastolic": {"min": 60, "max": 70}},
        "school_age": {"systolic": {"min": 100, "max": 120}, "diastolic": {"min": 60, "max": 75}},
    },
    "heart_rate": {
        "newborn": {"min": 100, "max": 160},
        "infant": {"min": 100, "max": 160},
        "toddler": {"min": 90, "max": 150},
        "preschool": {"min": 80, "max": 120},
        "school_age": {"min": 70, "max": 110},
        "adolescent": {"min": 60, "max": 100},
    },
    "respiratory_rate": {
        "newborn": {"min": 30, "max": 60},
        "infant": {"min": 25, "max": 35},
        "toddler": {"min": 24, "max": 40},
        "preschool": {"min": 22, "max": 34},
        "school_age": {"min": 18, "max": 30},
        "adolescent": {"min": 12, "max": 20},
    },
}

# ============================================================================
# MEDICATION CONSTANTS
# ============================================================================

# Standard pediatric spacing intervals (hours)
MEDICATION_INTERVALS = {
    "every_4_hours": 4,
    "every_6_hours": 6,
    "every_8_hours": 8,
    "every_12_hours": 12,
    "daily": 24,
    "twice_daily": 12,
    "three_times_daily": 8,
    "four_times_daily": 6,
}

# ============================================================================
# APGAR SCORE SCORING
# Source: Apgar, V. (1952). "A Proposal for a New Method of Evaluation of the Newborn Infant"
# ============================================================================

APGAR_COMPONENTS = {
    "appearance": {"0": "Blue/pale", "1": "Extremities blue", "2": "Completely pink"},
    "pulse": {"0": "Absent", "1": "<100", "2": ">100"},
    "grimace": {"0": "No response", "1": "Grimace", "2": "Cry"},
    "activity": {"0": "Limp", "1": "Some flexion", "2": "Active movement"},
    "respiration": {"0": "Absent", "1": "Weak cry/gasp", "2": "Crying"},
}

APGAR_INTERPRETATION = {
    range(0, 4): "Severe depression",
    range(4, 7): "Moderate depression", 
    range(7, 11): "Normal/reassuring",
}

# ============================================================================
# LABORATORY REFERENCE RANGES
# Source: Harriet Lane Handbook 24th Edition (Johns Hopkins)
# ============================================================================

LAB_REFERENCE_RANGES = {
    "hemoglobin": {
        "newborn_1day": {"min": 14.5, "max": 24.0, "unit": "g/dL"},
        "newborn_7days": {"min": 12.0, "max": 20.0, "unit": "g/dL"},
        "infant_1month": {"min": 9.0, "max": 14.0, "unit": "g/dL"},
        "infant_6months": {"min": 9.5, "max": 13.0, "unit": "g/dL"},
        "toddler_2years": {"min": 10.5, "max": 13.5, "unit": "g/dL"},
        "school_age": {"min": 11.5, "max": 15.5, "unit": "g/dL"},
    },
    "glucose": {
        "newborn_fasting": {"min": 40, "max": 100, "unit": "mg/dL"},
        "infant_fasting": {"min": 70, "max": 100, "unit": "mg/dL"},
        "child_fasting": {"min": 70, "max": 100, "unit": "mg/dL"},
    },
    "bilirubin_total": {
        "newborn_24hr": {"phototherapy_threshold": 18, "unit": "mg/dL"},
        "newborn_48hr": {"phototherapy_threshold": 25, "unit": "mg/dL"},
    },
}

# ============================================================================
# PRECISION TOLERANCES BY CALCULATION TYPE
# Clinical vs mathematical tolerance requirements
# ============================================================================

PRECISION_TOLERANCES = {
    "dosing_mg": {"relative": 0.005, "description": "±0.5% (clinical rounding)"},
    "dosing_mcg": {"relative": 0.01, "description": "±1% (microgram precision)"},
    "growth_percentile": {"relative": 0.01, "description": "±1% (lookup table interpolation)"},
    "severity_score": {"relative": 0.0, "description": "Exact integer match"},
    "lab_value_prediction": {"relative": 0.05, "description": "±5% (modeling uncertainty)"},
    "hemodynamic_calculation": {"relative": 0.03, "description": "±3% (physics-based)"},
    "ventilator_settings": {"relative": 0.05, "description": "±5% (clinical adjustment)"},
    "temperature_zone": {"absolute": 0.5, "unit": "°C", "description": "±0.5°C"},
}

# ============================================================================
# METADATA FOR GOVERNANCE & AUDIT
# ============================================================================

VALIDATION_STATUS = {
    "development": "Not yet validated",
    "testing": "Undergoing testing against golden cases",
    "approved": "Approved for clinical use",
    "deprecated": "Superseded by newer version",
}

SOURCE_TYPES = {
    "aap_official": "American Academy of Pediatrics official guideline",
    "acep_clinical_policy": "ACEP Clinical Policy",
    "cdc_guideline": "CDC Official Guideline",
    "peer_reviewed": "Peer-reviewed journal publication",
    "textbook": "Clinical textbook",
    "clinical_society": "Clinical society recommendation",
}

# ============================================================================
# METADATA: Clinical Constants Version
# ============================================================================

CONSTANTS_VERSION = "1.0.0"
CONSTANTS_LAST_UPDATED = "2026-04-09"
CONSTANTS_AUTHOR = "Timothy Hartzog, MD"
