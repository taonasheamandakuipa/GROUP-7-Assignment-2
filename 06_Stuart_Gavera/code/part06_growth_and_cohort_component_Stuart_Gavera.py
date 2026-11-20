"""
Author: Stuart Gavera    |    Role: Population Projection Modeller    |    Checked by: Taonashe Amanda Kuipa
HASTS206 Assignment 2, University of Zimbabwe

PART 6 - Arithmetic, geometric and cohort-component projections (Q2a, Q2b).

Projection district and period: selected district, 1 Jan 2025 -> 1 Jan 2030.

Timing assumptions for the cohort-component model (documented as the brief asks):
  * Survival: each 1 Jan 2025 cohort moves up one 5-year band with its supplied
    survival_5yr. Ages 80-84 survivors and 85+ survivors (retention) form 85+.
  * Births: 5 x (2025 births to women) x fertility multiplier, split 49% F /
    51% M, then multiplied by the scenario newborn survival and placed in 0-4.
  * Migration: 5 x each 2025 flow x scenario multiplier, added (arrivals) or
    removed (departures) at the END of the period by destination age and sex,
    including 0-4. Migrants are therefore not exposed to mortality or
    fertility inside the period (end-of-period adjustment).
"""
import numpy as np
import pandas as pd

from common import (load_raw, load_settings, show_table, save_table, HYPO, age_label,
                    FEMALE_BIRTH_SHARE, MALE_BIRTH_SHARE)


def growth_models(p2020: float, p2025: float, years: int = 5):
    """Arithmetic and geometric growth fitted to two opening counts."""
    slope = (p2025 - p2020) / years                       # persons per year
    r_arith = slope / p2020                               # constant absolute increase, as a rate of P2020
    r_geom = (p2025 / p2020) ** (1 / years) - 1           # constant compound annual rate
    return {
        "P2020_reported": p2020,
        "P2025_sum_of_age_sex": p2025,
        "arithmetic_increase_per_year": slope,
        "arithmetic_rate_per_year": r_arith,
        "geometric_rate_per_year": r_geom,
        "arithmetic_P2030": p2025 + slope * years,
        "geometric_P2030": p2025 * (1 + r_geom) ** years,
    }


def cohort_component(base: pd.DataFrame, scen_row: pd.Series, fert_override: float | None = None) -> pd.DataFrame:
    """Five-year projection for one district. `base` is that district's 36 age-sex rows."""
    fert = scen_row.fertility_multiplier if fert_override is None else fert_override
    births_2025 = base.loc[base.sex == "F", "births_to_women_2025"].sum()
    births_5yr = 5 * births_2025 * fert
    out = []
    for sex, share, nb in [("F", FEMALE_BIRTH_SHARE, scen_row.newborn_survival_f),
                           ("M", MALE_BIRTH_SHARE, scen_row.newborn_survival_m)]:
        b = base[base.sex == sex].sort_values("age_start")
        p = b.population_2025.to_numpy(float)
        s = b.survival_5yr.to_numpy(float)
        survived = np.zeros(18)
        survived[1:17] = p[0:16] * s[0:16]                  # 0-4 -> 5-9, ..., 75-79 -> 80-84
        survived[17] = p[16] * s[16] + p[17] * s[17]        # 80-84 -> 85+ plus 85+ retained
        births_sex = births_5yr * share
        surviving_births = np.zeros(18)
        surviving_births[0] = births_sex * nb
        arr = 5 * b.arrivals_2025.to_numpy(float) * scen_row.arrivals_multiplier
        dep = 5 * b.departures_2025.to_numpy(float) * scen_row.departures_multiplier
        pop2030 = survived + surviving_births + arr - dep
        out.append(pd.DataFrame({
            "sex": sex, "age_start": b.age_start.to_numpy(),
            "pop_2025": p, "survival_5yr": s,
            "survivors_2030": survived,
            "births_5yr": np.where(b.age_start == 0, births_sex, 0.0),
            "surviving_births": surviving_births,
            "arrivals_5yr": arr, "departures_5yr": dep,
            "net_migration_5yr": arr - dep,
            "pop_2030": pop2030,
        }))
    res = pd.concat(out, ignore_index=True)
    res["age_group"] = res.age_start.map(age_label)
    return res


