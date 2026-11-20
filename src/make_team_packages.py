"""
make_team_packages.py - gives each member their own folder in team/ with:
  * ROLE.md                      their role, duties, file, who checks them, and their key result
  * <NN>_<Name>_results.html     a one-page view of their part's tables, figures and console output
  * code/<their part>.py         a copy of their Python part (the copy that runs is in src/)
  * outputs/tables, outputs/figures   the files their part produced
  * console_output.txt           what their part printed when it ran
Run after run_all.py:   python src/make_team_packages.py
"""
import html
import shutil
from datetime import date

from common import ROOT, TABLES, FIGURES
from team import TEAM, folder_name
from make_results_html import CSS, part_content, log_block, table
import pandas as pd

TEAM_DIR = ROOT / "team"
SRC = ROOT / "src"
LOGS = ROOT / "outputs" / "logs"


def role_md(m):
    lines = [
        f"# Part {m['part']}: {m['title']}",
        "",
        f"**Member:** {m['name']}  ",
        f"**Role:** {m['role']}  ",
        f"**Assignment question:** {m['question']}  ",
        f"**Python file:** `src/{m['file']}`  ",
        f"**Checked by:** {m['checks']}",
        "",
        "> All figures are hypothetical: they come from the synthetic HASTS206 teaching dataset.",
        "",
        "## Responsibilities",
        "",
        *[f"- {d}" for d in m["duties"]],
        "",
        "## How to run your part",
        "",
        "From the repository root (your part uses `src/common.py` and the raw data in `data/raw/`):",
        "",
        "```bash",
        f"python src/{m['file']}",
        "```",
        "",
        "Run `python src/run_all.py` once first if `outputs/tables/selected_districts.json` does not exist yet.",
        "",
        "## Your output files",
        "",
        "| Type | File (in this folder) |",
        "|---|---|",
        *[f"| Table | `outputs/tables/{t}` |" for t in m["tables"]],
        *[f"| Figure | `outputs/figures/{f}` |" for f in m["figures"]],
        "| Console output | `console_output.txt` |",
        f"| Results page | `{folder_name(m)}_results.html` |",
        "",
        "## Your key result",
        "",
        m["result"],
        "",
        "## On GitHub",
        "",
        f"Upload `src/{m['file']}` from your own account on a branch named `part{m['part']:02d}-{m['name'].split()[0].lower()}`, "
        f"open a pull request, and ask {m['checks']} to review it before merging.",
        "",
    ]
    return "\n".join(lines)


def member_page(m):
    duties = "".join(f"<li>{html.escape(d)}</li>" for d in m["duties"])
    files = pd.DataFrame([{"Type": "Table", "File": f"outputs/tables/{t}"} for t in m["tables"]] +
                         [{"Type": "Figure", "File": f"outputs/figures/{f}"} for f in m["figures"]])
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Part {m['part']} - {html.escape(m['name'])}</title><style>{CSS}
.solo{{max-width:1180px;margin:0 auto;padding:28px 32px 60px}}.card{{display:grid;grid-template-columns:1.2fr 1fr;gap:24px}}
.card ul{{margin:6px 0 0;padding-left:20px}}.big{{font-size:15px;line-height:1.6}}@media (max-width:900px){{.card{{grid-template-columns:1fr}}}}</style></head><body>
<header><div class="tag" style="color:#cfe6ff">Part {m['part']} &middot; {m['question']}</div>
<h1>{html.escape(m['name'])}</h1><p>{html.escape(m['role'])} &middot; {html.escape(m['title'])}</p>
<span class="hyp">All figures are hypothetical: synthetic teaching data</span></header>
<div class="solo">
<section><div class="sec-head"><div><div class="tag">Role card</div><h2>{html.escape(m['role'])}</h2>
<div style="margin-top:6px"><code>src/{m['file']}</code></div></div>
<div class="who">Checked by<br><b>{html.escape(m['checks'])}</b></div></div>
<div class="card"><div class="big"><b>Responsibilities</b><ul>{duties}</ul></div>
<div><p class="note"><b>Key result.</b> {html.escape(m['result'])}</p>{table(files, "Output files produced by this part")}</div></div></section>
<section><div class="sec-head"><div><div class="tag">Results</div><h2>{html.escape(m['title'])}</h2></div></div>
{part_content(m['part'])}{log_block(m['part'])}</section>
<footer>Generated on {date.today():%d %B %Y} by src/make_team_packages.py &middot; HASTS206 Assignment 2, University of Zimbabwe</footer>
</div></body></html>"""


def main():
    if TEAM_DIR.exists():
        shutil.rmtree(TEAM_DIR)
    rows = []
    for m in TEAM:
        d = TEAM_DIR / folder_name(m)
        (d / "code").mkdir(parents=True)
        (d / "outputs" / "tables").mkdir(parents=True)
        (d / "outputs" / "figures").mkdir(parents=True)
        shutil.copy(SRC / m["file"], d / "code" / m["file"])
        for t in m["tables"]:
            shutil.copy(TABLES / t, d / "outputs" / "tables" / t)
        for f in m["figures"]:
            shutil.copy(FIGURES / f, d / "outputs" / "figures" / f)
        shutil.copy(LOGS / m["file"].replace(".py", ".txt"), d / "console_output.txt")
        (d / "ROLE.md").write_text(role_md(m), encoding="utf-8")
        (d / f"{folder_name(m)}_results.html").write_text(member_page(m), encoding="utf-8")
        rows.append(f"| {m['part']} | {m['name']} | {m['role']} | [`team/{folder_name(m)}/`]({folder_name(m)}/ROLE.md) |")
    (TEAM_DIR / "README.md").write_text(
        "# Team folders\n\nOne folder per member: role card (`ROLE.md`), a copy of their Python part, the output files it "
        "produced, its console output and a one-page results view. The code that actually runs is in `src/`.\n\n"
        "| Part | Member | Role | Folder |\n|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"Team folders written: {len(TEAM)} members in team/")


if __name__ == "__main__":
    main()
