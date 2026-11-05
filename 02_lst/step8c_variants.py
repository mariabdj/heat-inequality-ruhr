r"""Step 8c: LST composites for the sensitivity analyses S4, S5, S6, S6b, S12, S13, S14, S15, S16 (preregistration Q24),
with the same masks, grid and rules as the primary composite (02_lst/lst_pipeline.py), changing only what each
analysis names. Rules fixed in VERIFICATION_LOG.md (Step 8c decision record) before this script was run.
Usage: .venv\Scripts\python.exe 02_lst/step8c_variants.py download   (S4 scene and ST_QA bands, Earth Engine)
       .venv\Scripts\python.exe 02_lst/step8c_variants.py build      (all variant rasters, local)
"""
import json, pathlib, sys

import numpy as np
import pandas as pd
import rasterio

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "02_lst"
SC = OUT / "exports/scenes"
VAR = OUT / "exports/variants"
sys.stdout.reconfigure(encoding="utf-8")
st1 = pd.read_csv(OUT / "scenes_stage1.csv")
used = st1[st1.used].reset_index(drop=True)
hot = used[used.hot_day].reset_index(drop=True)


def download():
    import ee
    sys.argv = [sys.argv[0], "none"]
    sys.path.insert(0, str(OUT)); import lst_pipeline as P
    for sid in used.id:
        img = P.CAND.filter(ee.Filter.eq("system:index", sid)).first()
        if not (SC / f"{sid}_lst.tif").is_file():                       # S4: the non-hot-day scene
            P.download(P.on_grid(P.lst_c(img)).unmask(-999, False).toFloat(), f"scenes/{sid}_lst.tif"); print("LST", sid, flush=True)
        if not (SC / f"{sid}_stqa.tif").is_file():                      # S16: ST_QA in 0.01 K, masked like LST
            P.download(P.on_grid(img.select("ST_QA").updateMask(P.valid_mask(img))).unmask(-9999, False).toFloat(), f"scenes/{sid}_stqa.tif")
            print("ST_QA", sid, flush=True)


def read(p):
    with rasterio.open(p) as s:
        return s.read(1), s.profile


def write(name, mean, count, prof, extra=None):
    VAR.mkdir(parents=True, exist_ok=True)
    p = prof.copy(); p.update(count=2, dtype="float32", nodata=np.nan, compress="deflate")
    with rasterio.open(VAR / f"{name}.tif", "w", **p) as d:
        d.write(np.where(count >= 5, mean, np.nan).astype(np.float32), 1); d.write(count.astype(np.float32), 2)
    print(f"{name}: scenes {extra}, pixels with >= 5 obs {int((count >= 5).sum())}", flush=True)


def composite(ids, core, value_fn):
    """value_fn(lst, valid, sid) -> per-pixel values for valid pixels (or None to skip the scene)."""
    total = count = None
    for sid in ids:
        lst = read(SC / f"{sid}_lst.tif")[0]; valid = lst != -999
        v = value_fn(lst, valid, sid)
        if v is None:
            continue
        ok = valid & np.isfinite(v)
        total = np.where(ok, v, 0.0) if total is None else total + np.where(ok, v, 0.0)
        count = ok.astype(np.int32) if count is None else count + ok
    return total / np.maximum(count, 1), count


def build():
    dom, prof = read(OUT / "exports/domain_ref_core.tif")
    with rasterio.open(OUT / "exports/domain_ref_core.tif") as s:
        core = s.read(2) == 1; T = s.transform; shape = (s.height, s.width)
    info = {}
    med = lambda lst, valid: float(np.median(lst[valid & core]))
    anom = lambda lst, valid, sid: lst - med(lst, valid)
    # check: the primary composite is reproduced by this code
    m0, c0 = composite(hot.id, core, anom)
    prim = read(OUT / "exports/lst_anomaly_hot.tif")[0]
    d = np.nanmax(np.abs(np.where(c0 >= 5, m0, np.nan) - prim))
    print(f"check: primary composite reproduced, max |diff| {d:.2e} C"); assert d < 1e-4
    info["primary_reproduced_max_abs_diff"] = float(d)
    sets = {"S4_all_summer": used, "S6_landsat8": hot[hot.spacecraft == "LANDSAT_8"], "S6b_path196": hot[hot.path == 196],
            "S6b_path197": hot[hot.path == 197], "S12_valid95": hot[hot.valid_share >= 0.95]}
    for name, s in sets.items():
        m, c = composite(s.id, core, anom); write(name, m, c, prof, len(s)); info[name] = {"scenes": list(s.id)}
    m, c = composite(hot.id, core, lambda lst, valid, sid: lst)                    # S5 absolute LST
    write("S5_absolute", m, c, prof, len(hot))

    def std(lst, valid, sid):                                                      # S15 standardised anomaly
        q1, q2, q3 = np.percentile(lst[valid & core], [25, 50, 75]); return (lst - q2) / (q3 - q1)
    m, c = composite(hot.id, core, std); write("S15_standardised", m, c, prof, len(hot))
    # S14: mean of yearly mean anomalies
    yr = hot.date.str[:4]
    ytot, ycnt, allc = [], [], None
    for y in sorted(yr.unique()):
        m, c = composite(hot.id[yr == y], core, anom); ytot.append(np.where(c > 0, m, np.nan)); allc = c if allc is None else allc + c
    m = np.nanmean(np.stack(ytot), axis=0); write("S14_yearly_mean", np.nan_to_num(m, nan=0), allc, prof, len(hot))
    info["S14_years"] = sorted(yr.unique())
    # S13: anomaly relative to each city's median
    import geopandas as gpd
    from rasterio.features import rasterize
    cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(32632)
    cid = rasterize([(g, i + 1) for i, g in enumerate(cities.geometry)], out_shape=shape, transform=T, fill=0, all_touched=False, dtype="uint8")
    skipped = []

    def city_anom(lst, valid, sid):
        out = np.full(lst.shape, np.nan)
        for i in range(len(cities)):
            sel = (cid == i + 1) & valid & core
            if sel.sum() < 1000:
                skipped.append({"scene": sid, "city": cities.GEN.iloc[i], "valid_core_pixels": int(sel.sum())}); continue
            cm = float(np.median(lst[sel])); out[cid == i + 1] = lst[cid == i + 1] - cm
        return out
    m, c = composite(hot.id, core, city_anom); write("S13_city_median", m, c, prof, len(hot))
    info["S13_city_scenes_skipped"] = skipped
    # S16: ST_QA > 3 K also masked, medians recomputed
    retained = []

    def qa_anom(lst, valid, sid):
        q = read(SC / f"{sid}_stqa.tif")[0]
        ok = valid & (q != -9999) & (q * 0.01 <= 3.0)
        retained.append(q[valid & (q != -9999)] * 0.01)
        lst2 = np.where(ok, lst, np.nan)
        return lst2 - float(np.median(lst[ok & core]))
    m, c = composite(hot.id, core, qa_anom); write("S16_stqa3K", m, c, prof, len(hot))
    r = np.concatenate(retained)
    info["S16_stqa_K_valid_pixels"] = {"p50": float(np.percentile(r, 50)), "p90": float(np.percentile(r, 90)), "p99": float(np.percentile(r, 99)),
                                       "share_above_3K": float((r > 3).mean())}
    (VAR / "variants_info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in info.items() if k != "S13_city_scenes_skipped"}, indent=1)[:1500])
    print("S13 city-scene pairs skipped:", len(skipped))


if __name__ == "__main__":
    download() if sys.argv[1] == "download" else build()
