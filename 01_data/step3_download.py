r"""Step 3: download the four census grid files of the preregistration (Q5) and register them.
Usage (from the project folder): .venv\Scripts\python.exe 01_data/step3_download.py
"""
import csv, datetime, hashlib, pathlib, ssl, urllib.request

import certifi

CTX = ssl.create_default_context(cafile=certifi.where())
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data" / "raw"
REG = ROOT / "01_data" / "data_register.csv"
FIELDS = ["file", "dataset", "provider", "url", "download_date", "version", "licence", "attribution", "size_bytes", "sha256", "note"]
BASE = "https://www.destatis.de/static/DE/zensus/gitterdaten/"
PROV = "Statistische Ämter des Bundes und der Länder (Destatis)"
ATTR = "Statistische Ämter des Bundes und der Länder, Zensus 2022, dl-de/by-2-0"
FILES = [
    ("Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip", "Zensus 2022 average net cold rent and number of rented dwellings", "Version 2, 08.07.2025 (description file)"),
    ("Auslaenderanteil_in_Gitterzellen.zip", "Zensus 2022 share of foreign citizens", "Version 1, 07.10.2024 (description file)"),
    ("Anteil_ab_65-jaehrige_in_Gitterzellen.zip", "Zensus 2022 share aged 65 and over", "Version 1, 07.10.2024 (description file)"),
    ("Anteil_unter_18-jaehrige_in_Gitterzellen.zip", "Zensus 2022 share aged under 18", "Version 1, 07.10.2024 (description file)"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = list(csv.DictReader(open(REG, encoding="utf-8")))
known = {r["file"] for r in rows}
for name, label, ver in FILES:
    rel = f"zensus2022/{name}"
    dest = RAW / rel
    if not dest.is_file():
        req = urllib.request.Request(BASE + name, headers={"User-Agent": "research download (mailto:129296788+mariabdj@users.noreply.github.com)"})
        with urllib.request.urlopen(req, timeout=600, context=CTX) as r, open(dest, "wb") as f:
            f.write(r.read())
    if rel not in known:
        rows.append({"file": rel, "dataset": label, "provider": PROV, "url": BASE + name, "download_date": datetime.date.today().isoformat(),
                     "version": ver, "licence": "dl-de/by-2-0", "attribution": ATTR, "size_bytes": dest.stat().st_size,
                     "sha256": sha256(dest), "note": ""})
    print(rel, dest.stat().st_size)
with open(REG, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
