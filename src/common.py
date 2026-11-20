"""
common.py - shared paths, settings and small helpers used by all ten parts.

HASTS206 Assignment 2 (Applied Demographic Analysis), Group work.
All figures in this project come from the SYNTHETIC teaching dataset supplied
by the lecturer, so every number we report is hypothetical.
"""
from pathlib import Path
import json

import matplotlib
import pandas as pd

# ----------------------------------------------------------------------------
# Relative paths: everything is resolved from the repository root so the
# lecturer can rerun the code from any folder.
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

SETTINGS_FILE = TABLES / "selected_districts.json"

# Group settings we agreed on (changed in one place only)
SEED_PRIMARY = 2026          # main random seed for k-means
SEED_CHECK = 7               # second seed used for the stability check
N_INIT = 50                  # k-means initialisations per fit (brief asks >= 20)
RADIX = 100_000              # life-table radix
BENEFIT_USD = 1_000          # insurer benefit per covered death
ILL_DEATH_MULTIPLIER = 1.0   # what-if setting for the presentation: scales the I->D intensity (1.0 = estimated)
FEMALE_BIRTH_SHARE = 0.49    # given in the brief
MALE_BIRTH_SHARE = 0.51
HYPO = "Hypothetical synthetic data (HASTS206 teaching case)"

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", lambda v: f"{v:,.2f}" if abs(v) >= 100 else f"{v:,.4f}")


def in_notebook() -> bool:
    """True when the code runs inside Jupyter (so we can display nicely)."""
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"
    except Exception:
        return False


if not in_notebook():
    matplotlib.use("Agg")  # scripts run headless and just save the PNGs

import matplotlib.pyplot as plt  # noqa: E402  (import after choosing backend)

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "font.size": 9,
})

# Colour palette used in every chart and in the Power BI theme
BLUE = "#1E88E5"
DARK = "#0D47A1"
SKY = "#4FC3F7"
GREY = "#7A7A7A"
ORANGE = "#F57C00"
PALETTE = [DARK, BLUE, SKY, ORANGE, GREY, "#26A69A"]


def show_table(df: pd.DataFrame, title: str = "", decimals: int | None = None):
    """Print a table in a script, or render it in the notebook."""
    out = df.round(decimals) if decimals is not None else df
    if title:
        print(f"\n=== {title} ===")
    if in_notebook():
        from IPython.display import display
        display(out)
    else:
        print(out.to_string())


def save_table(df: pd.DataFrame, name: str, index: bool = False) -> Path:
    path = TABLES / name
    df.to_csv(path, index=index)
    return path


def save_fig(fig, name: str) -> Path:
    path = FIGURES / name
    fig.savefig(path, bbox_inches="tight")
    if in_notebook():
        plt.show()
    plt.close(fig)
    print(f"[figure saved] outputs/figures/{name}")
    return path


def load_raw() -> dict:
    """Read the original CSVs. We never overwrite these files."""
    return {
        "districts": pd.read_csv(RAW / "districts.csv"),
        "age_sex": pd.read_csv(RAW / "age_sex.csv"),
        "life": pd.read_csv(RAW / "life_table_inputs.csv"),
        "scen": pd.read_csv(RAW / "projection_scenarios.csv"),
        "ins": pd.read_csv(RAW / "insured_transitions.csv"),
    }


def save_settings(settings: dict):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2))


def load_settings() -> dict:
    return json.loads(SETTINGS_FILE.read_text())


def age_label(a: int) -> str:
    return "85+" if a == 85 else f"{a}-{a + 4}"
