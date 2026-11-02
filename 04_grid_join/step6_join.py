r"""Step 6: one table, one row per inhabited 100 m cell of the 11 cities (rule 1), with all variables.
Zonal statistics with exactextract: mean of the raster pixels weighted by the exact share of each pixel inside the cell
(preregistration Q12.7). Cell polygons are reprojected to each raster's CRS; rasters are never resampled.
- LST anomaly composite (EPSG:32632): mean; coverage share = (sum of coverage fractions of non-missing pixels) x 900 m2
  / cell area in that CRS (Q13 rule 4 needs >= 0.70).
- Tree cover 2022 and imperviousness 2021 (EPSG:3035, 10 m): mean; max kept to detect the no-data code 255.
- Elevation (NRW terrain model, EPSG:25832): mean.
No relationship between variables is computed here.
Usage: .venv\Scripts\python.exe 04_grid_join/step6_join.py  ->  04_grid_join/analysis_table.parquet, 05_analysis/results/step6_exclusions.csv
"""
import glob, pathlib, sys

import geopandas as gpd
import numpy as np
import pandas as pd
from exactextract import exact_extract

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
lst = lst.rename(columns={"lst_band_1_mean": "lst_anom", "lst_band_1_count": "lst_px_count", "lst_band_2_mean": "lst_nobs_mean"})
lst = lst.drop(columns=[c for c in lst.columns if c == "lst_band_2_count"])
lst["lst_cover_share"] = lst.lst_px_count * 900 / lst.lst_cell_area_m2

tcd = zonal(str(RAW / "copernicus/CLMS_HRLVLCC_TCD_R10m_2022_bbox.tif"), ["mean", "max"], 3035, "tree")
imd_parts = [zonal(f, ["mean", "max", "count"], 3035, "imp") for f in sorted(glob.glob(str(RAW / "copernicus/*IMD*2021*.tif")))]
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
for c in ("tree_cover", "imperviousness"):
    bad = t[f"{c.split('_')[0] if c == 'tree_cover' else 'imp'}_max"] > 100
    t.loc[bad, c] = np.nan            # no-data code 255 inside the cell
    print(f"{c}: cells touching the no-data code 255: {int(bad.sum())}")

census = pd.read_csv(ROOT / "01_data/processed/census_step3.csv").drop(columns=["city", "einwohner_n", "rule3"])
t = t.merge(census, on="gitter_id_100m", how="left")
t["rule4"] = t.rule3 & (t.lst_cover_share >= 0.70)
usable = {v: t[f"{v}_in_file"].fillna(False).astype(bool) & ~t[f"{v}_br"].fillna(False).astype(bool) for v in ("rent", "foreign", "age65", "under18")}
covs = t[["elevation", "tree_cover", "imperviousness", "lst_anom"]].notna().all(axis=1)
t["sample_model_A"] = t.rule4 & usable["rent"] & usable["foreign"] & usable["age65"] & usable["under18"] & covs
t.to_parquet(ROOT / "04_grid_join/analysis_table.parquet", index=False)

# exclusions, in the preregistered order (Q13)
rows = [("inhabited cells in the 11 cities (rule 1)", int(t.rule1.sum())),
        ("removed: population < 10 (rule 2)", int((t.rule1 & ~t.rule2).sum())),
        ("removed: >= 50% permanent water (rule 3)", int((t.rule2 & ~t.rule3).sum())),
        ("removed: < 70% of area with LST composite (rule 4)", int((t.rule3 & ~t.rule4).sum())),
        ("cells passing rules 1 to 4", int(t.rule4.sum()))]
for v in ("rent", "foreign", "age65", "under18"):
    rows.append((f"  of which {v} usable (present, not bracketed)", int((t.rule4 & usable[v]).sum())))
rows.append(("removed: a covariate missing", int((t.rule4 & ~covs).sum())))
rows.append(("Model A sample (rule 5: all four social variables usable)", int(t.sample_model_A.sum())))
ex = pd.DataFrame(rows, columns=["step", "cells"])
ex.to_csv(ROOT / "05_analysis/results/step6_exclusions.csv", index=False)
print(ex.to_string(index=False))
print("rows in table:", len(t), "| columns:", len(t.columns))
