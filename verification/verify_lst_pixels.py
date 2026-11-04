r"""GATE 4 (strengthened at Gate 7): independent checks of the LST pipeline (02_lst/lst_pipeline.py).
The pipeline's own masks and functions are NOT reused for the reference values: raw bands are downloaded and the rules
are re-implemented here.
(d) Domain: city mask rebuilt locally (pixel-centre rule) must contain the whole reference domain; water share of 2,000
    random city pixels recomputed from raw 10 m WorldCover pixels with exact overlap (exactextract) must agree with the
    pipeline within 0.02, with no different < 50% decision except within 0.02 of the threshold.
(e) 80% rule: for 6 scenes the raw QA_PIXEL, ST_B10, ST_CDIST and ST_QA bands are downloaded, masked with our own code,
    and the valid share of core reference pixels must equal the stage-1 table within 1e-6; for all scenes,
    used == (share >= 0.80) and the hot-day flags == hot_days.csv.
(a) Raw digital numbers: 3 scenes x 60 pixels (40 random core pixels + 20 pixels invalid in the exported scene file):
    own validity and own conversion vs the exported scene GeoTIFF: same validity, |diff| <= 0.01 C.
(b) Exact medians of 3 scenes recomputed from the exported scene files: equal to the stored median within 0.01 C.
(c) 20 composite pixels recomputed from the exported scene files: mean of (LST - median) within 0.01 C, same counts.
Usage: .venv\Scripts\python.exe verification/verify_lst_pixels.py
"""
import io, pathlib, sys

import ee
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from exactextract import exact_extract
from rasterio.features import rasterize
from rasterio.merge import merge
from shapely.geometry import box

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "02_lst"))
import lst_pipeline as P   # used only for the scene collection, the water-share image under test and stored outputs

rng = np.random.default_rng(20261102)
errors = []
E = ROOT / "02_lst/exports"
st1 = pd.read_csv(ROOT / "02_lst/scenes_stage1.csv")
used = pd.read_csv(ROOT / "02_lst/scenes_used_hot.csv")
dom = rasterio.open(E / "domain_ref_core.tif"); ref, core_ref = dom.read(1) == 1, dom.read(2) == 1
T = dom.transform
comp = rasterio.open(E / "lst_anomaly_hot.tif"); cmean, cnobs = comp.read(1), comp.read(2)


def raw_grid(img_bands):
    """Download raw bands on the same grid with computePixels (our own call, not P.download)."""
    out = []
    for oy in range(0, dom.height, 1024):
        row = []
        for ox in range(0, dom.width, 1024):
            req = {"expression": img_bands, "fileFormat": "GEO_TIFF",
                   "grid": {"dimensions": {"width": min(1024, dom.width - ox), "height": min(1024, dom.height - oy)},
                            "affineTransform": {"scaleX": 30, "shearX": 0, "translateX": T.c + ox * 30, "shearY": 0,
                                                "scaleY": -30, "translateY": T.f - oy * 30}, "crsCode": "EPSG:32632"}}
            with rasterio.open(io.BytesIO(ee.data.computePixels(req))) as s:
                row.append(s.read())
        out.append(np.concatenate(row, axis=2))
    return np.concatenate(out, axis=1)


def own_valid(dn, qa, cd, sq):
    bad = (qa & 0b111111) != 0
    conf = ((qa >> 8) & 3) >= 2
    return ~(bad | conf | (dn == 0) | (dn < 293) | (dn > 61440) | (cd == -9999) | (sq == -9999) | (cd < 100))


# (d) domain
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(32632)
city_local = rasterize([(g, 1) for g in cities.geometry], out_shape=ref.shape, transform=T, fill=0, all_touched=False).astype(bool)
outside = int((ref & ~city_local).sum())
print(f"(d) reference-domain pixels outside the locally rebuilt pixel-centre city mask: {outside}; "
      f"city pixels {int(city_local.sum())}, reference pixels {int(ref.sum())}")
if outside:
    errors.append("(d) reference domain extends beyond the pixel-centre city mask")
pick = np.argwhere(city_local)[rng.choice(int(city_local.sum()), 2000, replace=False)]
px = gpd.GeoDataFrame({"k": range(2000)}, geometry=[box(T.c + c * 30, T.f - (r + 1) * 30, T.c + (c + 1) * 30, T.f - r * 30)
                                                    for r, c in pick], crs=32632)
b = px.to_crs(4326).total_bounds
wc = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map")
nproj = wc.projection().getInfo()["transform"]; sx, sy = nproj[0], nproj[4]
x0w = nproj[2] + np.floor((b[0] - nproj[2]) / sx) * sx; y1w = nproj[5] + np.floor((b[3] - nproj[5]) / sy) * sy
nxw = int(np.ceil((b[2] - x0w) / sx)) + 1; nyw = int(np.ceil((b[1] - y1w) / sy)) + 1
tiles = []
for oy in range(0, nyw, 2048):
    for ox in range(0, nxw, 2048):
        req = {"expression": wc, "fileFormat": "GEO_TIFF",
               "grid": {"dimensions": {"width": min(2048, nxw - ox), "height": min(2048, nyw - oy)},
                        "affineTransform": {"scaleX": sx, "shearX": 0, "translateX": x0w + ox * sx, "shearY": 0, "scaleY": sy,
                                            "translateY": y1w + oy * sy}, "crsCode": "EPSG:4326"}}
        tiles.append(rasterio.open(io.BytesIO(ee.data.computePixels(req))))
