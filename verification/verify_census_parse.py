r"""GATE 3: the Python reader (official Destatis CSVs) and the R z22 reader give the same census values.
For every variable and every study-area cell: same presence, and |difference| <= 0.005 (values have 2 decimals).
Known, explained differences:
- where the official file has a dash ('–', zero or changed to zero), z22 has no value;
- z22 takes rent from the rent-only file (Version 2, 30.09.2024), while we use the rent + dwellings file (Version 2,
  08.07.2025, preregistration Q5). So z22 rent is compared with OUR parse of the rent-only file (same source), and the
  difference between the two official versions is reported separately.
Any other difference fails the check. Also checks that the missingness table matches the cell file.
Usage: .venv\Scripts\python.exe verification/verify_census_parse.py
"""
import io, pathlib, sys, zipfile

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
py = pd.read_csv(ROOT / "01_data/processed/census_step3.csv")
rz = pd.read_csv(ROOT / "01_data/processed/census_z22.csv")
zf = zipfile.ZipFile(ROOT / "01_data/raw/zensus2022/Zensus2022_Durchschn_Nettokaltmiete.zip")
old = pd.read_csv(io.BytesIO(zf.read("Zensus2022_Durchschn_Nettokaltmiete_100m-Gitter.csv")), sep=";", dtype=str, keep_default_na=False)
old.columns = [c.lower() for c in old.columns]
old["rent_v2024"] = pd.to_numeric(old["durchschnmieteqm"].str.replace(",", ".", regex=False), errors="coerce")
py = py.merge(old[["gitter_id_100m", "rent_v2024"]], on="gitter_id_100m", how="left")
m = py.merge(rz, on="gitter_id_100m", how="outer", indicator=True)
errors = []
if (m["_merge"] != "both").any():
    errors.append(f"cell lists differ: {m['_merge'].value_counts().to_dict()}")

vd = (m["rent"] - m["rent_v2024"]).abs()
print(f"official rent versions (2025 file we use vs 2024 file): cells differing {int((vd > 0.005).sum())}, max |diff| {vd.max():.4f} EUR")
if vd.max() > 0.0100001:
    errors.append("the two official rent versions differ by more than 1 cent")
for v in ["rent", "foreign", "age65", "under18"]:
    a, b, dash = m["rent_v2024" if v == "rent" else v], m[f"{v}_z22"], m[f"{v}_dash"].fillna(False).astype(bool)
    both = a.notna() & b.notna()
    diff = (a[both] - b[both]).abs()
    only_py = a.notna() & b.isna()
    only_z = a.isna() & b.notna()
    explained = only_py & dash
    unexplained = int((only_py & ~dash).sum()) + int(only_z.sum())
    print(f"{v}: both {int(both.sum())}, max |diff| {diff.max():.4f}, values > 0.005 apart {int((diff > 0.005).sum())}; "
          f"official dash with no z22 value {int(explained.sum())}; other presence differences {unexplained}")
    if (diff > 0.005).any() or unexplained:
        errors.append(f"{v}: values or presence differ")

miss = pd.read_csv(ROOT / "05_analysis/results/step3_missingness.csv")
a = py[py.rule3]
for v in ["rent", "foreign", "age65", "under18"]:
    usable = int((a[f"{v}_in_file"] & ~a[f"{v}_br"].fillna(False).astype(bool)).sum())
    if usable != int(miss.query("variable == @v and city == 'TOTAL'")["usable_primary"].iloc[0]):
        errors.append(f"missingness table wrong for {v}")

for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
