# Part 8: Three-state Markov model and claims

**Member:** Hillary Zivuku  
**Role:** Actuarial Modeller (Markov Model)  
**Assignment question:** Q3  
**Python file:** `src/part08_markov_model_Hillary_Zivuku.py`  
**Checked by:** Shaun Kanojerera

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Estimate the healthy-ill-dead generator Q from pooled data
- Calculate holding times and next-jump probabilities
- Compute P(1) and P(2), expected occupancy and expected benefits
- Change an assumption and rerun the code in the video

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part08_markov_model_Hillary_Zivuku.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p08_transition_intensities.csv` |
| Table | `outputs/tables/p08_generator_Q.csv` |
| Table | `outputs/tables/p08_holding_and_jump.csv` |
| Table | `outputs/tables/p08_probability_checks.csv` |
| Table | `outputs/tables/p08_expected_occupancy.csv` |
| Table | `outputs/tables/p08_expected_claims.csv` |
| Table | `outputs/tables/pbi_markov_transition_matrices.csv` |
| Table | `outputs/tables/pbi_markov_occupancy_by_district.csv` |
| Table | `outputs/tables/pbi_expected_claims_by_district.csv` |
| Figure | `outputs/figures/fig06_markov_state_diagram.png` |
| Figure | `outputs/figures/fig07_markov_occupancy.png` |
| Console output | `console_output.txt` |
| Results page | `08_Hillary_Zivuku_results.html` |

## Your key result

Holding times 8.23 years (healthy) and 3.20 years (ill). Expected benefits USD 616,501 in year 1 and USD 634,457 in year 2.

## On GitHub

Upload `src/part08_markov_model_Hillary_Zivuku.py` from your own account on a branch named `part08-hillary`, open a pull request, and ask Shaun Kanojerera to review it before merging.
