"""
make_results_html.py - builds results/HASTS206_Python_Results.html, one self-contained page that
shows every Python result (tables, checks and figures) part by part, with the member who wrote
each part. Run after run_all.py:   python src/make_results_html.py
"""
import base64
import html
import re
from datetime import date

import numpy as np
import pandas as pd

from common import ROOT, TABLES, FIGURES

OUT = ROOT / "results" / "HASTS206_Python_Results.html"
LOGS = ROOT / "outputs" / "logs"

from team import TEAM

PARTS = [(m["part"], m["title"], m["name"], m["file"], m["checks"], m["question"]) for m in TEAM]
ROLES = {m["part"]: m["role"] for m in TEAM}


def t(name):
    return pd.read_csv(TABLES / name)


def fmt(v, col=""):
    if isinstance(v, (bool, np.bool_)):
        return "Yes" if v else "No"
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "&ndash;"
    if isinstance(v, (int, np.integer)):
        return f"{v:,}" if abs(v) >= 10000 or col not in ("k", "age_start", "t_years") else str(v)
    if isinstance(v, (float, np.floating)):
        c = col.lower()
        if any(k in c for k in ("probability", "intensity", "qx", "mx", "silhouette", "ari", "rate_per_year")) or c in ("h", "i", "d"):
            return f"{v:.4f}" if abs(v) < 10 else f"{v:,.2f}"
        if float(v).is_integer() and abs(v) >= 100:
            return f"{v:,.0f}"
        if abs(v) >= 1000:
            return f"{v:,.1f}" if "exposure" in c else f"{v:,.0f}"
        return f"{v:,.2f}"
    s = str(v)
    if s in ("PASS", "Matches", "True"):
        return f'<span class="pill ok">{s}</span>'
    if s in ("FLAG", "FAIL", "Check"):
        return f'<span class="pill warn">{s}</span>'
    if s == "NOTE":
        return f'<span class="pill note">{s}</span>'
    return html.escape(s)


