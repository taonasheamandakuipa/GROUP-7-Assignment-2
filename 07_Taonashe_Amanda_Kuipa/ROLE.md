# Part 7: Projection comparison and fertility sensitivity

**Member:** Taonashe Amanda Kuipa  
**Role:** Scenario and Sensitivity Analyst  
**Assignment question:** Q2c  
**Python file:** `src/part07_projection_comparison_Taonashe_Amanda_Kuipa.py`  
**Checked by:** Stuart Gavera

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Compare the cohort-component totals with the trend models
- Report the shares under 15 and aged 65 and over
- Run the fertility sensitivity and state its planning implication
- Prepare the projection tables for the Power BI dashboard

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part07_projection_comparison_Taonashe_Amanda_Kuipa.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p07_projection_comparison.csv` |
| Table | `outputs/tables/p07_fertility_sensitivity.csv` |
| Table | `outputs/tables/pbi_projection_by_age_sex.csv` |
| Figure | `outputs/figures/fig04_projection_comparison.png` |
| Figure | `outputs/figures/fig05_projection_age_profile.png` |
| Console output | `console_output.txt` |
| Results page | `07_Taonashe_Amanda_Kuipa_results.html` |

## Your key result

Base with High fertility adds 2,288 children aged 0-4 (+12.2%); share under 15 stays near 29%.

## On GitHub

Upload `src/part07_projection_comparison_Taonashe_Amanda_Kuipa.py` from your own account on a branch named `part07-taonashe`, open a pull request, and ask Stuart Gavera to review it before merging.
