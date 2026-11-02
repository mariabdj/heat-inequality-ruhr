r"""Step 4 checks by eye: map of the LST anomaly composite, map of valid observations, and comparison with the
LANUK Klimaanalyse NRW 2026 day map (modelled, typical summer day), averaged onto our 30 m grid.
Usage: .venv\Scripts\python.exe 02_lst/lst_maps.py  ->  05_analysis/results/figures/step4_*.png, step4_lanuk_check.csv
"""
import pathlib, sys, zipfile

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import Resampling, reproject

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "05_analysis/results/figures"
sys.stdout.reconfigure(encoding="utf-8")
src = rasterio.open(ROOT / "02_lst/exports/lst_anomaly_hot.tif")
anom, nobs = src.read(1), src.read(2)
core = rasterio.open(ROOT / "02_lst/exports/core_ref_domain.tif").read(1) == 1
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(32632)
ext = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

fig, ax = plt.subplots(1, 2, figsize=(15, 5))
a = ax[0].imshow(np.where(core, anom, np.nan), extent=ext, cmap="RdYlBu_r", vmin=-8, vmax=8)
cities.boundary.plot(ax=ax[0], color="k", linewidth=0.4); fig.colorbar(a, ax=ax[0], label="LST anomaly (°C), mean of 16 hot-day scenes")
ax[0].set_title("Land surface temperature anomaly (core reference domain)")
b = ax[1].imshow(np.where(nobs > 0, nobs, np.nan), extent=ext, cmap="viridis")
cities.boundary.plot(ax=ax[1], color="w", linewidth=0.4); fig.colorbar(b, ax=ax[1], label="valid observations")
ax[1].set_title("Valid hot-day observations per 30 m pixel")
for x in ax: x.set_axis_off()
fig.tight_layout(); fig.savefig(FIG / "step4_lst_and_obs.png", dpi=150)

# LANUK day map (EPSG:25832), averaged onto our 30 m grid
z = ROOT / "01_data/raw/lanuk/Klimaanalyse-Karte-Tag_2026_EPSG25832_TIFF.zip"
with rasterio.open(f"zip://{z}!PL_KY_TAG_TYP.tif") as l:
    print("LANUK raster:", l.crs, l.res, l.dtypes[0], "nodata", l.nodata, "| first value counts:",
          np.unique(l.read(1, window=((20000, 20200), (20000, 20200))), return_counts=True))
    lan = np.full(anom.shape, np.nan, dtype="float32")
    reproject(rasterio.band(l, 1), lan, dst_transform=src.transform, dst_crs=src.crs, resampling=Resampling.average,
              src_nodata=l.nodata, dst_nodata=np.nan)
ok = core & np.isfinite(anom) & np.isfinite(lan)
rho = pd.Series(anom[ok]).corr(pd.Series(lan[ok]), method="spearman")
print(f"pixels compared: {int(ok.sum())}; Spearman correlation LST anomaly vs LANUK day map: {rho:.3f}")
pd.DataFrame({"pixels": [int(ok.sum())], "spearman": [rho]}).to_csv(ROOT / "05_analysis/results/step4_lanuk_check.csv", index=False)
fig, ax = plt.subplots(1, 2, figsize=(15, 5))
ax[0].imshow(np.where(core, anom, np.nan), extent=ext, cmap="RdYlBu_r", vmin=-8, vmax=8); ax[0].set_title("Our LST anomaly (Landsat, observed)")
ax[1].imshow(np.where(core, lan, np.nan), extent=ext, cmap="RdYlBu_r"); ax[1].set_title("LANUK Klimaanalyse 2026, day map (modelled)")
for x in ax:
    cities.boundary.plot(ax=x, color="k", linewidth=0.4); x.set_axis_off()
fig.tight_layout(); fig.savefig(FIG / "step4_lanuk_comparison.png", dpi=150)