mos, mtr = merge(tiles)
wfile = E / "check_worldcover_raw.tif"
# nodata 255: the downloaded tiles declare 0 as no-data, but here 0 means "not water"
prof = tiles[0].profile.copy(); prof.update(height=mos.shape[1], width=mos.shape[2], transform=mtr, driver="GTiff", dtype="uint8", nodata=255)
with rasterio.open(wfile, "w", **prof) as d:
    d.write((mos == 80).astype("uint8"))
own_w = exact_extract(str(wfile), px.to_crs(4326), ["mean"], output="pandas")["mean"].values
pipe_w = P.download(P.water_share.toFloat())[0][0][pick[:, 0], pick[:, 1]]
dw = np.abs(own_w - pipe_w)
flip = ((own_w < 0.5) != (pipe_w < 0.5)) & (np.minimum(np.abs(own_w - 0.5), np.abs(pipe_w - 0.5)) > 0.02)
print(f"(d) water share, 2000 pixels: max |diff| {dw.max():.4f}, decision flips beyond 0.02 of the threshold: {int(flip.sum())}")
if dw.max() > 0.02 or flip.any():
    errors.append("(d) water share differs")
# other direction: a city pixel with < 50% water (own value) must be in the stored reference domain, and >= 50% must not
wrong = (ref[pick[:, 0], pick[:, 1]] != (own_w < 0.5)) & (np.abs(own_w - 0.5) > 0.02)
print(f"(d) sampled city pixels whose reference-domain membership disagrees with the own water share: {int(wrong.sum())} "
      f"(pixels >= 50% water in the sample: {int((own_w >= 0.5).sum())})")
if wrong.any():
    errors.append("(d) reference domain membership differs from the own water rule")

# (e) 80% rule from raw bands, and the selection logic
hot = pd.read_csv(ROOT / "01_data/processed/hot_days.csv")
hot_set = set(hot.loc[hot.hot, "date"].str[:10])
if (st1.hot_day != st1.date.isin(hot_set)).any():
    errors.append("(e) hot-day flags differ from hot_days.csv")
if (st1.used != (st1.n_valid_core / st1.n_core >= 0.80)).any():
    errors.append("(e) used flag differs from the 80% rule")
if set(used.id) != set(st1.loc[st1.used & st1.hot_day, "id"]):
    errors.append("(e) used hot-day scenes differ from the stage-1 table")
scene_raw = {}
for sid in st1.id.iloc[[0, 40, 90]].tolist() + used.id.iloc[[0, len(used) // 2, len(used) - 1]].tolist():
    img = P.CAND.filter(ee.Filter.eq("system:index", sid)).first()
    raw = raw_grid(img.select(["ST_B10", "QA_PIXEL", "ST_CDIST", "ST_QA"]).unmask(-9999, False).toInt32())
    v = own_valid(raw[0], raw[1], raw[2], raw[3])
    share = (v & core_ref).sum() / core_ref.sum()
    stored = float(st1.loc[st1.id == sid, "valid_share"].iloc[0])
    print(f"(e) {sid}: own valid share {share:.6f}, stage-1 {stored:.6f}")
    if abs(share - stored) > 1e-6:
        errors.append(f"(e) valid share differs for {sid}")
    scene_raw[sid] = (raw, v)

# (a) raw DN vs exported scene files, incl. invalid pixels
for sid in used.id.iloc[[0, len(used) // 2, len(used) - 1]]:
    raw, v = scene_raw[sid]
    lst = rasterio.open(E / f"scenes/{sid}_lst.tif").read(1)
    cr = np.argwhere(core_ref)
    pts = cr[rng.choice(len(cr), 40, replace=False)]
    inv = np.argwhere(core_ref & (lst == -999))
    pts = np.vstack([pts, inv[rng.choice(len(inv), min(20, len(inv)), replace=False)]])
    mine_c = raw[0][pts[:, 0], pts[:, 1]] * 0.00341802 + 149.0 - 273.15
    mine_v = v[pts[:, 0], pts[:, 1]]
    file_v = lst[pts[:, 0], pts[:, 1]] != -999
    d = np.abs(mine_c[mine_v] - lst[pts[:, 0], pts[:, 1]][mine_v]).max() if mine_v.any() else 0
    print(f"(a) {sid}: {len(pts)} pixels ({int((~mine_v).sum())} invalid), validity agrees: {bool((mine_v == file_v).all())}, max |diff| {d:.5f} C")
    if not (mine_v == file_v).all() or d > 0.01:
        errors.append(f"(a) {sid}")

# (b) exact medians and (c) composite, both from the exported scene files
stack = {sid: rasterio.open(E / f"scenes/{sid}_lst.tif").read(1) for sid in used.id}
for sid in used.id.iloc[[0, len(used) // 2, len(used) - 1]]:
    l = stack[sid]; med = float(np.median(l[(l != -999) & core_ref]))
    st = float(used.loc[used.id == sid, "median_c"].iloc[0])
    print(f"(b) {sid}: median from file {med:.4f}, stored {st:.4f}")
    if abs(med - st) > 0.01:
        errors.append(f"(b) {sid}")
ok = np.argwhere(cnobs >= 5)
pick = ok[rng.choice(len(ok), 20, replace=False)]
worst = 0.0
for r, c in pick:
    vals = [stack[s][r, c] - m for s, m in zip(used.id, used.median_c) if stack[s][r, c] != -999]
    worst = max(worst, abs(np.mean(vals) - cmean[r, c]))
    if len(vals) != int(cnobs[r, c]):
        errors.append("(c) count differs")
print(f"(c) 20 composite pixels from the scene files: max |diff| {worst:.6f} C")
if worst > 0.01:
    errors.append("(c) composite differs")

for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
