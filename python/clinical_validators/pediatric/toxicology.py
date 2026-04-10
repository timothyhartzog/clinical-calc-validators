"""
Pediatric toxicology assessment module.

Functions for assessing severity of toxic exposures and managing pediatric poisoning cases.

Covers:
- Acetaminophen toxicity (Rumack-Matthew nomogram)
- Salicylate toxicity scoring
- Iron toxicity assessment
- Drug-induced hepatotoxicity
- Toxic ingestion risk stratification
"""

from dataclasses import dataclass


# =============================================================================
# RESULT DATACLASSES
# =============================================================================


@dataclass
class AcetaminophenToxicityResult:
    """Result of acetaminophen toxicity assessment using Rumack-Matthew nomogram."""
    toxicity_category: str  # "no_toxicity", "low_risk", "intermediate_risk", "high_risk"
    risk_zone: str  # "below_line", "possible_toxicity", "probable_toxicity"
    plasma_concentration_mcg_ml: float
    plasma_concentration_mmol_l: float
    hours_post_ingestion: int
    recommendation: str  # "observe", "treat_with_nac", "intensive_monitoring"
    nac_loading_dose_mg_kg: float | None
    liver_function_risk: str  # "low", "moderate", "high"


@dataclass
class SalicylateToxicityResult:
    """Result of salicylate toxicity assessment."""
    toxicity_score: int  # 0-100
    toxicity_category: str  # "no_toxicity", "mild", "moderate", "severe", "critical"
    plasma_salicylate_mg_dl: float
    estimated_toxicity_mg_kg: float
    acid_base_status: str  # "normal", "respiratory_alkalosis", "metabolic_acidosis", "mixed"
    clinical_recommendation: str
    activated_charcoal_indicated: bool
    dialysis_indicated: bool
    monitoring_frequency_hours: int


@dataclass
class IronToxicityResult:
    """Result of iron toxicity assessment."""
    toxicity_category: str  # "no_toxicity", "mild", "moderate", "severe", "critical"
    estimated_iron_dose_mg_kg: float
    serum_iron_level_mcg_dl: float
    tibc_mcg_dl: float
    iron_tibc_ratio: float
    phase_of_illness: str  # "phase_1_gi", "phase_2_latent", "phase_3_systemic", "phase_4_late"
    chelation_indicated: bool
    deferoxamine_loading_dose_mg_kg: float | None
    clinical_recommendation: str
    monitoring_interval_hours: int


@dataclass
class DrugInducedHepatotoxicityResult:
    """Result of drug-induced hepatotoxicity severity assessment."""
    toxicity_grade: int  # 0-5 (CTCAE-like grading)
    risk_category: str  # "no_injury", "low_risk", "moderate_risk", "high_risk", "critical"
    alt_iu_l: float
    ast_iu_l: float
    alt_ast_ratio: float
    bilirubin_mg_dl: float
    inr: float
    estimated_hepatocyte_injury_percent: float
    liver_synthetic_function_impaired: bool
    fulminant_hepatic_failure_risk: str  # "low", "moderate", "high"
    recommendation: str  # "continue_monitoring", "hold_drug", "intensive_management"
    monitoring_frequency_hours: int


@dataclass
class ToxicIngestionRiskAssessmentResult:
    """Result of toxic ingestion risk stratification."""
    risk_score: int  # 0-100
    risk_category: str  # "non_toxic", "low_risk", "moderate_risk", "high_risk", "critical"
    estimated_toxicity_severity: str  # "asymptomatic", "mild", "moderate", "severe", "life_threatening"
    onset_hours: int  # Expected time to symptom onset
    peak_toxicity_hours: int
    substance_type: str
    decontamination_indicated: bool  # Activated charcoal, gastric lavage, etc.
    antidote_available: bool
    antidote_name: str | None
    supportive_care_required: str  # Level of monitoring/support
    disposition: str  # "outpatient_observation", "hospital_observation", "icu"
    clinical_recommendation: str


