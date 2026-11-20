"""
make_powerbi_workbook.py - collects the pbi_*.csv outputs into one Excel workbook
(each sheet is an Excel table) so the Power BI service can import them in one upload.
Run after run_all.py:  python src/make_powerbi_workbook.py
"""
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

from common import ROOT, TABLES

OUT = ROOT / "powerbi" / "HASTS206_PowerBI_Data.xlsx"
SHEETS = {
    "DistrictProfiles": "pbi_district_profiles.csv",
    "AgeSex2025": "pbi_age_sex_2025.csv",
    "ProjectionAgeSex": "pbi_projection_by_age_sex.csv",
    "ProjectionMethods": "p07_projection_comparison.csv",
    "MarkovOccupancy": "pbi_markov_occupancy_by_district.csv",
    "ExpectedClaims": "pbi_expected_claims_by_district.csv",
    "TransitionMatrices": "pbi_markov_transition_matrices.csv",
    "ClusterCentroids": "pbi_cluster_centroids.csv",
    "KMeansDiagnostics": "pbi_kmeans_diagnostics.csv",
    "Reconciliation": "pbi_reconciliation_targets.csv",
}


def main():
    OUT.parent.mkdir(exist_ok=True)
    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        for sheet, f in SHEETS.items():
            df = pd.read_csv(TABLES / f)
            if sheet == "ProjectionMethods":
                df["method_order"] = range(1, len(df) + 1)
            df.to_excel(xw, sheet_name=sheet, index=False)
    wb = load_workbook(OUT)
    for sheet in SHEETS:
        ws = wb[sheet]
        ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
        t = Table(displayName=sheet, ref=ref)
        t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(t)
        for i in range(1, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(i)].width = 18
    wb.save(OUT)
    # Copy the CSVs the dashboard uses next to the .pbix as well
    for sheet, f in SHEETS.items():
        df = pd.read_csv(TABLES / f)
        if sheet == "ProjectionMethods":
            df["method_order"] = range(1, len(df) + 1)
        df.to_csv(ROOT / "powerbi" / f, index=False)
    print(f"Workbook written: powerbi/{OUT.name} ({len(SHEETS)} tables)")


if __name__ == "__main__":
    main()
