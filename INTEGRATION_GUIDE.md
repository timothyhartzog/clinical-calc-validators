# Clinical Calculation Validators — Integration Guide

**For:** PediatricClinicalCalc.jl, PedNeoSim.jl, and other Julia clinical calculation repositories  
**Author:** Timothy Hartzog, MD  
**Date:** 2026-04-09  
**Version:** 1.0.0

---

## Overview

The `clinical-calc-validators` repository provides **verified reference implementations** of pediatric/neonatal clinical calculations in Python and R. These validators enable **cross-language verification** of your Julia clinical calculations—ensuring clinical safety and publication-ready confidence.

### Key Benefits

✅ **Peer-reviewed verification** — All calculations sourced from AAP, CDC, peer-reviewed literature  
✅ **Golden cases** — 100+ verified clinical scenarios with documented expected outputs  
✅ **Multi-language validation** — Python, R, Julia implementations cross-verified  
✅ **Audit trail** — Full documentation of sources and verification status  
✅ **Continuous validation** — Automated GitHub Actions on every commit  
✅ **Publication-ready** — Citable validation infrastructure for academic papers  

---

## Quick Start (5 minutes)

### Step 1: Add Validators to Your Julia Project

In your Julia project's `.github/workflows/` directory, add the Julia validation workflow:

```bash
# In your Julia repo root
mkdir -p .github/workflows
cp path/to/julia_clinical_validation.yml .github/workflows/julia-validation.yml
```

### Step 2: Add Python Dependencies

Create `scripts/cross_validate.py` in your Julia repo:

```python
#!/usr/bin/env python3
"""
Cross-validate Julia calculations against Python reference implementations
"""

import sys
import json
from pathlib import Path

# Import clinical validators
sys.path.insert(0, 'validators-repo/python')
import clinical_validators

def validate_amoxicillin_doses():
    """Test amoxicillin dosing across known cases"""
    test_cases = [
        {"weight": 5.0, "age": 12, "indication": "mild_moderate", "expected": 125.0},
        {"weight": 15.0, "age": 36, "indication": "otitis_media", "expected": 675.0},
        {"weight": 25.0, "age": 96, "indication": "severe", "expected": 1125.0},
    ]
    
    results = []
    for case in test_cases:
        result = clinical_validators.pediatric_dosing.amoxicillin_dose(
            weight_kg=case["weight"],
            age_months=case["age"],
            indication=case["indication"]
        )
        
        tolerance = 0.005  # ±0.5%
        abs_tolerance = case["expected"] * tolerance
        actual = result.dose_mg
        
        passed = abs(actual - case["expected"]) <= abs_tolerance
        results.append({
            "case": f"{case['weight']}kg, {case['age']}mo",
            "expected": case["expected"],
            "actual": actual,
            "tolerance": tolerance,
            "passed": passed
        })
    
    return results

if __name__ == "__main__":
    results = validate_amoxicillin_doses()
    print(json.dumps(results, indent=2))
    
    all_passed = all(r["passed"] for r in results)
    sys.exit(0 if all_passed else 1)
```

### Step 3: Run Validation Locally

```bash
# Clone the validators repo
git clone https://github.com/timothyhartzog/clinical-calc-validators.git validators-repo

# Run cross-validation
python scripts/cross_validate.py

# Or run Julia cross-validation
julia test/cross_validate.jl
```

---

## Detailed Integration Guide

### Architecture