# =============================================================================
# ACETAMINOPHEN TOXICITY ASSESSMENT (RUMACK-MATTHEW NOMOGRAM)
# =============================================================================


def acetaminophen_toxicity_assessment(
    age_years: float,
    weight_kg: float,
    plasma_concentration_mcg_ml: float,
    hours_post_ingestion: int,
    reported_ingestion_amount_mg: float | None = None,
) -> AcetaminophenToxicityResult:
    """
    Assess acetaminophen toxicity using Rumack-Matthew nomogram.

    The Rumack-Matthew nomogram plots plasma acetaminophen concentration
    against time post-ingestion to determine toxicity risk and need for
    N-acetylcysteine (NAC) treatment.

    Args:
        age_years: Patient age in years (0-18)
        weight_kg: Patient weight in kg (1-150)
        plasma_concentration_mcg_ml: Plasma acetaminophen concentration in mcg/mL
        hours_post_ingestion: Hours since ingestion (0.5-24)
        reported_ingestion_amount_mg: Reported acetaminophen dose in mg (optional)

    Returns:
        AcetaminophenToxicityResult with toxicity assessment and recommendations

    Raises:
        ValueError: If inputs are invalid or out of range

    References:
        Rumack BH, Matthew H. "Acetaminophen poisoning and toxicity."
        Pediatrics. 1975;55(6):871-876.

        Bailey B, Blais R, Letarte A. Status epilepticus after
        repeated supratherapeutic acetaminophen dosing.
        Ann Emerg Med. 1997;29(2):262-264.
    """
    # Validation
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18, got {age_years}")
    if not 1 <= weight_kg <= 150:
        raise ValueError(f"Weight must be 1-150 kg, got {weight_kg}")
    if plasma_concentration_mcg_ml < 0:
        raise ValueError(f"Plasma concentration cannot be negative: {plasma_concentration_mcg_ml}")
    if not 0.5 <= hours_post_ingestion <= 24:
        raise ValueError(f"Hours post-ingestion must be 0.5-24, got {hours_post_ingestion}")

    # Convert mcg/mL to mmol/L (APAP MW = 151 g/mol)
    plasma_mmol_l = plasma_concentration_mcg_ml / 151 * 1000

    # Rumack-Matthew nomogram thresholds (reference line at 4 hours)
    # Values are normalized to different time points
    nomogram_values = {
        0.5: 200,
        1: 150,
        2: 100,
        3: 60,
        4: 30,    # Reference point
        6: 15,
        8: 8,
        12: 2,
        24: 0.4,
    }

    # Find threshold for this time point using interpolation
    time_points = sorted(nomogram_values.keys())
    threshold = None

    if hours_post_ingestion <= time_points[0]:
        threshold = nomogram_values[time_points[0]]
    elif hours_post_ingestion >= time_points[-1]:
        threshold = nomogram_values[time_points[-1]]
    else:
        # Linear interpolation between points
        for i in range(len(time_points) - 1):
            t1, t2 = time_points[i], time_points[i + 1]
            if t1 <= hours_post_ingestion <= t2:
                v1, v2 = nomogram_values[t1], nomogram_values[t2]
                threshold = v1 - (v1 - v2) * (hours_post_ingestion - t1) / (t2 - t1)
                break

    # Determine risk zone
    if plasma_concentration_mcg_ml <= threshold * 0.5:
        risk_zone = "below_line"
        toxicity_category = "no_toxicity"
        recommendation = "observe"
        nac_loading_dose = None
    elif plasma_concentration_mcg_ml <= threshold:
        risk_zone = "possible_toxicity"
        toxicity_category = "low_risk"
        recommendation = "consider_nac_treatment"
        nac_loading_dose = 140.0  # mg/kg
    else:
        risk_zone = "probable_toxicity"
        toxicity_category = "high_risk" if plasma_concentration_mcg_ml > threshold * 1.5 else "intermediate_risk"
        recommendation = "treat_with_nac"
        nac_loading_dose = 140.0  # mg/kg

    # Assess liver function risk based on concentration and time
    if plasma_concentration_mcg_ml > 100:
        liver_function_risk = "high"
    elif plasma_concentration_mcg_ml > 50 or hours_post_ingestion < 4:
        liver_function_risk = "moderate"
    else:
        liver_function_risk = "low"

    return AcetaminophenToxicityResult(
        toxicity_category=toxicity_category,
        risk_zone=risk_zone,
        plasma_concentration_mcg_ml=plasma_concentration_mcg_ml,
        plasma_concentration_mmol_l=round(plasma_mmol_l, 1),
        hours_post_ingestion=hours_post_ingestion,
        recommendation=recommendation,
        nac_loading_dose_mg_kg=nac_loading_dose,
        liver_function_risk=liver_function_risk,
    )