def table(df, caption="", cols=None, rename=None, index=False):
    d = df.copy()
    if index:
        d = d.reset_index()
    if cols:
        d = d[cols]
    if rename:
        d = d.rename(columns=rename)
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in d.columns)
    body = []
    for _, row in d.iterrows():
        cells = []
        for c in d.columns:
            v = row[c]
            num = isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool)
            cells.append(f'<td class="{"num" if num else ""}">{fmt(v, str(c))}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="tbl">{cap}<div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div></figure>'


def fig(name, caption):
    data = base64.b64encode((FIGURES / name).read_bytes()).decode()
    return f'<figure class="img"><img src="data:image/png;base64,{data}" alt="{html.escape(caption)}"><figcaption>{caption}</figcaption></figure>'


def kpis(items):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="kv">{v}</div><div class="kl">{l}</div></div>' for l, v in items) + "</div>"


def note(text):
    return f'<p class="note">{text}</p>'


def log_block(n):
    files = sorted(LOGS.glob(f"part{n:02d}_*.txt"))
    if not files:
        return ""
    txt = html.escape(files[0].read_text(encoding="utf-8"))
    return f'<details><summary>Console output of Part {n} ({files[0].name})</summary><pre>{txt}</pre></details>'


# ------------------------------------------------------------------------------------- content
def part_content(n):
    if n == 1:
        ov = t("p01_file_overview.csv")
        return kpis([("Files loaded", "5"), ("Rows in age_sex.csv", "864"), ("Districts", "24"), ("Insured rows", "96")]) + \
            table(ov, "Supplied files: rows, columns and missing cells", ["file", "rows", "columns", "missing_cells", "column_names"])
    if n == 2:
        q = t("p02_data_quality_log.csv")
        rec = t("p02_reconciliation_by_district.csv")
        c = q.status.value_counts()
        return kpis([("Checks recorded", len(q)), ("Passed", c.get("PASS", 0)), ("Notes", c.get("NOTE", 0)), ("Flags", c.get("FLAG", 0)),
                     ("Deaths among 2025 births", f"{int(rec.deaths_among_2025_births.sum()):,}")]) + \
            table(q, "Data-quality log (outputs/tables/p02_data_quality_log.csv)", ["check_no", "file", "check", "result", "status", "decision_or_action"]) + \
            table(rec, "Reconciliation by district: births, migration, scope of deaths and the 2026 balance",
                  ["district_id", "population_2025_agesex", "births_2025", "births_female_rows", "deaths_2025", "baseline_deaths_agesex",
                   "deaths_among_2025_births", "balance_2026", "population_2026", "balance_gap"])
    if n == 3:
        sc = t("p03_district_screen.csv")
        r = t("p03_structure_ratios.csv").set_index("district_id").T.reset_index().rename(columns={"index": "indicator"})
        return note("Selected districts: <b>D13</b> (young, high fertility, net out-migration) and <b>D24</b> (ageing, natural decrease). "
                    "Both have about 173,000 residents, so the common-scale pyramids compare shape rather than size. D13 is the projection district.") + \
            fig("fig01_population_pyramids.png", "Figure 1. Population pyramids on 1 January 2025, common scale") + \
            table(r, "Sex ratio and dependency ratios, 1 January 2025") + \
            table(sc.sort_values("share_65plus_pct"), "Screening table for all 24 districts (sorted by share 65+)",
                  ["district_id", "region", "population_2025", "share_u15_pct", "share_65plus_pct", "cbr", "cdr", "nmr", "piped_water_pct"])
    if n == 4:
        b = t("p04_balance_and_rates_all_districts.csv").set_index("district_id")
        sel = b.loc[["D13", "D24"], ["population_2025", "births_2025", "deaths_2025", "arrivals_2025", "departures_2025",
                                       "reconstructed_2026", "population_2026", "difference_reported_minus_reconstructed",
                                       "exposure_2025", "CBR_per_1000", "CDR_per_1000", "RNI_per_1000", "NMR_per_1000", "growth_rate_per_1000"]]
        return kpis([("Population 1 Jan 2025", f"{int(b.population_2025.sum()):,}"), ("Reported 1 Jan 2026", f"{int(b.population_2026.sum()):,}"),
                     ("Reconstructed 1 Jan 2026", f"{int(b.reconstructed_2026.sum()):,}"), ("Districts with a gap", int((b.difference_reported_minus_reconstructed != 0).sum()))]) + \
            table(sel.T.reset_index().rename(columns={"index": "quantity"}), "Balancing equation and crude rates per 1,000 (D13 and D24)") + \
            fig("fig02_crude_rates.png", "Figure 2. Drivers of 2025 growth") + \
            table(b.reset_index(), "All districts: balance and rates",
                  ["district_id", "population_2025", "population_2026", "reconstructed_2026", "CBR_per_1000", "CDR_per_1000", "NMR_per_1000", "growth_rate_per_1000"])
    if n == 5:
        lt = t("p05_life_table.csv")
        ch = t("p05_life_table_checks.csv")
        return kpis([("Life expectancy at birth", f"{lt.ex.iloc[0]:.2f} years"), ("Life expectancy at 65", f"{lt.ex.iloc[13]:.2f} years"),
                     ("Survivors to 65", f"{lt.lx.iloc[13]:,.0f} of 100,000")]) + \
            table(lt, "Abridged life table, radix 100,000") + table(ch, "Numerical checks") + \
            fig("fig03_life_table.png", "Figure 3. Survivorship l(x) and life expectancy e(x)")
    if n == 6:
        gm = t("p06_growth_models.csv").T.reset_index()
        gm.columns = ["quantity", "value"]
        s = t("p06_cohort_component_summary.csv").set_index("scenario").T.reset_index().rename(columns={"index": "component"})
        det = t("p06_cohort_component_detail.csv")
        wide = det.pivot_table(index=["age_start", "age_group", "sex"], columns="scenario", values="pop_2030").reset_index()[["age_group", "sex", "Low", "Base", "High"]]
        return table(gm, "Arithmetic and geometric growth (D13), fitted to 2020 and 2025") + \
            table(s, "Cohort-component accounting by scenario (identity gap and negative cells must be 0)") + \
            table(wide, "Projected population on 1 January 2030 by age and sex, D13")
    if n == 7:
        c = t("p07_projection_comparison.csv")
        sn = t("p07_fertility_sensitivity.csv").rename(columns={"sex": "group"})
        return table(c, "Totals for 1 January 2030 and age shares by method") + \
            fig("fig04_projection_comparison.png", "Figure 4. D13 total on 1 January 2030 by method") + \
            fig("fig05_projection_age_profile.png", "Figure 5. D13 age distribution, baseline and scenarios") + \
            table(sn, "Sensitivity: ages 0-4 when only the Base fertility multiplier is raised to 1.12")
    if n == 8:
        est = t("p08_transition_intensities.csv")
        Q = t("p08_generator_Q.csv")
        hj = t("p08_holding_and_jump.csv")
        tm = t("pbi_markov_transition_matrices.csv")
        p1 = tm[tm.t_years == 1].pivot(index="from_state", columns="to_state", values="probability").loc[["H", "I", "D"], ["H", "I", "D"]].reset_index()
        p2 = tm[tm.t_years == 2].pivot(index="from_state", columns="to_state", values="probability").loc[["H", "I", "D"], ["H", "I", "D"]].reset_index()
        cl = t("p08_expected_claims.csv")
        return kpis([("Benefits year 1", f"USD {cl.expected_benefits_usd.iloc[0]:,.0f}"), ("Benefits year 2", f"USD {cl.expected_benefits_usd.iloc[1]:,.0f}"),
                     ("Two-year total", f"USD {cl.expected_benefits_usd.iloc[2]:,.0f}")]) + \
            fig("fig06_markov_state_diagram.png", "Figure 6. Healthy-ill-dead state diagram with intensities") + \
            table(est, "Pooled jumps, exposure (one copy per district-origin) and intensities") + \
            table(Q, "Generator matrix Q (rows sum to zero)") + \
            table(hj, "Mean holding times and next-jump probabilities from the ill state") + \
            '<div class="two">' + table(p1, "P(1) = expm(Q)") + table(p2, "P(2) = expm(2Q)") + "</div>" + \
            table(t("p08_probability_checks.csv"), "Probability checks") + \
            table(t("p08_expected_occupancy.csv"), "Expected occupancy n(t) = n(0) P(t)") + \
            table(cl, "Expected deaths and benefit payments (USD 1,000 per death, undiscounted)") + \
            fig("fig07_markov_occupancy.png", "Figure 7. Expected occupancy over five years")
    if n == 9:
        f = t("p09_cluster_features.csv")
        return table(t("p09_imputation_notes.csv"), "KNN imputation (k = 3) of the two missing water values") + \
            table(t("p09_outlier_check.csv"), "Outlier check: 1.5 x IQR rule and |z| > 3") + \
            fig("fig08_feature_boxplots.png", "Figure 8. Distribution of the four clustering features") + \
            table(f, "Feature table in original units (water imputed for D04 and D17)",
                  ["district_id", "region", "share_u15_pct", "share_65plus_pct", "nmr_per_1000", "piped_water_pct", "piped_water_imputed_flag"])
    if n == 10:
        return table(t("p10_kmeans_diagnostics.csv"), "WCSS, % reduction and mean silhouette (50 initialisations per fit)") + \
            fig("fig09_wcss_silhouette.png", "Figure 9. Elbow plot and mean silhouette") + \
            fig("fig10_silhouette_candidates.png", "Figure 10. Individual silhouettes for k = 2 and k = 3") + \
            table(t("p10_stability_checks.csv"), "Stability of the k = 3 solution (adjusted Rand index)") + \
            table(t("pbi_cluster_centroids.csv"), "Cluster sizes and centroids (original units)",
                  ["cluster", "cluster_name", "n_districts", "share_u15_pct", "share_65plus_pct", "nmr_per_1000", "piped_water_pct", "districts"]) + \
            fig("fig11_cluster_map.png", "Figure 11. Districts coloured by cluster") + \
            table(t("pbi_reconciliation_targets.csv"), "Figures reconciled with the Power BI dashboard")
    return ""


CSS = """
:root{--ink:#14213d;--muted:#5b6475;--blue:#0d47a1;--blue2:#1e88e5;--sky:#e8f2fd;--line:#dde5ef;--bg:#f6f9fc}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:15px/1.55 "Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header{background:linear-gradient(120deg,#0a3f8f 0%,#1565c0 55%,#29a3ee 100%);color:#fff;padding:42px 48px 36px;position:relative;overflow:hidden}
header:after{content:"";position:absolute;right:-120px;top:-140px;width:520px;height:520px;border-radius:50%;background:rgba(255,255,255,.08)}
header h1{margin:0 0 6px;font-size:30px;letter-spacing:.2px}header p{margin:0;opacity:.9;max-width:900px}
.hyp{display:inline-block;margin-top:14px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);padding:4px 12px;border-radius:999px;font-size:13px}
main{min-width:0}.wrap{display:grid;grid-template-columns:270px minmax(0,1fr);gap:32px;max-width:1440px;margin:0 auto;padding:28px 32px 60px}
nav{position:sticky;top:20px;align-self:start;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px}
nav h3{margin:4px 8px 10px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
nav a{display:block;padding:7px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:13.5px}
nav a:hover{background:var(--sky)}nav a small{display:block;color:var(--muted);font-size:12px}
section{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px 28px;margin-bottom:26px;box-shadow:0 1px 2px rgba(16,40,80,.04)}
.sec-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:18px}
.sec-head h2{margin:0;font-size:21px;color:var(--blue)}.tag{font-size:12px;color:var(--blue2);font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.who{text-align:right;font-size:13px;color:var(--muted);white-space:nowrap}.who b{color:var(--ink);font-size:14px}.role{display:inline-block;margin:3px 0;background:#e8f0fe;color:#1a56b8;border-radius:999px;padding:1px 10px;font-weight:600;font-size:12px}
code{background:var(--sky);padding:1px 6px;border-radius:5px;font-size:12.5px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:4px 0 18px}
.kpi{background:linear-gradient(180deg,#f3f8fe,#eaf3fd);border:1px solid #d6e6f8;border-radius:10px;padding:12px 14px}
.kv{font-size:21px;font-weight:700;color:var(--blue)}.kl{font-size:12.5px;color:var(--muted)}
figure{margin:0 0 20px}figcaption{font-size:13px;font-weight:600;color:var(--blue);margin:0 0 8px}
figure.img{text-align:center}figure.img img{max-width:min(100%,920px);height:auto;border:1px solid var(--line);border-radius:10px;padding:8px;background:#fff}
figure.img figcaption{margin:8px 0 0;font-weight:500;color:var(--muted);font-style:italic}
.scroll{overflow:auto;max-height:520px;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13px}thead th{position:sticky;top:0;background:#1565c0;color:#fff;text-align:left;font-weight:600;padding:8px 10px;white-space:nowrap}
td{padding:7px 10px;border-top:1px solid #edf1f6;vertical-align:top}tbody tr:nth-child(even){background:#f8fbff}tbody tr:hover{background:#eef5fe}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11.5px;font-weight:700}.ok{background:#e3f6ea;color:#17803d}.warn{background:#fff1e0;color:#b55d00}.note{background:#e8f0fe;color:#1a56b8}
p.note{background:#f3f8fe;border-left:4px solid var(--blue2);padding:10px 14px;border-radius:6px;margin:0 0 18px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
details{margin-top:6px;border:1px solid var(--line);border-radius:10px;background:#fbfcfe}summary{cursor:pointer;padding:10px 14px;font-weight:600;color:var(--blue)}
pre{margin:0;padding:12px 16px;max-height:420px;overflow:auto;font:12px/1.45 Consolas,"Courier New",monospace;background:#0f1b2d;color:#d7e3f4;border-radius:0 0 10px 10px}
.team table td,.team table th{font-size:13px}footer{text-align:center;color:var(--muted);font-size:12.5px;padding:10px 0 30px}
@media (max-width:980px){.wrap{grid-template-columns:1fr}nav{position:static}.two{grid-template-columns:1fr}}
@media print{nav{display:none}.wrap{display:block}.scroll{max-height:none}section{break-inside:avoid-page}}
"""


def main():
    OUT.parent.mkdir(exist_ok=True)
    team = pd.DataFrame([{"Part": p, "Member": who, "Role": ROLES[p], "Topic": title, "Checked by": chk, "File (src/)": f}
                         for p, title, who, f, chk, q in PARTS])
    nav = "".join(f'<a href="#part{p}">Part {p}: {html.escape(title)}<small>{who} &middot; {ROLES[p]}</small></a>' for p, title, who, f, chk, q in PARTS)
    sections = []
    for p, title, who, f, chk, q in PARTS:
        sections.append(f"""
<section id="part{p}">
  <div class="sec-head"><div><div class="tag">Part {p} &middot; {q}</div><h2>{html.escape(title)}</h2>
  <div style="margin-top:6px"><code>src/{f}</code></div></div>
  <div class="who">Written by<br><b>{who}</b><br><span class="role">{ROLES[p]}</span><br>Checked by {chk}</div></div>
  {part_content(p)}
  {log_block(p)}
</section>""")
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HASTS206 Assignment 2 - Python results</title><style>{CSS}</style></head><body>
<header><h1>HASTS206 Assignment 2: Python results</h1>
<p>University of Zimbabwe, Department of Mathematics and Computational Sciences. Every table and figure below was produced by
<code style="background:rgba(255,255,255,.18);color:#fff">python src/run_all.py</code> and is read directly from <code style="background:rgba(255,255,255,.18);color:#fff">outputs/</code>.</p>
<span class="hyp">All figures are hypothetical: synthetic teaching data</span></header>
<div class="wrap"><nav><h3>Contents</h3><a href="#team">Group and contributions</a>{nav}</nav><main>
<section id="team" class="team"><div class="sec-head"><div><div class="tag">Overview</div><h2>Group and contributions</h2></div></div>
{table(team, "Roles: who wrote and who checked each part")}</section>
{''.join(sections)}
<footer>Generated on {date.today():%d %B %Y} by src/make_results_html.py &middot; HASTS206 Assignment 2</footer>
</main></div></body></html>"""
    OUT.write_text(page, encoding="utf-8")
    print(f"Results page written: results/{OUT.name} ({OUT.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
