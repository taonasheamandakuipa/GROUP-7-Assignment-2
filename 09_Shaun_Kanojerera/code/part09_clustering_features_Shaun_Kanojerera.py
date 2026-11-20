"""
Author: Shaun Kanojerera    |    Role: Feature Engineering Analyst    |    Checked by: Hillary Zivuku
HASTS206 Assignment 2, University of Zimbabwe

PART 9 - District feature table for clustering (Q4a).

Features (one row per district, all 24 districts):
  share_u15_pct     share of 1 Jan 2025 population aged 0-14 (%)
  share_65plus_pct  share aged 65+ (%)
  nmr_per_1000      2025 net migration rate per 1,000 (mid-year exposure from Part 4)
  piped_water_pct   household piped-water access (%)

Imputation rule (primary fit): k-nearest-neighbour imputation with k = 3. For a
district with missing water we find the 3 districts closest to it on the three
complete, standardised features and use the mean of their water values.
Why: in the 22 complete districts water access moves strongly with the
migration and age profile (see the correlations printed below), so neighbours
with the same profile give a more realistic value than one overall median,
which would place both districts in the middle of the range.
Sensitivity (Part 10): overall median imputation.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from common import load_raw, show_table, save_table, save_fig, plt, DARK, BLUE, SKY, HYPO

FEATURES = ["share_u15_pct", "share_65plus_pct", "nmr_per_1000", "piped_water_pct"]


def build_features(dist, ags):
    t = dist.set_index("district_id").copy()
    p25 = ags.groupby("district_id").population_2025.sum()
    t["share_u15_pct"] = 100 * ags[ags.age_start < 15].groupby("district_id").population_2025.sum() / p25
    t["share_65plus_pct"] = 100 * ags[ags.age_start >= 65].groupby("district_id").population_2025.sum() / p25
    expo = (p25 + t.population_2026) / 2
    t["nmr_per_1000"] = 1000 * (t.arrivals_2025 - t.departures_2025) / expo
    return t[["region"] + FEATURES].copy()


def knn_impute(feat: pd.DataFrame, target="piped_water_pct", k=3):
    base_cols = [c for c in FEATURES if c != target]
    z = (feat[base_cols] - feat[base_cols].mean()) / feat[base_cols].std(ddof=0)
    out = feat[target].copy()
    notes = []
    for d_id in feat.index[feat[target].isna()]:
        dist = np.sqrt(((z.loc[feat[target].notna()] - z.loc[d_id]) ** 2).sum(axis=1)).sort_values()
        nb = dist.index[:k]
        out[d_id] = feat.loc[nb, target].mean()
        notes.append({"district_id": d_id, "neighbours": ", ".join(nb),
                      "neighbour_water_values": ", ".join(f"{v:.1f}" for v in feat.loc[nb, target]),
                      "imputed_knn": out[d_id],
                      "overall_median_alternative": feat[target].median(),
                      "region_median_alternative": feat.loc[feat.region == feat.loc[d_id, "region"], target].median()})
    return out, pd.DataFrame(notes)


def main():
    print("Author: Shaun Kanojerera (Feature Engineering Analyst)")
    print("PART 9: Clustering feature table, imputation, outliers, standardisation (Q4a)")
    d = load_raw()
    feat = build_features(d["districts"], d["age_sex"])

    print("Correlation of water access with the other features (22 complete districts):")
    print(feat[FEATURES].dropna().corr()["piped_water_pct"].round(3).to_string())

    feat["piped_water_imputed_flag"] = feat.piped_water_pct.isna().astype(int)
    feat["piped_water_raw"] = feat.piped_water_pct
    feat["piped_water_pct"], notes = knn_impute(feat)
    show_table(notes, "Imputation of the two missing water values (k = 3 nearest neighbours)", 2)
    save_table(notes, "p09_imputation_notes.csv")

    # ---- Outlier check ------------------------------------------------------
    rows = []
    for c in FEATURES:
        x = feat[c]
        q1, q3 = x.quantile([0.25, 0.75])
        iqr = q3 - q1
        z = (x - x.mean()) / x.std(ddof=0)
        rows.append({"feature": c, "mean": x.mean(), "sd": x.std(ddof=0), "min": x.min(), "max": x.max(),
                     "max_abs_z": z.abs().max(),
                     "iqr_outliers": ", ".join(x.index[(x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)]) or "none",
                     "z_above_3": ", ".join(x.index[z.abs() > 3]) or "none"})
    out = pd.DataFrame(rows)
    show_table(out, "Outlier check (IQR rule and |z| > 3)", 2)
    save_table(out, "p09_outlier_check.csv")

    fig, axes = plt.subplots(1, 4, figsize=(10, 2.8))
    labels = ["Under 15 (%)", "65+ (%)", "Net migration per 1,000", "Piped water (%)"]
    for ax, c, lab in zip(axes, FEATURES, labels):
        ax.boxplot(feat[c], widths=0.5, patch_artist=True, boxprops=dict(facecolor=SKY, color=DARK),
                   medianprops=dict(color=DARK))
        ax.scatter(np.random.default_rng(1).normal(1, 0.04, len(feat)), feat[c], s=10, color=DARK, zorder=3)
        ax.set_title(lab, fontsize=8.5)
        ax.set_xticks([])
    fig.suptitle(f"Distribution of clustering features across 24 districts - {HYPO}", fontsize=9)
    fig.tight_layout()
    save_fig(fig, "fig08_feature_boxplots.png")

    # ---- Standardise --------------------------------------------------------
    scaler = StandardScaler()
    Z = pd.DataFrame(scaler.fit_transform(feat[FEATURES]), index=feat.index, columns=[f"z_{c}" for c in FEATURES])
    print("\nAfter standardising: means", Z.mean().round(10).tolist(), "sds", Z.std(ddof=0).round(6).tolist())
    print("district_id is excluded from the features: it is only a label. Its order (D01...D24) has no "
          "numerical meaning, so using it would create false distances between districts.")
    table = feat.join(Z)
    save_table(table.reset_index(), "p09_cluster_features.csv")
    show_table(table[FEATURES + ["piped_water_imputed_flag"]], "Feature table (original units)", 2)
    return table


if __name__ == "__main__":
    main()