# =============================================================================
# SALICYLATE TOXICITY ASSESSMENT
# =============================================================================


def salicylate_toxicity_assessment(
    age_years: float,
    weight_kg: float,
    plasma_salicylate_mg_dl: float,
    hours_post_ingestion: int,
    ph_arterial: float | None = None,
    respiratory_rate_min: int | None = None,
) -> SalicylateToxicityResult:
    """
    Assess salicylate toxicity severity.

    Salicylate poisoning causes metabolic and respiratory disturbances.
    Toxicity correlates with plasma levels but clinical severity also
    depends on pH, respiratory compensation, and time since ingestion.

    Args:
        age_years: Patient age in years (0-18)
        weight_kg: Patient weight in kg (1-150)
        plasma_salicylate_mg_dl: Plasma salicylate level in mg/dL
        hours_post_ingestion: Hours since ingestion (0.25-72)
        ph_arterial: Arterial pH (7.0-7.6, optional for better assessment)
        respiratory_rate_min: Respiratory rate in breaths/min (optional)

    Returns:
        SalicylateToxicityResult with toxicity classification and management

    References:
        Done AK. Salicylate intoxication. Significance of measurements
        of salicylate in blood and urine. Pediatrics. 1960;26:800-807.
    """
    # Validation
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18, got {age_years}")
    if not 1 <= weight_kg <= 150:
        raise ValueError(f"Weight must be 1-150 kg, got {weight_kg}")
    if plasma_salicylate_mg_dl < 0:
        raise ValueError(f"Plasma salicylate cannot be negative")
    if not 0.25 <= hours_post_ingestion <= 72:
        raise ValueError(f"Hours post-ingestion must be 0.25-72")

    # Classify toxicity by plasma level (Done's classification)
    if plasma_salicylate_mg_dl < 15:
        toxicity_category = "no_toxicity"
        toxicity_score = 0
    elif plasma_salicylate_mg_dl < 30:
        toxicity_category = "mild"
        toxicity_score = 25
    elif plasma_salicylate_mg_dl < 60:
        toxicity_category = "moderate"
        toxicity_score = 50
    elif plasma_salicylate_mg_dl < 100:
        toxicity_category = "severe"
        toxicity_score = 75
    else:
        toxicity_category = "critical"
        toxicity_score = 100

    # Assess acid-base status
    if ph_arterial is None:
        # Early: respiratory alkalosis; Late: metabolic acidosis
        if hours_post_ingestion < 6:
            acid_base_status = "respiratory_alkalosis"
        elif hours_post_ingestion < 12:
            acid_base_status = "mixed"
        else:
            acid_base_status = "metabolic_acidosis"
    else:
        if ph_arterial > 7.45:
            acid_base_status = "respiratory_alkalosis"
        elif ph_arterial > 7.35:
            acid_base_status = "normal"
        else:
            acid_base_status = "metabolic_acidosis"

    # Estimate ingestion dose
    estimated_dose_mg_kg = plasma_salicylate_mg_dl / 10  # Rough estimate

    # Recommendations based on level and time
    if plasma_salicylate_mg_dl < 30:
        recommendation = "Supportive care, monitor levels q2-4h"
        activated_charcoal = False
        dialysis = False
        monitoring_freq = 4
    elif plasma_salicylate_mg_dl < 60:
        recommendation = "Activated charcoal, alkaline urine, monitor q1-2h"
        activated_charcoal = True
        dialysis = False
        monitoring_freq = 2
    else:
        recommendation = "Aggressive alkalinization, hemodialysis indicated"
        activated_charcoal = True
        dialysis = True
        monitoring_freq = 1

    return SalicylateToxicityResult(
        toxicity_score=toxicity_score,
        toxicity_category=toxicity_category,
        plasma_salicylate_mg_dl=plasma_salicylate_mg_dl,
        estimated_toxicity_mg_kg=round(estimated_dose_mg_kg, 1),
        acid_base_status=acid_base_status,
        clinical_recommendation=recommendation,
        activated_charcoal_indicated=activated_charcoal,
        dialysis_indicated=dialysis,
        monitoring_frequency_hours=monitoring_freq,
    )


