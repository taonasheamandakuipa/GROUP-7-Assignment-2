HASTS206 | Assignment 2 | Dataset guide

All records are synthetic and describe hypothetical districts and insured lives
in a Zimbabwean teaching case. Dates and district labels are illustrative.
Extract this ZIP and keep the original CSV files for reproducibility.
Missing values are blank. Counts represent people unless stated otherwise.

districts.csv (24 rows, key district_id)
  population_2020 and population_2026 are opening stocks on 1 January.
  The opening 2025 stock is obtained by summing age_sex.csv.
  The four event counts cover calendar 2025 and close the balance at 1 Jan 2026.
  piped_water_pct is a district household percentage. Two values are missing.
  region is a synthetic reporting label.

age_sex.csv (864 rows, key district_id + age_start + sex)
  age_start gives 5-year bands (0 = 0-4, 5 = 5-9, ..., 85 = 85+).
  sex is F or M. population_2025 is the 1 Jan 2025 count.
  baseline_deaths_2025 is for residents present at baseline, classified by age
  at baseline. District deaths additionally include deaths among 2025 births.
  arrivals_2025 and departures_2025 are model inputs by destination age-band
  and sex for use as annual flow proxies in the projection.
  births_to_women_2025 is classified by the mother's baseline age. Rows for men
  contain structural zeros. Sum births across female rows for district totals.
  survival_5yr is a supplied scenario input; for 85+ it is the retention
  probability for people already in that open group.

projection_scenarios.csv (3 rows, key scenario)
  Multipliers scale fertility and migration flows for the five-year exercise.
  newborn_survival_f/m represent average survival from birth to the end of
  the five-year interval for children born across the interval.

life_table_inputs.csv (18 rows, key age_start)
  A separate illustrative mortality schedule, pooled across sexes.
  person_years and deaths give the central mortality rate m_x.
  ax is average years lived in the interval by those dying in it.
  Blank interval_years and ax at 85+ indicate an open final interval.

insured_transitions.csv (96 rows, key district_id + origin + destination)
  H = healthy, I = ill, D = dead. exposure_py and transition_count come from
  fictional complete spell histories, in person-years and observed jumps.
  Each district-origin exposure and initial_lives count is repeated across
  its two possible destinations. Count initial_lives once per district-origin;
  pool exposure once per district-origin when forming a common denominator.
  Initial lives describe a separate hypothetical projection cohort.
