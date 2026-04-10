#' Pediatric Medication Dosing Calculations
#'
#' Weight-based antibiotic and medication dosing for pediatric patients.
#' All doses based on AAP Red Book 2024 and established pharmacokinetic principles.
#'
#' @references
#' - American Academy of Pediatrics. (2024). Red Book: Report of the Committee on
#'   Infectious Diseases (34th ed.)
#' - Lexi-Drugs (electronic version)
#' - Harriet Lane Handbook. (2024). Johns Hopkins Manual of Pediatric Diagnostics
#'   and Therapy
#'
#' Tolerance: ±0.5% (clinical rounding acceptable)
#'
#' @name pediatric-dosing
NULL

#' Amoxicillin Dosing for Pediatric Patients
#'
#' Calculate amoxicillin dose based on weight, age, and clinical indication.
#'
#' @param weight_kg Patient weight in kilograms
#' @param age_months Patient age in months
#' @param indication Clinical indication. One of: "mild_moderate", "severe",
#'   "otitis_media", "strep_throat"
#' @param route Route of administration. One of: "oral", "IV", "IM" (default: "oral")
#'
#' @return A list with dose details:
#'   - drug_name: "Amoxicillin"
#'   - weight_kg: Input weight
#'   - age_months: Input age
#'   - indication: Clinical indication
#'   - dose_mg: Single dose in milligrams
#'   - frequency: Dosing frequency
#'   - interval_hours: Hours between doses
#'   - total_daily_mg: Total daily dose
#'   - max_daily_dose_mg: Maximum allowed daily dose
#'   - notes: Clinical notes and warnings
#'   - source: Literature source
#'
#' @details
#' Dosing guidelines from AAP Red Book 2024:
#' - Mild-moderate: 25 mg/kg/dose every 8 hours
#' - Severe: 45 mg/kg/dose every 6 hours
#' - Acute otitis media: 45 mg/kg/dose every 8 hours
#' - Streptococcal pharyngitis: 12.5 mg/kg/dose every 8 hours
#'
#' Limitations:
#' - For preterm infants <35 weeks, consult specialist
#' - Reduced dosing if CrCl <30
#' - Not validated for patients >50 kg
#'
#' @examples
#' # 15 kg child with otitis media
#' amoxicillin_dose(weight_kg = 15, age_months = 36, indication = "otitis_media")
#'
#' @export
amoxicillin_dose <- function(weight_kg, age_months, indication = "mild_moderate",
                            route = "oral") {

  # Input validation
  if (weight_kg <= 0 || weight_kg > 50) {
    stop(sprintf("Weight %.1f kg outside validated range (0.1-50 kg)", weight_kg))
  }

  if (age_months < 0) {
    stop("Age cannot be negative")
  }

  if (age_months == 0 && weight_kg < 2.5) {
    stop("Neonatal amoxicillin dosing requires specialist consultation")
  }

  # Determine dose parameters based on indication
  dose_params <- switch(indication,
    strep_throat = list(dose_per_kg = 12.5, interval_hours = 8, max_daily = NA),
    otitis_media = list(dose_per_kg = 45, interval_hours = 8, max_daily = 4000),
    severe = list(dose_per_kg = 45, interval_hours = 6, max_daily = 4000),
    mild_moderate = list(dose_per_kg = 25, interval_hours = 8, max_daily = NA),
    stop(sprintf("Unknown indication: %s", indication))
  )

  dose_per_kg <- dose_params$dose_per_kg
  interval_hours <- dose_params$interval_hours
  max_daily <- dose_params$max_daily

  # Calculate single dose
  single_dose_mg <- weight_kg * dose_per_kg

  # Round to nearest 5 mg
  single_dose_mg <- round(single_dose_mg / 5) * 5

  # Calculate total daily dose
  doses_per_day <- 24 / interval_hours
  total_daily_mg <- single_dose_mg * doses_per_day

  # Apply maximum daily dose if specified
  if (!is.na(max_daily) && total_daily_mg > max_daily) {
    single_dose_mg <- max_daily / doses_per_day
    total_daily_mg <- max_daily
  }

  frequency <- switch(as.integer(interval_hours),
    "4" = "every 4 hours",
    "6" = "every 6 hours",
    "8" = "every 8 hours",
    "24" = "once daily",
    sprintf("every %d hours", interval_hours)
  )

  notes <- sprintf("Amoxicillin %.0f mg %s for %s", single_dose_mg, frequency, indication)
  if (weight_kg > 40) {
    notes <- paste(notes, "[approaching adult dosing consideration]")
  }

  # Return as list
  list(
    drug_name = "Amoxicillin",
    weight_kg = weight_kg,
    age_months = age_months,
    indication = indication,
    route = route,
    dose_mg = single_dose_mg,
    dose_per_kg = dose_per_kg,
    frequency = frequency,
    interval_hours = interval_hours,
    total_daily_mg = total_daily_mg,
    max_daily_dose_mg = max_daily,
    notes = notes,
    source = "AAP Red Book 2024, Table 4.1"
  )
}

