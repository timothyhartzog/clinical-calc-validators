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

__version__ = "0.1.0"
__author__ = "Timothy Hartzog, MD"

from . import pediatric

__all__ = [
    "pediatric",
]
