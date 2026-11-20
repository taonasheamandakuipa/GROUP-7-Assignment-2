# HASTS206 Assignment 2: Applied Demographic Analysis

**University of Zimbabwe · Department of Mathematics and Computational Sciences**
Course: HASTS206 · Lecturer: Mr. G. Mazivisa · Submission: Sunday 22 November 2026, 23:59 CAT

> **All figures in this repository are hypothetical.** They come from the synthetic teaching dataset supplied with the assignment and do not describe real districts or insured lives.

**Quick view of every result:** open [`results/HASTS206_Python_Results.html`](results/HASTS206_Python_Results.html) in any browser. It shows all Python tables, checks and figures part by part, with the member who wrote each part.

## Roles

| Part | Member | Role | Personal folder |
|---|---|---|---|
| 1 | **Lennox Tawanda Jaricha** | Project Lead and Data Engineer | [`team/01_Lennox_Tawanda_Jaricha/`](team/01_Lennox_Tawanda_Jaricha/ROLE.md) |
| 2 | **Emeldah Munyanyi** | Data Quality Analyst | [`team/02_Emeldah_Munyanyi/`](team/02_Emeldah_Munyanyi/ROLE.md) |
| 3 | **Mlungisi Ncube K** | Population Structure Analyst | [`team/03_Mlungisi_Ncube_K/`](team/03_Mlungisi_Ncube_K/ROLE.md) |
| 4 | **Gogodi Vimbai** | Demographic Rates Analyst | [`team/04_Gogodi_Vimbai/`](team/04_Gogodi_Vimbai/ROLE.md) |
| 5 | **Ketso Thabiso Mdlongwa** | Mortality and Life-Table Analyst | [`team/05_Ketso_Thabiso_Mdlongwa/`](team/05_Ketso_Thabiso_Mdlongwa/ROLE.md) |
| 6 | **Stuart Gavera** | Population Projection Modeller | [`team/06_Stuart_Gavera/`](team/06_Stuart_Gavera/ROLE.md) |
| 7 | **Taonashe Amanda Kuipa** | Scenario and Sensitivity Analyst | [`team/07_Taonashe_Amanda_Kuipa/`](team/07_Taonashe_Amanda_Kuipa/ROLE.md) |
| 8 | **Hillary Zivuku** | Actuarial Modeller (Markov Model) | [`team/08_Hillary_Zivuku/`](team/08_Hillary_Zivuku/ROLE.md) |
| 9 | **Shaun Kanojerera** | Feature Engineering Analyst | [`team/09_Shaun_Kanojerera/`](team/09_Shaun_Kanojerera/ROLE.md) |
| 10 | **Trish Tembo** | Clustering Analyst and Dashboard Integrator | [`team/10_Trish_Tembo/`](team/10_Trish_Tembo/ROLE.md) |

Each personal folder holds the member's role card (`ROLE.md`), a copy of their Python part, the output files their part produced, its console output and a one-page results view (`<folder>_results.html`). The code that actually runs is in `src/`.

## Who uploaded what, and what output they got

