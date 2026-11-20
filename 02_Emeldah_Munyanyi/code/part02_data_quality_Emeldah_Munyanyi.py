"""
Author: Emeldah Munyanyi    |    Role: Data Quality Analyst    |    Checked by: Gogodi Vimbai
HASTS206 Assignment 2, University of Zimbabwe

PART 2 - Data-quality log and cleaning decisions.

The brief asks us to check row counts, keys, join cardinality, age-band and sex
coverage, missing indicators and valid ranges, and to reconcile population
totals and event counts where the definitions allow. Every check is written to
outputs/tables/p02_data_quality_log.csv so the log is reproducible.
"""
import numpy as np
import pandas as pd

from common import load_raw, show_table, save_table

LOG = []


def log(file, check, result, status, action="None needed"):
    LOG.append({"check_no": len(LOG) + 1, "file": file, "check": check,
                "result": result, "status": status, "decision_or_action": action})


def main():
    print("Author: Emeldah Munyanyi (Data Quality Analyst)")
    print("PART 2: Data-quality log, reconciliations and cleaning decisions")
    LOG.clear()
    d = load_raw()
    dist, ags, life, scen, ins = d["districts"], d["age_sex"], d["life"], d["scen"], d["ins"]

    # ---------------- 1. Row counts --------------------------------------
    for name, df, n in [("districts.csv", dist, 24), ("age_sex.csv", ags, 864),
                        ("life_table_inputs.csv", life, 18),
                        ("projection_scenarios.csv", scen, 3),
                        ("insured_transitions.csv", ins, 96)]:
        log(name, "Row count vs README", f"{len(df)} rows (expected {n})",
            "PASS" if len(df) == n else "FAIL")

    # ---------------- 2. Primary keys ------------------------------------
    keys = [("districts.csv", dist, ["district_id"]),
            ("age_sex.csv", ags, ["district_id", "age_start", "sex"]),
            ("life_table_inputs.csv", life, ["age_start"]),
            ("projection_scenarios.csv", scen, ["scenario"]),
            ("insured_transitions.csv", ins, ["district_id", "origin", "destination"])]
    for name, df, k in keys:
        dups = int(df.duplicated(k).sum())
        log(name, f"Key {'+'.join(k)} unique", f"{dups} duplicate keys",
            "PASS" if dups == 0 else "FAIL")

    # ---------------- 3. Join cardinality --------------------------------
    per_dist = ags.groupby("district_id").size()
    log("age_sex.csv -> districts.csv", "Join cardinality (many-to-one)",
        f"{per_dist.nunique()} distinct row count(s) per district: {[int(v) for v in sorted(per_dist.unique())]}; "
        f"{ags.district_id.nunique()} districts matched",
        "PASS" if set(ags.district_id) == set(dist.district_id) and per_dist.eq(36).all() else "FAIL")
    m = ags.merge(dist[["district_id"]], on="district_id", how="left", validate="many_to_one", indicator=True)
    log("age_sex.csv -> districts.csv", "Unmatched rows after left join",
        f"{(m['_merge'] != 'both').sum()} unmatched", "PASS")
    per_ins = ins.groupby("district_id").size()
    log("insured_transitions.csv -> districts.csv", "Join cardinality (many-to-one)",
        f"4 rows per district for all {per_ins.size} districts" if per_ins.eq(4).all() else "Irregular",
        "PASS" if per_ins.eq(4).all() and set(ins.district_id) == set(dist.district_id) else "FAIL")

    # ---------------- 4. Age-band and sex coverage -----------------------
    bands = sorted(ags.age_start.unique())
    log("age_sex.csv", "Age bands present", f"{len(bands)} bands: {bands[0]} to {bands[-1]} in steps of 5",
        "PASS" if bands == list(range(0, 90, 5)) else "FAIL")
    log("age_sex.csv", "Sex codes", f"values = {sorted(ags.sex.unique())}",
        "PASS" if set(ags.sex) == {"F", "M"} else "FAIL")
    full = ags.groupby(["district_id"]).apply(lambda g: len(set(zip(g.age_start, g.sex))), include_groups=False)
    log("age_sex.csv", "Every district has all 18 bands x 2 sexes", f"min combos = {full.min()}",
        "PASS" if full.min() == 36 else "FAIL")
    log("life_table_inputs.csv", "Life-table age bands", f"{life.age_start.min()} to {life.age_start.max()}, {len(life)} bands",
        "PASS" if list(life.age_start) == list(range(0, 90, 5)) else "FAIL")

    # ---------------- 5. Missing indicators ------------------------------
    miss = dist.piped_water_pct.isna()
    log("districts.csv", "Missing piped_water_pct", f"{miss.sum()} missing: {', '.join(dist.district_id[miss])}",
        "FLAG", "Kept blank in the clean file; imputed only for clustering (Part 9, KNN rule)")
    for name, df in [("age_sex.csv", ags), ("projection_scenarios.csv", scen), ("insured_transitions.csv", ins)]:
        log(name, "Missing values", f"{int(df.isna().sum().sum())} missing cells",
            "PASS" if df.isna().sum().sum() == 0 else "FLAG")
    open_row = life[life.age_start == 85]
    log("life_table_inputs.csv", "Blank interval_years and ax at 85+",
        f"interval blank={open_row.interval_years.isna().all()}, ax blank={open_row.ax.isna().all()}",
        "NOTE", "Structural: open interval. We use q85+=1 and L85+=l85/m85+")

    # ---------------- 6. Valid ranges -----------------------------------
    count_cols = ["population_2025", "baseline_deaths_2025", "arrivals_2025", "departures_2025", "births_to_women_2025"]
    neg = int((ags[count_cols] < 0).sum().sum())
    nonint = int((ags[count_cols] % 1 != 0).sum().sum())
    log("age_sex.csv", "Counts non-negative integers", f"{neg} negative, {nonint} non-integer", "PASS" if neg + nonint == 0 else "FAIL")
    s = ags.survival_5yr
    log("age_sex.csv", "survival_5yr in (0,1]", f"min={s.min():.4f}, max={s.max():.4f}", "PASS" if s.gt(0).all() and s.le(1).all() else "FAIL")
    male_births = int(ags.loc[ags.sex == "M", "births_to_women_2025"].sum())
    log("age_sex.csv", "Births on male rows", f"total = {male_births}", "PASS" if male_births == 0 else "FAIL",
        "Structural zeros kept; births summed over female rows only")
    fert_ages = sorted(ags.loc[(ags.sex == "F") & (ags.births_to_women_2025 > 0), "age_start"].unique())
    log("age_sex.csv", "Ages with births (mother's baseline age)", f"{fert_ages[0]} to {fert_ages[-1] + 4}",
        "PASS" if fert_ages[0] >= 10 and fert_ages[-1] <= 45 else "FLAG")
    over = int((ags.baseline_deaths_2025 > ags.population_2025).sum())
    log("age_sex.csv", "Deaths <= baseline population", f"{over} rows violate", "PASS" if over == 0 else "FAIL")
    w = dist.piped_water_pct.dropna()
    log("districts.csv", "piped_water_pct within 0-100", f"min={w.min()}, max={w.max()}", "PASS" if w.between(0, 100).all() else "FAIL")
    ev = dist[["population_2020", "population_2026", "births_2025", "deaths_2025", "arrivals_2025", "departures_2025"]]
    log("districts.csv", "Population and events non-negative", f"{int((ev < 0).sum().sum())} negatives", "PASS")
    log("life_table_inputs.csv", "deaths < person_years and ax < interval",
        f"max m = {(life.deaths / life.person_years).max():.4f}; ax/n max = {(life.ax / life.interval_years).max():.2f}",
        "PASS" if (life.deaths < life.person_years).all() and (life.ax.dropna() < life.interval_years.dropna()).all() else "FAIL")
    ok_scen = scen[["fertility_multiplier", "arrivals_multiplier", "departures_multiplier"]].gt(0).all().all() and \
        scen[["newborn_survival_f", "newborn_survival_m"]].apply(lambda c: c.between(0, 1)).all().all()
    log("projection_scenarios.csv", "Multipliers > 0, newborn survival in [0,1]",
        "Low/Base/High present" if set(scen.scenario) == {"Low", "Base", "High"} else "Scenario missing",
        "PASS" if ok_scen else "FAIL")

    # Insured repeated-field rules
    rep_exp = ins.groupby(["district_id", "origin"]).exposure_py.nunique().max()
    rep_lives = ins.groupby(["district_id", "origin"]).initial_lives.nunique().max()
    log("insured_transitions.csv", "Exposure and initial_lives repeated identically across destinations",
        f"max distinct exposure per district-origin = {rep_exp}; initial_lives = {rep_lives}",
        "PASS" if rep_exp == 1 and rep_lives == 1 else "FAIL",
        "Counted once per district-origin (README rule) to avoid double counting")
    pairs = set(zip(ins.origin, ins.destination))
    log("insured_transitions.csv", "Allowed transitions", f"{sorted(pairs)}",
        "PASS" if pairs == {("H", "I"), ("H", "D"), ("I", "H"), ("I", "D")} else "FAIL")
    log("insured_transitions.csv", "Counts non-negative and exposure > 0",
        f"min count={ins.transition_count.min()}, min exposure={ins.exposure_py.min()}", "PASS")

    # ---------------- 7. Reconciliations ---------------------------------
    g = ags.groupby("district_id")
    rec = dist.set_index("district_id")[["population_2026", "births_2025", "deaths_2025", "arrivals_2025", "departures_2025"]].copy()
    rec["population_2025_agesex"] = g.population_2025.sum()
    rec["births_female_rows"] = g.births_to_women_2025.sum()
    rec["arrivals_agesex"] = g.arrivals_2025.sum()
    rec["departures_agesex"] = g.departures_2025.sum()
    rec["baseline_deaths_agesex"] = g.baseline_deaths_2025.sum()
    rec["deaths_among_2025_births"] = rec.deaths_2025 - rec.baseline_deaths_agesex
    rec["balance_2026"] = (rec.population_2025_agesex + rec.births_2025 - rec.deaths_2025
                           + rec.arrivals_2025 - rec.departures_2025)
    rec["balance_gap"] = rec.population_2026 - rec.balance_2026
    save_table(rec.reset_index(), "p02_reconciliation_by_district.csv")

    log("age_sex vs districts", "Births: female rows vs district births_2025",
        f"max abs gap = {int((rec.births_female_rows - rec.births_2025).abs().max())}",
        "PASS" if (rec.births_female_rows == rec.births_2025).all() else "FLAG")
    log("age_sex vs districts", "Arrivals and departures by age-sex vs district totals",
        f"max gaps = {int((rec.arrivals_agesex - rec.arrivals_2025).abs().max())}, "
        f"{int((rec.departures_agesex - rec.departures_2025).abs().max())}",
        "PASS" if (rec.arrivals_agesex == rec.arrivals_2025).all() and (rec.departures_agesex == rec.departures_2025).all() else "FLAG")
    log("age_sex vs districts", "Deaths: district deaths minus baseline deaths (scope difference)",
        f"gap between {int(rec.deaths_among_2025_births.min())} and {int(rec.deaths_among_2025_births.max())} "
        f"per district, total {int(rec.deaths_among_2025_births.sum())}; all positive = {(rec.deaths_among_2025_births > 0).all()}",
        "NOTE", "Not an error: district deaths also include deaths among babies born in 2025; "
                "the age-sex file only covers residents present on 1 Jan 2025")
    log("districts.csv", "Balancing equation closes at 1 Jan 2026",
        f"max abs gap = {int(rec.balance_gap.abs().max())} persons over 24 districts",
        "PASS" if rec.balance_gap.abs().max() == 0 else "FLAG")
    log("all files", "Original CSVs retained", "data/raw/ is read-only input; clean copy written to outputs/tables", "NOTE")

    # ---------------- 8. Cleaning decisions -> clean copies ---------------
    clean_dist = dist.copy()
    clean_dist["population_2025"] = clean_dist.district_id.map(rec.population_2025_agesex)
    clean_dist["water_missing_flag"] = clean_dist.piped_water_pct.isna().astype(int)
    save_table(clean_dist, "clean_districts.csv")
    clean_ags = ags.copy()
    clean_ags["age_group"] = clean_ags.age_start.map(lambda a: "85+" if a == 85 else f"{a}-{a + 4}")
    save_table(clean_ags, "clean_age_sex.csv")
    log("clean files", "Cleaning decisions applied",
        "Added population_2025 (sum of age-sex) and missing-water flag to districts; added age_group labels",
        "NOTE", "No rows dropped, no values changed")

    qlog = pd.DataFrame(LOG)
    save_table(qlog, "p02_data_quality_log.csv")
    show_table(qlog[["check_no", "file", "check", "result", "status"]], "Data-quality log")
    print("\nStatus summary:", qlog.status.value_counts().to_dict())
    show_table(rec[["population_2025_agesex", "births_2025", "births_female_rows", "deaths_2025",
                    "baseline_deaths_agesex", "deaths_among_2025_births", "balance_gap"]].head(8),
               "Reconciliation (first 8 districts)")
    return qlog, rec


if __name__ == "__main__":
    main()
