r"""GATE 8: independent check of the Step 8c variant composites (02_lst/step8c_variants.py).
For every variant, 20 random pixels with at least 5 observations are recomputed directly from the per-scene files
with code written here (scene selection from scenes_stage1.csv, exact medians, the variant's rule), and compared with
the variant raster. Tolerance fixed before the run: 0.01 (C, or units of IQR for S15); observation counts identical.
Usage: .venv\Scripts\python.exe verification/verify_variants.py
"""
import pathlib, sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize

ROOT = pathlib.Path(__file__).resolve().parent.parent
SC, VAR = ROOT / "02_lst/exports/scenes", ROOT / "02_lst/exports/variants"
st = pd.read_csv(ROOT / "02_lst/scenes_stage1.csv"); st = st[st.n_valid_core / st.n_core >= 0.80]
hot = set(pd.read_csv(ROOT / "01_data/processed/hot_days.csv").query("hot").date.str[:10])
st["hot"] = st.date.isin(hot)
with rasterio.open(ROOT / "02_lst/exports/domain_ref_core.tif") as s:
    core = s.read(2) == 1; T = s.transform; shape = (s.height, s.width)
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(32632)
cid = rasterize([(g, i + 1) for i, g in enumerate(cities.geometry)], out_shape=shape, transform=T, fill=0, all_touched=False)
L = {sid: rasterio.open(SC / f"{sid}_lst.tif").read(1) for sid in st.id}
Q = {sid: rasterio.open(SC / f"{sid}_stqa.tif").read(1) for sid in st[st.hot].id}
H = st[st.hot]
SETS = {"S4_all_summer": st, "S6_landsat8": H[H.spacecraft == "LANDSAT_8"], "S6b_path196": H[H.path == 196],
        "S6b_path197": H[H.path == 197], "S12_valid95": H[H.n_valid_core / H.n_core >= 0.95]}
rng = np.random.default_rng(7)
errors = []


def value(name, sid, r, c):
    a = L[sid]; v = a != -999
    if not v[r, c]:
        return None
    if name == "S5_absolute":
        return a[r, c]
    if name == "S15_standardised":
        q1, q2, q3 = np.percentile(a[v & core], [25, 50, 75]); return (a[r, c] - q2) / (q3 - q1)
    if name == "S13_city_median":
        k = cid[r, c]; return a[r, c] - np.median(a[v & core & (cid == k)])
    if name == "S16_stqa3K":
        q = Q[sid]; ok = v & (q != -9999) & (q * 0.01 <= 3.0)
        return None if not ok[r, c] else a[r, c] - np.median(a[ok & core])
    return a[r, c] - np.median(a[v & core])


for f in sorted(VAR.glob("S*.tif")):
    name = f.stem
    with rasterio.open(f) as s:
        m, n = s.read(1), s.read(2)
    ids = (SETS.get(name, H)).id
    cand = np.argwhere((n >= 5) & (cid > 0)) if name == "S13_city_median" else np.argwhere(n >= 5)
    worst, bad_n = 0.0, 0
    for r, c in cand[rng.choice(len(cand), 20, replace=False)]:
        if name == "S14_yearly_mean":
            per = {}
            for sid in ids:
                x = value(name, sid, r, c)
                if x is not None:
                    per.setdefault(sid.split("_")[-1][:4], []).append(x)
            vals = [np.mean(v) for v in per.values()]; cnt = sum(len(v) for v in per.values())
        else:
            xs = [x for x in (value(name, sid, r, c) for sid in ids) if x is not None]; vals, cnt = xs, len(xs)
        worst = max(worst, abs(np.mean(vals) - m[r, c])); bad_n += int(cnt != int(n[r, c]))
    print(f"{name}: 20 pixels, max |diff| {worst:.6f}, observation counts differing {bad_n}")
    if worst > 0.01 or bad_n:
        errors.append(name)
print("RESULT: FAILED " + ", ".join(errors) if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
