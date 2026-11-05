r"""S17 (preregistration Q24): tree cover and imperviousness in a 300 m x 300 m window centred on each Model A cell
(the cell and its 8 neighbours), from the same rasters and no-data declaration as Step 6 (exactextract, exact shares).
Usage: .venv\Scripts\python.exe 04_grid_join/step8_window300.py  ->  04_grid_join/window300_covariates.csv
"""
import glob, pathlib, sys

import geopandas as gpd
import numpy as np
import pandas as pd
from exactextract import exact_extract
from shapely.geometry import box

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nodata_vrt import nodata_vrt

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw"
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
t = t[t.sample_model_A]
win = gpd.GeoDataFrame({"gitter_id_100m": t.gitter_id_100m.values},
                       geometry=[box(x - 150, y - 150, x + 150, y + 150) for x, y in zip(t.x_mp, t.y_mp)], crs=3035)
tcd = exact_extract(nodata_vrt(RAW / "copernicus/CLMS_HRLVLCC_TCD_R10m_2022_bbox.tif", 255, ROOT / "04_grid_join/tcd_nodata.vrt"),
                    win, ["mean"], include_cols=["gitter_id_100m"], output="pandas").rename(columns={"mean": "tree_cover_300"})
parts = []
for i, f in enumerate(sorted(glob.glob(str(RAW / "copernicus/*IMD*2021*.tif")))):
    p = exact_extract(nodata_vrt(f, 255, ROOT / f"04_grid_join/imd_nodata_{i}.vrt"), win, ["mean", "count"],
                      include_cols=["gitter_id_100m"], output="pandas")
    parts.append(p)
imd = pd.concat(parts).dropna(subset=["mean"])
imd = imd.groupby("gitter_id_100m").apply(lambda g: np.average(g["mean"], weights=g["count"]), include_groups=False).rename("imperviousness_300").reset_index()
out = tcd.merge(imd, on="gitter_id_100m", how="left")
out.to_csv(ROOT / "04_grid_join/window300_covariates.csv", index=False)
print(out.describe().round(2).to_string())
print("missing:", int(out.isna().any(axis=1).sum()))
