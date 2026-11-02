r"""Step 3: read the four census variables for the study-area cells (official Destatis CSVs, primary reader).
Rules (description files): ';' separator, decimal comma, '–' = exactly zero or changed to zero, flag 'KLAMMERN' =
value statistically uncertain (treated as missing in the primary analysis, Q14). In the rent file one flag column covers
rent and number of dwellings; it is applied to the rent. A cell absent from a file has no value for that variable.
Usage: .venv\Scripts\python.exe 01_data/step3_census.py
Writes 01_data/processed/census_step3.csv and 05_analysis/results/step3_missingness.csv.
"""
import io, pathlib, sys, zipfile

import geopandas as gpd
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
Z = ROOT / "01_data" / "raw" / "zensus2022"
sys.stdout.reconfigure(encoding="utf-8")

SOURCES = {  # variable: (zip, csv inside the zip, value column)
    "rent": ("Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip",
             "Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen/Zensus2022_Durchschn_Nettokaltmiete_Anzahl_der_Wohnungen_100m-Gitter.csv",
             "durchschnmieteqm"),
    "foreign": ("Auslaenderanteil_in_Gitterzellen.zip", "Zensus2022_Anteil_Auslaender_100m-Gitter.csv", "anteilauslaender"),
    "age65": ("Anteil_ab_65-jaehrige_in_Gitterzellen.zip", "Zensus2022_Anteil_ueber_65_100m-Gitter.csv", "anteilueber65"),
    "under18": ("Anteil_unter_18-jaehrige_in_Gitterzellen.zip", "Zensus2022_Anteil_unter_18_100m-Gitter.csv", "anteilunter18"),
}

cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells", ignore_geometry=True)
out = cells[["gitter_id_100m", "city", "einwohner_n", "rule3"]].copy()


def parse(raw):
    raw = raw.str.strip()
    dash = raw.isin(["–", "-"])
    val = pd.to_numeric(raw.str.replace(".", "", regex=False).str.replace(",", ".", regex=False).where(~dash, "0"), errors="coerce")
    return val, dash


for var, (zname, csvname, col) in SOURCES.items():
    df = pd.read_csv(io.BytesIO(zipfile.ZipFile(Z / zname).read(csvname)), sep=";", dtype=str, keep_default_na=False)
    df.columns = [c.lower() for c in df.columns]
    assert col in df.columns, (var, list(df.columns))
    df = df[df["gitter_id_100m"].isin(out["gitter_id_100m"])]
    val, dash = parse(df[col])
    bad = val.isna() & ~dash
    assert not bad.any(), (var, df.loc[bad, col].unique()[:10])
    part = pd.DataFrame({"gitter_id_100m": df["gitter_id_100m"], var: val, f"{var}_dash": dash,
                         f"{var}_br": df["werterlaeuternde_zeichen"].str.upper().eq("KLAMMERN")})
    if var == "rent":
        part["n_dwellings"], part["n_dwellings_dash"] = parse(df["anzahlwohnungen"])
    flags = set(df["werterlaeuternde_zeichen"].unique()) - {"", "KLAMMERN"}
    assert not flags, (var, flags)
    out = out.merge(part, on="gitter_id_100m", how="left")
    out[f"{var}_in_file"] = out[var].notna()
    print(f"{var}: rows in study area {len(part)}; value range {part[var].min()} to {part[var].max()}; "
          f"brackets {int(part[f'{var}_br'].sum())}; dashes {int(part[f'{var}_dash'].sum())}")

out.to_csv(ROOT / "01_data/processed/census_step3.csv", index=False)

# missingness among the cells passing rules 1 to 3
a = out[out.rule3]
rows = []
for var in SOURCES:
    for city, g in list(a.groupby("city")) + [("TOTAL", a)]:
        absent = int((~g[f"{var}_in_file"]).sum())
        br = int(g[f"{var}_br"].fillna(False).astype(bool).sum())
        dash = int(g[f"{var}_dash"].fillna(False).astype(bool).sum())
        usable = int((g[f"{var}_in_file"] & ~g[f"{var}_br"].fillna(False).astype(bool)).sum())
        rows.append({"variable": var, "city": city, "cells": len(g), "absent": absent, "bracketed": br,
                     "dash_zero": dash, "usable_primary": usable, "usable_share": round(usable / len(g), 4)})
miss = pd.DataFrame(rows)
(ROOT / "05_analysis/results").mkdir(parents=True, exist_ok=True)
miss.to_csv(ROOT / "05_analysis/results/step3_missingness.csv", index=False)
print(miss[miss.city == "TOTAL"].to_string(index=False))
comp = a[[f"{v}_in_file" for v in SOURCES]].all(axis=1) & ~a[[f"{v}_br" for v in SOURCES]].fillna(False).astype(bool).any(axis=1)
print("cells with all four variables usable (Model A sample before LST rules):", int(comp.sum()))
