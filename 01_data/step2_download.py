r"""Step 2: download the boundaries, the census population file and the BKG grid, and register each file.
Usage (from the project folder): .venv\Scripts\python.exe 01_data/step2_download.py
Each file goes to 01_data/raw/<source>/ and gets one row in 01_data/data_register.csv (URL, date, licence, size, SHA-256).
"""
import csv, datetime, hashlib, pathlib, ssl, urllib.request

import certifi

CTX = ssl.create_default_context(cafile=certifi.where())

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data" / "raw"
REG = ROOT / "01_data" / "data_register.csv"
FIELDS = ["file", "dataset", "provider", "url", "download_date", "version", "licence", "attribution", "size_bytes", "sha256", "note"]

FILES = [
    ("vg250/vg250_01-01.utm32s.gpkg.ebenen.zip", "VG250 municipal boundaries", "BKG",
     "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/aktuell/vg250_01-01.utm32s.gpkg.ebenen.zip",
     "Stand 01.01. (aktuell at download)", "dl-de/by-2-0", "© BKG (2026) dl-de/by-2-0", ""),
    ("zensus2022/Zensus2022_Bevoelkerungszahl.zip", "Zensus 2022 population in grid cells", "Statistische Ämter des Bundes und der Länder (Destatis)",
     "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip",
     "Version 2, 30.09.2024 (description file)", "dl-de/by-2-0", "Statistische Ämter des Bundes und der Länder, Zensus 2022, dl-de/by-2-0", ""),
    ("bkg_grid/DE_Grid_ETRS89-LAEA_100m.csv.zip", "GeoGitter INSPIRE 100 m (check only)", "BKG",
     "https://daten.gdz.bkg.bund.de/produkte/sonstige/geogitter/aktuell/DE_Grid_ETRS89-LAEA_100m.csv.zip",
     "aktuell at download", "dl-de/by-2-0", "© GeoBasis-DE / BKG (2026) dl-de/by-2-0", "used only for the Gate 2 geometry check"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = list(csv.DictReader(open(REG, encoding="utf-8"))) if REG.is_file() else []
known = {r["file"] for r in rows}
for rel, name, prov, url, ver, lic, attr, note in FILES:
    dest = RAW / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.is_file():
        req = urllib.request.Request(url, headers={"User-Agent": "research download (mailto:129296788+mariabdj@users.noreply.github.com)"})
        with urllib.request.urlopen(req, timeout=600, context=CTX) as r, open(dest, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
    if rel not in known:
        rows.append({"file": rel, "dataset": name, "provider": prov, "url": url, "download_date": datetime.date.today().isoformat(),
                     "version": ver, "licence": lic, "attribution": attr, "size_bytes": dest.stat().st_size,
                     "sha256": sha256(dest), "note": note})
    print(rel, dest.stat().st_size)

with open(REG, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
print("registered:", len(rows))
