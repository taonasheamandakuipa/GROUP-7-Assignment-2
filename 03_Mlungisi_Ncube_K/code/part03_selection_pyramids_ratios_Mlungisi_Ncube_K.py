"""
Author: Mlungisi Ncube K    |    Role: Population Structure Analyst    |    Checked by: Ketso Thabiso Mdlongwa
HASTS206 Assignment 2, University of Zimbabwe

PART 3 - District selection, population pyramids and dependency ratios (Q1a).

Selection rule we agreed as a group:
  * Look at all 24 districts on the share under 15, share 65+, crude birth and
    death rates and the net migration rate.
  * Pick two districts of almost the same total size (so the pyramids on a
    common scale compare shape, not size) that sit at opposite ends of the
    age-structure range.
  * D13 is the largest of the young, high-fertility, net out-migration
    districts; D24 is the largest of the old, natural-decrease districts.
    Both have about 173,000 residents on 1 January 2025.
  * D13 is used for the age-sex projection because its fertility assumptions
    matter most for planning (schools, maternal and child health).
"""
import numpy as np
import pandas as pd

from common import (load_raw, show_table, save_table, save_fig, save_settings, plt,
                    DARK, BLUE, SKY, ORANGE, HYPO, age_label)


def district_screen(dist, ags):
    """One row per district with the indicators used to choose the pair."""
    p25 = ags.groupby("district_id").population_2025.sum()
    u15 = ags[ags.age_start < 15].groupby("district_id").population_2025.sum()
    o65 = ags[ags.age_start >= 65].groupby("district_id").population_2025.sum()
    t = dist.set_index("district_id").copy()
    t["population_2025"] = p25
    t["exposure_2025"] = (t.population_2025 + t.population_2026) / 2
    t["share_u15_pct"] = 100 * u15 / p25
    t["share_65plus_pct"] = 100 * o65 / p25
    t["cbr"] = 1000 * t.births_2025 / t.exposure_2025
    t["cdr"] = 1000 * t.deaths_2025 / t.exposure_2025
    t["nmr"] = 1000 * (t.arrivals_2025 - t.departures_2025) / t.exposure_2025
    return t


def ratios(ags, district):
    a = ags[ags.district_id == district]
    f = a.loc[a.sex == "F", "population_2025"].sum()
    m = a.loc[a.sex == "M", "population_2025"].sum()
    young = a.loc[a.age_start < 15, "population_2025"].sum()
    work = a.loc[(a.age_start >= 15) & (a.age_start < 65), "population_2025"].sum()
    old = a.loc[a.age_start >= 65, "population_2025"].sum()
    return {
        "district_id": district,
        "population_2025": int(f + m),
        "females": int(f), "males": int(m),
        "pop_0_14": int(young), "pop_15_64": int(work), "pop_65plus": int(old),
        "sex_ratio_males_per_100_females": 100 * m / f,
        "youth_dependency_ratio": 100 * young / work,
        "old_age_dependency_ratio": 100 * old / work,
        "total_dependency_ratio": 100 * (young + old) / work,
    }


def main(district_a="D13", district_b="D24", projection_district="D13"):
    print("Author: Mlungisi Ncube K (Population Structure Analyst)")
    print("PART 3: District selection, pyramids and ratios (Q1a)")
    d = load_raw()
    dist, ags = d["districts"], d["age_sex"]

    screen = district_screen(dist, ags)
    cols = ["region", "population_2025", "share_u15_pct", "share_65plus_pct", "cbr", "cdr", "nmr", "piped_water_pct"]
    show_table(screen[cols].sort_values("share_65plus_pct"), "Screening table used to choose the two districts", 1)
    save_table(screen.reset_index(), "p03_district_screen.csv")

    save_settings({"district_a": district_a, "district_b": district_b,
                   "projection_district": projection_district,
                   "reason": "Similar size (~173k), opposite age structures: D13 young/high fertility/"
                             "net out-migration; D24 old/natural decrease. D13 used for projection."})
    print(f"\nSelected districts: {district_a} and {district_b}; projection district: {projection_district}")

    # ---- Ratios ------------------------------------------------------------
    r = pd.DataFrame([ratios(ags, district_a), ratios(ags, district_b)])
    show_table(r.set_index("district_id").T, "Structure indicators at 1 January 2025", 2)
    save_table(r, "p03_structure_ratios.csv")

    # ---- Pyramids on a common scale ----------------------------------------
    pyr = (ags[ags.district_id.isin([district_a, district_b])]
           .pivot_table(index=["district_id", "age_start"], columns="sex", values="population_2025")
           .reset_index())
    pyr["age_group"] = pyr.age_start.map(age_label)
    save_table(pyr, "p03_pyramid_data.csv")

    xmax = np.ceil(pyr[["F", "M"]].to_numpy().max() / 2000) * 2000  # same limit for both panels
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
    for ax, dname, colour in zip(axes, [district_a, district_b], [DARK, BLUE]):
        p = pyr[pyr.district_id == dname].sort_values("age_start")
        y = np.arange(len(p))
        ax.barh(y, -p.M, color=colour, label="Males", height=0.85)
        ax.barh(y, p.F, color=SKY, label="Females", height=0.85)
        ax.set_xlim(-xmax, xmax)
        ticks = np.arange(-xmax, xmax + 1, 2000)
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{abs(t) / 1000:.0f}" for t in ticks])
        ax.set_yticks(y)
        ax.set_yticklabels(p.age_group)
        ax.axvline(0, color="black", lw=0.6)
        tot = int(p[["F", "M"]].to_numpy().sum())
        ax.set_title(f"District {dname} (total {tot:,} persons)")
        ax.set_xlabel("Population, thousands of persons (males left, females right)")
        ax.legend(loc="upper right", frameon=False, fontsize=8)
    axes[0].set_ylabel("Age group (years)")
    fig.suptitle(f"Population pyramids at 1 January 2025, common scale - {HYPO}", fontsize=10)
    fig.tight_layout()
    save_fig(fig, "fig01_population_pyramids.png")

    a, b = r.iloc[0], r.iloc[1]
    print(f"\nInterpretation: {district_a} has a youth dependency ratio of {a.youth_dependency_ratio:.1f} "
          f"against {b.youth_dependency_ratio:.1f} in {district_b}, while the old-age ratio is "
          f"{a.old_age_dependency_ratio:.1f} vs {b.old_age_dependency_ratio:.1f}. Service pressure in "
          f"{district_a} is on schools and child health; in {district_b} it is on care of older people.")
    return screen, r


if __name__ == "__main__":
    main()
