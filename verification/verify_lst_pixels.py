r"""GATE 4: independent checks of the LST pipeline (02_lst/lst_pipeline.py).
(a) 3 used scenes x 20 random pixels: the raw ST_B10 digital number and QA_PIXEL are sampled from the untouched image,
    converted and masked HERE with our own code; must equal the pipeline value within 0.01 C, and agree on validity.
(b) 3 used scenes: exact median of the valid core reference-domain pixels computed HERE with numpy on the downloaded
    pixels; must equal the pipeline median within 0.01 C.
(c) 20 random composite pixels: mean over all used scenes of (pixel LST - scene median), recomputed HERE from sampled
    values; must equal the exported composite within 0.01 C, with the same observation count.
Usage: .venv\Scripts\python.exe verification/verify_lst_pixels.py
"""
import io, pathlib, sys

import ee
import numpy as np
import pandas as pd
import rasterio

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "02_lst"))
import lst_pipeline as P   # pipeline objects (grid, masks); the checks below use their own arithmetic

rng = np.random.default_rng(20261102)
errors = []
used = pd.read_csv(ROOT / "02_lst/scenes_used_hot.csv")
tif = rasterio.open(ROOT / "02_lst/exports/lst_anomaly_hot.tif")
comp, nobs = tif.read(1), tif.read(2)
T = tif.transform


def own_valid(dn, qa, cd, sq):
    bad = (qa & 0b111111) != 0
    conf = ((qa >> 8) & 3) >= 2
    return ~(bad | conf | (dn == 0) | (dn < 293) | (dn > 61440) | (cd == -9999) | (sq == -9999) | (cd < 100))


def pixel_points(rows, cols):
    xs = T.c + (cols + 0.5) * T.a
    ys = T.f + (rows + 0.5) * T.e
    return ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(x), float(y)], "EPSG:32632"), {"k": int(i)})
                                 for i, (x, y) in enumerate(zip(xs, ys))])


# (a) raw digital numbers -> C, 3 scenes x 20 pixels inside the composite area
ok_rc = np.argwhere(nobs >= 5)
for sid in used.id.iloc[[0, len(used) // 2, -1]]:
    img = P.CAND.filter(ee.Filter.eq("system:index", sid)).first()
    pick = ok_rc[rng.choice(len(ok_rc), 60, replace=False)]
    pts = pixel_points(pick[:, 0], pick[:, 1])
    raw = img.select(["ST_B10", "QA_PIXEL", "ST_CDIST", "ST_QA"]).unmask(-9999).sampleRegions(pts, scale=30, projection=P.PROJ, geometries=False).getInfo()
    pipe = P.on_grid(P.lst_c(img)).unmask(-999).sampleRegions(pts, scale=30, projection=P.PROJ, geometries=False).getInfo()
    r = pd.DataFrame([f["properties"] for f in raw["features"]]).set_index("k")
    p = pd.DataFrame([f["properties"] for f in pipe["features"]]).set_index("k")
    m = r.join(p, how="inner").head(20)
    dn = m.ST_B10.astype(np.int64)
    mine_valid = own_valid(dn.values, m.QA_PIXEL.astype(np.int64).values, m.ST_CDIST.values, m.ST_QA.values)
    mine_c = dn * 0.00341802 + 149.0 - 273.15
    pipe_valid = m.lst.values != -999
    agree = (mine_valid == pipe_valid).all()
    d = np.abs(mine_c[mine_valid] - m.lst[mine_valid]).max() if mine_valid.any() else 0.0
    print(f"(a) scene {sid}: {len(m)} pixels, valid {int(mine_valid.sum())}, validity agrees: {agree}, max |diff| {d:.5f} C "
          f"(example DN {dn.iloc[0]} -> {mine_c.iloc[0]:.3f} C)")
    if not agree or d > 0.01 or len(m) < 20:
        errors.append(f"(a) scene {sid}")

# (b) exact medians on the downloaded pixels
for sid in used.id.iloc[[0, len(used) // 2, -1]]:
    img = P.CAND.filter(ee.Filter.eq("system:index", sid)).first()
    two = ee.Image.cat(P.on_grid(P.lst_c(img)).unmask(-999, False).toFloat(), P.core_ref.toFloat())
    tr = P.GRID["crsTransform"]
    vals = []
    for oy in range(0, tif.height, 1024):
        for ox in range(0, tif.width, 1024):
            req = {"expression": two, "fileFormat": "GEO_TIFF",
                   "grid": {"dimensions": {"width": min(1024, tif.width - ox), "height": min(1024, tif.height - oy)},
                            "affineTransform": {"scaleX": 30, "shearX": 0, "translateX": T.c + ox * 30, "shearY": 0,
                                                "scaleY": -30, "translateY": T.f - oy * 30}, "crsCode": "EPSG:32632"}}
            with rasterio.open(io.BytesIO(ee.data.computePixels(req))) as src:
                a = src.read()
            sel = (a[1] == 1) & (a[0] != -999)
            vals.append(a[0][sel])
    v = np.concatenate(vals)
    mine = float(np.median(v))
    theirs = float(used.loc[used.id == sid, "median_c"].iloc[0])
    print(f"(b) scene {sid}: {len(v)} valid core pixels, numpy median {mine:.4f} C, pipeline median {theirs:.4f} C, |diff| {abs(mine - theirs):.4f}")
    if abs(mine - theirs) > 0.01:
        errors.append(f"(b) scene {sid}")

# (c) composite recomputed for 20 pixels
pick = ok_rc[rng.choice(len(ok_rc), 20, replace=False)]
pts = pixel_points(pick[:, 0], pick[:, 1])
acc = {i: [] for i in range(20)}
for sid, med in zip(used.id, used.median_c):
    img = P.CAND.filter(ee.Filter.eq("system:index", sid)).first()
    s = P.on_grid(P.lst_c(img)).unmask(-999).sampleRegions(pts, scale=30, projection=P.PROJ, geometries=False).getInfo()
    for f in s["features"]:
        if f["properties"]["lst"] != -999:
            acc[f["properties"]["k"]].append(f["properties"]["lst"] - med)
worst = 0.0
for i, (r, c) in enumerate(pick):
    mine = np.mean(acc[i])
    worst = max(worst, abs(mine - comp[r, c]))
    if len(acc[i]) != int(nobs[r, c]):
        errors.append(f"(c) pixel {i}: count {len(acc[i])} vs {int(nobs[r, c])}")
print(f"(c) 20 composite pixels recomputed from {len(used)} scenes: max |diff| {worst:.5f} C")
if worst > 0.01:
    errors.append("(c) composite differs")

for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
