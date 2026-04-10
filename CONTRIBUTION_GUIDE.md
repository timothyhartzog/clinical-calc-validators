# Contributing New Clinical Calculations

This guide walks through adding a new clinical calculation to the framework. We'll use an example calculation to illustrate the process.

**Estimated time:** 2-3 hours per function

---

## 📋 Quick Reference Checklist

For each new calculation, complete these steps in order:

- [ ] Research & document the calculation
- [ ] Implement in Python with docstrings
- [ ] Create 2-3 golden cases (JSON)
- [ ] Write unit tests (Python)
- [ ] Port to R with Roxygen documentation
- [ ] Write R tests
- [ ] Update project documentation
- [ ] Verify CI/CD passes
- [ ] Submit pull request

---

## Step 1: Research & Documentation

### 1.1 Identify Authoritative Source

Find the clinical reference for your calculation:

- **Pediatric dosing:** AAP Red Book, Lexi-Drugs, UpToDate
- **Hemodynamics:** ACCM PALS, ACLS, cardiology textbooks
- **Renal:** KDIGO guidelines, nephrology references
- **Growth:** CDC/WHO growth curves, Fenton charts
- **Scoring:** Original publication of the score

### 1.2 Document the Calculation

Create a brief technical specification:

```
EXAMPLE: Mean Arterial Pressure (MAP)

Formula: MAP = (SBP + 2×DBP) / 3

Parameters:
  - Systolic BP (mmHg): 0-300
  - Diastolic BP (mmHg): 0-200

Returns: MAP (mmHg)

Clinical Notes:
  - Normal MAP in children: 50-95 mmHg (age-dependent)
  - MAP <50 mmHg indicates shock
  - Used in perfusion pressure calculations

References:
  - PALS Textbook
  - Circulation. 2015;132(16_suppl_2):S444-S482
```

---

## Step 2: Python Implementation

### 2.1 Create Module File

Create a file in the appropriate submodule:

```
python/clinical_validators/
├── pediatric/
│   ├── dosing.py          (medication dosing)
│   ├── fluids.py          (fluids & electrolytes)
│   ├── scores.py          (APGAR, NEWS)
│   ├── hemodynamics.py    (new: cardiac output, MAP, etc.) ← ADD HERE
│   ├── respiratory.py     (new: oxygen indices)
│   └── growth.py          (growth percentiles)
├── neonatal/
│   ├── fenton_growth.py
│   └── assessment.py
└── utilities.py
```

### 2.2 Implement the Function

```python
"""
Pediatric Hemodynamic Calculations

Formula and clinical references here.
"""

from dataclasses import dataclass

@dataclass
class MeanArterialPressureResult:
    """Result of MAP calculation."""
    systolic_bp: float
    diastolic_bp: float
    mean_arterial_pressure: float
    interpretation: str  # "normal", "low", "high"

    age_months: int
    clinical_note: str

def mean_arterial_pressure(
    systolic_bp: float,
    diastolic_bp: float,
    age_months: int = None
) -> MeanArterialPressureResult:
    """
    Calculate mean arterial pressure.

    Mean arterial pressure is the average pressure in arteries during
    one cardiac cycle. It's a better indicator of tissue perfusion than
    systolic or diastolic pressure alone.

    Formula:
        MAP = (SBP + 2×DBP) / 3

    Args:
        systolic_bp: Systolic blood pressure in mmHg (0-300)
        diastolic_bp: Diastolic blood pressure in mmHg (0-200)
        age_months: Age in months for age-appropriate interpretation

    Returns:
        MeanArterialPressureResult with calculated MAP and interpretation

    Raises:
        ValueError: If systolic_bp < diastolic_bp or values out of range

    Example:
        >>> result = mean_arterial_pressure(120, 80, age_months=60)
        >>> result.mean_arterial_pressure
        93.33
        >>> result.interpretation
        'normal'

    Clinical Notes:
        - Normal MAP varies by age (wider range in older children)
        - MAP <50 mmHg indicates inadequate perfusion
        - Used to calculate cerebral perfusion pressure (CPP)
        - Normal ranges:
          * Infants (0-12 mo): 50-70 mmHg
          * Toddlers (1-3 yr): 60-75 mmHg
          * School-age (6-12 yr): 65-85 mmHg
          * Adolescents (>12 yr): 70-95 mmHg

    References:
        - PALS Textbook, 2015
        - Circulation. 2015;132(16_suppl_2):S444-S482
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

    # Interpret based on age
    normal_min, normal_max = _get_normal_map_range(age_months)

    if map_value < 50:
        interpretation = "shock"
        clinical_note = "Critical: MAP <50 indicates inadequate perfusion"
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
        clinical_note=clinical_note
    )


def _get_normal_map_range(age_months: int) -> tuple[float, float]:
    """Get age-appropriate normal MAP range."""
    if age_months is None:
        return (65, 85)  # Default adult/older child

    if age_months < 12:
        return (50, 70)  # Infants
    elif age_months < 36:
        return (60, 75)  # Toddlers
    elif age_months < 144:
        return (65, 85)  # School-age
    else:
        return (70, 95)  # Adolescents
```

