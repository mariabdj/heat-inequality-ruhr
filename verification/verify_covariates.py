r"""GATE 5: every covariate layer covers the study cells.
For each layer (tree cover 2022, imperviousness 2021, NRW terrain model): the value at the centre of every cell
passing rules 1 to 3 is read (cell centres reprojected to the layer CRS as points; the raster itself is never
resampled) and must be valid (not nodata, inside the documented value range). Cells failing are listed by city.
Usage: .venv\Scripts\python.exe verification/verify_covariates.py
"""
import glob, pathlib, sys

import geopandas as gpd
import numpy as np
import rasterio

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw"
sys.stdout.reconfigure(encoding="utf-8")
cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")
cells = cells[cells.rule3]
pts = gpd.GeoSeries(gpd.points_from_xy(cells.x_mp, cells.y_mp), crs=3035)

LAYERS = {  # name: (path pattern, valid range)
    "tree_cover_2022": ("copernicus/*TCD*2022*.tif", (0, 100)),
    "imperviousness_2021": ("copernicus/*IMD*2021*.tif", (0, 100)),
    "elevation_dgm": ("geobasis_nrw/dgm_nrw_10m.tif", (-50, 700)),
}
errors = []
for name, (pat, (lo, hi)) in LAYERS.items():
    files = sorted(glob.glob(str(RAW / pat)))
    if not files:
        errors.append(f"{name}: no file matching {pat}")
        continue
    vals = np.full(len(cells), np.nan)
    for f in files:
        with rasterio.open(f) as src:
            p = pts.to_crs(src.crs)
            v = np.array([x[0] for x in src.sample(zip(p.x, p.y), masked=True)], dtype=object)
            got = np.array([float(x) if x is not np.ma.masked else np.nan for x in v])
            inside = (p.x >= src.bounds.left) & (p.x <= src.bounds.right) & (p.y >= src.bounds.bottom) & (p.y <= src.bounds.top)
            ok = inside.values & np.isfinite(got)
            if src.nodata is not None:
                ok &= got != src.nodata
            vals = np.where(np.isnan(vals) & ok, got, vals)
    bad = ~np.isfinite(vals) | (vals < lo) | (vals > hi)
    print(f"{name}: files {len(files)}; cells {len(cells)}; missing or out of range {int(bad.sum())}; "
          f"range {np.nanmin(vals):.1f} to {np.nanmax(vals):.1f}")
    if bad.any():
        print("   by city:", cells.loc[bad, "city"].value_counts().to_dict())
        errors.append(f"{name}: {int(bad.sum())} cells without a valid value")
for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
