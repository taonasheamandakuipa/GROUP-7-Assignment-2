"""
Author: Taonashe Amanda Kuipa    |    Role: Scenario and Sensitivity Analyst    |    Checked by: Stuart Gavera
HASTS206 Assignment 2, University of Zimbabwe

PART 7 - Comparison of projections and fertility sensitivity (Q2c).

  * Compare cohort-component totals (Low, Base, High) with arithmetic and
    geometric totals for 1 Jan 2030.
  * Report shares under 15 and 65+.
  * Sensitivity: start from Base and change ONLY the fertility multiplier to the
    High value (1.12). Measure the effect on ages 0-4.
"""
import numpy as np
import pandas as pd

from common import (load_raw, load_settings, show_table, save_table, save_fig, plt,
                    DARK, BLUE, SKY, ORANGE, GREY, HYPO, age_label)
from part06_growth_and_cohort_component_Stuart_Gavera import growth_models, cohort_component, accounting


def main():
    s = load_settings()
    dname = s["projection_district"]
    print("Author: Taonashe Amanda Kuipa (Scenario and Sensitivity Analyst)")
    print(f"PART 7: Projection comparison and sensitivity for {dname} (Q2c)")
    d = load_raw()
    dist, ags, scen = d["districts"], d["age_sex"], d["scen"]
    base = ags[ags.district_id == dname]
    scen_i = scen.set_index("scenario")

    p2020 = float(dist.loc[dist.district_id == dname, "population_2020"].iloc[0])
    p2025 = float(base.population_2025.sum())
    gm = growth_models(p2020, p2025)

    rows = [{"method": "Baseline 1 Jan 2025", "P2030": p2025,
             "share_u15_pct": 100 * base.loc[base.age_start < 15, "population_2025"].sum() / p2025,
             "share_65plus_pct": 100 * base.loc[base.age_start >= 65, "population_2025"].sum() / p2025},
            {"method": "Arithmetic", "P2030": gm["arithmetic_P2030"], "share_u15_pct": np.nan, "share_65plus_pct": np.nan},
            {"method": "Geometric", "P2030": gm["geometric_P2030"], "share_u15_pct": np.nan, "share_65plus_pct": np.nan}]
    results = {}
    for sc in ["Low", "Base", "High"]:
        res = cohort_component(base, scen_i.loc[sc])
        acc = accounting(res)
        results[sc] = res
        rows.append({"method": f"Cohort-component {sc}", "P2030": acc["P2030"],
                     "share_u15_pct": acc["share_u15_pct"], "share_65plus_pct": acc["share_65plus_pct"]})
    comp = pd.DataFrame(rows)
    comp["change_from_2025"] = comp.P2030 - p2025
    comp["pct_change_from_2025"] = 100 * comp.change_from_2025 / p2025
    comp["difference_vs_CC_Base"] = comp.P2030 - comp.loc[comp.method == "Cohort-component Base", "P2030"].iloc[0]
    show_table(comp, "Projected totals for 1 Jan 2030 and age shares", 2)
    save_table(comp, "p07_projection_comparison.csv")

    # ---- Sensitivity: Base with High fertility -----------------------------
    base_row = scen_i.loc["Base"]
    sens = cohort_component(base, base_row, fert_override=scen_i.loc["High", "fertility_multiplier"])
    b04 = results["Base"].query("age_start == 0").groupby("sex").pop_2030.sum()
    s04 = sens.query("age_start == 0").groupby("sex").pop_2030.sum()
    sens_tab = pd.DataFrame({"Base": b04, "Base + High fertility": s04})
    sens_tab.loc["Total"] = sens_tab.sum()
    sens_tab["change"] = sens_tab["Base + High fertility"] - sens_tab["Base"]
    sens_tab["pct_change"] = 100 * sens_tab.change / sens_tab.Base
    show_table(sens_tab, "Sensitivity: ages 0-4 on 1 Jan 2030 (only fertility changed)", 1)
    save_table(sens_tab.reset_index(), "p07_fertility_sensitivity.csv")
    acc_s = accounting(sens)
    print(f"Total population changes from {accounting(results['Base'])['P2030']:,.0f} to {acc_s['P2030']:,.0f}; "
          f"share under 15 from {accounting(results['Base'])['share_u15_pct']:.2f}% to {acc_s['share_u15_pct']:.2f}%.")

    # ---- Charts ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    cmp = comp[comp.method != "Baseline 1 Jan 2025"]
    colours = [GREY, GREY, SKY, BLUE, DARK]
    bars = ax.bar(cmp.method.str.replace("Cohort-component ", "CC "), cmp.P2030, color=colours)
    ax.axhline(p2025, color=ORANGE, ls="--", lw=1, label=f"1 Jan 2025 baseline ({p2025:,.0f})")
    for b_, v in zip(bars, cmp.P2030):
        ax.text(b_.get_x() + b_.get_width() / 2, v + 600, f"{v:,.0f}", ha="center", fontsize=8)
    ax.set_ylim(p2025 * 0.9, cmp.P2030.max() * 1.03)
    ax.set_ylabel("Projected population, persons (1 Jan 2030)")
    ax.set_title(f"{dname}: total population on 1 January 2030 by method")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    ax.text(0, -0.2, HYPO, transform=ax.transAxes, fontsize=7, color="grey")
    save_fig(fig, "fig04_projection_comparison.png")

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ages = results["Base"].query("sex == 'F'").age_start.to_numpy()
    tot25 = base.groupby("age_start").population_2025.sum().reindex(ages).to_numpy()
    ax.plot(ages, tot25 / 1000, color=GREY, marker="o", ms=3, label="1 Jan 2025 (baseline)")
    for sc, c in zip(["Low", "Base", "High"], [SKY, BLUE, DARK]):
        y = results[sc].groupby("age_start").pop_2030.sum().reindex(ages).to_numpy()
        ax.plot(ages, y / 1000, color=c, marker="o", ms=3, label=f"1 Jan 2030 {sc}")
    ax.set_xticks(ages)
    ax.set_xticklabels([age_label(a) for a in ages], rotation=60, fontsize=7)
    ax.set_ylabel("Population, thousands of persons")
    ax.set_xlabel("Age group (years)")
    ax.set_title(f"{dname}: age distribution, baseline and projected scenarios")
    ax.legend(frameon=False, fontsize=8)
    ax.text(0, -0.32, HYPO, transform=ax.transAxes, fontsize=7, color="grey")
    save_fig(fig, "fig05_projection_age_profile.png")

    # Long table for Power BI (one row per scenario-age-sex)
    pbi = []
    for sc, res in list(results.items()) + [("Base + High fertility", sens)]:
        r = res[["sex", "age_start", "age_group", "pop_2025", "survivors_2030", "surviving_births",
                 "net_migration_5yr", "pop_2030"]].copy()
        r.insert(0, "scenario", sc)
        r.insert(0, "district_id", dname)
        pbi.append(r)
    pbi = pd.concat(pbi, ignore_index=True)
    pbi["scenario_order"] = pbi.scenario.map({"Low": 1, "Base": 2, "High": 3, "Base + High fertility": 4})
    save_table(pbi, "pbi_projection_by_age_sex.csv")
    return comp, sens_tab


if __name__ == "__main__":
    main()
