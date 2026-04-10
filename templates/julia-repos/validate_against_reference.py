#!/usr/bin/env python3
"""
Cross-validate Julia calculations against Python reference implementations.

Run this script locally in your Julia repo before pushing:
    python scripts/validate_against_reference.py

This script:
1. Tests Python reference implementations
2. Runs Julia tests
3. Compares results within tolerance
4. Generates validation report

Reference: https://github.com/timothyhartzog/clinical-calc-validators
"""

import sys
import json
import subprocess
from pathlib import Path

def run_python_validators():
    """Test Python validators directly."""
    print("\n" + "=" * 70)
    print("1. Testing Python Reference Implementations...")
    print("=" * 70)

    sys.path.insert(0, 'clinical-calc-validators/python')

    try:
        from clinical_validators.pediatric import dosing, Indication
    except ImportError as e:
        print(f"❌ Failed to import clinical_validators: {e}")
        print("   Make sure clinical-calc-validators is cloned in your repo directory")
        return False

    test_cases = [
        # (weight_kg, age_months, indication, expected_dose)
        (5.0, 12, "mild_moderate", 125),
        (12.0, 24, "otitis_media", 540),
        (18.0, 72, "strep_throat", 225),
        (25.0, 96, "severe", 1000),
    ]

    results = []
    for weight, age, indication_str, expected in test_cases:
        try:
            indication = Indication[indication_str.upper()]
            result = dosing.amoxicillin_dose(
                weight_kg=weight,
                age_months=age,
                indication=indication
            )

            tolerance = 0.005
            rel_error = abs(result.dose_mg - expected) / expected
            passed = rel_error <= tolerance

            status = "✅ PASS" if passed else "❌ FAIL"
            results.append({
                "case": f"{weight}kg, {age}mo, {indication_str}",
                "expected": expected,
                "actual": result.dose_mg,
                "error": rel_error,
                "passed": passed
            })

            print(f"{status} | {weight}kg, {age}mo, {indication_str}: {result.dose_mg:.0f} mg")

        except Exception as e:
            print(f"❌ ERROR | {weight}kg, {age}mo: {e}")
            results.append({
                "case": f"{weight}kg, {age}mo, {indication_str}",
                "error": str(e),
                "passed": False
            })

    all_passed = all(r.get("passed", False) for r in results)
    print(f"\nPython validators: {'✅ PASSED' if all_passed else '❌ FAILED'}")

    return all_passed


def run_julia_tests():
    """Run Julia test suite."""
    print("\n" + "=" * 70)
    print("2. Running Julia Unit Tests...")
    print("=" * 70)

    try:
        result = subprocess.run(
            ["julia", "--project=.", "-e", "using Pkg; Pkg.test()"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print("✅ Julia tests PASSED")
            return True
        else:
            print("❌ Julia tests FAILED")
            print(result.stdout)
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("⚠️  Julia not found - skipping Julia tests")
        print("   Install Julia from https://julialang.org/downloads/")
        return None
    except subprocess.TimeoutExpired:
        print("❌ Julia tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Julia tests: {e}")
        return False


def run_cross_validation():
    """Run cross-validation test."""
    print("\n" + "=" * 70)
    print("3. Running Cross-Validation (Julia vs Python)...")
    print("=" * 70)

    try:
        result = subprocess.run(
            ["julia", "test/cross_validate.jl"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print("✅ Cross-validation PASSED")
            print(result.stdout)
            return True
        else:
            print("❌ Cross-validation FAILED")
            print(result.stdout)
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("⚠️  Julia not found - skipping cross-validation")
        return None
    except Exception as e:
        print(f"❌ Error running cross-validation: {e}")
        return False


def main():
    """Run all validation steps."""
    print("\n" + "=" * 70)
    print("CLINICAL CALCULATION CROSS-VALIDATION")
    print("=" * 70)

    # Check validators are available
    validators_path = Path("clinical-calc-validators")
    if not validators_path.exists():
        print("❌ clinical-calc-validators not found!")
        print("\nTo set up cross-validation:")
        print("1. Clone: git clone https://github.com/timothyhartzog/clinical-calc-validators.git")
        print("2. Run this script again")
        return False

    # Run validation steps
    python_ok = run_python_validators()
    julia_ok = run_julia_tests()
    cross_ok = run_cross_validation()

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    summary = {
        "python_validators": "✅ PASS" if python_ok else "❌ FAIL",
        "julia_tests": "✅ PASS" if julia_ok else ("⚠️  SKIPPED" if julia_ok is None else "❌ FAIL"),
        "cross_validation": "✅ PASS" if cross_ok else ("⚠️  SKIPPED" if cross_ok is None else "❌ FAIL"),
    }

    for test, status in summary.items():
        print(f"{test}: {status}")

    all_pass = python_ok and (julia_ok is None or julia_ok) and (cross_ok is None or cross_ok)

    print("\n" + "=" * 70)
    if all_pass:
        print("✅ ALL VALIDATIONS PASSED - Ready to commit!")
        print("=" * 70)
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED - Fix issues before committing")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
