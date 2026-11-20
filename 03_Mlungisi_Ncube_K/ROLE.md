# Part 3: District selection, pyramids and ratios

**Member:** Mlungisi Ncube K  
**Role:** Population Structure Analyst  
**Assignment question:** Q1a  
**Python file:** `src/part03_selection_pyramids_ratios_Mlungisi_Ncube_K.py`  
**Checked by:** Ketso Thabiso Mdlongwa

> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.

## Responsibilities

- Screen all 24 districts and choose two contrasting districts (D13 and D24)
- Draw population pyramids on a common scale with units
- Calculate the sex ratio and the youth and old-age dependency ratios
- Start the input-to-dashboard trace in the video

## How to run your part

From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):

```bash
python src/part03_selection_pyramids_ratios_Mlungisi_Ncube_K.py
```

Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.

## Your output files

| Type | File (in this folder) |
|---|---|
| Table | `outputs/tables/p03_district_screen.csv` |
| Table | `outputs/tables/p03_structure_ratios.csv` |
| Table | `outputs/tables/p03_pyramid_data.csv` |
| Table | `outputs/tables/selected_districts.json` |
| Figure | `outputs/figures/fig01_population_pyramids.png` |
| Console output | `console_output.txt` |
| Results page | `03_Mlungisi_Ncube_K_results.html` |

## Your key result

Youth dependency 50.5 (D13) vs 15.5 (D24); old-age dependency 25.5 vs 44.2.

## On GitHub

Upload `src/part03_selection_pyramids_ratios_Mlungisi_Ncube_K.py` from your own account on a branch named `part03-mlungisi`, open a pull request, and ask Ketso Thabiso Mdlongwa to review it before merging.
