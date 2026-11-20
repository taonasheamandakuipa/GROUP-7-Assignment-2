# Part 6: Growth models and cohort-component projection

**Member:** Stuart Gavera  
**Role:** Population Projection Modeller  
**Assignment question:** Q2a, Q2b  
**Python file:** `src/part06_growth_and_cohort_component_Stuart_Gavera.py`  
**Checked by:** Taonashe Amanda Kuipa

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Fit arithmetic and geometric growth to the 2020 and 2025 totals
- Build the cohort-component projection of D13 to 1 January 2030
- Run the Low, Base and High scenarios
- Check the accounting identity and that no cell is negative

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part06_growth_and_cohort_component_Stuart_Gavera.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p06_growth_models.csv` |
| Table | `outputs/tables/p06_cohort_component_summary.csv` |
| Table | `outputs/tables/p06_cohort_component_detail.csv` |
| Console output | `console_output.txt` |
| Results page | `06_Stuart_Gavera_results.html` |

## Your key result

2030 totals: arithmetic 189,233; geometric 190,568; cohort-component Low 175,310, Base 181,638, High 188,034. Accounting gap 0.

## On GitHub

Upload `src/part06_growth_and_cohort_component_Stuart_Gavera.py` from your own account on a branch named `part06-stuart`, open a pull request, and ask Taonashe Amanda Kuipa to review it before merging.