# =============================================================================
# IRON TOXICITY ASSESSMENT
# =============================================================================


def iron_toxicity_assessment(
    age_years: float,
    weight_kg: float,
    serum_iron_mcg_dl: float,
    tibc_mcg_dl: float,
    hours_post_ingestion: int,
    reported_dose_mg: float | None = None,
) -> IronToxicityResult:
    """
    Assess iron toxicity and chelation need.

    Iron toxicity is assessed by serum iron level and iron-TIBC ratio.
    Clinical presentation follows characteristic phases post-ingestion.

    Args:
        age_years: Patient age in years (0-18)
        weight_kg: Patient weight in kg (1-150)
        serum_iron_mcg_dl: Serum iron level in mcg/dL
        tibc_mcg_dl: Total iron binding capacity in mcg/dL
        hours_post_ingestion: Hours since ingestion (0.25-72)
        reported_dose_mg: Reported iron dose in mg (optional)

    Returns:
        IronToxicityResult with toxicity assessment and chelation recommendations

    References:
        Tenenbein M. Iron poisoning: Critical decisions in management.
        Emerg Med J. 2007;24(2):101-104.
    """
    # Validation
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18, got {age_years}")
    if not 1 <= weight_kg <= 150:
        raise ValueError(f"Weight must be 1-150 kg, got {weight_kg}")
    if serum_iron_mcg_dl < 0 or tibc_mcg_dl < 0:
        raise ValueError("Iron levels cannot be negative")

    # Calculate iron-TIBC ratio
    iron_tibc_ratio = serum_iron_mcg_dl / tibc_mcg_dl if tibc_mcg_dl > 0 else 0

    # Estimate ingestion dose from serum iron
    estimated_dose_mg_kg = serum_iron_mcg_dl / 100  # Rough conversion

    # Classify toxicity by iron-TIBC ratio and serum level
    if serum_iron_mcg_dl < 100:
        toxicity_category = "no_toxicity"
        chelation = False
        deferoxamine_dose = None
    elif serum_iron_mcg_dl < 300 or iron_tibc_ratio < 0.5:
        toxicity_category = "mild"
        chelation = False
        deferoxamine_dose = None
    elif serum_iron_mcg_dl < 500 or iron_tibc_ratio < 1.0:
        toxicity_category = "moderate"
        chelation = True
        deferoxamine_dose = 15.0  # mg/kg IV loading dose
    elif serum_iron_mcg_dl < 1000 or iron_tibc_ratio < 2.0:
        toxicity_category = "severe"
        chelation = True
        deferoxamine_dose = 15.0
    else:
        toxicity_category = "critical"
        chelation = True
        deferoxamine_dose = 15.0

    # Determine phase of illness
    if hours_post_ingestion < 6:
        phase = "phase_1_gi"
    elif hours_post_ingestion < 24:
        phase = "phase_2_latent"
    elif hours_post_ingestion < 48:
        phase = "phase_3_systemic"
    else:
        phase = "phase_4_late"

    # Clinical recommendation
    if chelation:
        recommendation = f"Initiate deferoxamine at {deferoxamine_dose} mg/kg IV; monitor serum iron q4-6h"
        monitoring_hours = 4
    else:
        recommendation = "Supportive care; monitor for symptoms of systemic iron toxicity"
        monitoring_hours = 8

    return IronToxicityResult(
        toxicity_category=toxicity_category,
        estimated_iron_dose_mg_kg=round(estimated_dose_mg_kg, 1),
        serum_iron_level_mcg_dl=serum_iron_mcg_dl,
        tibc_mcg_dl=tibc_mcg_dl,
        iron_tibc_ratio=round(iron_tibc_ratio, 2),
        phase_of_illness=phase,
        chelation_indicated=chelation,
        deferoxamine_loading_dose_mg_kg=deferoxamine_dose,
        clinical_recommendation=recommendation,
        monitoring_interval_hours=monitoring_hours,
    )


