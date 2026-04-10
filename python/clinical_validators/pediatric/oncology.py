"""
Pediatric Oncology Assessment Module

Provides comprehensive assessment functions for pediatric cancer patients:
- Tumor risk stratification based on prognostic factors
- Chemotherapy-induced acute toxicity scoring (CTCAE v5.0)
- Cardiotoxicity risk assessment for cardiotoxic agents
- Hematologic recovery monitoring post-chemotherapy
- Neutropenia infection risk stratification

All functions follow established pediatric oncology guidelines from COG, NCCN, and
the Children's Oncology Group.

Author: Timothy Hartzog, MD
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Optional


# =============================================================================
# RESULT DATACLASSES
# =============================================================================


@dataclass
class TumorRiskStratificationResult:
    """Result of tumor risk stratification assessment."""

    age_years: float
    tumor_type: str
    stage: int
    risk_group: str  # "low", "intermediate", "high", "very_high"
    risk_score: int  # 0-100
    prognostic_factors_present: int  # count
    recommended_intensity: str  # "standard", "intensified", "very_intensive"
    clinical_recommendation: str


@dataclass
class CTCAEToxicityResult:
    """Result of CTCAE toxicity assessment."""

    age_years: float
    chemotherapy_agents: list[str]
    days_since_treatment: int
    hematologic_grade: int  # 0-5
    hepatic_grade: int  # 0-5
    renal_grade: int  # 0-5
    gi_grade: int  # 0-5
    neurologic_grade: int  # 0-5
    overall_max_grade: int  # 0-5
    toxicity_management: str
    clinical_recommendation: str


@dataclass
class CardiotoxicityRiskResult:
    """Result of cardiotoxicity risk assessment."""

    age_years: float
    cumulative_anthracycline_dose: float
    risk_category: str  # "low", "intermediate", "high"
    estimated_toxicity_probability_percent: float  # 0-100
    ejection_fraction_threshold: float  # safe lower limit
    monitoring_frequency_months: int
    recommended_cardioprotection: str  # "none", "ace_inhibitor", "beta_blocker", "combination"
    clinical_recommendation: str


@dataclass
class HematologicRecoveryResult:
    """Result of hematologic recovery assessment."""

    age_years: float
    chemotherapy_regimen: str
    recovery_phase: str  # "expected_nadir", "recovery", "recovered", "delayed"
    neutropenia_severity: str  # "none", "mild", "moderate", "severe", "profound"
    infection_risk_level: str  # "low", "moderate", "high", "critical"
    transfusion_threshold_triggered: bool
    estimated_recovery_days: Optional[int]
    clinical_recommendation: str


@dataclass
class NeutropeniaInfectionRiskResult:
    """Result of neutropenia infection risk assessment."""

    age_years: float
    absolute_neutrophil_count: float
    infection_risk_score: int  # 0-100
    risk_category: str  # "low", "moderate", "high", "very_high"
    sepsis_probability_percent: float  # 0-100
    recommended_prophylaxis: list[str]
    hospitalization_threshold_met: bool
    clinical_recommendation: str


# =============================================================================
# TUMOR RISK STRATIFICATION
# =============================================================================


def tumor_risk_stratification(
    age_years: float,
    tumor_type: str,
    stage: int,
    grade: Optional[int],
    cytogenetics_risk: str,
    other_risk_factors: int,
) -> TumorRiskStratificationResult:
    """
    Stratify pediatric tumor risk based on prognostic factors.

    Args:
        age_years: Patient age in years (0-18)
        tumor_type: Type of tumor ("lymphoma", "leukemia", "solid_tumor", "neuroblastoma")
        stage: Tumor stage (1-4)
        grade: Tumor grade (1-3 or None)
        cytogenetics_risk: Cytogenetics risk ("favorable", "intermediate", "unfavorable")
        other_risk_factors: Number of additional adverse factors

    Returns:
        TumorRiskStratificationResult with risk group and recommendations

    Raises:
        ValueError: If inputs are outside valid ranges
    """
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18 years, got {age_years}")
    if not 1 <= stage <= 4:
        raise ValueError(f"Stage must be 1-4, got {stage}")
    if grade is not None and not 1 <= grade <= 3:
        raise ValueError(f"Grade must be 1-3 or None, got {grade}")
    if cytogenetics_risk not in ["favorable", "intermediate", "unfavorable"]:
        raise ValueError(f"Cytogenetics risk must be favorable/intermediate/unfavorable, got {cytogenetics_risk}")
    if other_risk_factors < 0:
        raise ValueError(f"Risk factors must be >= 0, got {other_risk_factors}")

    valid_tumor_types = ["lymphoma", "leukemia", "solid_tumor", "neuroblastoma", "brain_tumor"]
    if tumor_type not in valid_tumor_types:
        raise ValueError(f"Tumor type must be one of {valid_tumor_types}, got {tumor_type}")

    # Base score by tumor type and stage
    base_scores = {
        "lymphoma": {1: 15, 2: 25, 3: 35, 4: 50},
        "leukemia": {1: 20, 2: 35, 3: 50, 4: 60},
        "neuroblastoma": {1: 10, 2: 30, 3: 50, 4: 60},
        "solid_tumor": {1: 20, 2: 35, 3: 50, 4: 60},
        "brain_tumor": {1: 25, 2: 40, 3: 55, 4: 65},
    }

    base_score = base_scores.get(tumor_type, {}).get(stage, 30)

    # Cytogenetics adjustment
    cyto_adjustment = {"favorable": -10, "intermediate": 0, "unfavorable": 10}
    cyto_adjust = cyto_adjustment.get(cytogenetics_risk, 0)

    # Age adjustment
    age_adjust = 5 if (age_years < 5 or age_years > 15) else 0

    # Grade adjustment
    grade_adjust = 0 if grade is None else (grade - 1) * 5

    # Other risk factors
    other_adjust = other_risk_factors * 5

    # Calculate final score
    risk_score = max(0, min(100, base_score + cyto_adjust + age_adjust + grade_adjust + other_adjust))

    # Determine risk group
    if risk_score <= 25:
        risk_group = "low"
        intensity = "standard"
    elif risk_score <= 50:
        risk_group = "intermediate"
        intensity = "intensified"
    elif risk_score <= 75:
        risk_group = "high"
        intensity = "intensified"
    else:
        risk_group = "very_high"
        intensity = "very_intensive"

    # Prognostic factors count
    prognostic_factors = other_risk_factors
    if cytogenetics_risk == "unfavorable":
        prognostic_factors += 1

    # Clinical recommendation
    if risk_group == "low":
        recommendation = (
            "Low-risk disease. Standard chemotherapy protocol recommended. "
            "Excellent prognosis with cure rates >85%. Plan 2-year follow-up after completion."
        )
    elif risk_group == "intermediate":
        recommendation = (
            "Intermediate-risk disease. Intensified chemotherapy recommended. "
            "Good prognosis with cure rates 70-85%. Enhanced monitoring for toxicity."
        )
    elif risk_group == "high":
        recommendation = (
            "High-risk disease. Intensified chemotherapy required. "
            "Cure rates 50-70%. Consider referral to specialized center. "
            "Enhanced supportive care needed."
        )
    else:  # very_high
        recommendation = (
            "Very high-risk disease. Referral to specialized pediatric oncology center strongly advised. "
            "Consider participation in clinical trials. Cure rates <50%. "
            "Very intensive therapy with stem cell transplantation consideration."
        )

    return TumorRiskStratificationResult(
        age_years=age_years,
        tumor_type=tumor_type,
        stage=stage,
        risk_group=risk_group,
        risk_score=int(risk_score),
        prognostic_factors_present=prognostic_factors,
        recommended_intensity=intensity,
        clinical_recommendation=recommendation,
    )


# =============================================================================
# CTCAE TOXICITY SCORING
# =============================================================================


def ctcae_toxicity_scoring(
    age_years: float,
    chemotherapy_agents: list[str],
    days_since_treatment: int,
    laboratory_values: dict,
    clinical_symptoms: dict,
) -> CTCAEToxicityResult:
    """
    Score acute chemotherapy-induced toxicity using CTCAE v5.0 criteria.

    Args:
        age_years: Patient age in years (0-18)
        chemotherapy_agents: List of chemotherapy agents given
        days_since_treatment: Days since chemotherapy administration
        laboratory_values: Dict with keys: wbc_k_ul, platelets_k_ul, hemoglobin_g_dl,
                          creatinine_mg_dl, alt_u_l, ast_u_l, bilirubin_mg_dl
        clinical_symptoms: Dict with keys: nausea (0-2), vomiting (0-2), diarrhea (0-2),
                          mucositis (0-5), neuropathy (0-5), fever (bool)

    Returns:
        CTCAEToxicityResult with organ-specific grades and recommendations

    Raises:
        ValueError: If inputs are invalid
    """
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18 years, got {age_years}")
    if days_since_treatment < 0:
        raise ValueError(f"Days since treatment must be >= 0, got {days_since_treatment}")

    # Extract lab values with defaults
    wbc = laboratory_values.get("wbc_k_ul", 1.5)
    platelets = laboratory_values.get("platelets_k_ul", 150)
    hemoglobin = laboratory_values.get("hemoglobin_g_dl", 12)
    creatinine = laboratory_values.get("creatinine_mg_dl", 0.5)
    alt = laboratory_values.get("alt_u_l", 40)
    ast = laboratory_values.get("ast_u_l", 40)
    bilirubin = laboratory_values.get("bilirubin_mg_dl", 0.3)

    # Age-specific upper limit of normal for creatinine (approximately)
    if age_years < 1:
        creatinine_uln = 0.4
    elif age_years < 5:
        creatinine_uln = 0.5
    elif age_years < 10:
        creatinine_uln = 0.7
    else:
        creatinine_uln = 0.9

    # Hematologic grades (based on ANC in WBC)
    if wbc >= 1.5:
        hematologic_grade = 0
    elif wbc >= 1.0:
        hematologic_grade = 1
    elif wbc >= 0.5:
        hematologic_grade = 2
    elif wbc >= 0.1:
        hematologic_grade = 3
    else:
        hematologic_grade = 4

    # Platelet grades
    if platelets >= 150:
        platelet_grade = 0
    elif platelets >= 100:
        platelet_grade = 1
    elif platelets >= 50:
        platelet_grade = 2
    elif platelets >= 25:
        platelet_grade = 3
    else:
        platelet_grade = 4

    hematologic_grade = max(hematologic_grade, platelet_grade)

    # Hemoglobin grades
    if hemoglobin >= 10:
        hgb_grade = 0
    elif hemoglobin >= 8:
        hgb_grade = 1
    elif hemoglobin >= 6.5:
        hgb_grade = 2
    elif hemoglobin >= 5:
        hgb_grade = 3
    else:
        hgb_grade = 4

    hematologic_grade = max(hematologic_grade, hgb_grade)

    # Hepatic grades (AST/ALT, bilirubin)
    if alt <= 40 and ast <= 40:
        hepatic_grade = 0
    elif alt <= 100 and ast <= 100:
        hepatic_grade = 1
    elif alt <= 250 and ast <= 250:
        hepatic_grade = 2
    elif alt <= 500 and ast <= 500:
        hepatic_grade = 3
    else:
        hepatic_grade = 4

    # Bilirubin grades
    if bilirubin <= 1.5:
        bili_grade = 0
    elif bilirubin <= 3:
        bili_grade = 1
    elif bilirubin <= 10:
        bili_grade = 2
    elif bilirubin <= 20:
        bili_grade = 3
    else:
        bili_grade = 4

    hepatic_grade = max(hepatic_grade, bili_grade)

    # Renal grades
    creatinine_ratio = creatinine / creatinine_uln if creatinine_uln > 0 else 1
    if creatinine_ratio <= 1:
        renal_grade = 0
    elif creatinine_ratio <= 1.5:
        renal_grade = 1
    elif creatinine_ratio <= 3:
        renal_grade = 2
    elif creatinine_ratio <= 6:
        renal_grade = 3
    else:
        renal_grade = 4

    # GI grades (from clinical symptoms)
    nausea_grade = clinical_symptoms.get("nausea", 0)
    vomiting_grade = clinical_symptoms.get("vomiting", 0)
    diarrhea_grade = clinical_symptoms.get("diarrhea", 0)
    gi_grade = max(nausea_grade, vomiting_grade, diarrhea_grade)

    # Neurologic grades (mucositis, neuropathy)
    mucositis_grade = clinical_symptoms.get("mucositis", 0)
    neuropathy_grade = clinical_symptoms.get("neuropathy", 0)
    neurologic_grade = max(min(mucositis_grade, 5), min(neuropathy_grade, 5))

    # Overall grade
    overall_max_grade = max(
        hematologic_grade,
        hepatic_grade,
        renal_grade,
        gi_grade,
        neurologic_grade,
    )

    # Toxicity management recommendations
    if overall_max_grade <= 2:
        toxicity_mgmt = "Continue monitoring. Supportive care as needed."
    elif overall_max_grade == 3:
        toxicity_mgmt = "Consider dose reduction or treatment delay. Increase monitoring frequency."
    else:  # 4-5
        toxicity_mgmt = (
            "Hold chemotherapy temporarily. Intensive supportive care required. "
            "Consider ICU-level monitoring if grade 5 toxicity."
        )

    # Clinical recommendation
    if overall_max_grade == 0:
        recommendation = "No adverse events. Continue current chemotherapy as planned."
    elif overall_max_grade == 1:
        recommendation = "Mild toxicity. Continue chemotherapy with supportive care."
    elif overall_max_grade == 2:
        recommendation = "Moderate toxicity. Monitor closely; consider supportive interventions."
    elif overall_max_grade == 3:
        recommendation = (
            "Severe toxicity. Evaluate for dose modification or treatment delay. "
            "Increase monitoring to 2-3 times weekly."
        )
    elif overall_max_grade == 4:
        recommendation = (
            "Life-threatening toxicity. Hold chemotherapy pending recovery. "
            "Intensive supportive/critical care required. Reassess treatment plan."
        )
    else:  # 5
        recommendation = "Fatal toxicity event. Review treatment protocol; prevent recurrence."

    return CTCAEToxicityResult(
        age_years=age_years,
        chemotherapy_agents=chemotherapy_agents,
        days_since_treatment=days_since_treatment,
        hematologic_grade=hematologic_grade,
        hepatic_grade=hepatic_grade,
        renal_grade=renal_grade,
        gi_grade=gi_grade,
        neurologic_grade=neurologic_grade,
        overall_max_grade=overall_max_grade,
        toxicity_management=toxicity_mgmt,
        clinical_recommendation=recommendation,
    )


# =============================================================================
# CARDIOTOXICITY RISK ASSESSMENT
# =============================================================================


def cardiotoxicity_risk_assessment(
    age_years: float,
    cumulative_anthracycline_dose_mg_m2: float,
    trastuzumab_exposure_months: Optional[float],
    baseline_ejection_fraction_percent: float,
    baseline_shortening_fraction_percent: Optional[float],
    previous_cardiotoxicity: bool,
    family_history_cardiomyopathy: bool,
    other_cardiac_drugs: list[str],
) -> CardiotoxicityRiskResult:
    """
    Assess risk of chemotherapy-induced cardiotoxicity.

    Args:
        age_years: Patient age in years (0-18)
        cumulative_anthracycline_dose_mg_m2: Total doxorubicin-equivalent dose (mg/m²)
        trastuzumab_exposure_months: Months of trastuzumab therapy (optional)
        baseline_ejection_fraction_percent: Baseline EF (20-80%)
        baseline_shortening_fraction_percent: Baseline SF (15-40%, optional)
        previous_cardiotoxicity: Prior cardiotoxicity history
        family_history_cardiomyopathy: Family history of cardiomyopathy
        other_cardiac_drugs: List of other potentially cardiotoxic drugs

    Returns:
        CardiotoxicityRiskResult with risk category and monitoring recommendations

    Raises:
        ValueError: If inputs are outside valid ranges
    """
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18 years, got {age_years}")
    if not 0 <= cumulative_anthracycline_dose_mg_m2 <= 500:
        raise ValueError(f"Anthracycline dose must be 0-500 mg/m², got {cumulative_anthracycline_dose_mg_m2}")
    if not 20 <= baseline_ejection_fraction_percent <= 80:
        raise ValueError(f"EF must be 20-80%, got {baseline_ejection_fraction_percent}")
    if baseline_shortening_fraction_percent is not None:
        if not 15 <= baseline_shortening_fraction_percent <= 40:
            raise ValueError(f"SF must be 15-40%, got {baseline_shortening_fraction_percent}")
    if trastuzumab_exposure_months is not None and trastuzumab_exposure_months < 0:
        raise ValueError(f"Trastuzumab exposure must be >= 0, got {trastuzumab_exposure_months}")

    # Base risk from anthracycline dose
    if cumulative_anthracycline_dose_mg_m2 < 100:
        dose_risk = 2.0
    elif cumulative_anthracycline_dose_mg_m2 < 200:
        dose_risk = 5.0
    elif cumulative_anthracycline_dose_mg_m2 < 300:
        dose_risk = 12.0
    elif cumulative_anthracycline_dose_mg_m2 < 400:
        dose_risk = 20.0
    else:
        dose_risk = 30.0

    # Trastuzumab adds synergistic risk
    if trastuzumab_exposure_months is not None and trastuzumab_exposure_months > 0:
        dose_risk += 12.0  # Additional 12% risk with trastuzumab

    # Age factor (younger children have higher relative risk)
    if age_years < 5:
        dose_risk *= 1.3
    elif age_years > 15:
        dose_risk *= 0.8

    # Baseline EF impact
    if baseline_ejection_fraction_percent < 50:
        dose_risk *= 1.5
    elif baseline_ejection_fraction_percent < 60:
        dose_risk *= 1.2

    # Previous cardiotoxicity
    if previous_cardiotoxicity:
        dose_risk *= 1.5

    # Family history
    if family_history_cardiomyopathy:
        dose_risk *= 1.2

    # Other cardiac drugs (e.g., tyrosine kinase inhibitors, checkpoint inhibitors)
    if other_cardiac_drugs:
        dose_risk *= 1.1

    # Clamp to 0-100%
    estimated_risk = min(100.0, dose_risk)

    # Determine risk category
    if estimated_risk < 10:
        risk_category = "low"
        monitoring_frequency = 12  # annual
    elif estimated_risk < 25:
        risk_category = "intermediate"
        monitoring_frequency = 6  # every 6 months
    else:
        risk_category = "high"
        monitoring_frequency = 3  # every 3 months

    # EF threshold (should not drop below)
    if baseline_ejection_fraction_percent >= 60:
        ef_threshold = 50.0
    elif baseline_ejection_fraction_percent >= 50:
        ef_threshold = 45.0
    else:
        ef_threshold = 40.0

    # Cardioprotection recommendations
    if risk_category == "low":
        cardioprotection = "none"
        protection_text = "No cardioprotection required at current dose level."
    elif risk_category == "intermediate":
        if cumulative_anthracycline_dose_mg_m2 > 200:
            cardioprotection = "ace_inhibitor"
            protection_text = "Start ACE inhibitor for cardiomyopathy prevention."
        else:
            cardioprotection = "none"
            protection_text = "Monitor for signs of decline; consider ACE inhibitor if EF drops >10%."
    else:  # high
        if trastuzumab_exposure_months and trastuzumab_exposure_months > 0:
            cardioprotection = "combination"
            protection_text = (
                "Start both ACE inhibitor and beta-blocker for cardioprotection. "
                "Consider cardiology co-management."
            )
        else:
            cardioprotection = "beta_blocker"
            protection_text = "Start beta-blocker; consider ACE inhibitor if EF declines."

    recommendation = (
        f"Risk category: {risk_category} ({estimated_risk:.0f}% estimated toxicity risk). "
        f"Recommend echocardiography every {monitoring_frequency} months. "
        f"{protection_text} "
        f"Monitor for signs of heart failure (dyspnea, edema, exercise intolerance)."
    )

    return CardiotoxicityRiskResult(
        age_years=age_years,
        cumulative_anthracycline_dose=cumulative_anthracycline_dose_mg_m2,
        risk_category=risk_category,
        estimated_toxicity_probability_percent=round(estimated_risk, 1),
        ejection_fraction_threshold=ef_threshold,
        monitoring_frequency_months=monitoring_frequency,
        recommended_cardioprotection=cardioprotection,
        clinical_recommendation=recommendation,
    )


# =============================================================================
# HEMATOLOGIC RECOVERY ASSESSMENT
# =============================================================================


def hematologic_recovery_assessment(
    age_years: float,
    chemotherapy_regimen: str,
    baseline_wbc_k_ul: float,
    baseline_platelets_k_ul: float,
    current_wbc_k_ul: float,
    current_platelets_k_ul: float,
    days_since_chemotherapy: int,
    g_csf_support: bool,
    infection_present: bool,
) -> HematologicRecoveryResult:
    """
    Assess hematologic recovery post-chemotherapy.

    Args:
        age_years: Patient age in years (0-18)
        chemotherapy_regimen: Type of regimen ("standard", "intensive", "stem_cell_transplant")
        baseline_wbc_k_ul: Baseline WBC (k/µL)
        baseline_platelets_k_ul: Baseline platelets (k/µL)
        current_wbc_k_ul: Current WBC (k/µL)
        current_platelets_k_ul: Current platelets (k/µL)
        days_since_chemotherapy: Days since chemotherapy
        g_csf_support: G-CSF given
        infection_present: Active infection

    Returns:
        HematologicRecoveryResult with recovery phase and recommendations

    Raises:
        ValueError: If inputs are invalid
    """
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18 years, got {age_years}")
    if days_since_chemotherapy < 0:
        raise ValueError(f"Days since chemotherapy must be >= 0, got {days_since_chemotherapy}")
    if current_wbc_k_ul < 0 or current_wbc_k_ul > 100:
        raise ValueError(f"WBC must be 0-100 k/µL, got {current_wbc_k_ul}")
    if current_platelets_k_ul < 0 or current_platelets_k_ul > 500:
        raise ValueError(f"Platelets must be 0-500 k/µL, got {current_platelets_k_ul}")

    valid_regimens = ["standard", "intensive", "stem_cell_transplant"]
    if chemotherapy_regimen not in valid_regimens:
        raise ValueError(f"Regimen must be one of {valid_regimens}, got {chemotherapy_regimen}")

    # Expected nadir timing by regimen
    nadir_days = {"standard": 10, "intensive": 12, "stem_cell_transplant": 14}
    expected_nadir = nadir_days.get(chemotherapy_regimen, 10)

    # Recovery timeline estimation
    if g_csf_support:
        recovery_timeline = 14 if chemotherapy_regimen == "standard" else 18
    else:
        recovery_timeline = 21 if chemotherapy_regimen == "standard" else 28

    # Determine recovery phase
    if days_since_chemotherapy < expected_nadir:
        recovery_phase = "expected_nadir"
        estimated_recovery = expected_nadir
    elif days_since_chemotherapy < expected_nadir + 7:
        recovery_phase = "recovery"
        estimated_recovery = recovery_timeline
    elif current_wbc_k_ul > 1.0 and current_platelets_k_ul > 100:
        recovery_phase = "recovered"
        estimated_recovery = None
    else:
        recovery_phase = "delayed"
        estimated_recovery = recovery_timeline + 7

    # Neutropenia severity
    if current_wbc_k_ul >= 1.5:
        neutropenia_severity = "none"
    elif current_wbc_k_ul >= 1.0:
        neutropenia_severity = "mild"
    elif current_wbc_k_ul >= 0.5:
        neutropenia_severity = "moderate"
    elif current_wbc_k_ul >= 0.1:
        neutropenia_severity = "severe"
    else:
        neutropenia_severity = "profound"

    # Infection risk based on WBC and clinical factors
    if current_wbc_k_ul >= 1.0 and not infection_present:
        infection_risk_level = "low"
    elif current_wbc_k_ul >= 0.5 or (current_wbc_k_ul >= 0.1 and not infection_present):
        infection_risk_level = "moderate"
    elif current_wbc_k_ul < 0.1 or (current_wbc_k_ul < 0.5 and infection_present):
        infection_risk_level = "high"
    else:
        infection_risk_level = "critical"

    # Transfusion thresholds
    platelet_threshold = 10 if not infection_present else 20
    transfusion_triggered = current_platelets_k_ul < platelet_threshold

    # Clinical recommendation
    if recovery_phase == "expected_nadir":
        recommendation = (
            "Expected nadir phase. Monitor blood counts daily. "
            "Prepare for potential infection; consider antimicrobial prophylaxis. "
            f"Blood count recovery expected in {recovery_timeline - days_since_chemotherapy} days."
        )
    elif recovery_phase == "recovery":
        recommendation = (
            "Recovery phase in progress. Continue daily monitoring until counts normalize. "
            f"Expected full recovery in {estimated_recovery - days_since_chemotherapy} days. "
            "May resume standard prophylaxis once ANC >500 and platelets >50k."
        )
    elif recovery_phase == "recovered":
        recommendation = (
            "Hematologic recovery achieved. Can resume outpatient management. "
            "Continue monitoring weekly until stable for 2 weeks. "
            "Plan next chemotherapy cycle as appropriate."
        )
    else:  # delayed
        recommendation = (
            "Delayed hematologic recovery. Evaluate for infection, medications, "
            "underlying marrow disease. Consider growth factor support if not already given. "
            "May need additional supportive care (transfusions, antibiotics)."
        )

    return HematologicRecoveryResult(
        age_years=age_years,
        chemotherapy_regimen=chemotherapy_regimen,
        recovery_phase=recovery_phase,
        neutropenia_severity=neutropenia_severity,
        infection_risk_level=infection_risk_level,
        transfusion_threshold_triggered=transfusion_triggered,
        estimated_recovery_days=estimated_recovery,
        clinical_recommendation=recommendation,
    )


# =============================================================================
# NEUTROPENIA INFECTION RISK
# =============================================================================


def neutropenia_infection_risk(
    age_years: float,
    absolute_neutrophil_count_k_ul: float,
    days_of_neutropenia: int,
    chemotherapy_intensity: str,
    fever_present: bool,
    mucositis_grade: int,
    indwelling_catheter: bool,
    previous_infections: int,
    nutritional_status: str,
) -> NeutropeniaInfectionRiskResult:
    """
    Assess infection risk in neutropenic patients.

    Args:
        age_years: Patient age in years (0-18)
        absolute_neutrophil_count_k_ul: ANC in k/µL
        days_of_neutropenia: Number of days with ANC <1.5
        chemotherapy_intensity: "standard" or "intensive"
        fever_present: Current fever
        mucositis_grade: Mucositis grade (0-5)
        indwelling_catheter: Central line present
        previous_infections: Number of previous infections during treatment
        nutritional_status: "well_nourished", "malnourished", "severely_malnourished"

    Returns:
        NeutropeniaInfectionRiskResult with risk score and recommendations

    Raises:
        ValueError: If inputs are invalid
    """
    if not 0 <= age_years <= 18:
        raise ValueError(f"Age must be 0-18 years, got {age_years}")
    if not 0 <= absolute_neutrophil_count_k_ul <= 10:
        raise ValueError(f"ANC must be 0-10 k/µL, got {absolute_neutrophil_count_k_ul}")
    if days_of_neutropenia < 0:
        raise ValueError(f"Days of neutropenia must be >= 0, got {days_of_neutropenia}")
    if not 0 <= mucositis_grade <= 5:
        raise ValueError(f"Mucositis grade must be 0-5, got {mucositis_grade}")
    if previous_infections < 0:
        raise ValueError(f"Previous infections must be >= 0, got {previous_infections}")
    if chemotherapy_intensity not in ["standard", "intensive"]:
        raise ValueError(f"Intensity must be standard or intensive, got {chemotherapy_intensity}")

    valid_status = ["well_nourished", "malnourished", "severely_malnourished"]
    if nutritional_status not in valid_status:
        raise ValueError(f"Nutritional status must be one of {valid_status}, got {nutritional_status}")

    # Risk scoring (0-100)
    risk_score = 0

    # ANC severity (0-40 points)
    if absolute_neutrophil_count_k_ul >= 1.0:
        anc_score = 0
    elif absolute_neutrophil_count_k_ul >= 0.5:
        anc_score = 10
    elif absolute_neutrophil_count_k_ul >= 0.1:
        anc_score = 20
    else:
        anc_score = 40
    risk_score += anc_score

    # Duration of neutropenia (0-20 points)
    if days_of_neutropenia <= 7:
        duration_score = 5
    elif days_of_neutropenia <= 14:
        duration_score = 10
    else:
        duration_score = 20
    risk_score += duration_score

    # Chemotherapy intensity (0-15 points)
    intensity_score = 15 if chemotherapy_intensity == "intensive" else 0
    risk_score += intensity_score

    # Clinical factors (0-25 points)
    clinical_score = 0
    if fever_present:
        clinical_score += 10
    clinical_score += mucositis_grade  # 0-5 points
    if indwelling_catheter:
        clinical_score += 5
    clinical_score += min(previous_infections * 2, 10)  # 0-10 points for infection history

    # Nutrition
    if nutritional_status == "severely_malnourished":
        clinical_score += 5
    elif nutritional_status == "malnourished":
        clinical_score += 2

    risk_score += min(clinical_score, 25)

    # Determine risk category
    if risk_score <= 25:
        risk_category = "low"
    elif risk_score <= 50:
        risk_category = "moderate"
    elif risk_score <= 75:
        risk_category = "high"
    else:
        risk_category = "very_high"

    # Estimate sepsis probability (log-linear model)
    sepsis_probability = min(100.0, 5.0 + (risk_score * 0.8))

    # Prophylaxis recommendations
    prophylaxis = []
    if risk_category == "low":
        prophylaxis = ["standard precautions", "daily monitoring"]
    elif risk_category == "moderate":
        prophylaxis = ["fluoroquinolone prophylaxis", "daily CBC monitoring"]
    elif risk_category == "high":
        prophylaxis = [
            "fluoroquinolone prophylaxis",
            "antifungal prophylaxis (fluconazole or itraconazole)",
            "twice-daily monitoring",
        ]
    else:  # very_high
        prophylaxis = [
            "hospitalization strongly recommended",
            "broad-spectrum antibiotics (empiric)",
            "antifungal coverage",
            "intensive monitoring (vital signs q2-4h)",
        ]

    # Hospitalization threshold
    hospitalization_threshold = risk_category in ["high", "very_high"] or fever_present

    # Clinical recommendation
    if risk_category == "low":
        recommendation = (
            "Low infection risk. Outpatient management appropriate. "
            "Monitor CBC daily; educate on fever precautions. Contact clinic if fever develops."
        )
    elif risk_category == "moderate":
        recommendation = (
            "Moderate infection risk. Consider outpatient vs inpatient management. "
            "If outpatient: daily CBC, fluoroquinolone prophylaxis, able to contact rapidly. "
            "If inpatient: 1-2 times daily monitoring, IV antibiotics if fever."
        )
    elif risk_category == "high":
        recommendation = (
            "High infection risk. Hospitalization recommended. "
            "IV fluoroquinolone and antifungal prophylaxis. Obtain cultures before empiric antibiotics "
            "if fever develops. Monitor vitals q4h. May consider ICU if sepsis develops."
        )
    else:  # very_high
        recommendation = (
            "Very high infection/sepsis risk. Hospitalization strongly recommended. "
            "Intensive monitoring in ICU if possible. Prophylactic empiric antibiotics may be warranted. "
            "Any fever requires immediate physician evaluation and blood cultures. "
            "Assess nutritional status and address deficiencies."
        )

    return NeutropeniaInfectionRiskResult(
        age_years=age_years,
        absolute_neutrophil_count=absolute_neutrophil_count_k_ul,
        infection_risk_score=int(risk_score),
        risk_category=risk_category,
        sepsis_probability_percent=round(sepsis_probability, 1),
        recommended_prophylaxis=prophylaxis,
        hospitalization_threshold_met=hospitalization_threshold,
        clinical_recommendation=recommendation,
    )
