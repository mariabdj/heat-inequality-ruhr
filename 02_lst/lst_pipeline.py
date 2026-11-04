r"""Land surface temperature pipeline (Step 4), preregistration Q12 and Q23.
Stage 1 (flags only, no temperature):  .venv\Scripts\python.exe 02_lst/lst_pipeline.py stage1
Stage 2 (temperatures, composite):     .venv\Scripts\python.exe 02_lst/lst_pipeline.py stage2 --scenes hot|all
All rasters are on the native Landsat 30 m grid (EPSG:32632, transform of the candidate scenes' QA_PIXEL band).
"""
import json, pathlib, sys

import ee
import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "02_lst"
sys.stdout.reconfigure(encoding="utf-8")
ee.Initialize(project="peppy-apparatus-452923-g2")

SCALE, OFFSET = 0.00341802, 149.0           # USGS LSDS-1619 Table 6-1
DN_MIN, DN_MAX = 293, 61440                  # valid range of ST_B10 (same table)
CDIST_MIN = 100                              # ST_CDIST x 0.01 >= 1 km
FILL = -9999


# ---------- study area and grid
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(32632)
# GeoJSON is read by Earth Engine as longitude/latitude (EPSG:4326), so the outlines are sent in that system
fc_cities = ee.FeatureCollection(json.loads(cities.to_crs(4326)[["geometry"]].assign(one=1).to_json()))
bbox_utm = cities.total_bounds
region = ee.Geometry.Rectangle([float(bbox_utm[0]) - 300, float(bbox_utm[1]) - 300, float(bbox_utm[2]) + 300, float(bbox_utm[3]) + 300],
                               "EPSG:32632", False)


CAND_LIST = ROOT / "01_data/raw/landsat/candidate_scenes.csv"   # fixed list (Q12.4), written once by freeze_candidates()


def candidates_query():
    """Q12.1: Landsat 8 and 9 Tier 1 L2SP, path 196 or 197, row 24, June to August 2018 to 2025."""
    col = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").merge(ee.ImageCollection("LANDSAT/LC09/C02/T1_L2"))
    return (col.filter(ee.Filter.inList("WRS_PATH", [196, 197])).filter(ee.Filter.eq("WRS_ROW", 24))
            .filter(ee.Filter.calendarRange(2018, 2025, "year")).filter(ee.Filter.calendarRange(6, 8, "month"))
            .filter(ee.Filter.eq("PROCESSING_LEVEL", "L2SP")))


def freeze_candidates():
    q = candidates_query()
    rows = {k: q.aggregate_array(k).getInfo() for k in ["system:index", "LANDSAT_PRODUCT_ID", "DATE_PRODUCT_GENERATED", "WRS_PATH", "SPACECRAFT_ID"]}
    CAND_LIST.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).rename(columns={"system:index": "id"}).to_csv(CAND_LIST, index=False)


def candidates():
    ids = pd.read_csv(CAND_LIST).id.tolist()
    return candidates_query().filter(ee.Filter.inList("system:index", ids))


if len(sys.argv) > 1 and sys.argv[1] == "freeze":
    if CAND_LIST.is_file():
        sys.exit(f"{CAND_LIST} exists: the candidate list is frozen and must not be rewritten")
    freeze_candidates()
    sys.exit(0)
if not CAND_LIST.is_file():
    sys.exit(f"{CAND_LIST} missing: the frozen candidate list is required (Q12.4)")
CAND = candidates()
# the live catalogue must still match the frozen list (same scenes, same processing version)
_frozen = pd.read_csv(CAND_LIST).sort_values("id").reset_index(drop=True)
_live = pd.DataFrame({k: CAND.aggregate_array(k).getInfo() for k in ["system:index", "LANDSAT_PRODUCT_ID", "DATE_PRODUCT_GENERATED"]}
                     ).rename(columns={"system:index": "id"}).sort_values("id").reset_index(drop=True)
if len(_live) != len(_frozen) or not _live.equals(_frozen[["id", "LANDSAT_PRODUCT_ID", "DATE_PRODUCT_GENERATED"]].astype(_live.dtypes.to_dict())):
    sys.exit("the Earth Engine catalogue no longer matches the frozen candidate list: stop and check")
