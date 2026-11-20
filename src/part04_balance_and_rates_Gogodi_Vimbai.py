"""
Author: Gogodi Vimbai    |    Role: Demographic Rates Analyst    |    Checked by: Mlungisi Ncube K
HASTS206 Assignment 2, University of Zimbabwe

PART 4 - Population balance and demographic rates (Q1b).

Balancing equation for calendar 2025:
    P(1 Jan 2026) = P(1 Jan 2025) + Births - Deaths + Arrivals - Departures
P(1 Jan 2025) is the sum of age_sex.csv (README). Approximate mid-year exposure
is the mean of the two opening stocks, as the brief specifies.
"""
import numpy as np
import pandas as pd

from common import (load_raw, load_settings, show_table, save_table, save_fig, plt,
                    DARK, BLUE, SKY, ORANGE, HYPO)


def main():
    print("Author: Gogodi Vimbai (Demographic Rates Analyst)")
    print("PART 4: Population balance and crude rates (Q1b)")
    d = load_raw()
    dist, ags = d["districts"], d["age_sex"]
    s = load_settings()
    sel = [s["district_a"], s["district_b"]]

    t = dist.set_index("district_id").copy()
    t["population_2025"] = ags.groupby("district_id").population_2025.sum()
    print(f"Total baseline population, 1 Jan 2025 (all 24 districts): {int(t.population_2025.sum()):,}")
    print(f"Total reported population, 1 Jan 2026: {int(t.population_2026.sum()):,}")

    t["natural_increase"] = t.births_2025 - t.deaths_2025
    t["net_migration"] = t.arrivals_2025 - t.departures_2025
    t["reconstructed_2026"] = t.population_2025 + t.natural_increase + t.net_migration
    t["difference_reported_minus_reconstructed"] = t.population_2026 - t.reconstructed_2026
    t["exposure_2025"] = (t.population_2025 + t.population_2026) / 2
    t["CBR_per_1000"] = 1000 * t.births_2025 / t.exposure_2025
    t["CDR_per_1000"] = 1000 * t.deaths_2025 / t.exposure_2025
    t["RNI_per_1000"] = t.CBR_per_1000 - t.CDR_per_1000
    t["NMR_per_1000"] = 1000 * t.net_migration / t.exposure_2025
    t["growth_rate_per_1000"] = t.RNI_per_1000 + t.NMR_per_1000
    t["share_growth_from_migration_pct"] = 100 * t.net_migration / (t.population_2026 - t.population_2025)

    bal_cols = ["population_2025", "births_2025", "deaths_2025", "arrivals_2025", "departures_2025",
                "reconstructed_2026", "population_2026", "difference_reported_minus_reconstructed"]
    show_table(t.loc[sel, bal_cols].T, "Balancing equation, selected districts")
    tot = t[bal_cols].sum()
    show_table(tot.to_frame("All 24 districts"), "Balancing equation, all districts combined")
    print(f"Districts where the reconstruction differs from the report: "
          f"{int((t.difference_reported_minus_reconstructed != 0).sum())} of 24")

    rate_cols = ["exposure_2025", "CBR_per_1000", "CDR_per_1000", "RNI_per_1000", "NMR_per_1000", "growth_rate_per_1000"]
    show_table(t.loc[sel, rate_cols].T, "Crude rates per 1,000 residents, 2025", 2)
    save_table(t.reset_index(), "p04_balance_and_rates_all_districts.csv")

    # Chart: rates side by side
    fig, ax = plt.subplots(figsize=(7, 3.6))
    labels = ["Crude birth rate", "Crude death rate", "Natural increase", "Net migration rate"]
    keys = ["CBR_per_1000", "CDR_per_1000", "RNI_per_1000", "NMR_per_1000"]
    x = np.arange(len(labels))
    for i, (dn, c) in enumerate(zip(sel, [DARK, SKY])):
        vals = t.loc[dn, keys].to_numpy(float)
        bars = ax.bar(x + (i - 0.5) * 0.38, vals, 0.38, color=c, label=dn)
        for b_, v in zip(bars, vals):
            ax.text(b_.get_x() + b_.get_width() / 2, v + (0.4 if v >= 0 else -1.2), f"{v:.1f}",
                    ha="center", fontsize=7.5)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Rate per 1,000 residents (2025)")
    ax.set_title(f"Drivers of 2025 growth, {sel[0]} vs {sel[1]}")
    ax.legend(frameon=False)
    ax.text(0, -0.2, HYPO, transform=ax.transAxes, fontsize=7, color="grey")
    save_fig(fig, "fig02_crude_rates.png")

    a, b = t.loc[sel[0]], t.loc[sel[1]]
    print(f"\n{sel[0]}: growth {a.growth_rate_per_1000:.1f} per 1,000 = natural increase {a.RNI_per_1000:.1f} "
          f"+ net migration {a.NMR_per_1000:.1f}.")
    print(f"{sel[1]}: growth {b.growth_rate_per_1000:.1f} per 1,000 = natural increase {b.RNI_per_1000:.1f} "
          f"+ net migration {b.NMR_per_1000:.1f}.")
    return t


if __name__ == "__main__":
    main()
