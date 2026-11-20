# Part 5: Abridged life table

**Member:** Ketso Thabiso Mdlongwa  
**Role:** Mortality and Life-Table Analyst  
**Assignment question:** Q1c  
**Python file:** `src/part05_life_table_Ketso_Thabiso_Mdlongwa.py`  
**Checked by:** Emeldah Munyanyi

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Build the abridged life table: m, q, l, d, L, T and e
- Handle the open 85+ interval correctly
- Show a numerical check by hand
- Interpret life expectancy at birth and at 65

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part05_life_table_Ketso_Thabiso_Mdlongwa.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p05_life_table.csv` |
| Table | `outputs/tables/p05_life_table_checks.csv` |
| Figure | `outputs/figures/fig03_life_table.png` |
| Console output | `console_output.txt` |
| Results page | `05_Ketso_Thabiso_Mdlongwa_results.html` |

## Your key result

e0 = 73.11 years and e65 = 18.10 years; all five checks pass.

## On GitHub

Upload `src/part05_life_table_Ketso_Thabiso_Mdlongwa.py` from your own account on a branch named `part05-ketso`, open a pull request, and ask Emeldah Munyanyi to review it before merging.
