# Clinical Calculation Validators — Implementation Roadmap

**Status:** Phase 2 (Golden Cases & Multi-Language Expansion)
**Last Updated:** 2026-04-09
**Maintained by:** Timothy Hartzog, MD

---

## 📊 Phase Overview

This document outlines the planned expansion of the clinical calculation validation framework from **12 implemented functions** to **50+ clinical calculations** across Python, R, and Julia.

### Current Status (Phase 1-2 Complete)

✅ **Completed:**
- 3 pediatric medication dosing functions (Amoxicillin, Gentamicin, Cefotaxime)
- 2 pediatric fluid/electrolyte calculations (Holliday-Segar, deficit replacement)
- 2 pediatric severity scores (APGAR, NEWS)
- 2 neonatal assessment functions (Fenton growth, SNAP-II)
- Comprehensive golden case sets (25+ validation scenarios)
- Multi-language CI/CD pipeline (Python, R cross-validation)
- Julia integration templates and workflow

---

## 🗺️ Planned Expansion (Phase 3 & 4)

### Phase 3: Core Pediatric Calculations (Q2 2026)

**Goal:** Add 25+ essential pediatric clinical calculations

#### 3.1 Hemodynamics & Perfusion (8 functions)

```python
# Calculated hemodynamic parameters
- cardiac_output()           # CO = HR × SV
- cardiac_index()            # CI = CO / BSA
- systemic_vascular_resistance()
- pulmonary_vascular_resistance()
- mean_arterial_pressure()   # MAP = (SBP + 2×DBP)/3
- shock_index()              # SI = HR / SBP
- body_surface_area_peds()   # BSA from weight (Mosteller, DuBois)
- perfusion_pressure_cerebral()
```

**Reference:** ACCM PALS algorithms, Texbook of Pediatric Advanced Life Support
**Golden cases:** 12 (normal, shock, hypertensive, post-op scenarios)

#### 3.2 Respiratory & Gas Exchange (6 functions)

```python
# Respiratory mechanics and oxygenation
- alveolar_arterial_gradient()      # A-a gradient
- oxygenation_index()               # OI = (FiO2 × MAP) / PaO2
- ventilation_index()               # VI = (Rate × PIP) / PaCO2
- fraction_inspired_oxygen()         # FiO2 from nasal cannula, mask, etc.
- ideal_body_weight_peds()
- lung_recruitment_maneuver_params()
```

**Reference:** PARDS criteria, ERN guidelines
**Golden cases:** 10 (mild/moderate/severe hypoxia, different delivery systems)

#### 3.3 Renal & Electrolyte Management (7 functions)

```python
# Kidney function and electrolyte corrections
- estimated_glomerular_filtration_rate()  # Schwartz formula, updated
- urine_osmolality_check()
- sodium_correction_rate()          # Safe hypernatremia correction
- potassium_replacement()           # Dosing for hypokalemia
- calcium_ionized_from_total()
- anion_gap_calculation()
- free_water_deficit()              # For dehydration management
```

**Reference:** KDIGO guidelines, AAP Nephrology
**Golden cases:** 14 (CKD stages, electrolyte imbalances, specific scenarios)

#### 3.4 Nutritional Assessment (4 functions)

```python
# Growth and nutritional support
- weight_for_height_percentile()    # CDC growth charts
- mid_upper_arm_circumference_percentile()
- triceps_skinfold_percentile()
- nutritional_requirements_estimation()  # Caloric, protein by age
```

**Reference:** CDC growth data, ASPEN pediatric guidelines
**Golden cases:** 8 (underweight, overweight, failure to thrive scenarios)

---

### Phase 4: Neonatal & Advanced Calculations (Q3 2026)

**Goal:** Comprehensive neonatal assessment and advanced clinical scoring

#### 4.1 Neonatal Assessment (6 functions)

```python
# Comprehensive neonatal evaluation
- maturational_assessment_score()   # Ballard score
- bilirubin_risk_stratification()   # AAP nomogram
- glucose_management_newborn()      # Dextrostix interpretation
- thermal_environment_calculation() # Neutral thermal zone
- metabolic_rate_estimation()       # For energy requirements
- retinopathy_of_prematurity_risk() # ROPScore
```

