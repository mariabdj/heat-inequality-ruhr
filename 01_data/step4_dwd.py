r"""Step 4: hot days at DWD station Essen-Bredeney (01303), preregistration Q12.2.
The rule was fixed in data_register.csv before this download: TXK >= 25.0 C, QN_4 in {2, 3, 5, 7, 8, 9, 10},
TXK missing (-999 or empty) = not a hot day.
Usage: .venv\Scripts\python.exe 01_data/step4_dwd.py   ->  01_data/processed/hot_days.csv (all June-August days 2018-2025)
"""
import csv, datetime, hashlib, io, pathlib, re, ssl, urllib.request, zipfile

import certifi
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw/dwd"
REG = ROOT / "01_data/data_register.csv"
BASE = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/"
CTX = ssl.create_default_context(cafile=certifi.where())
ACCEPT = {2, 3, 5, 7, 8, 9, 10}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research download"}), timeout=300, context=CTX).read()


rows = list(csv.DictReader(open(REG, encoding="utf-8")))
known = {r["file"] for r in rows}
frames = []
for sub in ("historical", "recent"):
    # files downloaded beforehand with curl (Python timed out on this server); the script reads them locally
    dest = sorted(RAW.glob("tageswerte_KL_01303_*_hist.zip" if sub == "historical" else "tageswerte_KL_01303_akt.zip"))[0]
    name = dest.name
    rel = f"dwd/{name}"
    if rel not in known:
        rows.append({"file": rel, "dataset": f"DWD daily climate KL, station 01303 Essen-Bredeney ({sub})", "provider": "Deutscher Wetterdienst",
                     "url": BASE + sub + "/" + name, "download_date": datetime.date.today().isoformat(), "version": sub,
                     "licence": "CC BY 4.0 (DWD CDC terms of use, May 2024)", "attribution": "Deutscher Wetterdienst (DWD), Climate Data Center",
                     "size_bytes": dest.stat().st_size, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(), "note": ""})
    zf = zipfile.ZipFile(dest)
    prod = [n for n in zf.namelist() if n.startswith("produkt_klima_tag")][0]
    df = pd.read_csv(io.BytesIO(zf.read(prod)), sep=";", skipinitialspace=True, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    df["source"] = sub
    frames.append(df[["MESS_DATUM", "QN_4", "TXK", "source"]])
w = csv.DictWriter(open(REG, "w", newline="", encoding="utf-8"), fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)

d = pd.concat(frames)
d["date"] = pd.to_datetime(d["MESS_DATUM"].str.strip(), format="%Y%m%d")
d = d.sort_values(["date", "source"]).drop_duplicates("date", keep="first")   # historical preferred where both exist
d = d[(d.date.dt.year.between(2018, 2025)) & (d.date.dt.month.isin([6, 7, 8]))].copy()
d["qn4"] = pd.to_numeric(d["QN_4"], errors="coerce")
d["txk"] = pd.to_numeric(d["TXK"], errors="coerce")
d.loc[d.txk <= -999, "txk"] = float("nan")
d["hot"] = (d.txk >= 25.0) & d.qn4.isin(ACCEPT)
expected = sum(92 for _ in range(2018, 2026))
print(f"June-August days 2018-2025: {len(d)} (expected {expected}); missing TXK: {int(d.txk.isna().sum())}; "
      f"QN_4 codes: {sorted(d.qn4.dropna().astype(int).unique())}; hot days: {int(d.hot.sum())}")
print(d.groupby(d.date.dt.year).hot.sum().to_string())
d[["date", "qn4", "txk", "hot", "source"]].to_csv(ROOT / "01_data/processed/hot_days.csv", index=False)
