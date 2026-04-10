"""
Pediatric Severity Scores and Clinical Assessments

APGAR score, NEWS (National Early Warning Score), and other severity indices.

References:
    - Apgar V. Proposal for a new method of evaluation of the newborn infant.
      Anesth Analg. 1953;32:260-267
    - Royal College of Physicians. National Early Warning Score (NEWS).
      London: RCP; 2012
"""

from dataclasses import dataclass
from typing import Literal, Dict
from enum import Enum


class ApgarComponent(Enum):
    """APGAR score components."""
    APPEARANCE = "appearance"  # skin color
    PULSE = "pulse"  # heart rate
    GRIMACE = "grimace"  # reflex irritability/response
    ACTIVITY = "activity"  # muscle tone
    RESPIRATION = "respiration"  # respiratory effort


@dataclass
class ApgarResult:
    """Result of APGAR score calculation."""
    total_score: int  # 0-10
    appearance: int  # 0-2 (pink, acrocyanotic, pale)
    pulse: int  # 0-2 (absent, <100, >100)
    grimace: int  # 0-2 (no response, grimace, cry)
    activity: int  # 0-2 (limp, some flexion, active)
    respiration: int  # 0-2 (absent, weak, strong)

    interpretation: str
    clinical_action: str

    # Timing
    time_minutes: int  # 1 or 5 minute score


def apgar_score(
    appearance: int,
    pulse: int,
    grimace: int,
    activity: int,
    respiration: int,
    time_minutes: int = 1
) -> ApgarResult:
    """
    Calculate APGAR score at 1 or 5 minutes of life.

    APGAR components (each scored 0-2):
    A - Appearance (skin color): 0=pale/blue, 1=acrocyanosis, 2=pink
    P - Pulse (HR): 0=absent, 1=<100, 2=>100
    G - Grimace (reflex response): 0=none, 1=grimace, 2=cry
    A - Activity (muscle tone): 0=limp, 1=some flexion, 2=active
    R - Respiration (effort): 0=absent, 1=weak, 2=strong/crying

    Total: 0-10 (higher is better)

    Args:
        appearance: 0, 1, or 2
        pulse: 0, 1, or 2
        grimace: 0, 1, or 2
        activity: 0, 1, or 2
        respiration: 0, 1, or 2
        time_minutes: 1 or 5 (when score was assigned)

    Returns:
        ApgarResult with score and interpretation

    Clinical interpretation:
        10: Perfect score (rare)
        8-10: Normal, no intervention needed
        7-7: Monitor closely
        4-6: Moderate depression, needs assistance
        0-3: Severe depression, immediate resuscitation needed

    Reference:
        Apgar V. Anesth Analg. 1953
    """

    # Validate inputs
    for component, value in [
        ("appearance", appearance),
        ("pulse", pulse),
        ("grimace", grimace),
        ("activity", activity),
        ("respiration", respiration),
    ]:
        if value not in [0, 1, 2]:
            raise ValueError(f"{component} must be 0, 1, or 2, got {value}")

    if time_minutes not in [1, 5]:
        raise ValueError("time_minutes must be 1 or 5")

    total = appearance + pulse + grimace + activity + respiration

    # Interpretation
    if total == 10:
        interpretation = "Excellent"
        clinical_action = "Normal newborn care"
    elif total >= 8:
        interpretation = "Normal"
        clinical_action = "Normal newborn care"
    elif total == 7:
        interpretation = "Concerning"
        clinical_action = "Monitor closely, may need stimulation"
    elif total >= 4:
        interpretation = "Moderate depression"
        clinical_action = "Assist with ventilation, consider intubation"
    else:
        interpretation = "Severe depression"
        clinical_action = "Immediate resuscitation, intubation likely needed"

    return ApgarResult(
        total_score=total,
        appearance=appearance,
        pulse=pulse,
        grimace=grimace,
        activity=activity,
        respiration=respiration,
        interpretation=interpretation,
        clinical_action=clinical_action,
        time_minutes=time_minutes
    )


@dataclass
class NewsResult:
    """Result of NEWS (National Early Warning Score) calculation."""
    total_score: int
    respiration_rate: int
    oxygen_saturation: int
    temperature: int
    systolic_bp: int
    heart_rate: int
    consciousness: int

    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    recommended_action: str


def news_pediatric(
    respiration_rate: int,
    oxygen_saturation: float,
    temperature_c: float,
    systolic_bp: int,
    heart_rate: int,
    alert: bool = True
) -> NewsResult:
    """
    Calculate NEWS (National Early Warning Score) for pediatric patient.

    NOTE: This is a simplified version adapted for pediatric use.
    Official NEWS is designed for adults. Use age-specific normal ranges.

    Components scored 0-3 points:
    - Respiration rate (breaths/min)
    - Oxygen saturation (%)
    - Temperature (°C)
    - Systolic BP (mmHg)
    - Heart rate (bpm)
    - Consciousness (Alert vs altered)

    Args:
        respiration_rate: Breaths per minute
        oxygen_saturation: 0-100%
        temperature_c: Temperature in Celsius
        systolic_bp: Systolic blood pressure in mmHg
        heart_rate: Heart rate in bpm
        alert: True if patient alert, False if altered consciousness

    Returns:
        NewsResult with score and risk level

    Total score interpretation:
        0-4: Low risk
        5-6: Medium risk
        7+: High risk (may need escalation of care)

    Reference:
        Royal College of Physicians. National Early Warning Score. 2012

    WARNING:
        This is a simplified pediatric adaptation. Use age-specific
        vital sign ranges and consult pediatric guidelines.
    """

    rr_score = 0
    if respiration_rate < 8 or respiration_rate > 25:
        rr_score = 3
    elif respiration_rate <= 10 or respiration_rate >= 21:
        rr_score = 2
    elif respiration_rate <= 12 or respiration_rate >= 20:
        rr_score = 1

    o2_score = 0
    if oxygen_saturation < 92:
        o2_score = 3
    elif oxygen_saturation < 94:
        o2_score = 2
    elif oxygen_saturation < 95:
        o2_score = 1

    temp_score = 0
    if temperature_c < 35.1 or temperature_c > 39.0:
        temp_score = 3
    elif temperature_c <= 36 or temperature_c >= 38.1:
        temp_score = 2
    elif temperature_c <= 36.4 or temperature_c >= 37.5:
        temp_score = 1

    bp_score = 0
    if systolic_bp < 90 or systolic_bp > 220:
        bp_score = 3
    elif systolic_bp < 100 or systolic_bp > 200:
        bp_score = 2
    elif systolic_bp < 110 or systolic_bp > 180:
        bp_score = 1

    hr_score = 0
    if heart_rate < 40 or heart_rate > 130:
        hr_score = 3
    elif heart_rate < 50 or heart_rate > 120:
        hr_score = 2
    elif heart_rate < 60 or heart_rate > 110:
        hr_score = 1

    consciousness_score = 0 if alert else 3

    total = rr_score + o2_score + temp_score + bp_score + hr_score + consciousness_score

    if total <= 4:
        risk_level = "LOW"
        recommended_action = "Routine care, reassess regularly"
    elif total <= 6:
        risk_level = "MEDIUM"
        recommended_action = "Increased monitoring, consider escalation"
    else:
        risk_level = "HIGH"
        recommended_action = "Urgent review, consider ICU/escalation"

    return NewsResult(
        total_score=total,
        respiration_rate=rr_score,
        oxygen_saturation=o2_score,
        temperature=temp_score,
        systolic_bp=bp_score,
        heart_rate=hr_score,
        consciousness=consciousness_score,
        risk_level=risk_level,
        recommended_action=recommended_action
    )
