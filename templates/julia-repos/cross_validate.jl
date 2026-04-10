"""
Cross-validate Julia implementations against Python reference implementations
from the clinical-calc-validators repository.

Copy this file to your Julia repo's test/ directory and customize:
1. Update the module imports (your Julia module name)
2. Update the Python function calls to match your implementations
3. Run: julia test/cross_validate.jl

Reference: https://github.com/timothyhartzog/clinical-calc-validators
"""

using Test
using JSON
using PyCall

# Configure Python path to find clinical_validators
pushfirst!(PyObject(py"""import sys""").path, "clinical-calc-validators/python")

# Import validators (adjust path as needed)
validators = pyimport("clinical_validators")

# Import your Julia module (customize this!)
# include("../src/YourModule.jl")
# using .YourModule

# Load test data
golden_cases_path = "clinical-calc-validators/python/golden_cases/pediatric_golden_cases.json"
golden_cases = JSON.parse(read(golden_cases_path, String))

@testset "Cross-validate Dosing Functions" begin

    @testset "Amoxicillin Dosing" begin
        # Test against golden cases
        for case in golden_cases["pediatric_dosing_golden_cases"]
            if case["drug"] != "Amoxicillin"
                continue
            end

            weight = case["inputs"]["weight_kg"]
            age = case["inputs"]["age_months"]
            indication = case["indication"]

            # Get Python reference result
            py_result = validators.pediatric.dosing.amoxicillin_dose(
                weight_kg = weight,
                age_months = age,
                indication = indication
            )

            # Get Julia result (customize this to call your function!)
            # julia_result = your_amoxicillin_dose(weight, age, indication)

            # For now, compare Python with itself
            expected_dose = case["expected_output"]["dose_mg"]
            tolerance = case["tolerance"]

            actual_dose = py_result.dose_mg

            # Check within tolerance
            @test isapprox(actual_dose, expected_dose, rtol = tolerance) "Amoxicillin: $(case["id"])"
        end
    end

    @testset "Gentamicin Dosing" begin
        for case in golden_cases["pediatric_dosing_golden_cases"]
            if case["drug"] != "Gentamicin"
                continue
            end

            weight = case["inputs"]["weight_kg"]
            age = case["inputs"]["age_months"]

            py_result = validators.pediatric.dosing.gentamicin_dose(
                weight_kg = weight,
                age_months = age
            )

            # julia_result = your_gentamicin_dose(weight, age)

            expected_dose = case["expected_output"]["dose_mg"]
            tolerance = case["tolerance"]
            actual_dose = py_result.dose_mg

            @test isapprox(actual_dose, expected_dose, rtol = tolerance) "Gentamicin: $(case["id"])"
        end
    end

    @testset "Cefotaxime Dosing" begin
        for case in golden_cases["pediatric_dosing_golden_cases"]
            if case["drug"] != "Cefotaxime"
                continue
            end

            weight = case["inputs"]["weight_kg"]
            age = case["inputs"]["age_months"]
            indication = case["indication"]

            py_result = validators.pediatric.dosing.cefotaxime_dose(
                weight_kg = weight,
                age_months = age,
                indication = indication
            )

            # julia_result = your_cefotaxime_dose(weight, age, indication)

            expected_dose = case["expected_output"]["dose_mg"]
            tolerance = case["tolerance"]
            actual_dose = py_result.dose_mg

            @test isapprox(actual_dose, expected_dose, rtol = tolerance) "Cefotaxime: $(case["id"])"
        end
    end

end

println("\n✅ Cross-validation complete!")