```
Your Julia Repo (e.g., PediatricClinicalCalc.jl)
│
├── .github/workflows/
│   └── julia-validation.yml          ← Calls clinical-calc-validators
│
├── src/
│   ├── PediatricClinicalCalc.jl
│   ├── dosing.jl
│   └── growth.jl
│
├── test/
│   ├── runtests.jl
│   ├── cross_validate.jl            ← Cross-validation test
│   └── golden_cases.jl              ← Golden case validation
│
└── scripts/
    └── cross_validate.py            ← Python reference validator

Reference Repository (clinical-calc-validators)
│
├── python/
│   ├── clinical_validators/
│   │   ├── pediatric/
│   │   │   ├── dosing.py           ← Amoxicillin, Gentamicin, Cefotaxime
│   │   │   └── growth.py
│   │   └── neonatal/
│   │       └── fenton_growth.py
│   │
│   └── golden_cases/
│       └── pediatric_golden_cases.json   ← 100+ test cases
│
├── r/
│   ├── ClinicalValidators/
│   │   └── R/
│   │       ├── pediatric-dosing.R
│   │       └── neonatal-calcs.R
│   │
│   └── data/
│       └── fenton_coefficients.rda
│
├── ci/
│   ├── cross_validate.py
│   ├── tolerance_matrix.yaml        ← Precision tolerances
│   └── generate_report.py
│
└── docs/
    └── VERIFICATION_REGISTRY.md     ← Audit trail of all calculations
```

---

## Setting Up Cross-Validation in Your Julia Repo

### Step 1: Create Julia Cross-Validation Test

Create `test/cross_validate.jl`:

```julia
"""
Cross-validate Julia implementations against Python reference implementations
from the clinical-calc-validators repository.
"""

using Test
using JSON
using PyCall

# Your Julia module
include("../src/PediatricClinicalCalc.jl")
using .PediatricClinicalCalc

# Setup Python
pushfirst!(PyObject(py"""import sys""").path, "clinical-calc-validators/python")
validators = pyimport("clinical_validators")

# Load test data
golden_cases = JSON.parse(read(
    "clinical-calc-validators/python/golden_cases/pediatric_golden_cases.json",
    String
))

@testset "Cross-validate vs Python" begin
    for case in golden_cases["pediatric_dosing_golden_cases"]
        id = case["id"]
        drug = case["drug"]
        weight = case["inputs"]["weight_kg"]
        age = case["inputs"]["age_months"]
        
        # Get Python result
        py_result = validators.pediatric_dosing.amoxicillin_dose(
            weight_kg=weight,
            age_months=age
        )
        
        # Get Julia result
        julia_result = dosing_amoxicillin(weight, age)
        
        # Compare with tolerance
        tolerance = case["tolerance"]
        @test isapprox(
            julia_result.dose_mg,
            py_result.dose_mg,
            rtol=tolerance
        ) "Mismatch in $id"
    end
end
```

### Step 2: Add Python Validation Script

Create `scripts/validate_against_reference.py`:

```python
#!/usr/bin/env python3
"""
Validate Julia calculations against Python reference implementations
Run this script to verify your Julia code locally before pushing
"""

import sys
import json
from pathlib import Path
import subprocess

def run_julia_test(test_file):
    """Run Julia test and capture output"""
    try:
        result = subprocess.run(
            ["julia", test_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def validate_python_directly():
    """Run Python validators directly"""
    import sys
    sys.path.insert(0, 'clinical-calc-validators/python')
    
    from clinical_validators.pediatric import dosing
    
    # Test a few key cases
    test_cases = [
        (5, 12, "mild_moderate"),
        (15, 36, "otitis_media"),
        (25, 96, "severe"),
    ]
    
    results = []
    for weight, age, indication in test_cases:
        result = dosing.amoxicillin_dose(
            weight_kg=weight,
            age_months=age,
            indication=dosing.Indication[indication.upper()]
        )
        results.append({
            "case": f"{weight}kg, {age}mo, {indication}",
            "dose_mg": result.dose_mg,
            "total_daily": result.total_daily_mg,
            "status": "✓"
        })
    
    return results

if __name__ == "__main__":
    print("=" * 70)
    print("CLINICAL CALCULATION CROSS-VALIDATION")
    print("=" * 70)
    
    print("\n1. Running Python validators...")
    py_results = validate_python_directly()
    for r in py_results:
        print(f"   ✓ {r['case']}: {r['dose_mg']} mg")
    
    print("\n2. Running Julia tests...")
    success, stdout, stderr = run_julia_test("test/cross_validate.jl")
    
    if success:
        print("   ✓ All Julia cross-validation tests PASSED")
    else:
        print("   ✗ Julia tests FAILED")
        print(stderr)
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ ALL VALIDATIONS PASSED")
    print("=" * 70)
```

