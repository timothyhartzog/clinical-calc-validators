"""
Pediatric Medication Dosing Calculations

Weight-based antibiotic and medication dosing for pediatric patients.
All doses based on AAP Red Book 2024 and established pharmacokinetic principles.

References:
    - American Academy of Pediatrics. (2024). Red Book: Report of the Committee on Infectious Diseases (34th ed.)
    - Harriet Lane Handbook. (2024). Johns Hopkins Manual of Pediatric Diagnostics and Therapy.
    - Drug Information. Lexi-Drugs (electronic version).

Tolerance: ±0.5% (clinical rounding acceptable)
"""

from dataclasses import dataclass
from typing import Optional, Dict, Literal
from enum import Enum

# ============================================================================
# DOSING ENUMERATIONS
# ============================================================================

class Route(Enum):
    """Medication administration routes."""
    ORAL = "oral"
    IV = "intravenous"
    IM = "intramuscular"
    RECTAL = "rectal"

class Indication(Enum):
    """Clinical indications for dosing."""
    PROPHYLAXIS = "prophylaxis"
    MILD_MODERATE = "mild_moderate"
    SEVERE = "severe"
    MENINGITIS = "meningitis"
    OTITIS_MEDIA = "otitis_media"
    STREP_THROAT = "strep_throat"
    PNEUMONIA = "pneumonia"

# ============================================================================
# DOSING DATA STRUCTURES
# ============================================================================

@dataclass
class DoseCalculation:
    """Result of a dose calculation."""
    drug_name: str
    weight_kg: float
    age_months: int
    indication: str
    route: str
    dose_mg: float
    dose_per_kg: float
    frequency: str
    interval_hours: float
    total_daily_mg: float
    max_daily_dose_mg: Optional[float]
    notes: str
    source: str
    

# ============================================================================
# AMOXICILLIN DOSING
# Source: AAP Red Book 2024, Table 4.1; Lexi-Drugs pediatric data
# ============================================================================

def amoxicillin_dose(
    weight_kg: float,
    age_months: int,
    indication: Indication = Indication.MILD_MODERATE,
    route: Route = Route.ORAL
) -> DoseCalculation:
    """
    Calculate amoxicillin dose for pediatric patient.
    
    Args:
        weight_kg: Patient weight in kilograms
        age_months: Patient age in months
        indication: Clinical indication (mild_moderate, severe, otitis_media, strep_throat)
        route: Route of administration (oral, IV, IM)
        
    Returns:
        DoseCalculation with dose details
        
    Dosing:
        Mild-moderate infection (oral): 25 mg/kg/dose every 8 hours
        Severe infection (oral): 45 mg/kg/dose every 6 hours
        Acute otitis media: 40-45 mg/kg/dose daily in divided doses
        Streptococcal pharyngitis: 12.5 mg/kg/dose every 8 hours (min 125 mg/dose)
        
    Limitations:
        - For preterm infants < 35 weeks gestational age, consult specialist
        - Reduced dosing if significant renal impairment (CrCl < 30)
        - Not validated for patients > 50 kg (use adult dosing)
        
    References:
        - AAP Red Book 2024, Antimicrobial Agents and Related Therapy
        - Lexi-Drugs pediatric database
    """
    
    if weight_kg <= 0 or weight_kg > 50:
        raise ValueError(f"Weight {weight_kg} kg outside validated range (0.1-50 kg)")
    
    if age_months < 0:
        raise ValueError(f"Age cannot be negative")
    
    # Special case: newborns < 7 days may need different dosing
    if age_months == 0 and weight_kg < 2.5:
        raise ValueError("Neonatal amoxicillin dosing requires specialist consultation")
    
    dose_per_kg = None
    frequency = None
    interval_hours = None
    max_daily_dose = None
    indication_str = indication.value if isinstance(indication, Indication) else str(indication)
    
    # Determine dose based on indication
    if indication == Indication.STREP_THROAT:
        dose_per_kg = 12.5
        frequency = "every 8 hours"
        interval_hours = 8
        max_daily_dose = None  # No fixed max for pediatric dosing
        daily_doses_per_kg = 37.5  # 12.5 × 3
        
    elif indication == Indication.OTITIS_MEDIA:
        # High-dose amoxicillin for AOM
        dose_per_kg = 45  # Aggressive dosing for AOM
        frequency = "every 8 hours"  
        interval_hours = 8
        max_daily_dose = 4000  # mg/day maximum
        daily_doses_per_kg = 135
        
    elif indication == Indication.SEVERE:
        dose_per_kg = 45
        frequency = "every 6 hours"
        interval_hours = 6
        max_daily_dose = 4000
        daily_doses_per_kg = 180
        
    else:  # Mild-moderate (default)
        dose_per_kg = 25
        frequency = "every 8 hours"
        interval_hours = 8
        max_daily_dose = None
        daily_doses_per_kg = 75
    
    # Calculate single dose
    single_dose_mg = weight_kg * dose_per_kg
    
    # Round to nearest 5 mg for practicality
    single_dose_mg = round(single_dose_mg / 5) * 5
    
    # Calculate total daily dose
    total_daily_mg = single_dose_mg * (24 / interval_hours)
    
    # Apply maximum daily dose if specified
    if max_daily_dose and total_daily_mg > max_daily_dose:
        # Recalculate single dose based on max daily
        single_dose_mg = max_daily_dose / (24 / interval_hours)
        total_daily_mg = max_daily_dose
    
    notes = f"Amoxicillin {single_dose_mg:.0f} mg {frequency} for {indication_str}"
    if weight_kg > 40:
        notes += " [approaching adult dosing consideration]"
    
    return DoseCalculation(
        drug_name="Amoxicillin",
        weight_kg=weight_kg,
        age_months=age_months,
        indication=indication_str,
        route=route.value if isinstance(route, Route) else str(route),
        dose_mg=single_dose_mg,
        dose_per_kg=dose_per_kg,
        frequency=frequency,
        interval_hours=interval_hours,
        total_daily_mg=total_daily_mg,
        max_daily_dose_mg=max_daily_dose,
        notes=notes,
        source="AAP Red Book 2024, Table 4.1"
    )