**Reference:** Ballard 2019, AAP 2024, ROP consortium
**Golden cases:** 12 (term, preterm, sick, well infants)

#### 4.2 Intensive Care Scoring (5 functions)

```python
# Prognostic scoring systems
- pediatric_logistic_organ_dysfunction()      # PELOD
- sequential_organ_failure_assessment_peds()  # pSOFA
- illness_severity_index_neonatal()  # ISNPS
- estimated_mortality_risk_multivariable()
- quality_of_life_score_assessment()
```

**Reference:** Leteurtre et al. PELOD, ESICM criteria
**Golden cases:** 12 (varying illness severities)

#### 4.3 Growth Curve Interpretation (3 functions)

```python
# Advanced growth assessment
- head_circumference_percentile()   # Fenton/WHO standards
- length_percentile_preterm()
- growth_velocity_assessment()      # Month-to-month change
```

**Reference:** Fenton 2013, WHO growth standards
**Golden cases:** 8 (normal, accelerated, decelerated growth)

---

## 📋 Implementation Strategy

### Timeline & Phases

| Phase | Period | Scope | Functions | Golden Cases | Status |
|-------|--------|-------|-----------|--------------|--------|
| 1 | Q1 2026 | Core dosing | 3 | 8 | ✅ Complete |
| 2 | Q2 2026 | Fluids, Scores, Growth | 7 | 17 | ✅ In Progress |
| 3 | Q2-Q3 2026 | Hemodynamics, Respiratory, Renal, Nutrition | 25 | 44 | 📅 Planned |
| 4 | Q3-Q4 2026 | Neonatal Advanced, ICU Scoring | 14 | 32 | 📅 Planned |
| 5 | Q4 2026 | Publication & Julia Integration | - | - | 📅 Planned |

### Per-Function Checklist

For each calculation function, implement in this order:

1. **Reference & Literature Review**
   - [ ] Identify authoritative source (AAP, ACCM, KDIGO, etc.)
   - [ ] Document formula/algorithm
   - [ ] List any age/weight thresholds

2. **Python Implementation** (`python/clinical_validators/`)
   - [ ] Create `.py` file in appropriate submodule
   - [ ] Implement function with docstring
   - [ ] Add dataclass for complex return types
   - [ ] Include validation (weight ranges, age limits)
   - [ ] Add clinical pearls in comments

3. **Golden Cases** (`python/golden_cases/`)
   - [ ] Create JSON entry with 2-3 realistic scenarios
   - [ ] Include edge cases (boundary conditions)
   - [ ] Cite clinical source for expected values
   - [ ] Set tolerance based on calculation type

4. **Unit Tests** (`python/tests/`)
   - [ ] Test normal/expected case
   - [ ] Test edge cases
   - [ ] Test error handling (invalid inputs)
   - [ ] Verify golden case compatibility

5. **R Implementation** (`r/ClinicalValidators/`)
   - [ ] Port Python function to R
   - [ ] Match function signature
   - [ ] Add Roxygen documentation
   - [ ] Create corresponding R tests

6. **CI/CD Integration**
   - [ ] Update `validate.yml` if new test categories
   - [ ] Ensure cross-language validation runs
   - [ ] Generate golden case report

7. **Documentation**
   - [ ] Update README with calculation description
   - [ ] Add to VERIFICATION_REGISTRY
   - [ ] Include clinical use case

---

## 🧪 Golden Case Strategy

### Current Coverage
- **Dosing:** 8 cases (3 drugs × multiple indications)
- **Fluids:** 6 cases (maintenance: 4, deficit: 2)
- **Scores:** 7 cases (APGAR: 4, NEWS: 3)
- **Growth:** 7 cases (Fenton: 4, SNAP-II: 3)

**Total:** 28 golden cases

### Target Coverage (Phase 3-4)

- **Minimum:** 2-3 per function
- **Ideal:** 3-5 per function (normal, edge cases, error conditions)
- **Total Target:** 120+ golden cases

### Golden Case Template Structure

```json
{
  "id": "FUNCTION_SCENARIO_###",
  "clinical_scenario": "Description of patient context",
  "calculation_type": "function_name",
  "inputs": { /* ... */ },
  "expected_output": { /* ... */ },
  "source": "Published reference",
  "verified_by": "MD/expert",
  "confidence": "HIGH/MEDIUM",
  "tolerance": 0.01,
  "notes": "Clinical significance or special conditions"
}
```

