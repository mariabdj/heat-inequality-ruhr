r"""Step 6: one table, one row per inhabited 100 m cell of the 11 cities (rule 1), with all variables.
Zonal statistics with exactextract: mean of the raster pixels weighted by the exact share of each pixel inside the cell
(preregistration Q12.7). Cell polygons are reprojected to each raster's CRS; rasters are never resampled.
- LST anomaly composite (EPSG:32632): mean; coverage share = (sum of coverage fractions of non-missing pixels) x 900 m2
  / cell area in that CRS (Q13 rule 4 needs >= 0.70).
- Tree cover 2022 and imperviousness 2021 (EPSG:3035, 10 m): mean of valid pixels; the no-data code 255 (legend file)
  is declared through a small VRT file pointing to the raw raster (the raw file is not changed).
- Elevation (NRW terrain model, EPSG:25832): mean.
No relationship between variables is computed here.
Usage: .venv\Scripts\python.exe 04_grid_join/step6_join.py  ->  04_grid_join/analysis_table.parquet, 05_analysis/results/step6_exclusions.csv
"""
import glob, pathlib, sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from exactextract import exact_extract

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nodata_vrt import nodata_vrt

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw"
sys.stdout.reconfigure(encoding="utf-8")

cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")[
    ["gitter_id_100m", "city", "einwohner_n", "water_share", "rule1", "rule2", "rule3", "x_mp", "y_mp", "geometry"]]


def zonal(raster, ops, crs, prefix):
    poly = cells[["gitter_id_100m", "geometry"]].to_crs(crs)
    df = exact_extract(raster, poly, ops, include_cols=["gitter_id_100m"], output="pandas")
    df.columns = ["gitter_id_100m"] + [f"{prefix}_{c}" for c in df.columns[1:]]
    if prefix == "lst":
        df["lst_cell_area_m2"] = poly.area.values
    return df


lst = zonal(str(ROOT / "02_lst/exports/lst_anomaly_hot.tif"), ["mean", "count"], 32632, "lst")
lst = lst.rename(columns={"lst_band_1_mean": "lst_anom", "lst_band_1_count": "lst_px_count", "lst_band_2_mean": "lst_nobs_mean",
                          "lst_band_3_mean": "lst_nobs196_mean", "lst_band_4_mean": "lst_nobs197_mean"})
lst = lst.drop(columns=[c for c in lst.columns if c.endswith("_count") and c != "lst_px_count"])
# Q12.5 reporting: composite pixels (>= 5 obs) seen by one path only; share of the cell's composite area that is one-path
with rasterio.open(ROOT / "02_lst/exports/lst_anomaly_hot.tif") as src:
    n, n196, n197 = src.read(2), src.read(3), src.read(4)
    prof = src.profile.copy()
one = np.where(n >= 5, ((n196 == 0) | (n197 == 0)).astype("float32"), np.nan)
prof.update(count=1, dtype="float32", nodata=np.nan)
one_path_tif = ROOT / "02_lst/exports/one_path_pixels.tif"
with rasterio.open(one_path_tif, "w", **prof) as dst:
    dst.write(one, 1)
op = zonal(str(one_path_tif), ["mean"], 32632, "op").rename(columns={"op_mean": "one_path_share"})
lst = lst.merge(op, on="gitter_id_100m", how="left")
lst["one_path_only"] = lst.one_path_share == 1             # fully one-path
lst["one_path_partly"] = lst.one_path_share > 0            # any part one-path
lst["lst_cover_share"] = lst.lst_px_count * 900 / lst.lst_cell_area_m2

tcd = zonal(nodata_vrt(RAW / "copernicus/CLMS_HRLVLCC_TCD_R10m_2022_bbox.tif", 255, ROOT / "04_grid_join/tcd_nodata.vrt"), ["mean", "max"], 3035, "tree")
imd_parts = [zonal(nodata_vrt(f, 255, ROOT / f"04_grid_join/imd_nodata_{i}.vrt"), ["mean", "max", "count"], 3035, "imp")
             for i, f in enumerate(sorted(glob.glob(str(RAW / "copernicus/*IMD*2021*.tif"))))]
# a cell lies in one tile, or straddles the tile border: combine the two tiles weighted by covered pixels
imd = pd.concat(imd_parts).dropna(subset=["imp_mean"])
imd["w"] = imd.imp_count
imd = imd.groupby("gitter_id_100m").apply(lambda g: pd.Series({"imp_mean": np.average(g.imp_mean, weights=g.w), "imp_max": g.imp_max.max()}),
                                          include_groups=False).reset_index()
dgm = zonal(str(RAW / "geobasis_nrw/dgm_nrw_10m.tif"), ["mean"], 25832, "elev")

t = cells.drop(columns="geometry")
for part in (lst, tcd, imd, dgm):
    t = t.merge(part, on="gitter_id_100m", how="left")
t = t.rename(columns={"tree_mean": "tree_cover", "imp_mean": "imperviousness", "elev_mean": "elevation"})
for c, mx in (("tree_cover", "tree_max"), ("imperviousness", "imp_max")):
    print(f"{c}: cells with a value above 100 after the no-data declaration: {int((t[mx] > 100).sum())}")