PROJ = CAND.first().select("QA_PIXEL").projection()
GRID = {"crs": "EPSG:32632", "crsTransform": PROJ.getInfo()["transform"]}
_tr = GRID["crsTransform"]
# download grid: the native 30 m grid over the cities' bounding box + 300 m
X0 = _tr[2] + np.floor((bbox_utm[0] - 300 - _tr[2]) / 30) * 30
Y1 = _tr[5] + np.ceil((bbox_utm[3] + 300 - _tr[5]) / 30) * 30
NX = int(np.ceil((bbox_utm[2] + 300 - X0) / 30)); NY = int(np.ceil((Y1 - (bbox_utm[1] - 300)) / 30))


def local_city_mask(all_touched=False):
    """Q12.4 pixel-centre rule, computed locally on the download grid (rasterio)."""
    from rasterio.features import rasterize
    from rasterio.transform import from_origin
    return rasterize([(g, 1) for g in cities.geometry], out_shape=(NY, NX), transform=from_origin(X0, Y1, 30, 30),
                     fill=0, all_touched=all_touched, dtype="uint8").astype(bool)


def on_grid(img):
    return img.reproject(crs=GRID["crs"], crsTransform=GRID["crsTransform"])


# Q12.4: reference domain = pixel centre in the 11 cities and < 50% permanent water (exact 10 m overlap)
# Earth Engine rasterises polygons with "any pixel touched"; the pixels touched but with their centre outside the
# cities (computed locally) are sent as points and removed, so the mask follows the pixel-centre rule.
_touch = on_grid(fc_cities.reduceToImage(["one"], ee.Reducer.first()).unmask(0).gt(0))
_fr = np.argwhere(local_city_mask(True) & ~local_city_mask(False))
_fringe_pts = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(X0 + (c + 0.5) * 30), float(Y1 - (r + 0.5) * 30)], "EPSG:32632"), {"one": 1})
                                    for r, c in _fr])
_fringe = on_grid(_fringe_pts.reduceToImage(["one"], ee.Reducer.first()).unmask(0).gt(0))
city_mask = _touch.And(_fringe.Not())
water10 = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").eq(80).unmask(0)
water_share = on_grid(water10.reduceResolution(ee.Reducer.mean(), maxPixels=64))
ref_domain = city_mask.And(water_share.lt(0.5))
# core: inside the image and not fill (QA bit 0 = 0) in every candidate scene; masked or outside = fill
core = on_grid(CAND.map(lambda i: i.select("QA_PIXEL").bitwiseAnd(1).eq(0).unmask(0, False)).min())
core_ref = ref_domain.And(core)


def valid_mask(img):
    """Q12.3 pixel mask (flags and ST_B10 range only, no temperature conversion)."""
    qa = img.select("QA_PIXEL").unmask(1)
    bad_bits = qa.bitwiseAnd(0b111111).neq(0)                      # bits 0-5: fill, dilated cloud, cirrus, cloud, shadow, snow
    cloud_conf = qa.rightShift(8).bitwiseAnd(3).gte(2)             # bits 8-9 medium (2) or high (3)
    st = img.select("ST_B10").unmask(0)
    st_bad = st.eq(0).Or(st.lt(DN_MIN)).Or(st.gt(DN_MAX))
    cd = img.select("ST_CDIST").unmask(FILL)
    sq = img.select("ST_QA").unmask(FILL)
    other_bad = cd.eq(FILL).Or(sq.eq(FILL)).Or(cd.lt(CDIST_MIN))
    return bad_bits.Or(cloud_conf).Or(st_bad).Or(other_bad).Not().rename("valid")


def scene_table():
    def f(img):
        v = on_grid(valid_mask(img)).And(core_ref)
        s = ee.Image.cat(v.rename("valid"), core_ref.rename("core")).reduceRegion(ee.Reducer.sum(), region, crs=GRID["crs"], crsTransform=GRID["crsTransform"], maxPixels=1e9)
        return ee.Feature(None, {"id": img.get("system:index"), "spacecraft": img.get("SPACECRAFT_ID"), "path": img.get("WRS_PATH"),
                                 "date": img.date().format("YYYY-MM-dd"), "time": img.get("SCENE_CENTER_TIME"),
                                 "n_valid_core": s.get("valid"), "n_core": s.get("core")})
    feats = ee.FeatureCollection(CAND.map(f)).getInfo()["features"]
    t = pd.DataFrame([x["properties"] for x in feats])
    t["valid_share"] = t.n_valid_core / t.n_core
    t["used"] = t.valid_share >= 0.80
    hot = pd.read_csv(ROOT / "01_data/processed/hot_days.csv")
    hot = set(hot.loc[hot.hot, "date"].str[:10])
    t["hot_day"] = t.date.isin(hot)
    return t


