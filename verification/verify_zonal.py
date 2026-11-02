r"""GATE 6: two independent zonal-statistics implementations agree, and the table is complete.
- Python exactextract (04_grid_join/step6_join.py) vs R exactextractr (verification/verify_zonal.R, cells rebuilt from IDs):
  LST anomaly within 0.01 C; tree cover, imperviousness and LST coverage share within 0.1 percentage point; elevation within 0.01 m.
- rasterstats (pixel-centre rule, a different method) on the LST anomaly: difference reported, not a pass/fail criterion.
- Row count = inhabited cells (rule 1); exclusions table adds up.
Usage: .venv\Scripts\python.exe verification/verify_zonal.py
"""
import pathlib, sys

import geopandas as gpd
import numpy as np
import pandas as pd
from rasterstats import zonal_stats

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
r = pd.read_csv(ROOT / "04_grid_join/zonal_R.csv")
m = t.merge(r, on="gitter_id_100m", how="outer", indicator=True)
errors = []
if (m["_merge"] != "both").any():
    errors.append("cell lists differ between Python and R")

CHECKS = [("lst_anom", 0.01), ("lst_cover_share", 0.001), ("tree_cover", 0.1), ("imperviousness", 0.1), ("elevation", 0.01)]
for col, tol in CHECKS:
    a, b = m[col], m[f"{col}_R"]
    both = a.notna() & b.notna()
    d = (a[both] - b[both]).abs()
    pres = int((a.isna() != b.isna()).sum())
    print(f"{col}: compared {int(both.sum())}, max |diff| {d.max():.6f} (tolerance {tol}), cells above tolerance {int((d > tol).sum())}, presence differs {pres}")
    if (d > tol).any() or pres:
        errors.append(f"{col} differs")

# a different method, for information: pixel-centre mean of the LST composite in the cells passing rule 4
cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")
cells = cells[cells.gitter_id_100m.isin(t.loc[t.rule4, "gitter_id_100m"])].to_crs(32632)
zs = zonal_stats(list(cells.geometry), str(ROOT / "02_lst/exports/lst_anomaly_hot.tif"), stats=["mean"], band=1, nodata=np.nan)
rs = pd.Series([z["mean"] for z in zs], index=cells.gitter_id_100m.values)
ex = t.set_index("gitter_id_100m").loc[rs.index, "lst_anom"]
d = (rs - ex).abs()
print(f"rasterstats (pixel centres) vs exactextract (exact shares), cells passing rule 4: mean |diff| {d.mean():.3f} C, "
      f"90th percentile {d.quantile(.9):.3f} C, max {d.max():.3f} C")

ex_tab = pd.read_csv(ROOT / "05_analysis/results/step6_exclusions.csv").set_index("step")["cells"]
if len(t) != int(t.rule1.sum()) or len(t) != ex_tab.iloc[0]:
    errors.append("row count is not the number of inhabited cells")
if ex_tab.iloc[0] - ex_tab.iloc[1] - ex_tab.iloc[2] - ex_tab.iloc[3] != ex_tab.iloc[4]:
    errors.append("exclusions do not add up")
print(f"rows: {len(t)}; passing rules 1 to 4: {int(t.rule4.sum())}; Model A sample: {int(t.sample_model_A.sum())}")
for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
