# Clinical Calculation Validators Repository
## Project Plan & Architecture

**Repository:** `timothyhartzog/clinical-calc-validators`

### Overview
Reference implementations of pediatric/neonatal clinical calculations in Python, R, and C/C++. Each calculation is:
- Sourced from peer-reviewed literature or official guidelines
- Verified against authoritative reference data
- Tested with golden cases
- Cross-validated across languages
- Documented with clinical context and limitations

---

## Repository Structure

```
clinical-calc-validators/
├── .github/
│   ├── workflows/
│   │   ├── validate-all-languages.yml      # Main cross-validation workflow
│   │   ├── python-tests.yml                # Python unit tests
│   │   ├── r-tests.yml                     # R statistical validation
│   │   ├── precision-tolerance.yml         # Floating-point tolerance verification
│   │   └── documentation-check.yml         # Verify all calcs documented
│   └── ISSUE_TEMPLATE/
│       └── new-calculation.md              # Template for adding calculations
│
├── python/
│   ├── clinical_validators/
│   │   ├── __init__.py
│   │   ├── pediatric/
│   │   │   ├── __init__.py
│   │   │   ├── dosing.py                   # Weight-based dosing
│   │   │   ├── growth.py                   # Growth chart percentiles
│   │   │   ├── scores.py                   # Pediatric severity scores
│   │   │   ├── hemodynamics.py             # Cardiac/hemodynamic calcs
│   │   │   └── lab_predictions.py          # Lab value normalcy ranges
│   │   ├── neonatal/
│   │   │   ├── __init__.py
│   │   │   ├── ventilation.py              # Vent settings, PIP, etc
│   │   │   ├── fenton_growth.py            # Fenton 2013 growth curves
│   │   │   ├── severity_scores.py          # SNAP-II, SNAPPE-II, etc
│   │   │   ├── thermoregulation.py         # Neutral thermal zone
│   │   │   └── nutrition.py                # TPN, mineral requirements
│   │   ├── utilities/
│   │   │   ├── __init__.py
│   │   │   ├── constants.py                # Clinical constants
│   │   │   ├── interpolation.py            # LMS interpolation for growth
│   │   │   └── unit_conversion.py          # kg→lbs, mg→mcg, etc
│   │   └── validation.py                   # Cross-validation utilities
│   ├── tests/
│   │   ├── test_dosing.py
│   │   ├── test_growth.py
│   │   ├── test_scores.py
│   │   ├── test_neonatal.py
│   │   └── test_cross_validation.py
│   ├── golden_cases/
│   │   ├── pediatric_golden_cases.json
│   │   └── neonatal_golden_cases.json
│   ├── requirements.txt
│   └── setup.py
│
├── r/
│   ├── ClinicalValidators/
│   │   ├── R/
│   │   │   ├── pediatric-dosing.R
│   │   │   ├── growth-charts.R
│   │   │   ├── severity-scores.R
│   │   │   ├── neonatal-calcs.R
│   │   │   ├── statistical-validation.R
│   │   │   └── utils.R
│   │   ├── data/
│   │   │   ├── fenton_coefficients.rda
│   │   │   ├── cdc_growth_lms.rda
│   │   │   └── golden_cases.rda
│   │   ├── tests/
│   │   │   ├── testthat/
│   │   │   │   ├── test-dosing.R
│   │   │   │   ├── test-growth.R
│   │   │   │   └── test-neonatal.R
│   │   │   └── testthat.R
│   │   ├── DESCRIPTION
│   │   ├── NAMESPACE
│   │   └── README.md
│   └── requirements.txt
│
├── reference_data/
│   ├── pediatric/
│   │   ├── AAP_Bright_Futures_growth_2024.csv
│   │   ├── CDC_growth_charts_lms.csv
│   │   ├── ACEP_dosing_tables.csv
│   │   └── PALS_medications.csv
│   ├── neonatal/
│   │   ├── Fenton_2013_LMS_coefficients.csv
│   │   ├── Vermont_Oxford_Risk_Adjustment.csv
│   │   ├── SNAP_II_scoring.csv
│   │   └── Neutral_Thermal_Zone_coefficients.csv
│   └── shared/
│       ├── unit_conversions.json
│       └── clinical_constants.json
│
├── docs/
│   ├── VERIFICATION_REGISTRY.md            # Audit trail of all calculations
│   ├── CALCULATION_SOURCES.md              # Where each calc comes from
│   ├── GOLDEN_CASES.md                     # Documentation of test cases
│   ├── CROSS_VALIDATION_RESULTS.md         # Latest validation runs
│   ├── PRECISION_TOLERANCES.md             # Tolerance matrix by calc type
│   ├── HOW_TO_ADD_CALCULATION.md          # Contribution guide
│   ├── PYTHON_API.md                       # Python usage documentation
│   ├── R_API.md                            # R usage documentation
│   └── INTEGRATION_GUIDE.md                # How to use in Julia repos
│
├── ci/
│   ├── cross_validate.py                   # Master validation script
│   ├── compare_languages.py                # Compare Julia vs Python vs R
│   ├── generate_report.py                  # Create validation report
│   └── tolerance_matrix.yaml               # Precision tolerance config
│
├── CLAUDE.md                               # Project state file
├── README.md                               # Top-level documentation
├── LICENSE                                 # MIT or similar
├── .gitignore
└── CONTRIBUTING.md
```

