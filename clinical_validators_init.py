"""
Clinical Calculation Validators
Reference implementations of pediatric/neonatal clinical calculations in Python.

Each calculation is:
- Sourced from peer-reviewed literature or official guidelines
- Verified against authoritative reference data  
- Tested with golden cases
- Cross-validated across languages

Repository: timothyhartzog/clinical-calc-validators
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Timothy Hartzog, MD"

from .utilities.constants import *
from .utilities.unit_conversion import *
from .pediatric import dosing as pediatric_dosing
from .pediatric import growth as pediatric_growth
from .pediatric import scores as pediatric_scores
from .neonatal import fenton_growth as neonatal_growth
from .neonatal import severity_scores as neonatal_scores

__all__ = [
    "pediatric_dosing",
    "pediatric_growth", 
    "pediatric_scores",
    "neonatal_growth",
    "neonatal_scores",
]