def accounting(res: pd.DataFrame) -> dict:
    """Totals and the accounting identity P2030 = P2025 - deaths + surviving births + net migration."""
    p25 = res.pop_2025.sum()
    surv = res.survivors_2030.sum()
    deaths_cohort = p25 - surv
    births = res.births_5yr.sum()
    sb = res.surviving_births.sum()
    nm = res.net_migration_5yr.sum()
    p30 = res.pop_2030.sum()
    identity = p25 - deaths_cohort + sb + nm
    return {
        "P2025": p25, "deaths_baseline_cohorts": deaths_cohort, "births_5yr": births,
        "deaths_among_births": births - sb, "surviving_births": sb,
        "arrivals_5yr": res.arrivals_5yr.sum(), "departures_5yr": res.departures_5yr.sum(),
        "net_migration_5yr": nm, "P2030": p30,
        "identity_check_gap": p30 - identity,
        "negative_cells": int((res.pop_2030 < 0).sum()),
        "P2030_females": res.loc[res.sex == "F", "pop_2030"].sum(),
        "P2030_males": res.loc[res.sex == "M", "pop_2030"].sum(),
        "share_u15_pct": 100 * res.loc[res.age_start < 15, "pop_2030"].sum() / p30,
        "share_65plus_pct": 100 * res.loc[res.age_start >= 65, "pop_2030"].sum() / p30,
        "pop_0_4": res.loc[res.age_start == 0, "pop_2030"].sum(),
    }


def main():
    s = load_settings()
    dname = s["projection_district"]
    print("Author: Stuart Gavera (Population Projection Modeller)")
    print(f"PART 6: Growth models and cohort-component projection for {dname} (Q2a, Q2b)")
    d = load_raw()
    dist, ags, scen = d["districts"], d["age_sex"], d["scen"]
    base = ags[ags.district_id == dname]

    # ---- Q2a arithmetic and geometric -------------------------------------
    p2020 = float(dist.loc[dist.district_id == dname, "population_2020"].iloc[0])
    p2025 = float(base.population_2025.sum())
    gm = growth_models(p2020, p2025)
    show_table(pd.Series(gm).to_frame(dname), "Arithmetic and geometric growth, 2020-2025 fit")
    save_table(pd.DataFrame([{"district_id": dname, **gm}]), "p06_growth_models.csv")
    print("Inputs that are estimates: P2020 (reported opening stock) and P2025 (sum of the age-sex "
          "estimates). The 2030 totals are conditional projections: they hold only if the 2020-25 "
          "pattern of change continues unchanged.")

    # ---- Q2b cohort-component, three scenarios ---------------------------
    all_res, summ = [], []
    for _, row in scen.iterrows():
        res = cohort_component(base, row)
        res.insert(0, "scenario", row.scenario)
        res.insert(0, "district_id", dname)
        all_res.append(res)
        acc = accounting(res)
        summ.append({"scenario": row.scenario, **acc})
    detail = pd.concat(all_res, ignore_index=True)
    summary = pd.DataFrame(summ).set_index("scenario").loc[["Low", "Base", "High"]]
    save_table(detail, "p06_cohort_component_detail.csv")
    save_table(summary.reset_index(), "p06_cohort_component_summary.csv")

    show_table(summary[["P2025", "deaths_baseline_cohorts", "births_5yr", "deaths_among_births",
                        "net_migration_5yr", "P2030", "identity_check_gap", "negative_cells"]].T,
               "Cohort-component accounting by scenario", 1)
    assert summary.identity_check_gap.abs().max() < 1e-6, "accounting identity failed"
    assert summary.negative_cells.max() == 0, "negative population cell"
    # Check: survivors computed band by band equal the total
    base_res = detail[detail.scenario == "Base"]
    check_85 = base_res.query("age_start == 85").survivors_2030.sum()
    manual_85 = sum(r.population_2025 * r.survival_5yr for r in base.itertuples() if r.age_start >= 80)
    print(f"85+ survivors check: model {check_85:,.2f} vs manual {manual_85:,.2f}")
    print("All accounting checks passed: identity gap = 0, no negative cells.")

    wide = detail.pivot_table(index=["age_start", "age_group", "sex"], columns="scenario",
                              values="pop_2030").reset_index()[["age_group", "sex", "Low", "Base", "High"]]
    show_table(wide.round(0), f"Projected population on 1 Jan 2030 by age and sex, {dname}")
    return gm, detail, summary


if __name__ == "__main__":
    main()