def stage1():
    t = scene_table()
    t.to_csv(OUT / "scenes_stage1.csv", index=False)
    dom = ee.Image.cat(ref_domain.rename("ref"), core_ref.rename("core_ref"), city_mask.rename("city")).reduceRegion(
        ee.Reducer.sum(), region, crs=GRID["crs"], crsTransform=GRID["crsTransform"], maxPixels=1e9).getInfo()
    print(f"candidate scenes: {len(t)}; used (>= 80% valid core pixels): {int(t.used.sum())}; hot-day and used: {int((t.used & t.hot_day).sum())}")
    # Q12.4: core share per city (local, from the downloaded domain rasters)
    from rasterio.features import rasterize
    from rasterio.transform import from_origin
    cid = rasterize([(g, i + 1) for i, g in enumerate(cities.geometry)], out_shape=(NY, NX), transform=from_origin(X0, Y1, 30, 30),
                    fill=0, all_touched=False, dtype="uint8")
    rr, _ = download(ee.Image.cat(ref_domain.unmask(0), core_ref.unmask(0)).toFloat(), "domain_ref_core.tif")
    shares = pd.DataFrame([{"city": cities.GEN.iloc[i], "ref_pixels": int(((cid == i + 1) & (rr[0] == 1)).sum()),
                            "core_ref_pixels": int(((cid == i + 1) & (rr[1] == 1)).sum())} for i in range(len(cities))])
    shares["core_share"] = shares.core_ref_pixels / shares.ref_pixels
    shares.to_csv(OUT / "stage1_core_share_by_city.csv", index=False)
    print(shares.round(3).to_string(index=False))
    print(f"city pixels: {dom['city']:.0f} ({dom['city'] * 900 / 1e6:.1f} km2, VG250 area {cities.area.sum() / 1e6:.1f} km2); reference domain: {dom['ref']}; core reference domain: {dom['core_ref']} "
          f"({dom['core_ref'] / dom['ref']:.1%} of the reference domain)")
    # Q23: share of cells passing rules 1-3 with < 70% of their area covered by pixels with >= 5 valid hot-day observations
    hot_used = t[t.used & t.hot_day].id.tolist()
    cnt = on_grid(CAND.filter(ee.Filter.inList("system:index", hot_used)).map(lambda i: on_grid(valid_mask(i)).unmask(0)).sum())
    ok5 = cnt.gte(5).unmask(0).rename("ok")
    cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")
    cells = cells[cells.rule3].to_crs(32632)
    cover = {}
    for i in range(0, len(cells), 2500):
        part = cells.iloc[i:i + 2500]
        fc = ee.FeatureCollection([ee.Feature(ee.Geometry(g.__geo_interface__, "EPSG:32632", False), {"id": gid})
                                   for gid, g in zip(part.gitter_id_100m, part.geometry)])
        res = ok5.reduceRegions(fc, ee.Reducer.mean(), crs=GRID["crs"], crsTransform=GRID["crsTransform"]).getInfo()
        cover.update({f["properties"]["id"]: f["properties"].get("mean") for f in res["features"]})
        print(f"  coverage: {min(i + 2500, len(cells))} / {len(cells)}")
    c = pd.Series(cover)
    share_low = float((c < 0.70).mean())
    pd.DataFrame({"gitter_id_100m": c.index, "share_area_ge5_hot_obs": c.values}).to_csv(OUT / "stage1_cell_coverage.csv", index=False)
    print(f"Q23 check: cells with < 70% of area covered by pixels with >= 5 valid hot-day observations: {share_low:.1%} "
          f"-> {'FALLBACK to all summer scenes' if share_low > 0.30 else 'hot-day rule kept'}")


def lst_c(img):
    """ST_B10 digital number -> degrees C (USGS scale and offset), masked to valid pixels."""
    return img.select("ST_B10").multiply(SCALE).add(OFFSET).subtract(273.15).updateMask(valid_mask(img)).rename("lst")


# Earth Engine computes medians with histograms (approximate: 0.05 to 0.11 C off in the Gate 4 check), so each scene's
# LST is downloaded on the native grid and the exact median, the anomalies and the composite are computed here with numpy.