# =============================================================================
# DRUG-INDUCED HEPATOTOXICITY ASSESSMENT
# =============================================================================


def drug_induced_hepatotoxicity_assessment(
    age_years: float,
    weight_kg: float,
    alt_iu_l: float,
    ast_iu_l: float,
    bilirubin_mg_dl: float,
    albumin_g_dl: float | None = None,
    inr: float | None = None,
    days_on_drug: int = 7,
) -> DrugInducedHepatotoxicityResult:
    """
    Assess severity of drug-induced liver injury.

    Uses CTCAE-like grading combined with synthetic function assessment
    to determine severity and management approach.

    Args:
        age_years: Patient age in years (0-18)
        weight_kg: Patient weight in kg (1-150)
        alt_iu_l: Alanine aminotransferase in IU/L
        ast_iu_l: Aspartate aminotransferase in IU/L
        bilirubin_mg_dl: Total bilirubin in mg/dL
        albumin_g_dl: Serum albumin in g/dL (optional)
        inr: International normalized ratio (optional)
        days_on_drug: Days of drug exposure (1-365)

    Returns:
        DrugInducedHepatotoxicityResult with toxicity grading

    References:
        Aithal GP, Watkins PB, Andrade RJ, et al. Case definition and
        phenotype standardization in drug-induced liver injury.
        Clin Pharmacol Ther. 2011;89(6):806-815.
    """
    # Validation
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18, got {age_years}")
    if not 1 <= weight_kg <= 150:
        raise ValueError(f"Weight must be 1-150 kg, got {weight_kg}")
    if alt_iu_l < 0 or ast_iu_l < 0 or bilirubin_mg_dl < 0:
        raise ValueError("Lab values cannot be negative")

    # Normal ranges for age
    alt_upper_normal = 40 if age_years >= 5 else 45

    # Grade based on ALT elevation (CTCAE-like)
    if alt_iu_l <= alt_upper_normal:
        toxicity_grade = 0
    elif alt_iu_l <= 3 * alt_upper_normal:
        toxicity_grade = 1
    elif alt_iu_l <= 5 * alt_upper_normal:
        toxicity_grade = 2
    elif alt_iu_l <= 10 * alt_upper_normal:
        toxicity_grade = 3
    elif alt_iu_l <= 20 * alt_upper_normal:
        toxicity_grade = 4
    else:
        toxicity_grade = 5

    # Adjust for bilirubin elevation
    if bilirubin_mg_dl > 3:
        toxicity_grade = max(toxicity_grade, 4)

    # Calculate ALT/AST ratio (pattern recognition)
    alt_ast_ratio = alt_iu_l / ast_iu_l if ast_iu_l > 0 else 1

    # Assess synthetic function
    synthetic_function_impaired = False
    if inr is not None and inr > 1.5:
        synthetic_function_impaired = True
    if albumin_g_dl is not None and albumin_g_dl < 3.0:
        synthetic_function_impaired = True

    # Estimate hepatocyte injury
    injury_percent = min(100, (alt_iu_l / alt_upper_normal) * 10)

    # Risk of fulminant failure
    if toxicity_grade >= 4 and synthetic_function_impaired:
        fulminant_risk = "high"
    elif toxicity_grade >= 3:
        fulminant_risk = "moderate"
    else:
        fulminant_risk = "low"

    # Recommendation based on toxicity grade
    if toxicity_grade == 0:
        risk_category = "no_injury"
        recommendation = "Continue monitoring"
        monitoring_hours = 72
    elif toxicity_grade <= 2:
        risk_category = "low_risk"
        recommendation = "Monitor LFTs, consider continuing drug with close follow-up"
        monitoring_hours = 24
    elif toxicity_grade == 3:
        risk_category = "moderate_risk"
        recommendation = "Consider hold of drug, increase monitoring frequency"
        monitoring_hours = 12
    elif toxicity_grade == 4:
        risk_category = "high_risk"
        recommendation = "Hold drug, intensive hepatology consultation"
        monitoring_hours = 6
    else:
        risk_category = "critical"
        recommendation = "Hold drug immediately, intensive care management"
        monitoring_hours = 4

    return DrugInducedHepatotoxicityResult(
        toxicity_grade=toxicity_grade,
        risk_category=risk_category,
        alt_iu_l=alt_iu_l,
        ast_iu_l=ast_iu_l,
        alt_ast_ratio=round(alt_ast_ratio, 1),
        bilirubin_mg_dl=bilirubin_mg_dl,
        inr=inr or 1.0,
        estimated_hepatocyte_injury_percent=round(injury_percent, 1),
        liver_synthetic_function_impaired=synthetic_function_impaired,
        fulminant_hepatic_failure_risk=fulminant_risk,
        recommendation=recommendation,
        monitoring_frequency_hours=monitoring_hours,
    )


