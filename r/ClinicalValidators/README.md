# ClinicalValidators R Package

Reference implementations of pediatric and neonatal clinical calculations, verified against peer-reviewed literature and AAP Red Book 2024.

## Installation

```r
# Install from GitHub
devtools::install_github("timothyhartzog/clinical-calc-validators", subdir = "r/ClinicalValidators")
```

## Usage

### Pediatric Antibiotic Dosing

```r
library(ClinicalValidators)

# Amoxicillin for otitis media
amoxicillin_dose(weight_kg = 15, age_months = 36, indication = "otitis_media")

# Gentamicin (extended-interval dosing)
gentamicin_dose(weight_kg = 20, age_months = 60)

# Cefotaxime for meningitis (HIGH DOSE)
cefotaxime_dose(weight_kg = 8, age_months = 12, indication = "meningitis")
```

## Features

- ✅ **Pediatric Dosing** — Amoxicillin, gentamicin, cefotaxime
- ✅ **Clinical Indications** — Mild-moderate, severe, meningitis, otitis media, strep throat
- ✅ **AAP Red Book 2024** — All doses sourced from authoritative guidelines
- ✅ **Weight-based Calculations** — Automatic rounding for clinical use
- ✅ **Maximum Daily Dose Enforcement** — Safety limits built in
- ✅ **Cross-validated** — Tested against Python and Julia implementations

## Testing

```r
# Run tests
devtools::test()
```

## References

- American Academy of Pediatrics. (2024). Red Book: Report of the Committee on Infectious Diseases (34th ed.)
- Lexi-Drugs (electronic version)
- Harriet Lane Handbook. (2024). Johns Hopkins Manual of Pediatric Diagnostics and Therapy

## License

MIT License. See LICENSE file for details.

## Tolerance

Clinical rounding tolerance: ±0.5% relative error acceptable