### 2.3 Update Module Exports

Update `__init__.py` in the submodule:

```python
# python/clinical_validators/pediatric/__init__.py

from .hemodynamics import (
    MeanArterialPressureResult,
    mean_arterial_pressure,
)

__all__ = [
    "MeanArterialPressureResult",
    "mean_arterial_pressure",
]
```

---

## Step 3: Golden Cases (JSON)

### 3.1 Create Golden Case File

Add to `python/golden_cases/hemodynamics_golden_cases.json`:

```json
{
  "metadata": {
    "description": "Golden cases for pediatric hemodynamic calculations",
    "source": "PALS Textbook, AHA guidelines, pediatric cardiology",
    "tolerance_percent": 0.5,
    "version": "1.0.0",
    "last_updated": "2026-04-09",
    "verified_by": "Timothy Hartzog, MD"
  },
  "hemodynamic_calculations": [
    {
      "id": "MAP_NORMAL_6YO_001",
      "clinical_scenario": "Healthy 6-year-old with normal vital signs",
      "calculation_type": "mean_arterial_pressure",
      "inputs": {
        "systolic_bp": 105,
        "diastolic_bp": 65,
        "age_months": 72
      },
      "expected_output": {
        "mean_arterial_pressure": 78.33,
        "interpretation": "normal"
      },
      "source": "PALS guidelines: normal MAP for 6yo",
      "reference_url": "https://pubmed.ncbi.nlm.nih.gov/...",
      "calculation_method": "(105 + 2×65) / 3 = 78.33 mmHg",
      "verified_by": "Timothy Hartzog, MD",
      "confidence": "HIGH",
      "tolerance": 0.005,
      "notes": "Normal blood pressure and perfusion for age"
    },
    {
      "id": "MAP_SHOCK_INFANT_001",
      "clinical_scenario": "Septic infant with hypotension",
      "calculation_type": "mean_arterial_pressure",
      "inputs": {
        "systolic_bp": 65,
        "diastolic_bp": 40,
        "age_months": 9
      },
      "expected_output": {
        "mean_arterial_pressure": 48.33,
        "interpretation": "shock"
      },
      "source": "PALS critical care: hypotension in sepsis",
      "reference_url": "https://pubmed.ncbi.nlm.nih.gov/...",
      "calculation_method": "(65 + 2×40) / 3 = 48.33 mmHg",
      "verified_by": "Timothy Hartzog, MD",
      "confidence": "HIGH",
      "tolerance": 0.005,
      "notes": "Critical: MAP <50 indicates shock state"
    }
  ]
}
```

**Guidelines for golden cases:**

- **Minimum:** 2 cases per calculation
- **Ideal:** 3-5 cases (normal, edge cases, error conditions)
- **Components:**
  - Realistic clinical scenario
  - Representative inputs
  - Expected output verified from reference
  - Published source citation
  - Tolerance justified
  - Clinical notes

---

## Step 4: Python Unit Tests

### 4.1 Create Test File

Create `python/tests/test_hemodynamics_golden_cases.py`:

```python
"""
Test hemodynamic calculations against golden cases.
"""
import json
import pytest
from pathlib import Path

from clinical_validators.pediatric.hemodynamics import (
    mean_arterial_pressure,
)

@pytest.fixture
def hemodynamics_golden_cases():
    """Load hemodynamics golden cases from JSON."""
    cases_file = (
        Path(__file__).parent.parent
        / "golden_cases"
        / "hemodynamics_golden_cases.json"
    )
    with open(cases_file) as f:
        return json.load(f)

class TestMeanArterialPressure:
    """Test MAP calculations."""

    def test_map_normal_6yo(self, hemodynamics_golden_cases):
        """Test normal MAP in 6-year-old."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][0]

        result = mean_arterial_pressure(
            systolic_bp=case["inputs"]["systolic_bp"],
            diastolic_bp=case["inputs"]["diastolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        tolerance = case["tolerance"]

        # Verify MAP within tolerance
        assert (
            abs(result.mean_arterial_pressure - expected["mean_arterial_pressure"])
            / expected["mean_arterial_pressure"]
            < tolerance
        )
        assert result.interpretation == expected["interpretation"]

    def test_map_shock_infant(self, hemodynamics_golden_cases):
        """Test MAP in septic shock."""
        case = hemodynamics_golden_cases["hemodynamic_calculations"][1]

        result = mean_arterial_pressure(
            systolic_bp=case["inputs"]["systolic_bp"],
            diastolic_bp=case["inputs"]["diastolic_bp"],
            age_months=case["inputs"]["age_months"],
        )

        expected = case["expected_output"]
        assert result.interpretation == "shock"

    def test_all_cases(self, hemodynamics_golden_cases):
        """Test all hemodynamics golden cases."""
        for case in hemodynamics_golden_cases["hemodynamic_calculations"]:
            result = mean_arterial_pressure(
                systolic_bp=case["inputs"]["systolic_bp"],
                diastolic_bp=case["inputs"]["diastolic_bp"],
                age_months=case["inputs"]["age_months"],
            )

            expected = case["expected_output"]
            tolerance = case["tolerance"]

            assert (
                abs(result.mean_arterial_pressure - expected["mean_arterial_pressure"])
                / expected["mean_arterial_pressure"]
                < tolerance
            ), f"Failed for case {case['id']}"

    def test_invalid_inputs(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            mean_arterial_pressure(systolic_bp=-10, diastolic_bp=60)

        with pytest.raises(ValueError):
            mean_arterial_pressure(systolic_bp=50, diastolic_bp=80)  # SBP < DBP
```

---

## Step 5: R Implementation

### 5.1 Create R Function

Create `r/ClinicalValidators/R/hemodynamics.R`:

```r
#' Calculate Mean Arterial Pressure
#'
#' Calculates mean arterial pressure (MAP) from systolic and diastolic
#' blood pressure measurements.
#'
#' @param systolic_bp Systolic blood pressure in mmHg (0-300)
#' @param diastolic_bp Diastolic blood pressure in mmHg (0-200)
#' @param age_months Age in months (for age-appropriate interpretation)
#'
#' @return List with components:
#'   \item{systolic_bp}{Input systolic BP}
#'   \item{diastolic_bp}{Input diastolic BP}
#'   \item{mean_arterial_pressure}{Calculated MAP in mmHg}
#'   \item{interpretation}{Clinical interpretation (normal/low/high/shock)}
#'   \item{clinical_note}{Age-appropriate note}
#'
#' @details
#' Formula: MAP = (SBP + 2×DBP) / 3
#'
#' Normal ranges by age:
#' - Infants (0-12 mo): 50-70 mmHg
#' - Toddlers (1-3 yr): 60-75 mmHg
#' - School-age (6-12 yr): 65-85 mmHg
#' - Adolescents (>12 yr): 70-95 mmHg
#'
#' @references
#' American Heart Association. PALS Textbook. 2015.
#' Circulation. 2015;132(16_suppl_2):S444-S482.
#'
#' @export
#'
#' @examples
#' result <- mean_arterial_pressure(105, 65, age_months = 72)
#' result$mean_arterial_pressure  # 78.33
#' result$interpretation          # "normal"
mean_arterial_pressure <- function(systolic_bp, diastolic_bp, age_months = NULL) {

  # Input validation
  if (systolic_bp < 0 || systolic_bp > 300) {
    stop(sprintf("Systolic BP %f out of range (0-300)", systolic_bp))
  }
  if (diastolic_bp < 0 || diastolic_bp > 200) {
    stop(sprintf("Diastolic BP %f out of range (0-200)", diastolic_bp))
  }
  if (systolic_bp < diastolic_bp) {
    stop("Systolic BP cannot be less than diastolic BP")
  }

  # Calculate MAP
  map_value <- (systolic_bp + 2 * diastolic_bp) / 3

  # Get age-appropriate normal range
  if (is.null(age_months)) {
    normal_min <- 65
    normal_max <- 85
  } else if (age_months < 12) {
    normal_min <- 50
    normal_max <- 70
  } else if (age_months < 36) {
    normal_min <- 60
    normal_max <- 75
  } else if (age_months < 144) {
    normal_min <- 65
    normal_max <- 85
  } else {
    normal_min <- 70
    normal_max <- 95
  }

  # Interpret
  if (map_value < 50) {
    interpretation <- "shock"
    clinical_note <- "Critical: MAP <50 indicates inadequate perfusion"
  } else if (map_value < normal_min) {
    interpretation <- "low"
    clinical_note <- sprintf("Below normal for age (%d-%d mmHg)", normal_min, normal_max)
  } else if (map_value > normal_max) {
    interpretation <- "high"
    clinical_note <- sprintf("Above normal for age (%d-%d mmHg)", normal_min, normal_max)
  } else {
    interpretation <- "normal"
    clinical_note <- sprintf("Within normal range for age (%d-%d mmHg)", normal_min, normal_max)
  }

  list(
    systolic_bp = systolic_bp,
    diastolic_bp = diastolic_bp,
    mean_arterial_pressure = round(map_value, 2),
    interpretation = interpretation,
    age_months = age_months,
    clinical_note = clinical_note
  )
}
```

