"""
run_all.py - runs the ten parts in order and keeps a copy of the console output
in outputs/run_log.txt.

Usage (from the repository root):
    python src/run_all.py
"""
import io
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import part01_load_and_inspect_Lennox_Tawanda_Jaricha as p01
import part02_data_quality_Emeldah_Munyanyi as p02
import part03_selection_pyramids_ratios_Mlungisi_Ncube_K as p03
import part04_balance_and_rates_Gogodi_Vimbai as p04
import part05_life_table_Ketso_Thabiso_Mdlongwa as p05
import part06_growth_and_cohort_component_Stuart_Gavera as p06
import part07_projection_comparison_Taonashe_Amanda_Kuipa as p07
import part08_markov_model_Hillary_Zivuku as p08
import part09_clustering_features_Shaun_Kanojerera as p09
import part10_kmeans_and_exports_Trish_Tembo as p10
from common import ROOT


class Tee(io.TextIOBase):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)
        return len(s)

    def flush(self):
        for st in self.streams:
            st.flush()


def main():
    log_path = ROOT / "outputs" / "run_log.txt"
    part_logs = ROOT / "outputs" / "logs"
    part_logs.mkdir(parents=True, exist_ok=True)
    parts = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10]
    with open(log_path, "w", encoding="utf-8") as fh, redirect_stdout(Tee(sys.__stdout__, fh)):
        start = time.time()
        for part in parts:
            # each member's output is also saved on its own, e.g. outputs/logs/part08_markov_model_Hillary_Zivuku.txt
            name = Path(part.__file__).stem
            with open(part_logs / f"{name}.txt", "w", encoding="utf-8") as pf, redirect_stdout(Tee(sys.stdout, pf)):
                print("=" * 90)
                part.main()
        print("\n" + "=" * 90)
        print(f"Finished all ten parts in {time.time() - start:.1f} s. Outputs in outputs/tables, outputs/figures and outputs/logs.")


if __name__ == "__main__":
    main()
