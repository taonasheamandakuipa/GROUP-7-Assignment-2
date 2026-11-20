"""
Author: Ketso Thabiso Mdlongwa    |    Role: Mortality and Life-Table Analyst    |    Checked by: Emeldah Munyanyi
HASTS206 Assignment 2, University of Zimbabwe

PART 5 - Abridged life table from the separate mortality schedule (Q1c).

    m_x  = deaths / person_years
    q_x  = n m_x / (1 + (n - a_x) m_x)          (q_85+ = 1)
    l_0  = 100,000 ; d_x = l_x q_x ; l_{x+n} = l_x - d_x
    L_x  = n l_{x+n} + a_x d_x                    (L_85+ = l_85 / m_85+)
    T_x  = sum of L from x upwards ; e_x = T_x / l_x
"""
import numpy as np
import pandas as pd

from common import load_raw, show_table, save_table, save_fig, plt, DARK, BLUE, HYPO, RADIX, age_label


def build_life_table(life: pd.DataFrame, radix: int = RADIX) -> pd.DataFrame:
    lt = life.copy().sort_values("age_start").reset_index(drop=True)
    lt["age_group"] = lt.age_start.map(age_label)
    lt["n"] = lt.interval_years
    lt["mx"] = lt.deaths / lt.person_years
    lt["qx"] = lt.n * lt.mx / (1 + (lt.n - lt.ax) * lt.mx)
    last = lt.index[-1]
    lt.loc[last, "qx"] = 1.0                        # open interval: everyone dies eventually
    lx = [float(radix)]
    for q in lt.qx.iloc[:-1]:
        lx.append(lx[-1] * (1 - q))
    lt["lx"] = lx
    lt["dx"] = lt.lx * lt.qx
    lt["l_next"] = lt.lx.shift(-1).fillna(0.0)
    lt["Lx"] = lt.n * lt.l_next + lt.ax * lt.dx
    lt.loc[last, "Lx"] = lt.loc[last, "lx"] / lt.loc[last, "mx"]
    lt["Tx"] = lt.Lx[::-1].cumsum()[::-1]
    lt["ex"] = lt.Tx / lt.lx
    return lt


def main():
    print("Author: Ketso Thabiso Mdlongwa (Mortality and Life-Table Analyst)")
    print("PART 5: Abridged life table (Q1c)")
    life = load_raw()["life"]
    lt = build_life_table(life)
    out = lt[["age_group", "n", "ax", "mx", "qx", "lx", "dx", "Lx", "Tx", "ex"]]
    show_table(out.round({"mx": 5, "qx": 5, "lx": 0, "dx": 0, "Lx": 0, "Tx": 0, "ex": 2}),
               "Abridged life table (radix 100,000)")
    save_table(out, "p05_life_table.csv")

    e0 = lt.loc[0, "ex"]
    e65 = lt.loc[lt.age_start == 65, "ex"].iloc[0]
    print(f"\nLife expectancy at birth e0 = {e0:.2f} years; at age 65 e65 = {e65:.2f} years")

    # ---- Numerical checks ----------------------------------------------------
    checks = pd.DataFrame([
        {"check": "Sum of d_x equals the radix", "value": lt.dx.sum(), "target": RADIX},
        {"check": "T_0 equals the sum of all L_x", "value": lt.Tx.iloc[0], "target": lt.Lx.sum()},
        {"check": "e_85+ equals 1 / m_85+", "value": lt.ex.iloc[-1], "target": 1 / lt.mx.iloc[-1]},
        {"check": "l_5 = l_0 x (1 - q_0)", "value": lt.lx.iloc[1], "target": RADIX * (1 - lt.qx.iloc[0])},
        {"check": "Manual q_0 = 5(0.008)/(1+(5-1.2)(0.008))", "value": lt.qx.iloc[0],
         "target": 5 * 0.008 / (1 + 3.8 * 0.008)},
    ])
    checks["abs_difference"] = (checks.value - checks.target).abs()
    checks["passed"] = checks.abs_difference < 1e-6
    show_table(checks, "Life-table checks")
    save_table(checks, "p05_life_table_checks.csv")

    fig, ax1 = plt.subplots(figsize=(7, 3.4))
    ax1.plot(lt.age_start, lt.lx, marker="o", color=DARK, label="l(x) survivors")
    ax1.set_xlabel("Exact age x (years)")
    ax1.set_ylabel("Survivors l(x) out of 100,000 births")
    ax2 = ax1.twinx()
    ax2.plot(lt.age_start, lt.ex, marker="s", color=BLUE, ls="--", label="e(x) years")
    ax2.set_ylabel("Life expectancy e(x), years")
    ax1.set_title(f"Survivorship and life expectancy (e0 = {e0:.1f}, e65 = {e65:.1f})")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, frameon=False, loc="lower left")
    ax1.text(0, -0.22, HYPO, transform=ax1.transAxes, fontsize=7, color="grey")
    save_fig(fig, "fig03_life_table.png")
    return lt


if __name__ == "__main__":
    main()