census = pd.read_csv(ROOT / "01_data/processed/census_step3.csv").drop(columns=["city", "einwohner_n", "rule3"])
t = t.merge(census, on="gitter_id_100m", how="left")
t["rule4"] = t.rule3 & (t.lst_cover_share >= 0.70)
usable = {v: t[f"{v}_in_file"].fillna(False).astype(bool) & ~t[f"{v}_br"].fillna(False).astype(bool) for v in ("rent", "foreign", "age65", "under18")}
covs_A = t[["elevation", "lst_anom"]].notna().all(axis=1)                                   # Model A covariates (Q19)
covs = covs_A & t[["tree_cover", "imperviousness"]].notna().all(axis=1)                    # Model B adds these
t["sample_model_A"] = t.rule4 & usable["rent"] & usable["foreign"] & usable["age65"] & usable["under18"] & covs_A
t["sample_model_B"] = t.sample_model_A & covs
t.to_parquet(ROOT / "04_grid_join/analysis_table.parquet", index=False)

# exclusions, in the preregistered order (Q13)
rows = [("inhabited cells in the 11 cities (rule 1)", int(t.rule1.sum())),
        ("removed: population < 10 (rule 2)", int((t.rule1 & ~t.rule2).sum())),
        ("removed: >= 50% permanent water (rule 3)", int((t.rule2 & ~t.rule3).sum())),
        ("removed: < 70% of area with LST composite (rule 4)", int((t.rule3 & ~t.rule4).sum())),
        ("cells passing rules 1 to 4", int(t.rule4.sum()))]
for v in ("rent", "foreign", "age65", "under18"):
    rows.append((f"  of which {v} usable (present, not bracketed)", int((t.rule4 & usable[v]).sum())))
rows.append(("removed: a Model A covariate missing", int((t.rule4 & ~covs_A).sum())))
rows.append(("Model A sample (rule 5: all four social variables usable)", int(t.sample_model_A.sum())))
rows.append(("Model B sample (Model A + tree cover and imperviousness present)", int(t.sample_model_B.sum())))
ex = pd.DataFrame(rows, columns=["step", "cells"])
ex.to_csv(ROOT / "05_analysis/results/step6_exclusions.csv", index=False)
print(ex.to_string(index=False))

# Q14: per city, cells lost to each reason; Q12.5: cells observed by one path only
pc = t.groupby("city").apply(lambda g: pd.Series({
    "rule1": int(g.rule1.sum()), "lost_rule2": int((g.rule1 & ~g.rule2).sum()), "lost_rule3": int((g.rule2 & ~g.rule3).sum()),
    "lost_rule4": int((g.rule3 & ~g.rule4).sum()), "pass_rules_1_4": int(g.rule4.sum()),
    **{f"usable_{v}": int((g.rule4 & usable[v].loc[g.index]).sum()) for v in usable},
    "model_A": int(g.sample_model_A.sum()), "one_path_fully_rule4": int((g.rule4 & g.one_path_only).sum()),
    "one_path_partly_rule4": int((g.rule4 & g.one_path_partly).sum()), "one_path_over_half_rule4": int((g.rule4 & (g.one_path_share > 0.5)).sum()),
    "one_path_partly_model_A": int((g.sample_model_A & g.one_path_partly).sum())}), include_groups=False)
pc.loc["TOTAL"] = pc.sum()
pc.to_csv(ROOT / "05_analysis/results/step6_exclusions_by_city.csv")
print(pc.to_string())

# Q15: extreme values (kept, counted): beyond Q1 - 3 IQR or Q3 + 3 IQR among cells passing rule 4 with a usable value (D6)
a = t[t.rule4]
ext = []
for v in ["lst_anom", "rent", "foreign", "age65", "under18", "tree_cover", "imperviousness", "elevation"]:
    x = (a.loc[usable[v].loc[a.index], v] if v in usable else a[v]).dropna(); q1, q3 = x.quantile([.25, .75]); iqr = q3 - q1
    ext.append({"variable": v, "n": len(x), "low_limit": q1 - 3 * iqr, "high_limit": q3 + 3 * iqr,
                "n_extreme": int(((x < q1 - 3 * iqr) | (x > q3 + 3 * iqr)).sum()), "min": x.min(), "max": x.max()})
pd.DataFrame(ext).to_csv(ROOT / "05_analysis/results/step6_extreme_values.csv", index=False)

# selection: Model A sample vs all cells passing rule 4 (overall and per city)
def summ(d):
    return pd.Series({"cells": len(d), "population": int(d.einwohner_n.sum()), "median_population": d.einwohner_n.median(),
                      "pw_mean_lst_anom": np.average(d.lst_anom, weights=d.einwohner_n), "median_imperviousness": d.imperviousness.median(),
                      "median_tree_cover": d.tree_cover.median()})
sel = pd.concat({"rule4_all": a.groupby("city").apply(summ, include_groups=False),
                 "model_A": t[t.sample_model_A].groupby("city").apply(summ, include_groups=False)}, axis=1)
sel.loc["TOTAL"] = pd.concat({"rule4_all": summ(a), "model_A": summ(t[t.sample_model_A])})
sel.to_csv(ROOT / "05_analysis/results/step6_sample_comparison.csv")
print("rows in table:", len(t), "| columns:", len(t.columns))