def download(img, name=None):
    """Download an image on the native grid in 1024-pixel tiles with computePixels; return (array, profile); optionally save."""
    import io, rasterio
    from rasterio.merge import merge
    x0, y1, nx, ny = X0, Y1, NX, NY
    tiles, step = [], 1024
    for oy in range(0, ny, step):
        for ox in range(0, nx, step):
            req = {"expression": img, "fileFormat": "GEO_TIFF",
                   "grid": {"dimensions": {"width": min(step, nx - ox), "height": min(step, ny - oy)},
                            "affineTransform": {"scaleX": 30, "shearX": 0, "translateX": x0 + ox * 30,
                                                "shearY": 0, "scaleY": -30, "translateY": y1 - oy * 30},
                            "crsCode": "EPSG:32632"}}
            tiles.append(rasterio.open(io.BytesIO(ee.data.computePixels(req))))
    mosaic, transform = merge(tiles)
    prof = tiles[0].profile.copy()
    prof.update(height=mosaic.shape[1], width=mosaic.shape[2], count=mosaic.shape[0], transform=transform,
                compress="deflate", driver="GTiff")
    if name:
        (OUT / "exports").mkdir(exist_ok=True)
        with rasterio.open(OUT / "exports" / name, "w", **prof) as dst:
            dst.write(mosaic)
    return mosaic, prof


def stage2(which="hot"):
    import rasterio
    t = pd.read_csv(OUT / "scenes_stage1.csv")
    sel = t[t.used & (t.hot_day if which == "hot" else True)].reset_index(drop=True)
    core, prof = download(core_ref.unmask(0).toFloat().rename("core_ref"), "core_ref_domain.tif")
    core = core[0] == 1
    total, count, meds, cpath = None, None, [], {}
    for sid in sel.id:
        img = CAND.filter(ee.Filter.eq("system:index", sid)).first()
        # sameFootprint=False: pixels outside the scene footprint become -999 (missing), not 0
        lst, _ = download(on_grid(lst_c(img)).unmask(-999, False).toFloat(), f"scenes/{sid}_lst.tif")
        lst = lst[0]
        valid = lst != -999
        med = float(np.median(lst[valid & core]))          # Q12.5, exact median of the valid core reference-domain pixels
        meds.append(med)
        anom = np.where(valid, lst - med, 0.0)
        total = anom if total is None else total + anom
        count = valid.astype(np.int32) if count is None else count + valid
        path = int(sel.loc[sel.id == sid, "path"].iloc[0])
        cpath[path] = valid.astype(np.int32) if path not in cpath else cpath[path] + valid
        print(f"  {sid}: median {med:.4f} C over {int((valid & core).sum())} pixels")
    sel["median_c"] = meds
    sel.to_csv(OUT / f"scenes_used_{which}.csv", index=False)
    mean = np.where(count >= 5, total / np.maximum(count, 1), np.nan).astype(np.float32)   # Q12.6: pixels with < 5 obs missing
    prof.update(count=4, dtype="float32", nodata=np.nan)
    zero = np.zeros_like(count)
    with rasterio.open(OUT / "exports" / f"lst_anomaly_{which}.tif", "w", **prof) as dst:
        dst.write(mean, 1); dst.write(count.astype(np.float32), 2)
        dst.write(cpath.get(196, zero).astype(np.float32), 3); dst.write(cpath.get(197, zero).astype(np.float32), 4)
        for b, n in enumerate(["anom_mean_C", "n_obs", "n_obs_path196", "n_obs_path197"], 1):
            dst.set_band_description(b, n)
    bal = sel.assign(year=sel.date.str[:4], month=sel.date.str[5:7]).groupby(["year", "month", "path", "spacecraft"]).size()
    bal.rename("scenes").reset_index().to_csv(OUT / f"scenes_balance_{which}.csv", index=False)
    print("scenes per month:", sel.date.str[5:7].value_counts().sort_index().to_dict())
    print(f"scenes: {len(sel)}; medians (C): min {min(meds):.2f}, max {max(meds):.2f}; "
          f"composite pixels with >= 5 obs: {int((count >= 5).sum())}")


if __name__ == "__main__":
    if sys.argv[1] == "stage1":
        stage1()
    elif sys.argv[1] == "stage2":
        stage2(sys.argv[3] if len(sys.argv) > 3 else "hot")
