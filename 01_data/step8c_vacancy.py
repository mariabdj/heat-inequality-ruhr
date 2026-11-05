r"""Exploratory (preregistration Q25): vacancy rate (Leerstandsquote) of the Zensus 2022 100 m grid.
Downloads the official Destatis file, registers it (01_data/data_register.csv), and reads it with the Step 3 rules
(';' separator, decimal comma, dash = exactly zero or changed to zero, KLAMMERN = uncertain).
Usage: .venv\Scripts\python.exe 01_data/step8c_vacancy.py  ->  01_data/processed/census_vacancy.csv
"""
import csv, datetime, hashlib, io, pathlib, ssl, sys, urllib.request, zipfile

import certifi
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw"
REG = ROOT / "01_data/data_register.csv"
NAME = "Leerstandsquote_in_Gitterzellen.zip"
URL = "https://www.destatis.de/static/DE/zensus/gitterdaten/" + NAME
sys.stdout.reconfigure(encoding="utf-8")
dest = RAW / "zensus2022" / NAME
if not dest.is_file():
    req = urllib.request.Request(URL, headers={"User-Agent": "research download"})
    with urllib.request.urlopen(req, timeout=600, context=ssl.create_default_context(cafile=certifi.where())) as r, open(dest, "wb") as f:
        f.write(r.read())
h = hashlib.sha256(dest.read_bytes()).hexdigest()
rows = list(csv.DictReader(open(REG, encoding="utf-8")))
rel = f"zensus2022/{NAME}"
if rel not in {r["file"] for r in rows}:
    ref = next(r for r in rows if r["file"].startswith("zensus2022/Auslaender"))
    rows.append({**ref, "file": rel, "dataset": "Zensus 2022 vacancy rate (Leerstandsquote), 100 m grid", "url": URL,
                 "download_date": datetime.date.today().isoformat(), "version": "see description file in the zip",
                 "size_bytes": dest.stat().st_size, "sha256": h, "note": "exploratory, Q25"})
    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
z = zipfile.ZipFile(dest)
print("files in zip:", z.namelist())
name = next(n for n in z.namelist() if n.lower().endswith(".csv") and "100m" in n.lower())
df = pd.read_csv(io.BytesIO(z.read(name)), sep=";", dtype=str, keep_default_na=False)
df.columns = [c.lower() for c in df.columns]
print("columns:", list(df.columns))
col = next(c for c in df.columns if "leerstand" in c)
cells = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet", columns=["gitter_id_100m"])
df = df[df.gitter_id_100m.isin(cells.gitter_id_100m)]
raw = df[col].str.strip(); dash = raw.isin(["–", "-"])
val = pd.to_numeric(raw.str.replace(".", "", regex=False).str.replace(",", ".", regex=False).where(~dash, "0"), errors="coerce")
assert not (val.isna() & ~dash).any(), raw[val.isna() & ~dash].unique()[:10]
flags = set(df["werterlaeuternde_zeichen"].unique()) - {"", "KLAMMERN"}
assert not flags, flags
out = pd.DataFrame({"gitter_id_100m": df.gitter_id_100m, "vacancy": val, "vacancy_dash": dash,
                    "vacancy_br": df["werterlaeuternde_zeichen"].str.upper().eq("KLAMMERN")})
out.to_csv(ROOT / "01_data/processed/census_vacancy.csv", index=False)
print(f"column {col}; rows in study area {len(out)}; range {out.vacancy.min()} to {out.vacancy.max()}; "
      f"brackets {int(out.vacancy_br.sum())}; dashes {int(out.vacancy_dash.sum())}; sha256 {h}")
