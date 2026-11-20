"""
Author: Lennox Tawanda Jaricha    |    Role: Project Lead and Data Engineer    |    Checked by: Trish Tembo
HASTS206 Assignment 2, University of Zimbabwe

PART 1 - Load the supplied CSVs and take a first look.

We keep the original files untouched in data/raw/ and only work on copies in
memory. Cleaning decisions are recorded in Part 2 (data-quality log).
"""
import pandas as pd

from common import load_raw, show_table, save_table, HYPO


def main():
    print("Author: Lennox Tawanda Jaricha (Project Lead and Data Engineer)")
    print(f"PART 1: Loading data ({HYPO})")
    data = load_raw()

    # Shape and dtypes of every file
    rows = []
    for name, df in data.items():
        rows.append({
            "file": name,
            "rows": len(df),
            "columns": df.shape[1],
            "missing_cells": int(df.isna().sum().sum()),
            "column_names": ", ".join(df.columns),
        })
    overview = pd.DataFrame(rows)
    show_table(overview, "File overview")
    save_table(overview, "p01_file_overview.csv")

    # Peek at each file
    for name, df in data.items():
        show_table(df.head(4), f"First rows of {name}")

    # Expected sizes from the dataset README
    expected = {"districts": 24, "age_sex": 864, "life": 18, "scen": 3, "ins": 96}
    for name, n in expected.items():
        status = "OK" if len(data[name]) == n else "MISMATCH"
        print(f"  {name:<10} rows = {len(data[name]):>4}  expected {n:>4}  -> {status}")
    return data


if __name__ == "__main__":
    main()