# ============================================================================
# GENTAMICIN DOSING (RENAL DOSING)
# Source: AAP Red Book 2024; Kaushal et al. pharmacokinetic modeling
# ============================================================================

def gentamicin_dose(
    weight_kg: float,
    age_months: int,
    indication: Indication = Indication.MILD_MODERATE,
    renal_function: Literal["normal", "mild_impairment", "moderate_impairment"] = "normal"
) -> DoseCalculation:
    """
    Calculate gentamicin dose for pediatric patient.
    
    NOTE: Gentamicin is nephrotoxic and ototoxic. Use only when appropriate
    gram-negative coverage is required. Extended-interval dosing (once daily)
    preferred when possible.
    
    Args:
        weight_kg: Patient weight in kilograms
        age_months: Patient age in months
        indication: Clinical indication
        renal_function: Baseline renal function assessment
        
    Returns:
        DoseCalculation with dose details
        
    Dosing (once-daily extended interval dosing):
        Normal renal function: 7.5 mg/kg/dose every 24 hours IV
        Monitor: Trough just before next dose (goal <1 mcg/mL)
        Peak: 1 hour post-infusion (goal 15-30 mcg/mL)
        
    For traditional q8h dosing (less preferred):
        2.5 mg/kg/dose every 8 hours
        
    References:
        - AAP Red Book 2024
        - Glauser et al. Pediatr Infect Dis J. 2009
    """
    
    if weight_kg <= 0 or weight_kg > 50:
        raise ValueError(f"Weight {weight_kg} kg outside validated range")
    
    # Extended-interval (once-daily) dosing is preferred
    dose_per_kg = 7.5
    interval_hours = 24
    frequency = "once daily"
    max_daily_dose = 500  # mg
    
    single_dose_mg = weight_kg * dose_per_kg
    single_dose_mg = round(single_dose_mg / 2.5) * 2.5  # Round to nearest 2.5 mg
    
    total_daily_mg = single_dose_mg
    
    if total_daily_mg > max_daily_dose:
        single_dose_mg = max_daily_dose
    
    # Renal function adjustments
    notes = f"Gentamicin {single_dose_mg:.1f} mg {frequency} IV (extended-interval)"
    if renal_function != "normal":
        notes += f" [ADJUST for {renal_function}]"
    
    notes += "\nMONITOR: Trough (pre-dose) <1 mcg/mL, Peak (1h post) 15-30 mcg/mL"
    notes += "\nCAUTION: Nephrotoxic and ototoxic - use only when indicated"
    
    return DoseCalculation(
        drug_name="Gentamicin",
        weight_kg=weight_kg,
        age_months=age_months,
        indication=indication.value if isinstance(indication, Indication) else str(indication),
        route="intravenous",
        dose_mg=single_dose_mg,
        dose_per_kg=dose_per_kg,
        frequency=frequency,
        interval_hours=interval_hours,
        total_daily_mg=total_daily_mg,
        max_daily_dose_mg=max_daily_dose,
        notes=notes,
        source="AAP Red Book 2024; Glauser et al. 2009"
    )