### 5.2 Create R Tests

Create `r/ClinicalValidators/tests/testthat/test-hemodynamics.R`:

```r
test_that("MAP normal in school-age child", {
  result <- mean_arterial_pressure(105, 65, age_months = 72)
  expect_equal(result$mean_arterial_pressure, 78.33, tolerance = 0.01)
  expect_equal(result$interpretation, "normal")
})

test_that("MAP indicates shock", {
  result <- mean_arterial_pressure(65, 40, age_months = 9)
  expect_equal(result$interpretation, "shock")
})

test_that("Invalid inputs raise errors", {
  expect_error(mean_arterial_pressure(-10, 60))
  expect_error(mean_arterial_pressure(50, 80))  # SBP < DBP
})
```

---

## Step 6: Documentation

### 6.1 Update README

Add function to calculation table in README.md

### 6.2 Update Verification Registry

Add to `docs/VERIFICATION_REGISTRY.md`:

```markdown
### Mean Arterial Pressure (MAP)

**Function:** `mean_arterial_pressure(systolic_bp, diastolic_bp, age_months)`

**Languages:** Python, R

**Status:** ✅ Implemented & Validated

**Golden Cases:** 2 (normal, shock)

**Source:** PALS Textbook 2015, AHA Circulation 2015

**Tolerance:** ±0.5%

**Last Verified:** 2026-04-09
```

---

## Step 7: Testing & CI/CD

### 7.1 Run Local Tests

```bash
cd python
python -m pytest tests/test_hemodynamics_golden_cases.py -v

cd ../r/ClinicalValidators
Rscript -e "testthat::test_dir('tests/testthat', filter='hemodynamics')"
```

### 7.2 Push & PR

1. Create feature branch: `git checkout -b feature/add-map-calculation`
2. Commit changes with descriptive message
3. Push: `git push origin feature/add-map-calculation`
4. Open PR with:
   - Calculation summary
   - Reference links
   - Golden case report output
   - Test results

---

## 📊 Summary Template

When submitting a PR for a new calculation, include:

```markdown
## New Calculation: [Function Name]

### Overview
- **Calculation:** [Brief description]
- **Source:** [Citation]
- **Implementation:** Python, R
- **Golden Cases:** [Number]
- **Tests:** [Number]

### Coverage
- [✅/❌] Python implementation
- [✅/❌] R implementation
- [✅/❌] Golden cases (2+ scenarios)
- [✅/❌] Python unit tests
- [✅/❌] R unit tests
- [✅/❌] Documentation

### Test Results
```
Python Tests: ✅ All passed
R Tests: ✅ All passed
Coverage: 98%
```

### References
- [Citation 1]
- [Citation 2]
```

---

## 🔍 Quality Checklist

Before submitting your PR:

- [ ] Function has complete docstring with examples
- [ ] All inputs validated with helpful error messages
- [ ] Output clearly documented (dataclass, list, etc.)
- [ ] 2+ golden cases with realistic scenarios
- [ ] Python tests pass locally
- [ ] R tests pass locally
- [ ] Cross-language results match (<0.5% difference)
- [ ] CI/CD passes on GitHub
- [ ] README updated with function
- [ ] Verification registry updated

---

## ❓ Getting Help

- **General questions:** GitHub Discussions
- **Clinical accuracy:** Email clinical@example.com
- **Technical issues:** GitHub Issues with [bug] tag
- **Integration help:** Reach out to maintainers

---

**Happy contributing! 🎉**