Each member wrote one Python part (the file name carries the part and the member's name) and checked another member's part. Every part saves its console output to `outputs/logs/<same file name>.txt`.

| Part | Member (uploaded) | File in `src/` | What the part does | Output files produced | Key result obtained |
|---|---|---|---|---|---|
| 1 | **Lennox Tawanda Jaricha** | `part01_load_and_inspect_Lennox_Tawanda_Jaricha.py` | Loads the five CSVs without changing them and checks row counts against the dataset README | `p01_file_overview.csv` | All 5 files loaded: 24, 864, 18, 3 and 96 rows, as expected |
| 2 | **Emeldah Munyanyi** | `part02_data_quality_Emeldah_Munyanyi.py` | Data-quality log: keys, joins, age and sex coverage, missing values, valid ranges, reconciliations, cleaning decisions | `p02_data_quality_log.csv`, `p02_reconciliation_by_district.csv`, `clean_districts.csv`, `clean_age_sex.csv` | 40 checks: 35 pass, 4 notes, 1 flag (missing water for D04 and D17). District deaths exceed baseline deaths by 621 (deaths among 2025 births) |
| 3 | **Mlungisi Ncube K** | `part03_selection_pyramids_ratios_Mlungisi_Ncube_K.py` | Q1a: screens all districts, selects D13 and D24, draws common-scale pyramids, computes sex and dependency ratios | `p03_district_screen.csv`, `p03_structure_ratios.csv`, `p03_pyramid_data.csv`, `selected_districts.json`, `fig01_population_pyramids.png` | Youth dependency 50.5 (D13) vs 15.5 (D24); old-age dependency 25.5 vs 44.2 |
| 4 | **Gogodi Vimbai** | `part04_balance_and_rates_Gogodi_Vimbai.py` | Q1b: balancing equation for 2025, mid-year exposure, CBR, CDR and NMR | `p04_balance_and_rates_all_districts.csv`, `fig02_crude_rates.png` | Baseline 2,636,363; reconstructed 1 Jan 2026 = reported 2,658,389 in all 24 districts. D13 grows 6.35 per 1,000, D24 falls 9.71 per 1,000 |
| 5 | **Ketso Thabiso Mdlongwa** | `part05_life_table_Ketso_Thabiso_Mdlongwa.py` | Q1c: abridged life table (q, l, d, L, T, e) with numerical checks | `p05_life_table.csv`, `p05_life_table_checks.csv`, `fig03_life_table.png` | e0 = 73.11 years, e65 = 18.10 years; all 5 checks pass |
| 6 | **Stuart Gavera** | `part06_growth_and_cohort_component_Stuart_Gavera.py` | Q2a–b: arithmetic and geometric growth; cohort-component projection of D13 under Low, Base and High | `p06_growth_models.csv`, `p06_cohort_component_summary.csv`, `p06_cohort_component_detail.csv` | 2030: arithmetic 189,233; geometric 190,568; cohort-component Low 175,310, Base 181,638, High 188,034; accounting gap 0 |
| 7 | **Taonashe Amanda Kuipa** | `part07_projection_comparison_Taonashe_Amanda_Kuipa.py` | Q2c: compares methods, age shares and the fertility sensitivity | `p07_projection_comparison.csv`, `p07_fertility_sensitivity.csv`, `pbi_projection_by_age_sex.csv`, `fig04`, `fig05` | Base with High fertility adds 2,288 children aged 0–4 (+12.2%); share under 15 about 29% |
| 8 | **Hillary Zivuku** | `part08_markov_model_Hillary_Zivuku.py` | Q3: generator Q, holding times, next-jump probabilities, P(1) and P(2), occupancy, expected benefits | `p08_*.csv`, `pbi_markov_*.csv`, `pbi_expected_claims_by_district.csv`, `fig06`, `fig07` | Mean holding time 8.23 years (healthy), 3.20 years (ill). Expected benefits USD 616,501 (year 1) and USD 634,457 (year 2) |
| 9 | **Shaun Kanojerera** | `part09_clustering_features_Shaun_Kanojerera.py` | Q4a: district feature table, KNN imputation, outlier check, standardisation | `p09_cluster_features.csv`, `p09_imputation_notes.csv`, `p09_outlier_check.csv`, `fig08_feature_boxplots.png` | Water imputed: D04 → 35.9%, D17 → 73.6%; no outliers (largest abs(z) = 1.71) |
| 10 | **Trish Tembo** | `part10_kmeans_and_exports_Trish_Tembo.py` | Q4b–c: k-means for k = 1–6, silhouettes, stability, cluster profiles, Power BI tables | `p10_kmeans_diagnostics.csv`, `p10_stability_checks.csv`, `pbi_cluster_centroids.csv`, `pbi_district_profiles.csv`, `pbi_reconciliation_targets.csv`, `fig09`–`fig11` | k = 3 chosen (WCSS falls 94% from k = 2 to 3; mean silhouette 0.864); ARI = 1.000 under all three stability checks |

**Who checked whose part:** Trish Tembo checked Part 1 · Gogodi Vimbai checked Part 2 · Ketso Thabiso Mdlongwa checked Part 3 · Mlungisi Ncube K checked Part 4 · Emeldah Munyanyi checked Part 5 · Taonashe Amanda Kuipa checked Part 6 · Stuart Gavera checked Part 7 · Shaun Kanojerera checked Part 8 · Hillary Zivuku checked Part 9 · Lennox Tawanda Jaricha checked Part 10.

## Repository layout

```
data/raw/            original CSVs and dataset README (never edited)
src/
  common.py                                   shared paths, settings and helpers
  part01_load_and_inspect_Lennox_Tawanda_Jaricha.py
  part02_data_quality_Emeldah_Munyanyi.py
  part03_selection_pyramids_ratios_Mlungisi_Ncube_K.py
  part04_balance_and_rates_Gogodi_Vimbai.py
  part05_life_table_Ketso_Thabiso_Mdlongwa.py
  part06_growth_and_cohort_component_Stuart_Gavera.py
  part07_projection_comparison_Taonashe_Amanda_Kuipa.py
  part08_markov_model_Hillary_Zivuku.py
  part09_clustering_features_Shaun_Kanojerera.py
  part10_kmeans_and_exports_Trish_Tembo.py
  run_all.py                                  runs Parts 1-10 in order
  team.py                                     roles, duties and output files of each member
  make_results_html.py                        builds results/HASTS206_Python_Results.html
  make_team_packages.py                       builds the team/ folders
  make_powerbi_workbook.py                    gathers the dashboard tables into one workbook
results/HASTS206_Python_Results.html          all Python results on one page
team/                one folder per member: role card, their code, their outputs and results page
notebook/            executed notebook (.ipynb) and its HTML export
outputs/tables/      every result table (pXX_*.csv) and dashboard table (pbi_*.csv)
outputs/figures/     fig01-fig11
outputs/logs/        console output of each member's part
outputs/run_log.txt  console output of the full run
powerbi/             HASTS206_Assignment2_Dashboard.pbix, its CSVs and workbook, and the pbip/ project version
report/              PDF report and editable Word version
presentation/        speaking script for the recorded group presentation
```

## How to rerun everything

Requires Python 3.10 or newer.

```bash
git clone <repository-url>
cd HASTS206_Assignment2
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python src/run_all.py                # Parts 1-10, about 3 seconds
python src/make_results_html.py      # rebuild the results page
python src/make_team_packages.py     # rebuild each member's folder
python src/make_powerbi_workbook.py  # refresh the Power BI tables
```

Each part can also be run on its own, for example `python src/part08_markov_model_Hillary_Zivuku.py`. Parts 4–10 read `outputs/tables/selected_districts.json`, which Part 3 writes, so run Part 3 at least once first.

To re-execute the notebook and rebuild its HTML:

```bash
cd notebook
jupyter nbconvert --to notebook --execute --inplace HASTS206_Assignment2_Analysis.ipynb
jupyter nbconvert --to html HASTS206_Assignment2_Analysis.ipynb
```

All paths are relative to the repository root, so the code runs from any folder on any machine.

## Main settings (change them in one place)

| Setting | Where | Value |
|---|---|---|
| Selected districts | Part 3 `main()` | D13 and D24; projection district D13 |
| k-means initialisations and seeds | `common.py` | `N_INIT = 50`, `SEED_PRIMARY = 2026`, `SEED_CHECK = 7` |
| Chosen number of clusters | Part 10 | `CHOSEN_K = 3` |
| Life-table radix | `common.py` | 100,000 |
| Benefit per death | `common.py` | USD 1,000 |
| Birth sex split | `common.py` | 49% female, 51% male |
| What-if for the presentation | `common.py` | `ILL_DEATH_MULTIPLIER = 1.0` (set 1.2 to rerun Part 8 with 20% higher ill-to-dead intensity) |

## Power BI dashboard

Open `powerbi/HASTS206_Assignment2_Dashboard.pbix`. It has five pages: District profiles, Projection scenarios, Insured occupancy and claims, Clustering, and Reconciliation. The district, region, scenario and cluster slicers filter the visuals. The Reconciliation page shows that the dashboard and Python agree on five figures (difference 0).

The model reads the CSV files in `powerbi/` through one parameter, `DataFolder`. If the repository is in a different folder on your computer, open **Transform data → Edit parameters**, set `DataFolder` to the full path of your `powerbi\` folder (ending with a backslash), then click **Refresh**. After rerunning Python, run `make_powerbi_workbook.py` and click **Refresh**.

## Group workflow on GitHub

Each member uploaded their own `src/partXX_..._<Name>.py` file from their own GitHub account on a branch named after the part (for example `part08-hillary-zivuku`). They then opened a pull request, which the checking member listed above reviewed before merging. The commit history of each file shows who wrote it and who reviewed it.
