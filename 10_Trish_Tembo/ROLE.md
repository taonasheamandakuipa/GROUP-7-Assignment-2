# Part 10: k-means, stability and dashboard exports

**Member:** Trish Tembo  
**Role:** Clustering Analyst and Dashboard Integrator  
**Assignment question:** Q4b, Q4c  
**Python file:** `src/part10_kmeans_and_exports_Trish_Tembo.py`  
**Checked by:** Lennox Tawanda Jaricha

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Fit k-means for k = 1 to 6 and read WCSS and silhouettes
- Choose k, check stability and describe the cluster profiles
- Export the tables the Power BI dashboard reads
- Present the two recommendations and close the video

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part10_kmeans_and_exports_Trish_Tembo.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p10_kmeans_diagnostics.csv` |
| Table | `outputs/tables/p10_stability_checks.csv` |
| Table | `outputs/tables/pbi_cluster_centroids.csv` |
| Table | `outputs/tables/pbi_district_profiles.csv` |
| Table | `outputs/tables/pbi_age_sex_2025.csv` |
| Table | `outputs/tables/pbi_kmeans_diagnostics.csv` |
| Table | `outputs/tables/pbi_reconciliation_targets.csv` |
| Figure | `outputs/figures/fig09_wcss_silhouette.png` |
| Figure | `outputs/figures/fig10_silhouette_candidates.png` |
| Figure | `outputs/figures/fig11_cluster_map.png` |
| Console output | `console_output.txt` |
| Results page | `10_Trish_Tembo_results.html` |

## Your key result

k = 3 chosen (WCSS falls 94% from k = 2 to 3; mean silhouette 0.864). ARI = 1.000 under all three stability checks.

## On GitHub

Upload `src/part10_kmeans_and_exports_Trish_Tembo.py` from your own account on a branch named `part10-trish`, open a pull request, and ask Lennox Tawanda Jaricha to review it before merging.
