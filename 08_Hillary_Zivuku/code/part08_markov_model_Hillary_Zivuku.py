"""
Author: Hillary Zivuku    |    Role: Actuarial Modeller (Markov Model)    |    Checked by: Shaun Kanojerera
HASTS206 Assignment 2, University of Zimbabwe

PART 8 - Three-state continuous-time Markov model for the insured cohort (Q3a-Q3d).

States: H (healthy), I (ill), D (dead, absorbing). Recovery I -> H is allowed.
Pooling rule from the README: exposure_py and initial_lives are repeated across
the two destinations of each district-origin, so we keep ONE copy per
district-origin before summing. Transition counts are summed over all rows.

    mu_ij = (sum of observed i->j jumps) / (pooled exposure in origin state i)
"""
import numpy as np
import pandas as pd
from scipy.linalg import expm

from common import (load_raw, show_table, save_table, save_fig, plt, DARK, BLUE, SKY, ORANGE,
                    GREY, HYPO, BENEFIT_USD, ILL_DEATH_MULTIPLIER)
from matplotlib.patches import FancyArrowPatch, Circle

STATES = ["H", "I", "D"]
NAMES = {"H": "Healthy", "I": "Ill", "D": "Dead"}


def estimate_generator(ins: pd.DataFrame):
    exposure = (ins.drop_duplicates(["district_id", "origin"])      # one copy per district-origin
                .groupby("origin").exposure_py.sum())
    counts = ins.groupby(["origin", "destination"]).transition_count.sum()
    rows = []
    for (o, dst), n in counts.items():
        rows.append({"origin": o, "destination": dst, "pooled_jumps": int(n),
                     "pooled_exposure_py": float(exposure[o]), "intensity": n / exposure[o]})
    est = pd.DataFrame(rows)
    mu = {(r.origin, r.destination): r.intensity for r in est.itertuples()}
    Q = np.zeros((3, 3))
    Q[0, 1], Q[0, 2] = mu[("H", "I")], mu[("H", "D")]
    Q[1, 0], Q[1, 2] = mu[("I", "H")], mu[("I", "D")]
    for i in range(3):
        Q[i, i] = -Q[i].sum()
    return est, Q


def draw_state_diagram(Q, path_name):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    pos = {"H": (0.1, 0.72), "I": (0.9, 0.72), "D": (0.5, 0.1)}
    cols = {"H": BLUE, "I": ORANGE, "D": GREY}
    for st, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.095, color=cols[st], alpha=0.95, zorder=3))
        ax.text(x, y, f"{st}\n{NAMES[st]}", ha="center", va="center", color="white", fontsize=9,
                fontweight="bold", zorder=4)

    def arrow(a, b, label, rad, off):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), connectionstyle=f"arc3,rad={rad}",
                                     arrowstyle="-|>", mutation_scale=16, lw=1.6, color=DARK,
                                     shrinkA=24, shrinkB=24, zorder=2))
        ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], label, ha="center", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))

    arrow("H", "I", f"onset  mu_HI = {Q[0, 1]:.4f}", -0.2, (0, 0.12))
    arrow("I", "H", f"recovery  mu_IH = {Q[1, 0]:.4f}", -0.2, (0, -0.15))
    arrow("H", "D", f"death  mu_HD = {Q[0, 2]:.4f}", 0.0, (-0.2, -0.02))
    arrow("I", "D", f"death  mu_ID = {Q[1, 2]:.4f}", 0.0, (0.2, -0.02))
    ax.text(0.5, -0.04, "D is absorbing (no exits). Intensities per person-year, pooled over 24 districts.",
            ha="center", fontsize=7.5, color="black")
    ax.text(0.5, -0.11, HYPO, ha="center", fontsize=7, color="grey")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.14, 0.92)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Healthy-ill-dead model with recovery")
    save_fig(fig, path_name)


