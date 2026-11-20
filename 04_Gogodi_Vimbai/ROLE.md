# Part 4: Balancing equation and crude rates

**Member:** Gogodi Vimbai  
**Role:** Demographic Rates Analyst  
**Assignment question:** Q1b  
**Python file:** `src/part04_balance_and_rates_Gogodi_Vimbai.py`  
**Checked by:** Mlungisi Ncube K

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Sum the baseline population and rebuild the 1 January 2026 population
- Calculate mid-year exposure, CBR, CDR, natural increase and NMR
- Explain what drives growth in D13 and D24
- Finish the input-to-dashboard trace in Power BI

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part04_balance_and_rates_Gogodi_Vimbai.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p04_balance_and_rates_all_districts.csv` |
| Figure | `outputs/figures/fig02_crude_rates.png` |
| Console output | `console_output.txt` |
| Results page | `04_Gogodi_Vimbai_results.html` |

## Your key result

Baseline 2,636,363; rebuilt 1 Jan 2026 = reported 2,658,389 in all 24 districts. D13 grows 6.35 per 1,000; D24 falls 9.71 per 1,000.

## On GitHub

Upload `src/part04_balance_and_rates_Gogodi_Vimbai.py` from your own account on a branch named `part04-gogodi`, open a pull request, and ask Mlungisi Ncube K to review it before merging.