# =============================================================================
# TOXIC INGESTION RISK ASSESSMENT
# =============================================================================


def toxic_ingestion_risk_assessment(
    age_years: float,
    weight_kg: float,
    substance: str,
    reported_dose_mg: float | None = None,
    hours_post_ingestion: float = 1.0,
    symptoms_present: bool = False,
) -> ToxicIngestionRiskAssessmentResult:
    """
    Stratify risk of toxic ingestion and guide initial management.

    Assesses common pediatric toxic exposures and provides disposition
    and management recommendations.

    Args:
        age_years: Patient age in years (0-18)
        weight_kg: Patient weight in kg (1-150)
        substance: Type of toxic substance (acetaminophen, iron, salicylate, etc.)
        reported_dose_mg: Reported ingestion amount in mg (optional)
        hours_post_ingestion: Hours since ingestion (0.25-72)
        symptoms_present: Whether symptoms are currently present

    Returns:
        ToxicIngestionRiskAssessmentResult with risk stratification

    References:
        Woolf AD. Poisoning in children and adolescents.
        Pediatr Rev. 2000;21(10):307-320.
    """
    # Validation
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18, got {age_years}")
    if not 1 <= weight_kg <= 150:
        raise ValueError(f"Weight must be 1-150 kg, got {weight_kg}")
    if not 0.25 <= hours_post_ingestion <= 72:
        raise ValueError(f"Hours post-ingestion must be 0.25-72")

    # Define substance properties
    substance_database = {
        "acetaminophen": {
            "toxic_dose_mg_kg": 150,
            "onset_hours": 0.5,
            "peak_hours": 4,
            "antidote": "N-acetylcysteine",
            "decontamination": True,
        },
        "iron": {
            "toxic_dose_mg_kg": 20,
            "onset_hours": 1,
            "peak_hours": 6,
            "antidote": "Deferoxamine",
            "decontamination": True,
        },
        "salicylate": {
            "toxic_dose_mg_kg": 150,
            "onset_hours": 0.5,
            "peak_hours": 6,
            "antidote": None,
            "decontamination": True,
        },
        "tricyclic_antidepressant": {
            "toxic_dose_mg_kg": 10,
            "onset_hours": 0.5,
            "peak_hours": 3,
            "antidote": None,
            "decontamination": True,
        },
        "calcium_channel_blocker": {
            "toxic_dose_mg_kg": 0.1,
            "onset_hours": 0.5,
            "peak_hours": 2,
            "antidote": "Calcium",
            "decontamination": True,
        },
    }

    # Get substance properties
    if substance.lower() in substance_database:
        props = substance_database[substance.lower()]
    else:
        props = {
            "toxic_dose_mg_kg": 100,
            "onset_hours": 1,
            "peak_hours": 6,
            "antidote": None,
            "decontamination": True,
        }

    # Calculate estimated toxicity
    if reported_dose_mg is not None:
        dose_mg_kg = reported_dose_mg / weight_kg
        toxic_dose = props["toxic_dose_mg_kg"]

        if dose_mg_kg < toxic_dose * 0.5:
            risk_category = "non_toxic"
            risk_score = 0
        elif dose_mg_kg < toxic_dose:
            risk_category = "low_risk"
            risk_score = 25
        elif dose_mg_kg < toxic_dose * 2:
            risk_category = "moderate_risk"
            risk_score = 50
        elif dose_mg_kg < toxic_dose * 5:
            risk_category = "high_risk"
            risk_score = 75
        else:
            risk_category = "critical"
            risk_score = 100
    else:
        # Default scoring if dose unknown
        risk_category = "moderate_risk"
        risk_score = 50

    # Adjust for symptoms
    if symptoms_present:
        risk_score = min(100, risk_score + 25)
        if risk_category == "low_risk":
            risk_category = "moderate_risk"
        elif risk_category == "moderate_risk":
            risk_category = "high_risk"

    # Adjust for time post-ingestion (absorption window)
    if hours_post_ingestion > 2 and not symptoms_present:
        risk_score = max(0, risk_score - 10)

    # Determine disposition
    if risk_score < 25:
        disposition = "outpatient_observation"
        severity = "asymptomatic"
        support_required = "Telephone follow-up"
    elif risk_score < 50:
        disposition = "hospital_observation"
        severity = "mild"
        support_required = "Monitoring with serial labs"
    elif risk_score < 75:
        disposition = "hospital_observation"
        severity = "moderate"
        support_required = "ICU-level monitoring if symptomatic"
    else:
        disposition = "icu"
        severity = "severe" if risk_score < 90 else "life_threatening"
        support_required = "ICU with intensive monitoring"

    # Clinical recommendation
    if props["decontamination"]:
        recommendation = f"Consider activated charcoal if within 1-2 hours of ingestion; "
    else:
        recommendation = "No specific decontamination; "

    if props["antidote"]:
        recommendation += f"Antidote ({props['antidote']}) available and indicated if elevated levels"
    else:
        recommendation += "Supportive care with specific monitoring"

    return ToxicIngestionRiskAssessmentResult(
        risk_score=risk_score,
        risk_category=risk_category,
        estimated_toxicity_severity=severity,
        onset_hours=int(props["onset_hours"]),
        peak_toxicity_hours=int(props["peak_hours"]),
        substance_type=substance,
        decontamination_indicated=props["decontamination"],
        antidote_available=props["antidote"] is not None,
        antidote_name=props["antidote"],
        supportive_care_required=support_required,
        disposition=disposition,
        clinical_recommendation=recommendation,
    )
