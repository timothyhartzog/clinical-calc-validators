library(testthat)

test_that("Amoxicillin dosing - mild moderate 5kg infant", {
  result <- amoxicillin_dose(weight_kg = 5.0, age_months = 12, indication = "mild_moderate")
  expect_equal(result$dose_mg, 125)  # 5 × 25 mg/kg
  expect_equal(result$dose_per_kg, 25)
  expect_equal(result$total_daily_mg, 375)
  expect_equal(result$frequency, "every 8 hours")
})

test_that("Amoxicillin dosing - otitis media 12kg toddler", {
  result <- amoxicillin_dose(weight_kg = 12.0, age_months = 24, indication = "otitis_media")
  expect_equal(result$dose_mg, 540)  # 12 × 45 mg/kg
  expect_equal(result$dose_per_kg, 45)
  expect_equal(result$total_daily_mg, 1620)
  expect_equal(result$frequency, "every 8 hours")
})

test_that("Amoxicillin dosing - strep throat 18kg child", {
  result <- amoxicillin_dose(weight_kg = 18.0, age_months = 72, indication = "strep_throat")
  expect_equal(result$dose_mg, 225)  # 18 × 12.5 mg/kg
  expect_equal(result$dose_per_kg, 12.5)
  expect_equal(result$frequency, "every 8 hours")
})

test_that("Amoxicillin dosing - severe infection 25kg preteen", {
  result <- amoxicillin_dose(weight_kg = 25.0, age_months = 96, indication = "severe")
  # 25 × 45 = 1125, but 1125 × 4 = 4500 > 4000 max, so capped to 1000
  expect_equal(result$dose_mg, 1000)
  expect_equal(result$frequency, "every 6 hours")
  expect_equal(result$total_daily_mg, 4000)
})

test_that("Amoxicillin dosing - rejects invalid weight", {
  expect_error(
    amoxicillin_dose(weight_kg = 51.0, age_months = 120),
    "outside validated range"
  )
})

test_that("Amoxicillin dosing - rejects negative age", {
  expect_error(
    amoxicillin_dose(weight_kg = 10.0, age_months = -1),
    "cannot be negative"
  )
})

test_that("Gentamicin dosing - 6kg infant extended-interval", {
  result <- gentamicin_dose(weight_kg = 6.5, age_months = 4)
  # 6.5 × 7.5 = 48.75, rounds to 50
  expect_equal(result$dose_mg, 50)
  expect_equal(result$frequency, "once daily")
  expect_equal(result$interval_hours, 24)
})

test_that("Gentamicin dosing - 25kg child", {
  result <- gentamicin_dose(weight_kg = 25.0, age_months = 96)
  # 25 × 7.5 = 187.5
  expect_equal(result$dose_mg, 187.5)
  expect_equal(result$frequency, "once daily")
})

test_that("Cefotaxime dosing - mild moderate 15kg child", {
  result <- cefotaxime_dose(weight_kg = 15.0, age_months = 36, indication = "mild_moderate")
  expect_equal(result$dose_mg, 750)  # 15 × 50 mg/kg
  expect_equal(result$frequency, "every 8 hours")
  expect_equal(result$dose_per_kg, 50)
})

test_that("Cefotaxime dosing - meningitis 8kg infant", {
  result <- cefotaxime_dose(weight_kg = 8.0, age_months = 12, indication = "meningitis")
  expect_equal(result$dose_mg, 400)  # 8 × 50 mg/kg
  expect_equal(result$frequency, "every 4 hours")
  expect_match(tolower(result$notes), "meningitis")
})

test_that("Cefotaxime dosing - dose capped at 2000 mg", {
  result <- cefotaxime_dose(weight_kg = 50.0, age_months = 144, indication = "severe")
  expect_equal(result$dose_mg, 2000)  # Capped, not 50 × 50 = 2500
})