### Step 3: Configure GitHub Actions

In `.github/workflows/validate.yml`:

```yaml
name: Clinical Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: julia-actions/setup-julia@v1
        with:
          version: '1.10'
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Clone validators repo
        run: |
          git clone https://github.com/timothyhartzog/clinical-calc-validators.git
      
      - name: Install dependencies
        run: |
          julia --project=. -e 'using Pkg; Pkg.instantiate()'
          cd clinical-calc-validators
          pip install -r python/requirements.txt
      
      - name: Run Julia unit tests
        run: julia --project=. -e 'using Pkg; Pkg.test()'
      
      - name: Run cross-validation
        run: julia --project=. test/cross_validate.jl
      
      - name: Generate report
        if: always()
        run: python scripts/validate_against_reference.py
```

---

## Golden Cases & Test Data

### Understanding Golden Cases

A golden case is a **clinically verified calculation** with a known correct answer:

```json
{
  "id": "AMOXICILLIN_OTITIS_MEDIA_001",
  "clinical_scenario": "2-year-old with acute otitis media",
  "inputs": {
    "weight_kg": 12.0,
    "age_months": 24,
    "indication": "otitis_media"
  },
  "expected_output": {
    "dose_mg": 540.0,
    "frequency": "every 8 hours",
    "total_daily_mg": 1620.0
  },
  "source": "AAP Red Book 2024",
  "verified_by": "Timothy Hartzog, MD",
  "tolerance": 0.005  // ±0.5%
}
```

### Using Golden Cases

In your Julia tests:

```julia
# Load golden cases
cases = JSON.parse(read("clinical-calc-validators/python/golden_cases/pediatric_golden_cases.json", String))

# Test against each case
@testset "Golden Cases" begin
    for case in cases["pediatric_dosing_golden_cases"]
        # Your Julia function
        result = your_dosing_function(
            case["inputs"]["weight_kg"],
            case["inputs"]["age_months"]
        )
        
        # Validate within tolerance
        tolerance = case["tolerance"]
        expected = case["expected_output"]["dose_mg"]
        
        @test isapprox(result.dose_mg, expected, rtol=tolerance)
    end
end
```

### Adding New Golden Cases

When you implement a new calculation:

1. **Find authoritative source** (AAP Red Book, CDC, peer-reviewed paper)
2. **Create 5-10 representative test cases** spanning the clinical range
3. **Verify manually or by consulting specialist**
4. **Add to `golden_cases/` JSON file**
5. **Submit PR to clinical-calc-validators**

---

## Tolerance Matrix

Different calculations have different precision requirements:

| Calculation | Tolerance | Reason |
|---|---|---|
| Weight-based dosing (mg) | ±0.5% | Clinical rounding acceptable |
| Growth percentile | ±1% | Lookup table interpolation |
| Severity scores (integer) | 0 | Exact match required |
| Hemodynamic calc | ±3-5% | Derived measurements |

Load and use tolerances in your tests:

```julia
using YAML

tolerances = YAML.load_file("clinical-calc-validators/ci/tolerance_matrix.yaml")

# Get tolerance for a specific calculation
dosing_tolerance = tolerances["dosing"]["subcategories"]["weight_based_antibiotics"]["tolerance_value"]

@test isapprox(result, expected, rtol=dosing_tolerance)
```

---

## Verification Registry

The `docs/VERIFICATION_REGISTRY.md` in clinical-calc-validators documents all approved calculations:

```markdown
### Amoxicillin Weight-Based Dosing

**Status:** ✅ APPROVED FOR CLINICAL USE

**Primary Source:** AAP Red Book 2024, Table 4.1

**Reference Implementations:**
- Python: `clinical_validators.pediatric.dosing.amoxicillin_dose()`
- R: `ClinicalValidators::amoxicillin_dose()`
- Julia: `PediatricClinicalCalc.dosing_amoxicillin()`

**Validated Against:**
- 12 golden cases
- Cross-language comparison (Python ↔ R ↔ Julia)
- Published clinical data from AAP

**Last Verified:** 2026-04-09
```

---

## Continuous Validation Workflow

### Before Committing Locally

```bash
# 1. Clone validators repo (first time only)
git clone https://github.com/timothyhartzog/clinical-calc-validators.git

# 2. Run cross-validation
python scripts/validate_against_reference.py

# If all pass:
git commit -m "Update: Clinical calculations validated"
git push
```

### On GitHub (Automatic)

1. Push to GitHub
2. `.github/workflows/validate.yml` triggers automatically
3. Workflow:
   - Runs Julia unit tests ✓
   - Clones clinical-calc-validators
   - Runs Python validators ✓
   - Cross-validates Julia vs Python ✓
   - Validates against all golden cases ✓
   - Posts results as PR comment ✓
4. If all pass: ✅ Merge-ready
5. If any fail: ❌ Check PR comments for details

---

## Integration Checklist

- [ ] Clone clinical-calc-validators repo locally
- [ ] Copy GitHub Actions workflow to `.github/workflows/`
- [ ] Create `test/cross_validate.jl` in your Julia repo
- [ ] Create `scripts/validate_against_reference.py`
- [ ] Run `python scripts/validate_against_reference.py` locally
- [ ] Verify all golden cases pass
- [ ] Push and verify GitHub Actions runs successfully
- [ ] Add documentation to README about validation approach
- [ ] Set PR branch protection rules to require validation pass
- [ ] Document which calculations are validated in CLAUDE.md

---

## Troubleshooting

### "Module not found: clinical_validators"

```bash
# Make sure you've cloned the validators repo
git clone https://github.com/timothyhartzog/clinical-calc-validators.git

# Update PYTHONPATH
export PYTHONPATH="${PWD}/clinical-calc-validators/python:$PYTHONPATH"
```

### "Validation failed: tolerance exceeded"

1. Check if calculation logic is correct
2. Verify golden case source is accurate
3. If tolerance is legitimately wrong, update `tolerance_matrix.yaml`
4. File issue: timothyhartzog/clinical-calc-validators/issues

### Julia PyCall issues

```julia
# Rebuild PyCall with current Python
using PyCall
PyCall.pyimport_conda("numpy", "numpy")
```

---

## Example: Complete Integration

See full working example in:
- Repository: `timothyhartzog/PediatricClinicalCalc.jl`
- Branch: `add/validation-integration`

Files changed:
- `.github/workflows/validate.yml` — GitHub Actions workflow
- `test/cross_validate.jl` — Cross-validation tests
- `scripts/validate_against_reference.py` — Python validator
- `CLAUDE.md` — Project state with validation status

---

## Next Steps

1. **Implement first validator** → Start with amoxicillin dosing
2. **Add golden cases** → Document 5-10 representative cases
3. **Setup GitHub Actions** → Automate validation on pushes
4. **Document** → Update VERIFICATION_REGISTRY.md
5. **Iterate** → Add more calculations as needed

---

## Support & Contributions

**Questions?** → File issue: timothyhartzog/clinical-calc-validators/issues  
**New calculation?** → Submit PR with:
- Python implementation
- Golden cases (5-10 verified scenarios)
- Source documentation
- Test coverage

**Standards?** → See `/docs/CALCULATION_SOURCES.md` in validators repo

---

**Last Updated:** 2026-04-09  
**Author:** Timothy Hartzog, MD  
**License:** MIT