---

## 🔄 Multi-Language Implementation

### Python (Primary Implementation)
- **Framework:** Pure Python with dataclasses
- **Testing:** pytest with golden case fixtures
- **Deployment:** PyPI package (clinical-validators)

### R (Parallel Implementation)
- **Framework:** tidyverse-compatible functions
- **Testing:** testthat framework
- **Documentation:** Roxygen2
- **Deployment:** CRAN submission (ClinicalValidators)

### Julia (Integration via Templates)
- **Approach:** Reference Python via PyCall
- **Custom implementations:** For performance-critical calculations
- **Deployment:** Julia registry (PediatricClinicalCalc.jl)

### Cross-Language Validation

Each function must pass:
1. ✅ Python unit tests
2. ✅ R unit tests
3. ✅ Python ↔ R equivalence tests
4. ✅ Golden case validation (>98% accuracy)
5. ✅ Julia reference validation (if implemented)

---

## 📦 Deliverables

### By End of Phase 4

#### Code
- [ ] 50+ calculation functions (Python, R)
- [ ] 120+ golden case scenarios (JSON)
- [ ] 200+ unit tests (Python, R, Julia templates)
- [ ] Cross-language validation suite

#### Documentation
- [ ] Function reference manual (PDF, HTML)
- [ ] Implementation guide for clinicians
- [ ] Developer guide for contributors
- [ ] Clinical validation report

#### Infrastructure
- [ ] Automated CI/CD pipeline (GitHub Actions)
- [ ] Code coverage >95%
- [ ] Performance benchmarks
- [ ] Docker containers for reproducibility

#### Publication
- [ ] Peer-reviewed methods paper
- [ ] Open-source release (GitHub, PyPI, CRAN)
- [ ] Clinical practice guidelines integration

---

## 🎯 Success Criteria

### Clinical Validation
- ✅ All functions match published algorithms
- ✅ Golden cases verified by pediatric specialists
- ✅ Tolerance thresholds clinically justified
- ✅ Cross-language calculations differ <0.5%

### Code Quality
- ✅ >95% code coverage
- ✅ All functions documented
- ✅ Edge cases tested
- ✅ Error handling robust

### Integration
- ✅ Python, R, Julia all functional
- ✅ CI/CD fully automated
- ✅ Artifact generation reliable
- ✅ Community contributions enabled

---

## 🤝 Contributing

### Adding a New Calculation

1. **Create feature branch:** `feature/add-{function_name}`
2. **Implement in order:**
   - Python implementation + tests
   - Golden cases (2-3 scenarios)
   - R port + tests
   - Documentation
3. **Pull request:** Include golden case report + test results
4. **Review:** Clinician verification + code review

### Reporting Issues

- **Clinical accuracy:** clinical-calc-validators/issues (clinical tag)
- **Code defects:** standard GitHub issue
- **Validation failures:** include golden case ID and platform

---

## 📚 References

### Standards & Guidelines
- AAP Red Book 2024 — Pediatric Dosing
- ACCM PALS Algorithms — Hemodynamics
- KDIGO — Renal Function Assessment
- ESICM — Neonatal/Pediatric ICU Scoring
- CDC Growth Charts — Anthropometric Assessment
- WHO Standards — International Growth Curves

### Key References
- Holliday MA, Segar WE. Maintenance need for water in parenteral fluid therapy. *Pediatrics*. 1957.
- Apgar V. Proposal for a new method of evaluation of the newborn infant. *Anesth Analg*. 1953;32:260-267.
- Fenton TR. A new growth chart for preterm infants. *Arch Dis Child Fetal Neonatal Ed*. 2013;98(5):F394-F398.
- Richardson DK, et al. SNAP-II scoring system. *Pediatrics*. 2001;107(1):33-40.

---

## 📞 Contact & Support

- **Questions:** Open GitHub issue with [question] tag
- **Clinical validation:** clinical@example.com
- **Integration support:** developers@example.com
- **Maintainer:** Timothy Hartzog, MD (@timothyhartzog)

---

**Next Review:** 2026-05-15
**Target Completion:** Q4 2026
