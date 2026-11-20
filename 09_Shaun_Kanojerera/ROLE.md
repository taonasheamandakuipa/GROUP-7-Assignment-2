# Part 9: Clustering features, imputation and outliers

**Member:** Shaun Kanojerera  
**Role:** Feature Engineering Analyst  
**Assignment question:** Q4a  
**Python file:** `src/part09_clustering_features_Shaun_Kanojerera.py`  
**Checked by:** Hillary Zivuku

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Build the four-feature district table for clustering
- Impute the two missing water values and justify the rule
- Check for outliers and standardise the features
- Explain why the district identifier is left out

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part09_clustering_features_Shaun_Kanojerera.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p09_cluster_features.csv` |
| Table | `outputs/tables/p09_imputation_notes.csv` |
| Table | `outputs/tables/p09_outlier_check.csv` |
| Figure | `outputs/figures/fig08_feature_boxplots.png` |
| Console output | `console_output.txt` |
| Results page | `09_Shaun_Kanojerera_results.html` |

## Your key result

Water imputed: D04 35.9%, D17 73.6%. No outliers (largest absolute z = 1.71).

## On GitHub

Upload `src/part09_clustering_features_Shaun_Kanojerera.py` from your own account on a branch named `part09-shaun`, open a pull request, and ask Hillary Zivuku to review it before merging.
