"""
Author: Trish Tembo    |    Role: Clustering Analyst and Dashboard Integrator    |    Checked by: Lennox Tawanda Jaricha
HASTS206 Assignment 2, University of Zimbabwe

PART 10 - k-means clustering, diagnostics, stability and dashboard exports (Q4b, Q4c).

  * k = 1..6, n_init = 50 random starts per fit (brief asks for at least 20).
  * WCSS (inertia) and % reduction between successive k.
  * Mean silhouette for k = 2..6 and silhouette plots for two candidates.
  * Stability: (i) a different seed, (ii) overall-median imputation instead of
    KNN, (iii) dropping piped water. Compared with the adjusted Rand index (ARI),
    which ignores how cluster labels are numbered.
  * Profiles: sizes and centroids in original units.
  * Final step: write the tidy CSVs that the Power BI dashboard reads.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score
from sklearn.preprocessing import StandardScaler

from common import (load_raw, load_settings, show_table, save_table, save_fig, plt, TABLES,
                    DARK, BLUE, SKY, ORANGE, GREY, PALETTE, HYPO, SEED_PRIMARY, SEED_CHECK, N_INIT)
from part09_clustering_features_Shaun_Kanojerera import FEATURES, build_features, knn_impute

CHOSEN_K = 3


def fit(X, k, seed):
    return KMeans(n_clusters=k, n_init=N_INIT, random_state=seed).fit(X)


def name_clusters(centroids: pd.DataFrame) -> dict:
    """Give each cluster a demographic name from its centroid (original units)."""
    names = {}
    old = centroids.share_65plus_pct.idxmax()
    names[old] = "Ageing, natural decrease"
    rest = centroids.drop(index=old)
    hub = rest.nmr_per_1000.idxmax()
    names[hub] = "Working-age in-migration hubs"
    for c in rest.index.drop(hub):
        names[c] = "Young, high fertility, out-migration"
    return names


def silhouette_panel(ax, X, labels, k, colours):
    sil = silhouette_samples(X, labels)
    y = 0
    for c in range(k):
        v = np.sort(sil[labels == c])
        ax.barh(np.arange(y, y + len(v)), v, height=1.0, color=colours[c % len(colours)], edgecolor="white")
        ax.text(-0.08, y + len(v) / 2, f"C{c}", va="center", fontsize=8)
        y += len(v) + 2
    avg = silhouette_score(X, labels)
    ax.axvline(avg, color="red", ls="--", lw=1)
    ax.set_title(f"k = {k}: mean silhouette {avg:.3f}")
    ax.set_xlabel("Silhouette value s(i)")
    ax.set_yticks([])
    ax.set_xlim(-0.15, 1)


def main():
    print("Author: Trish Tembo (Clustering Analyst and Dashboard Integrator)")
    print("PART 10: k-means clustering, diagnostics, stability and exports (Q4b-c)")
    s = load_settings()
    feats = pd.read_csv(TABLES / "p09_cluster_features.csv", index_col="district_id")
    X = feats[[f"z_{c}" for c in FEATURES]].to_numpy()

    # ---- 4b diagnostics ------------------------------------------------------
    rows, models = [], {}
    for k in range(1, 7):
        km = fit(X, k, SEED_PRIMARY)
        models[k] = km
        rows.append({"k": k, "WCSS": km.inertia_,
                     "mean_silhouette": silhouette_score(X, km.labels_) if k > 1 else np.nan})
    diag = pd.DataFrame(rows)
    diag["pct_reduction_from_previous_k"] = 100 * (1 - diag.WCSS / diag.WCSS.shift(1))
    show_table(diag, f"k-means diagnostics (n_init = {N_INIT}, seed = {SEED_PRIMARY})", 4)
    save_table(diag, "p10_kmeans_diagnostics.csv")

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.3))
    axes[0].plot(diag.k, diag.WCSS, marker="o", color=DARK)
    for r in diag.itertuples():
        if r.k > 1:
            axes[0].annotate(f"-{r.pct_reduction_from_previous_k:.0f}%", (r.k, r.WCSS), textcoords="offset points",
                             xytext=(4, 6), fontsize=7.5, color=BLUE)
    axes[0].set_xlabel("Number of clusters k")
    axes[0].set_ylabel("Within-cluster sum of squares (standardised units)")
    axes[0].set_title("Elbow plot: WCSS against k")
    d2 = diag.dropna()
    axes[1].bar(d2.k, d2.mean_silhouette, color=[DARK if k == CHOSEN_K else SKY for k in d2.k])
    for r in d2.itertuples():
        axes[1].text(r.k, r.mean_silhouette + 0.01, f"{r.mean_silhouette:.3f}", ha="center", fontsize=8)
    axes[1].set_xlabel("Number of clusters k")
    axes[1].set_ylabel("Mean silhouette")
    axes[1].set_title("Mean silhouette, k = 2 to 6")
    fig.text(0.01, -0.03, HYPO, fontsize=7, color="grey")
    fig.tight_layout()
    save_fig(fig, "fig09_wcss_silhouette.png")

    # Silhouette plots for two plausible candidates
    cand = [2, 3]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8))
    for ax, k in zip(axes, cand):
        silhouette_panel(ax, X, models[k].labels_, k, [DARK, BLUE, SKY, ORANGE])
    fig.suptitle("Individual silhouette values by cluster for the two candidate solutions", fontsize=9)
    fig.tight_layout()
    save_fig(fig, "fig10_silhouette_candidates.png")
    for k in cand:
        sv = silhouette_samples(X, models[k].labels_)
        print(f"k={k}: min silhouette {sv.min():.3f}, districts with s(i) < 0.1: {int((sv < 0.1).sum())}")

    # ---- 4c chosen k, stability -------------------------------------------------
    km = models[CHOSEN_K]
    labels = km.labels_
    km_seed = fit(X, CHOSEN_K, SEED_CHECK)
    ari_seed = adjusted_rand_score(labels, km_seed.labels_)

    raw = load_raw()
    f2 = build_features(raw["districts"], raw["age_sex"])
    f2["piped_water_pct"] = f2.piped_water_pct.fillna(f2.piped_water_pct.median())   # overall median rule
    X_med = StandardScaler().fit_transform(f2[FEATURES])
    km_med = fit(X_med, CHOSEN_K, SEED_PRIMARY)
    ari_med = adjusted_rand_score(labels, km_med.labels_)

    X_nowater = StandardScaler().fit_transform(feats[FEATURES[:3]])
    km_nw = fit(X_nowater, CHOSEN_K, SEED_PRIMARY)
    ari_nw = adjusted_rand_score(labels, km_nw.labels_)

    def moved(a, b):
        """Districts not in the best-matching renamed cluster (labels can be permuted)."""
        return int(len(a) - pd.crosstab(a, b).max(axis=1).sum())

    stab = pd.DataFrame([
        {"check": f"Different seed ({SEED_CHECK} instead of {SEED_PRIMARY})", "ARI_vs_primary": ari_seed,
         "districts_changing_cluster": moved(labels, km_seed.labels_)},
        {"check": "Overall-median imputation of water (instead of KNN)", "ARI_vs_primary": ari_med,
         "districts_changing_cluster": moved(labels, km_med.labels_)},
        {"check": "Drop piped water (3 demographic features only)", "ARI_vs_primary": ari_nw,
         "districts_changing_cluster": moved(labels, km_nw.labels_)},
    ])
    show_table(stab, f"Stability of the k = {CHOSEN_K} solution (adjusted Rand index)", 3)
    save_table(stab, "p10_stability_checks.csv")
    show_table(pd.crosstab(pd.Series(labels, name="primary"), pd.Series(km_med.labels_, name="median_imputation")),
               "Membership cross-tab: primary vs median imputation (labels may be renamed)")

    # ---- Profiles in original units ----------------------------------------------
    feats["cluster"] = labels
    cent = feats.groupby("cluster")[FEATURES].mean()
    names = name_clusters(cent)
    feats["cluster_name"] = feats.cluster.map(names)
    prof = cent.copy()
    prof["n_districts"] = feats.groupby("cluster").size()
    prof["cluster_name"] = prof.index.map(names)
    prof["districts"] = feats.groupby("cluster").apply(lambda g: ", ".join(g.index), include_groups=False)
    # centroids from the scaler back-transform agree with the plain means (check)
    sc = StandardScaler().fit(feats[FEATURES])
    back = pd.DataFrame(sc.inverse_transform(km.cluster_centers_), columns=FEATURES)
    print(f"Centroid back-transform equals cluster means: {np.allclose(back.to_numpy(), cent.to_numpy())}")
    show_table(prof[["cluster_name", "n_districts"] + FEATURES + ["districts"]], "Cluster sizes and centroids (original units)", 2)
    save_table(prof.reset_index(), "pbi_cluster_centroids.csv")

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
    pairs = [("share_u15_pct", "share_65plus_pct", "Share under 15 (%)", "Share aged 65+ (%)"),
             ("nmr_per_1000", "piped_water_pct", "Net migration rate per 1,000 (2025)", "Piped-water access (%)")]
    for ax, (xc, yc, xl, yl) in zip(axes, pairs):
        for c, col in zip(sorted(feats.cluster.unique()), [DARK, ORANGE, SKY]):
            g = feats[feats.cluster == c]
            ax.scatter(g[xc], g[yc], s=45, color=col, alpha=0.9, edgecolor="white",
                       label=f"C{c}: {names[c]} (n={len(g)})")
            cx, cy = g[xc].mean(), g[yc].mean()
            ax.scatter(cx, cy, marker="X", s=110, color="black", zorder=4)
        imp = feats[feats.piped_water_imputed_flag == 1]
        ax.scatter(imp[xc], imp[yc], s=110, facecolor="none", edgecolor="red", lw=1.2,
                   label="Imputed water (D04, D17)")
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
    axes[0].legend(frameon=False, fontsize=7, loc="upper right")
    fig.suptitle(f"District clusters (k = {CHOSEN_K}); X marks each centroid - {HYPO}", fontsize=9)
    fig.tight_layout()
    save_fig(fig, "fig11_cluster_map.png")

    # ---- Dashboard exports ---------------------------------------------------------
    bal = pd.read_csv(TABLES / "p04_balance_and_rates_all_districts.csv").set_index("district_id")
    prof_d = bal[["district_name", "region", "population_2020", "population_2025", "population_2026",
                  "births_2025", "deaths_2025", "arrivals_2025", "departures_2025",
                  "reconstructed_2026", "CBR_per_1000", "CDR_per_1000", "RNI_per_1000", "NMR_per_1000",
                  "growth_rate_per_1000"]].join(
        feats[["share_u15_pct", "share_65plus_pct", "piped_water_raw", "piped_water_pct",
               "piped_water_imputed_flag", "cluster", "cluster_name"]])
    prof_d = prof_d.rename(columns={"piped_water_pct": "piped_water_used_pct"})
    prof_d["selected_for_comparison"] = prof_d.index.isin([s["district_a"], s["district_b"]]).astype(int)
    prof_d["projection_district"] = (prof_d.index == s["projection_district"]).astype(int)
    save_table(prof_d.reset_index(), "pbi_district_profiles.csv")

    ags = pd.read_csv(TABLES / "clean_age_sex.csv")
    save_table(ags[["district_id", "age_start", "age_group", "sex", "population_2025"]], "pbi_age_sex_2025.csv")
    save_table(diag, "pbi_kmeans_diagnostics.csv")

    # Figures we reconcile between Python and Power BI
    comp = pd.read_csv(TABLES / "p07_projection_comparison.csv").set_index("method")
    claims = pd.read_csv(TABLES / "p08_expected_claims.csv")
    recon = pd.DataFrame([
        {"figure": "Total population 1 Jan 2025 (24 districts)", "python_value": prof_d.population_2025.sum()},
        {"figure": f"{s['projection_district']} cohort-component Base total 2030",
         "python_value": comp.loc["Cohort-component Base", "P2030"]},
        {"figure": "Expected benefits year 1 (USD)", "python_value": claims.expected_benefits_usd.iloc[0]},
        {"figure": "Expected benefits year 2 (USD)", "python_value": claims.expected_benefits_usd.iloc[1]},
        {"figure": f"Districts in '{names[feats.loc[s['district_b'], 'cluster']]}' cluster",
         "python_value": int((feats.cluster == feats.loc[s['district_b'], 'cluster']).sum())},
    ])
    show_table(recon, "Python figures to reconcile with the Power BI dashboard", 2)
    save_table(recon, "pbi_reconciliation_targets.csv")
    print("\nAll Power BI tables written to outputs/tables/pbi_*.csv")
    return diag, stab, prof


if __name__ == "__main__":
    main()