---

## Phase 1: Core Calculations (Priority Order)

### Pediatric Dosing
- [ ] Weight-based antibiotic dosing (amoxicillin, ampicillin, cefotaxime, gentamicin)
- [ ] PALS medication dosing (epinephrine, atropine, amiodarone)
- [ ] Maintenance fluid requirements (Holliday-Segar)
- [ ] Deficit replacement calculations
- [ ] Electrolyte dosing (calcium, magnesium, sodium)

### Growth & Anthropometry
- [ ] CDC growth chart percentile lookup
- [ ] Fenton 2013 neonatal growth curves
- [ ] BMI calculation and percentile
- [ ] Growth velocity calculations
- [ ] Head circumference percentile

### Neonatal Calculations
- [ ] Ventilator settings (PIP, PEEP, rate, FiO2)
- [ ] Neutral thermal zone (NTZ) temperature
- [ ] Insensible water loss (IWL)
- [ ] TPN calculations (dextrose, amino acids, lipids)
- [ ] Phototherapy nomogram (AAP 2009)

### Severity Scores
- [ ] APGAR score validation
- [ ] SNAP-II (neonatal severity)
- [ ] SNAPPE-II (mortality prediction)
- [ ] PECARN pediatric severity index
- [ ] NEWS (National Early Warning Score)

### Hemodynamics
- [ ] Mean arterial pressure (MAP)
- [ ] Cardiac output calculations
- [ ] SVR/PVR calculations
- [ ] Perfusion index assessment

---

## Golden Cases

### Structure
Each golden case includes:
```json
{
  "id": "DOSING_AMOXICILLIN_001",
  "calculation": "Weight-based amoxicillin dosing",
  "clinical_scenario": "3-year-old with acute otitis media",
  "inputs": {
    "weight_kg": 15.0,
    "age_months": 36,
    "indication": "acute_otitis_media",
    "route": "oral"
  },
  "expected_output": {
    "dose_mg": 375,
    "frequency": "every_8_hours",
    "total_daily_mg": 1125
  },
  "source": "AAP Red Book 2024, Table 4.1",
  "reference_url": "https://redbook.solutions.aap.org/",
  "verified_by": "Timothy Hartzog, MD",
  "confidence": "HIGH",
  "tolerance": 0.005,
  "notes": "Standard dosing for mild-moderate infection"
}
```

### Golden Case Data Files
- `python/golden_cases/pediatric_golden_cases.json` — 100+ verified pediatric cases
- `python/golden_cases/neonatal_golden_cases.json` — 100+ verified neonatal cases

---

## GitHub Actions Workflows

### 1. Main Cross-Validation (`validate-all-languages.yml`)
Runs on every push/PR:
- [ ] Python tests (pytest)
- [ ] R tests (testthat)
- [ ] Compares Python vs R results
- [ ] Validates against golden cases
- [ ] Checks tolerance matrix
- [ ] Generates validation report
- [ ] Posts results as PR comment

### 2. Precision Tolerance Testing (`precision-tolerance.yml`)
Detects floating-point drift:
- [ ] Tests with extreme inputs
- [ ] Validates tolerance bounds
- [ ] Checks for loss of precision
- [ ] Compares across architectures (x86, ARM)