#' Gentamicin Dosing for Pediatric Patients (Extended-Interval)
#'
#' Calculate gentamicin dose using extended-interval (once-daily) dosing.
#'
#' @param weight_kg Patient weight in kilograms
#' @param age_months Patient age in months
#' @param indication Clinical indication (default: "mild_moderate")
#' @param renal_function Baseline renal function. One of: "normal", "mild_impairment",
#'   "moderate_impairment" (default: "normal")
#'
#' @return A list with dose details
#'
#' @details
#' Extended-interval dosing (once daily) is preferred over traditional q8h dosing.
#' - Normal renal function: 7.5 mg/kg/dose every 24 hours IV
#' - Monitor: Trough <1 mcg/mL, Peak 15-30 mcg/mL
#'
#' WARNING: Gentamicin is nephrotoxic and ototoxic. Use only when appropriate
#' gram-negative coverage is required.
#'
#' @examples
#' # 20 kg child with severe gram-negative infection
#' gentamicin_dose(weight_kg = 20, age_months = 60)
#'
#' @export
gentamicin_dose <- function(weight_kg, age_months, indication = "mild_moderate",
                           renal_function = "normal") {

  if (weight_kg <= 0 || weight_kg > 50) {
    stop(sprintf("Weight %.1f kg outside validated range", weight_kg))
  }

  # Extended-interval dosing (once daily)
  dose_per_kg <- 7.5
  interval_hours <- 24
  frequency <- "once daily"
  max_daily_dose <- 500

  single_dose_mg <- weight_kg * dose_per_kg
  single_dose_mg <- round(single_dose_mg / 2.5) * 2.5

  total_daily_mg <- single_dose_mg

  if (total_daily_mg > max_daily_dose) {
    single_dose_mg <- max_daily_dose
  }

  notes <- sprintf("Gentamicin %.1f mg %s IV (extended-interval)", single_dose_mg, frequency)
  if (renal_function != "normal") {
    notes <- paste(notes, sprintf("[ADJUST for %s]", renal_function))
  }
  notes <- paste(notes, "\nMONITOR: Trough (pre-dose) <1 mcg/mL, Peak (1h post) 15-30 mcg/mL")
  notes <- paste(notes, "\nCAUTION: Nephrotoxic and ototoxic - use only when indicated")

  list(
    drug_name = "Gentamicin",
    weight_kg = weight_kg,
    age_months = age_months,
    indication = indication,
    route = "intravenous",
    dose_mg = single_dose_mg,
    dose_per_kg = dose_per_kg,
    frequency = frequency,
    interval_hours = interval_hours,
    total_daily_mg = total_daily_mg,
    max_daily_dose_mg = max_daily_dose,
    notes = notes,
    source = "AAP Red Book 2024; Glauser et al. 2009"
  )
}

#' Cefotaxime Dosing for Pediatric Patients
#'
#' Calculate cefotaxime dose based on weight and clinical indication.
#'
#' @param weight_kg Patient weight in kilograms
#' @param age_months Patient age in months
#' @param indication Clinical indication. One of: "mild_moderate", "severe", "meningitis"
#' @param route Route of administration. One of: "IV", "IM" (default: "IV")
#'
#' @return A list with dose details
#'
#' @details
#' Dosing from AAP Red Book 2024:
#' - Non-meningitis (mild-moderate): 50 mg/kg/dose every 6-8 hours
#' - Non-meningitis (severe): 50 mg/kg/dose every 4-6 hours
#' - Bacterial meningitis: 50 mg/kg/dose every 4 hours (HIGH DOSE!)
#' - Maximum single dose: 2000 mg
#'
#' @examples
#' # 8 kg infant with bacterial meningitis
#' cefotaxime_dose(weight_kg = 8, age_months = 12, indication = "meningitis")
#'
#' @export
cefotaxime_dose <- function(weight_kg, age_months, indication = "mild_moderate",
                           route = "IV") {

  if (weight_kg <= 0 || weight_kg > 50) {
    stop(sprintf("Weight %.1f kg outside validated range", weight_kg))
  }

  dose_params <- switch(indication,
    meningitis = list(dose_per_kg = 50, interval_hours = 4, max_daily = 12000),
    severe = list(dose_per_kg = 50, interval_hours = 6, max_daily = 8000),
    mild_moderate = list(dose_per_kg = 50, interval_hours = 8, max_daily = 6000),
    stop(sprintf("Unknown indication: %s", indication))
  )

  dose_per_kg <- dose_params$dose_per_kg
  interval_hours <- dose_params$interval_hours
  max_daily <- dose_params$max_daily

  single_dose_mg <- weight_kg * dose_per_kg

  # Cap at 2000 mg per dose
  if (single_dose_mg > 2000) {
    single_dose_mg <- 2000
  } else {
    single_dose_mg <- round(single_dose_mg / 50) * 50
  }

  total_daily_mg <- single_dose_mg * (24 / interval_hours)

  if (total_daily_mg > max_daily) {
    single_dose_mg <- max_daily / (24 / interval_hours)
    total_daily_mg <- max_daily
  }

  frequency <- switch(as.integer(interval_hours),
    "4" = "every 4 hours",
    "6" = "every 6 hours",
    "8" = "every 8 hours",
    sprintf("every %d hours", interval_hours)
  )

  notes <- switch(indication,
    meningitis = "HIGH-DOSE cefotaxime for MENINGITIS",
    severe = "Cefotaxime for severe infection",
    "Cefotaxime for mild-moderate infection"
  )

  list(
    drug_name = "Cefotaxime",
    weight_kg = weight_kg,
    age_months = age_months,
    indication = indication,
    route = route,
    dose_mg = single_dose_mg,
    dose_per_kg = dose_per_kg,
    frequency = frequency,
    interval_hours = interval_hours,
    total_daily_mg = total_daily_mg,
    max_daily_dose_mg = max_daily,
    notes = notes,
    source = "AAP Red Book 2024"
  )
}
