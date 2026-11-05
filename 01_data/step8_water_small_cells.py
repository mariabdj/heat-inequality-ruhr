r"""S11 (preregistration Q24) needs rule 3 (less than 50% permanent water) for cells with 3 to 9 inhabitants, which
Step 2 computed only for cells with at least 10. Same calculation as 01_data/step2_build_grid.py: ESA WorldCover v200,
class 80, area-weighted mean over the 100 m cell in EPSG:3035 at 10 m (Earth Engine reduceRegions), for every
inhabited cell of the 11 cities with fewer than 10 inhabitants.
Usage: .venv\Scripts\python.exe 01_data/step8_water_small_cells.py  ->  01_data/processed/water_share_small_cells.csv
"""
import pathlib, sys

import ee
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
todo = t[t.rule1 & ~t.rule2][["gitter_id_100m", "x_mp", "y_mp"]].reset_index(drop=True)
todo["x_ll"], todo["y_ll"] = todo.x_mp - 50, todo.y_mp - 50
ee.Initialize(project="peppy-apparatus-452923-g2")
water = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").eq(80).rename("water")
proj = ee.Projection("EPSG:3035")
shares, B = {}, 2500
for i in range(0, len(todo), B):
    part = todo.iloc[i:i + B]
    feats = [ee.Feature(ee.Geometry.Rectangle([int(x), int(y), int(x) + 100, int(y) + 100], proj, False), {"id": gid})
             for gid, x, y in zip(part.gitter_id_100m, part.x_ll, part.y_ll)]
    res = water.reduceRegions(ee.FeatureCollection(feats), ee.Reducer.mean(), scale=10).getInfo()
    for f in res["features"]:
        shares[f["properties"]["id"]] = f["properties"].get("mean")
    print(f"  water share: {min(i + B, len(todo))} / {len(todo)}", flush=True)
todo["water_share"] = todo.gitter_id_100m.map(shares)
todo[["gitter_id_100m", "water_share"]].to_csv(ROOT / "01_data/processed/water_share_small_cells.csv", index=False)
print("cells:", len(todo), "| without a value:", int(todo.water_share.isna().sum()), "| >= 50% water:", int((todo.water_share >= 0.5).sum()))