### 3. Documentation Check (`documentation-check.yml`)
Ensures every calculation is documented:
- [ ] Every .py/.R function has clinical source
- [ ] Golden cases exist for each calculation
- [ ] Tolerance matrix entry exists
- [ ] Verification registry is current

---

## Integration with Julia Repos

### For `PediatricClinicalCalc.jl`
```julia
# In test/cross_validate.jl
function validate_against_python(calc_name::String, inputs::Dict)
    # Call to clinical-calc-validators Python module
    py_result = py_clinical_validators.compute(calc_name, inputs)
    julia_result = your_julia_calc(inputs)
    return isapprox(julia_result, py_result, rtol=TOLERANCE[calc_name])
end
```

### For `PedNeoSim.jl`
```julia
# In test/physiological_validation.jl
# Compare ODE solver output against published physiological models
# Validate against Guyton-Coleman equivalents
# Cross-check with literature baseline values
```

---

## Verification Registry Entry Format

Each calculation needs an entry in `docs/VERIFICATION_REGISTRY.md`:

```markdown
### Amoxicillin Weight-Based Dosing

**Status:** ✅ APPROVED FOR CLINICAL USE

**Primary Source:**
- AAP Red Book 2024, Antimicrobial Agents and Related Therapy, Table 4.1
- Link: https://redbook.solutions.aap.org/

**Secondary Validation:**
- Lexi-Drugs (pharmacokinetic review)
- CDC Treatment Guidelines

**Reference Implementation:**
- Python: `clinical_validators.pediatric.dosing.amoxicillin_dose()`
- R: `ClinicalValidators::amoxicillin_dose()`

**Golden Cases:** 12 cases covering:
- Newborn (2.5 kg)
- Infant (6 kg)
- Toddler (15 kg)
- School age (25 kg)

**Cross-Validation Results:**
| Language | Test Cases | Pass Rate | Last Verified |
|----------|------------|-----------|---------------|
| Python   | 12         | 100%      | 2026-04-09    |
| R        | 12         | 100%      | 2026-04-09    |
| Julia    | 12         | 100%      | 2026-04-09    |

**Tolerance:** ±0.5% (clinical rounding acceptable)

**Clinical Notes:**
- Dosing assumes normal renal/hepatic function
- Not validated for premature infants <35 weeks
- See WARNINGS section for drug interactions
```

---

## How Integration Works

When you push to `PediatricClinicalCalc.jl`:

```
1. Your Julia tests run locally
2. GitHub Action calls clinical-calc-validators Python module
3. Compare Julia results against Python reference
4. If drift detected > tolerance: FAIL PR
5. If all pass: Comment on PR with validation report
6. Store results in this repo's verification logs
```

---

## Data Sources

### Pediatric
- [ ] AAP Red Book (authoritative)
- [ ] CDC Growth Charts (LMS data)
- [ ] ACEP Clinical Policies
- [ ] PubMed literature (endocrine, infectious disease, critical care)
- [ ] Harriet Lane Handbook (Johns Hopkins)

### Neonatal
- [ ] Fenton 2013 publication (Arch Dis Child 2013)
- [ ] Vermont Oxford Network (risk models)
- [ ] NICHD Neonatal Research Network (mortality prediction)
- [ ] AAP Phototherapy nomograms

### Statistical/Pharmacological
- [ ] R `scales` package (normalization)
- [ ] `scipy.stats` (distribution functions)
- [ ] Published pharmacokinetic models (compartmental)

---

## Next Steps

1. Create repo: `timothyhartzog/clinical-calc-validators`
2. Initialize Python structure with pediatric dosing module
3. Create first 20 golden cases (pediatric dosing)
4. Build Python validators for those cases
5. Create GitHub Actions workflow for validation
6. Populate reference data from authoritative sources
7. Create R parallel implementation
8. Integrate with `PediatricClinicalCalc.jl` and `PedNeoSim.jl`

---

## Success Criteria

- ✅ 50+ clinical calculations verified across Python/R/Julia
- ✅ 200+ golden cases with literature sourcing
- ✅ <5 minute validation time on GitHub Actions
- ✅ 100% of Julia clinical calcs pass cross-validation
- ✅ Publicly documented audit trail (VERIFICATION_REGISTRY.md)
- ✅ Can be cited in clinical publications as reference implementation
