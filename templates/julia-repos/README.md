# Julia Repo Integration Template

This directory contains templates for integrating clinical-calc-validators cross-validation into your Julia clinical calculation repositories.

## Quick Start (5 minutes)

### 1. Copy Files to Your Julia Repo

```bash
# In your Julia repo root
mkdir -p test scripts .github/workflows

# Copy test file
cp path/to/clinical-calc-validators/templates/julia-repos/cross_validate.jl test/

# Copy validation script
cp path/to/clinical-calc-validators/templates/julia-repos/validate_against_reference.py scripts/

# Copy GitHub Actions workflow
cp path/to/clinical-calc-validators/templates/julia-repos/github-actions-validate.yml .github/workflows/validate.yml
```

### 2. Clone Validators Locally

```bash
# In your Julia repo root
git clone https://github.com/timothyhartzog/clinical-calc-validators.git
```

### 3. Run Validation Locally

```bash
# Test Python validators and run cross-validation
python scripts/validate_against_reference.py
```

### 4. Push to GitHub

```bash
# GitHub Actions will automatically run validation on every push
git add .
git commit -m "Add clinical validation integration"
git push
```

## Files Explained

### `cross_validate.jl`
Julia test file that:
- Loads golden cases from clinical-calc-validators
- Imports Python reference implementations
- Compares Julia results against Python reference
- Reports pass/fail for each test case

**To use:**
1. Copy to your `test/` directory
2. Update the module import to use your Julia package
3. Replace Python function calls with your Julia functions
4. Run: `julia test/cross_validate.jl`

### `validate_against_reference.py`
Python script for local validation:
- Tests Python reference implementations
- Runs Julia unit tests
- Performs cross-validation
- Generates validation report

**To use:**
```bash
python scripts/validate_against_reference.py
```

### `github-actions-validate.yml`
GitHub Actions workflow that:
- Runs Julia unit tests
- Clones clinical-calc-validators
- Performs cross-validation on every push/PR
- Uploads validation results as artifact

**To use:**
1. Copy to `.github/workflows/validate.yml` in your Julia repo
2. Push to GitHub
3. Validation will automatically run on all commits and PRs

## Integration Steps

### Step 1: Update Test File

Edit `test/cross_validate.jl`:

```julia
# Change this:
# include("../src/YourModule.jl")
# using .YourModule

# To this:
include("../src/YourModule.jl")
using .YourModule
```

And update the function calls:

```julia
# Change:
# julia_result = your_amoxicillin_dose(weight, age, indication)

# To:
julia_result = dosing_amoxicillin(weight, age, indication)
```

### Step 2: Configure Paths

In `validate_against_reference.py`, ensure paths are correct:

```python
# Should match where you cloned clinical-calc-validators
sys.path.insert(0, 'clinical-calc-validators/python')
```

### Step 3: Test Locally

```bash
# From your Julia repo root
python scripts/validate_against_reference.py
```

You should see:
```
======================================================================
CLINICAL CALCULATION CROSS-VALIDATION
======================================================================

1. Testing Python Reference Implementations...
✅ PASS | 5.0kg, 12mo, mild_moderate: 125 mg
...

2. Running Julia Unit Tests...
✅ Julia tests PASSED

3. Running Cross-Validation (Julia vs Python)...
✅ Cross-validation PASSED

VALIDATION SUMMARY
python_validators: ✅ PASS
julia_tests: ✅ PASS
cross_validation: ✅ PASS

======================================================================
✅ ALL VALIDATIONS PASSED - Ready to commit!
======================================================================
```

## Tolerance Matrix

Different calculations have different precision requirements. See `ci/tolerance_matrix.yaml` in clinical-calc-validators for exact tolerances.

**Common tolerances:**
- Weight-based dosing: ±0.5%
- Growth percentiles: ±1%
- Severity scores: 0 (exact match)

## Troubleshooting

### "ModuleNotFoundError: No module named 'clinical_validators'"

Make sure you've cloned the validators repo:
```bash
git clone https://github.com/timothyhartzog/clinical-calc-validators.git
```

### Julia tests pass but cross-validation fails

Check that:
1. Your Julia function names match those in `cross_validate.jl`
2. Function signatures (parameters) match expected inputs
3. Return values match expected structure
4. Results are within tolerance

### GitHub Actions fails but local validation passes

- Check Julia version compatibility (Actions uses Julia 1.10)
- Verify all dependencies are in Project.toml
- Check that test files exist and paths are correct

## Examples

See working examples:
- **Python**: `python/tests/test_pediatric_dosing.py`
- **R**: `r/ClinicalValidators/tests/testthat/test-pediatric-dosing.R`
- **Julia workflow**: `.github/workflows/julia-validate.yml`

## Support

Questions or issues?

- 📖 See `docs/INTEGRATION_GUIDE.md` in clinical-calc-validators
- 🐛 Report bugs: https://github.com/timothyhartzog/clinical-calc-validators/issues
- 💬 Discussions: https://github.com/timothyhartzog/clinical-calc-validators/discussions

## Next Steps

After integrating:

1. ✅ Run validation locally: `python scripts/validate_against_reference.py`
2. ✅ Push to GitHub and verify Actions passes
3. ✅ Add validation badge to your README
4. ✅ Document which calculations are validated in your CLAUDE.md

---

**Reference:** [clinical-calc-validators](https://github.com/timothyhartzog/clinical-calc-validators)
**License:** MIT
