"""Pediatric clinical calculations module."""

from .dosing import (
    Indication,
    Route,
    DoseCalculation,
    amoxicillin_dose,
    gentamicin_dose,
    cefotaxime_dose,
    dose_to_dict,
)

from .hemodynamics import (
    MeanArterialPressureResult,
    CardiacOutputResult,
    CardiacIndexResult,
    VascularResistanceResult,
    ShockIndexResult,
    BodySurfaceAreaResult,
    CerebralPerfusionPressureResult,
    mean_arterial_pressure,
    cardiac_output,
    cardiac_index,
    systemic_vascular_resistance,
    shock_index,
    body_surface_area,
    cerebral_perfusion_pressure,
)

__all__ = [
    # Dosing
    "Indication",
    "Route",
    "DoseCalculation",
    "amoxicillin_dose",
    "gentamicin_dose",
    "cefotaxime_dose",
    "dose_to_dict",
    # Hemodynamics
    "MeanArterialPressureResult",
    "CardiacOutputResult",
    "CardiacIndexResult",
    "VascularResistanceResult",
    "ShockIndexResult",
    "BodySurfaceAreaResult",
    "CerebralPerfusionPressureResult",
    "mean_arterial_pressure",
    "cardiac_output",
    "cardiac_index",
    "systemic_vascular_resistance",
    "shock_index",
    "body_surface_area",
    "cerebral_perfusion_pressure",
]