def main():
    print("Author: Hillary Zivuku (Actuarial Modeller (Markov Model))")
    print("PART 8: Three-state continuous-time Markov model (Q3)")
    ins = load_raw()["ins"]

    # ---- 3a generator -----------------------------------------------------
    est, Q = estimate_generator(ins)
    if ILL_DEATH_MULTIPLIER != 1.0:
        # What-if run: scale mu_ID and rebuild the diagonal so rows still sum to zero
        Q[1, 2] *= ILL_DEATH_MULTIPLIER
        Q[1, 1] = -(Q[1, 0] + Q[1, 2])
        print(f"WHAT-IF: I->D intensity multiplied by {ILL_DEATH_MULTIPLIER} -> mu_ID = {Q[1, 2]:.4f}")
    show_table(est, "Pooled jumps, exposure and transition intensities")
    save_table(est, "p08_transition_intensities.csv")
    Qdf = pd.DataFrame(Q, index=STATES, columns=STATES)
    show_table(Qdf, "Generator matrix Q (order H, I, D)", 6)
    save_table(Qdf.reset_index().rename(columns={"index": "from_state"}), "p08_generator_Q.csv")
    off = Q[~np.eye(3, dtype=bool)]
    print(f"Row sums of Q: {np.round(Q.sum(axis=1), 12)}  -> all zero: {np.allclose(Q.sum(axis=1), 0)}")
    print(f"Off-diagonal entries non-negative: {(off >= 0).all()}; diagonal non-positive: {(np.diag(Q) <= 0).all()}")
    draw_state_diagram(Q, "fig06_markov_state_diagram.png")

    # ---- 3b holding times and jump chain -------------------------------------
    hold = pd.DataFrame({"state": ["H", "I"], "total_exit_intensity": [-Q[0, 0], -Q[1, 1]],
                         "mean_holding_time_years": [1 / -Q[0, 0], 1 / -Q[1, 1]]})
    show_table(hold, "Mean holding times in the living states", 4)
    q_i = -Q[1, 1]
    jump = pd.DataFrame({"from": ["I", "I"], "next_state": ["H (recovery)", "D (death)"],
                         "probability": [Q[1, 0] / q_i, Q[1, 2] / q_i]})
    show_table(jump, "Next-jump destinations from the ill state", 4)
    save_table(pd.concat([hold, jump], axis=1), "p08_holding_and_jump.csv")

    # ---- 3c transition matrices --------------------------------------------
    P1, P2 = expm(Q * 1.0), expm(Q * 2.0)
    for name, P in [("P(1)", P1), ("P(2)", P2)]:
        show_table(pd.DataFrame(P, index=STATES, columns=STATES), f"Transition probability matrix {name}", 6)
    checks = pd.DataFrame([
        {"check": "P(1) entries non-negative", "result": bool((P1 >= -1e-12).all())},
        {"check": "P(2) entries non-negative", "result": bool((P2 >= -1e-12).all())},
        {"check": "P(1) rows sum to 1", "result": bool(np.allclose(P1.sum(1), 1, atol=1e-12))},
        {"check": "P(2) rows sum to 1", "result": bool(np.allclose(P2.sum(1), 1, atol=1e-12))},
        {"check": "Death absorbing: row D of P(1), P(2) = (0,0,1)",
         "result": bool(np.allclose(P1[2], [0, 0, 1]) and np.allclose(P2[2], [0, 0, 1]))},
        {"check": "P(2) = P(1) @ P(1) (Chapman-Kolmogorov)",
         "result": bool(np.allclose(P2, P1 @ P1, atol=1e-12)),
         "max_abs_diff": float(np.abs(P2 - P1 @ P1).max())},
    ])
    show_table(checks, "Probability checks")
    save_table(checks, "p08_probability_checks.csv")
    print(f"\nNext-jump recovery probability from I = {jump.probability.iloc[0]:.4f}, but "
          f"P_IH(1) = {P1[1, 0]:.4f}. The jump probability ignores timing (it is where the next move "
          f"goes, whenever it happens), while P_IH(1) is the chance of being healthy exactly at t = 1: "
          f"some ill lives have not moved yet, and some recover and fall ill again or die within the year.")

    tm = []
    for t, P in [(1, P1), (2, P2)]:
        for i, a in enumerate(STATES):
            for j, b in enumerate(STATES):
                tm.append({"t_years": t, "from_state": a, "to_state": b, "probability": P[i, j]})
    tm = pd.DataFrame(tm)
    order = {"H": 1, "I": 2, "D": 3}
    tm["from_order"], tm["to_order"] = tm.from_state.map(order), tm.to_state.map(order)
    save_table(tm, "pbi_markov_transition_matrices.csv")

    # Initial pooled counts (once per district-origin)
    init_by_d = (ins.drop_duplicates(["district_id", "origin"])
                 .pivot(index="district_id", columns="origin", values="initial_lives"))
    init_by_d["D"] = 0
    n0 = init_by_d[STATES].sum().to_numpy(float)
    occ = pd.DataFrame([n0, n0 @ P1, n0 @ P2], columns=STATES, index=["t=0", "t=1", "t=2"])
    occ["total"] = occ.sum(axis=1)
    show_table(occ, "Expected occupancy of the pooled insured cohort", 1)
    save_table(occ.reset_index().rename(columns={"index": "time"}), "p08_expected_occupancy.csv")

    # ---- 3d benefits ---------------------------------------------------------
    deaths_y1 = occ.loc["t=1", "D"] - occ.loc["t=0", "D"]
    deaths_y2 = occ.loc["t=2", "D"] - occ.loc["t=1", "D"]
    claims = pd.DataFrame({"year": ["Year 1 (0-1)", "Year 2 (1-2)", "Two years"],
                           "expected_deaths": [deaths_y1, deaths_y2, deaths_y1 + deaths_y2]})
    claims["expected_benefits_usd"] = claims.expected_deaths * BENEFIT_USD
    show_table(claims, "Expected covered deaths and benefit payments (USD 1,000 per death, undiscounted)", 2)
    save_table(claims, "p08_expected_claims.csv")

    # District split for the dashboard: pooled Q applied to each district's initial lives
    rows = []
    for dist_id, r in init_by_d.iterrows():
        v0 = r[STATES].to_numpy(float)
        v1, v2 = v0 @ P1, v0 @ P2
        for t, v in [(0, v0), (1, v1), (2, v2)]:
            for st, val in zip(STATES, v):
                rows.append({"district_id": dist_id, "t_years": t, "state": NAMES[st], "expected_lives": val})
        rows_claim = [(1, v1[2] - v0[2]), (2, v2[2] - v1[2])]
        for yr, dth in rows_claim:
            rows.append({"district_id": dist_id, "t_years": yr, "state": f"Claims year {yr}",
                         "expected_lives": dth})
    dshare = pd.DataFrame(rows)
    occ_long = dshare[~dshare.state.str.startswith("Claims")].copy()
    occ_long["state_order"] = occ_long.state.map({"Healthy": 1, "Ill": 2, "Dead": 3})
    save_table(occ_long, "pbi_markov_occupancy_by_district.csv")
    cl = dshare[dshare.state.str.startswith("Claims")].rename(columns={"expected_lives": "expected_deaths",
                                                                       "t_years": "policy_year"})
    cl["expected_benefits_usd"] = cl.expected_deaths * BENEFIT_USD
    save_table(cl.drop(columns="state"), "pbi_expected_claims_by_district.csv")
    print(f"District split reconciles to pooled claims: year 1 {cl[cl.policy_year == 1].expected_benefits_usd.sum():,.2f} "
          f"vs {claims.expected_benefits_usd.iloc[0]:,.2f}")

    # Occupancy chart over 0-5 years
    ts = np.linspace(0, 5, 51)
    path = np.array([n0 @ expm(Q * t) for t in ts])
    fig, ax = plt.subplots(figsize=(7, 3.3))
    for k, (st, c) in enumerate(zip(STATES, [BLUE, ORANGE, GREY])):
        ax.plot(ts, path[:, k], color=c, lw=2, label=NAMES[st])
    for t in (1, 2):
        ax.axvline(t, color="black", ls=":", lw=0.8)
    ax.set_xlabel("Years from the start of cover")
    ax.set_ylabel("Expected number of lives")
    ax.set_title("Expected occupancy of the pooled insured cohort, n(t) = n(0) P(t)")
    ax.legend(frameon=False)
    ax.text(0, -0.22, HYPO, transform=ax.transAxes, fontsize=7, color="grey")
    save_fig(fig, "fig07_markov_occupancy.png")
    return Q, P1, P2, occ, claims


if __name__ == "__main__":
    main()
