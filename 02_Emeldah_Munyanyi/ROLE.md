# Part 2: Data-quality log and cleaning

**Member:** Emeldah Munyanyi  
**Role:** Data Quality Analyst  
**Assignment question:** Data quality  
**Python file:** `src/part02_data_quality_Emeldah_Munyanyi.py`  
**Checked by:** Gogodi Vimbai

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Check keys, joins, age and sex coverage, missing values and valid ranges
- Reconcile births, migration and deaths between the files
- Explain the scope difference between district deaths and baseline deaths
- Record every cleaning decision and write the clean copies

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part02_data_quality_Emeldah_Munyanyi.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p02_data_quality_log.csv` |
| Table | `outputs/tables/p02_reconciliation_by_district.csv` |
| Table | `outputs/tables/clean_districts.csv` |
| Table | `outputs/tables/clean_age_sex.csv` |
| Console output | `console_output.txt` |
| Results page | `02_Emeldah_Munyanyi_results.html` |

## Your key result

40 checks: 35 pass, 4 notes, 1 flag (water missing for D04 and D17). District deaths exceed baseline deaths by 621 (deaths among 2025 births).

## On GitHub

Upload `src/part02_data_quality_Emeldah_Munyanyi.py` from your own account on a branch named `part02-emeldah`, open a pull request, and ask Gogodi Vimbai to review it before merging.
