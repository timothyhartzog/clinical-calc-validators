# Clinical Calculation Validators

**Reference implementations of pediatric and neonatal clinical calculations** verified against peer-reviewed literature and official clinical guidelines.

[![Python Tests](https://github.com/timothyhartzog/clinical-calc-validators/actions/workflows/validate.yml/badge.svg)](https://github.com/timothyhartzog/clinical-calc-validators/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

`clinical-calc-validators` provides **clinically verified, cross-language validated** reference implementations of pediatric and neonatal calculations. Use this repository to:

- ✅ **Validate** clinical calculations against authoritative reference implementations
- ✅ **Integrate** clinical calculation validation into your Julia, Python, or R projects
- ✅ **Publish** research with confidence in calculation accuracy
- ✅ **Teach** clinical decision-making with peer-reviewed, auditable calculations

**Status:** Production-ready for pediatric dosing, growth calculations, and severity scores. Expanding to 50+ calculations.

---

## Quick Start

### Python

```python
from clinical_validators.pediatric import dosing, Indication

# Calculate antibiotic dose
result = dosing.amoxicillin_dose(
    weight_kg=15.0,
    age_months=36,
    indication=Indication.OTITIS_MEDIA
)
print(f"Amoxicillin: {result.dose_mg} mg {result.frequency}")
# Output: Amoxicillin: 540 mg every 8 hours
```

### R

```r
library(ClinicalValidators)

result <- amoxicillin_dose(weight_kg = 15, age_months = 36, indication = "otitis_media")
cat(sprintf("Amoxicillin: %.0f mg %s\n", result$dose_mg, result$frequency))
# Output: Amoxicillin: 540 mg every 8 hours
```

### Julia

```julia
# Copy integration files from templates/julia-repos/
# Run validation locally: python scripts/validate_against_reference.py
# GitHub Actions validates automatically on every commit
```

---

## Implemented Calculations

### Pediatric (Ages 2-19)

#### Dosing (AAP Red Book 2024)
- ✅ **Amoxicillin** — Strep throat, otitis media, mild-moderate, severe
- ✅ **Gentamicin** — Extended-interval dosing with TDM
- ✅ **Cefotaxime** — Meningitis, severe, non-meningitis
- 📋 *10+ additional antibiotics planned*

#### Growth & Anthropometry
- ✅ **Weight percentiles** (2-19 years)
- ✅ **BMI calculation** and categorization
- 📋 *CDC growth percentiles (comprehensive)*

#### Fluids & Electrolytes
- ✅ **Maintenance fluids** (Holliday-Segar formula)
- ✅ **Deficit replacement** (dehydration protocols)
- 📋 *Electrolyte dosing*

#### Severity Scores
- ✅ **APGAR score** (1 and 5 minute)
- ✅ **NEWS** (National Early Warning Score)
- 📋 *PECARN severity index, pSOFA*

### Neonatal (Preterm & Term)

#### Growth
- ✅ **Fenton 2013 percentiles** (22-50 weeks PMA)
- 📋 *Intrauterine growth curves*

#### Severity Assessment
- ✅ **SNAP-II** (Score for Neonatal Acute Physiology)
- 📋 *SNAPPE-II, Simplified SNAP-II*

---

## Installation

### Python

```bash
git clone https://github.com/timothyhartzog/clinical-calc-validators.git
cd clinical-calc-validators

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e python/

# Run tests
pytest python/tests/ -v
```

### R

```r
# From R:
devtools::install_github("timothyhartzog/clinical-calc-validators",
                         subdir = "r/ClinicalValidators")

# Run tests:
devtools::test()
```

### Julia

See [Julia Integration Guide](templates/julia-repos/README.md)

---

## Validation & Testing

### Golden Cases
- **8+ pediatric dosing cases** — AAP Red Book sourced, clinically verified
- **Expanding to 100+ cases** — Growth, neonatal, all calculation types
- **Format:** JSON with expected outputs, tolerance specs, clinical context

### Cross-Language Validation
- **Python ↔ R:** Automated comparison in CI/CD
- **Julia ↔ Python:** Template-based cross-validation
- **Tolerance:** ±0.5% for dosing, ±1% for growth, exact for scores

### GitHub Actions CI/CD

Automatic validation on every commit:
1. Python unit tests (3.9-3.12)
2. R statistical validation
3. Golden case verification
4. Cross-language comparison
5. Documentation verification
6. Floating-point precision testing

[View workflow results →](https://github.com/timothyhartzog/clinical-calc-validators/actions)

---

## Documentation

- 📖 **[Integration Guide](docs/INTEGRATION_GUIDE.md)** — Set up cross-validation in Julia repos
- 📋 **[Setup Summary](docs/SETUP_SUMMARY.md)** — Project overview and roadmap
- 🔍 **[Verification Registry](docs/VERIFICATION_REGISTRY.md)** — Audit trail of all calculations
- 📚 **[Calculation Sources](docs/CALCULATION_SOURCES.md)** — Literature references for each function

---

## Clinical Use & Safety

### ⚠️ Disclaimer

These implementations are **reference implementations** for validation and research. Always:
- ✅ Verify against current clinical guidelines
- ✅ Consult pediatric specialists for critical decisions
- ✅ Use appropriate margin of safety in clinical practice
- ✅ Validate against patient-specific factors

### Tolerance Matrix

Different calculations require different precision:

| Calculation | Tolerance | Reason |
|---|---|---|
| Weight-based dosing | ±0.5% | Clinical rounding acceptable |
| Growth percentiles | ±1% | LMS interpolation variation |
| Severity scores | 0 (exact) | Integer-based, no rounding |
| Hemodynamic | ±3-5% | Derived measurements |

See [ci/tolerance_matrix.yaml](ci/tolerance_matrix.yaml) for complete specs.

---

## Contributing

### Adding a New Calculation

1. **Find authoritative source** (AAP Red Book, CDC, peer-reviewed paper)
2. **Create 5-10 golden cases** with documented expected outputs
3. **Implement in Python** with comprehensive docstrings
4. **Add unit tests** covering edge cases
5. **Implement in R** (parallel validation)
6. **Submit PR** with source documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Architecture

### Python Module Structure
```
python/clinical_validators/
├── pediatric/
│   ├── dosing.py          # Antibiotic calculations
│   ├── growth.py          # Percentile lookups
│   ├── fluids.py          # Maintenance & deficit
│   ├── scores.py          # APGAR, NEWS, etc.
│   └── __init__.py
├── neonatal/
│   ├── fenton_growth.py   # Preterm growth curves
│   ├── severity_scores.py # SNAP-II, SNAPPE-II
│   └── __init__.py
└── golden_cases/
    └── pediatric_golden_cases.json
```

### Design Principles
- **Simplicity** — Clear, understandable implementations
- **Verification** — Every calculation source-documented
- **Testing** — Golden cases ensure accuracy
- **Language-agnostic** — Parallel implementations in Python/R/Julia
- **Auditable** — Complete trail of design decisions

---

## Performance & Precision

- ⚡ **<1ms per calculation** (negligible computational cost)
- 📊 **IEEE 754 floating-point** (standard precision)
- 🔬 **Precision tests** — Detect rounding errors
- 📈 **Benchmark suite** — Monitor performance

---

## References & Citations

**Cite this work:**

```bibtex
@software{hartzog_clinical_calc_validators_2026,
  author = {Hartzog, Timothy},
  title = {Clinical Calculation Validators: Multi-Language Reference Implementation},
  year = {2026},
  url = {https://github.com/timothyhartzog/clinical-calc-validators},
  note = {GitHub repository}
}
```

**Clinical sources used:**
- American Academy of Pediatrics. (2024). Red Book: Report of the Committee on Infectious Diseases (34th ed.)
- CDC Growth Charts: https://www.cdc.gov/growthcharts/
- Fenton TR. Arch Dis Child Fetal Neonatal Ed. 2013;98(5):F394-F398
- Richardson DK et al. J Pediatr. 2001;138(5):644-649

---

## Support

- 📧 **Questions?** Open an [issue](https://github.com/timothyhartzog/clinical-calc-validators/issues)
- 💬 **Discussion?** Start a [discussion](https://github.com/timothyhartzog/clinical-calc-validators/discussions)
- 🐛 **Bug report?** [Report here](https://github.com/timothyhartzog/clinical-calc-validators/issues/new?labels=bug)
- 🎯 **Feature request?** [Suggest here](https://github.com/timothyhartzog/clinical-calc-validators/issues/new?labels=feature)

---

## License

MIT License — See [LICENSE](LICENSE) for details

---

## Acknowledgments

**Author:** Timothy Hartzog, MD
**Contributors:** Clinical validation team
**Last Updated:** 2026-04-09

---

🚀 **Ready to validate clinical calculations?** See the [Integration Guide](docs/INTEGRATION_GUIDE.md) to get started!