# ============================================================================
# CEFOTAXIME DOSING
# Source: AAP Red Book 2024; commonly used for gram-negative/anaerobic coverage
# ============================================================================

def cefotaxime_dose(
    weight_kg: float,
    age_months: int,
    indication: Indication = Indication.MILD_MODERATE,
    route: Route = Route.IV
) -> DoseCalculation:
    """
    Calculate cefotaxime dose for pediatric patient.
    
    Args:
        weight_kg: Patient weight in kilograms
        age_months: Patient age in months
        indication: Clinical indication (mild_moderate, severe, meningitis)
        route: IV or IM
        
    Returns:
        DoseCalculation with dose details
        
    Dosing:
        Non-meningitis (mild-moderate): 50 mg/kg/dose every 6-8 hours
        Non-meningitis (severe): 50 mg/kg/dose every 4-6 hours
        Bacterial meningitis: 50 mg/kg/dose every 4-6 hours (HIGHER doses required!)
        Maximum single dose: 2000 mg
        
    References:
        - AAP Red Book 2024
        - Lexi-Drugs pediatric data
    """
    
    if weight_kg <= 0 or weight_kg > 50:
        raise ValueError(f"Weight {weight_kg} kg outside validated range")
    
    if indication == Indication.MENINGITIS:
        dose_per_kg = 50
        interval_hours = 4
        frequency = "every 4 hours"
        max_daily_dose = 12000  # Higher for meningitis
        notes = "HIGH-DOSE cefotaxime for MENINGITIS"
    elif indication == Indication.SEVERE:
        dose_per_kg = 50
        interval_hours = 6
        frequency = "every 6 hours"
        max_daily_dose = 8000
        notes = "Cefotaxime for severe infection"
    else:  # Mild-moderate
        dose_per_kg = 50
        interval_hours = 8
        frequency = "every 8 hours"
        max_daily_dose = 6000
        notes = "Cefotaxime for mild-moderate infection"
    
    single_dose_mg = weight_kg * dose_per_kg
    
    # Cap at 2000 mg per dose
    if single_dose_mg > 2000:
        single_dose_mg = 2000
    else:
        single_dose_mg = round(single_dose_mg / 50) * 50  # Round to nearest 50 mg
    
    total_daily_mg = single_dose_mg * (24 / interval_hours)
    
    if total_daily_mg > max_daily_dose:
        single_dose_mg = max_daily_dose / (24 / interval_hours)
        total_daily_mg = max_daily_dose
    
    return DoseCalculation(
        drug_name="Cefotaxime",
        weight_kg=weight_kg,
        age_months=age_months,
        indication=indication.value if isinstance(indication, Indication) else str(indication),
        route=route.value if isinstance(route, Route) else str(route),
        dose_mg=single_dose_mg,
        dose_per_kg=dose_per_kg,
        frequency=frequency,
        interval_hours=interval_hours,
        total_daily_mg=total_daily_mg,
        max_daily_dose_mg=max_daily_dose,
        notes=notes,
        source="AAP Red Book 2024"
    )


# ============================================================================
# EXPORT & VALIDATION UTILITIES
# ============================================================================

def dose_to_dict(calc: DoseCalculation) -> Dict:
    """Convert DoseCalculation to dictionary for JSON serialization."""
    return {
        "drug_name": calc.drug_name,
        "weight_kg": calc.weight_kg,
        "age_months": calc.age_months,
        "indication": calc.indication,
        "route": calc.route,
        "dose_mg": calc.dose_mg,
        "dose_per_kg": calc.dose_per_kg,
        "frequency": calc.frequency,
        "interval_hours": calc.interval_hours,
        "total_daily_mg": calc.total_daily_mg,
        "max_daily_dose_mg": calc.max_daily_dose_mg,
        "notes": calc.notes,
        "source": calc.source,
    }
