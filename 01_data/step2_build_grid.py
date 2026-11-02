r"""Step 2: build the 100 m census cells of the 11 Ruhr cities and apply inclusion rules 1 to 3 (preregistration Q13).
Rule 1: cell centre inside one of the 11 kreisfreie Städte (VG250).
Rule 2: population >= 10 (Zensus 2022 population file; the only census value opened in this step).
Rule 3: less than 50% of the cell area is ESA WorldCover v200 class 80 (permanent water), area-weighted mean in Earth Engine.
Usage (from the project folder): .venv\Scripts\python.exe 01_data/step2_build_grid.py
Writes 01_data/processed/cells_step2.gpkg and 01_data/processed/step2_counts.csv. No temperature and no other census variable is read.
"""
import io, pathlib, sys, zipfile

import ee
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data" / "raw"
OUT = ROOT / "01_data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

# Official municipality keys (AGS) of the 11 independent cities of the RVR; names are checked against VG250 below
CITIES = {"05112000": "Duisburg", "05113000": "Essen", "05117000": "Mülheim an der Ruhr", "05119000": "Oberhausen",
          "05512000": "Bottrop", "05513000": "Gelsenkirchen", "05911000": "Bochum", "05913000": "Dortmund",
          "05914000": "Hagen", "05915000": "Hamm", "05916000": "Herne"}

# --- boundaries: VG250 municipalities, reprojected to the census CRS
vg = gpd.read_file(f"zip://{RAW / 'vg250/vg250_01-01.utm32s.gpkg.ebenen.zip'}!vg250_ebenen_0101/DE_VG250.gpkg", layer="vg250_gem")
vg = vg[vg["AGS"].isin(CITIES)]  # all parts of each municipality (land and water)
for ags, name in CITIES.items():
    got = sorted(set(vg.loc[vg["AGS"] == ags, "GEN"]))
    assert got and got[0].replace("a.d.", "an der").startswith(name.split()[0]), (ags, name, got)
cities = vg.dissolve(by="AGS")[["GEN", "geometry"]].to_crs(3035).reset_index()
print("cities:", len(cities), "| area km2:", round(cities.area.sum() / 1e6, 1))

# --- population file: ID, centre, inhabitants
zf = zipfile.ZipFile(RAW / "zensus2022/Zensus2022_Bevoelkerungszahl.zip")
pop = pd.read_csv(io.BytesIO(zf.read("Zensus2022_Bevoelkerungszahl_100m-Gitter.csv")), sep=";", dtype=str)
pop.columns = [c.lower() for c in pop.columns]
assert list(pop.columns) == ["gitter_id_100m", "x_mp_100m", "y_mp_100m", "einwohner"], list(pop.columns)
ll = pop["gitter_id_100m"].str.extract(r"^CRS3035RES100mN(\d+)E(\d+)$").astype(int)
pop["y_ll"], pop["x_ll"] = ll[0], ll[1]
pop["x_mp"], pop["y_mp"] = pop["x_mp_100m"].astype(int), pop["y_mp_100m"].astype(int)
bad = (pop["x_mp"] != pop["x_ll"] + 50) | (pop["y_mp"] != pop["y_ll"] + 50)
print("cells in Germany file:", len(pop), "| ID vs centre mismatches:", int(bad.sum()))
pop["einwohner_n"] = pd.to_numeric(pop["einwohner"].replace({"–": "0", "-": "0"}), errors="coerce")
print("population values not numeric:", int(pop["einwohner_n"].isna().sum()))

# --- rule 1: centre inside one of the 11 cities
xmin, ymin, xmax, ymax = cities.total_bounds
sub = pop[(pop.x_mp >= xmin) & (pop.x_mp <= xmax) & (pop.y_mp >= ymin) & (pop.y_mp <= ymax)].copy()
pts = gpd.GeoDataFrame(sub, geometry=gpd.points_from_xy(sub.x_mp, sub.y_mp), crs=3035)
j = gpd.sjoin(pts, cities[["AGS", "GEN", "geometry"]], predicate="within", how="inner")
cells = j.drop(columns=["geometry", "index_right"]).copy()
cells["city"] = cells["AGS"].map(CITIES)
cells["rule1"] = True
cells["rule2"] = cells["einwohner_n"] >= 10

# --- rule 3: share of permanent water (WorldCover class 80), only for cells passing rules 1 and 2
ee.Initialize(project="peppy-apparatus-452923-g2")
water = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").eq(80).rename("water")
proj = ee.Projection("EPSG:3035")
todo = cells[cells.rule2]
shares = {}
B = 2500
for i in range(0, len(todo), B):
    part = todo.iloc[i:i + B]
    feats = [ee.Feature(ee.Geometry.Rectangle([int(x), int(y), int(x) + 100, int(y) + 100], proj, False), {"id": gid})
             for gid, x, y in zip(part.gitter_id_100m, part.x_ll, part.y_ll)]
    res = water.reduceRegions(ee.FeatureCollection(feats), ee.Reducer.mean(), scale=10).getInfo()
    for f in res["features"]:
        shares[f["properties"]["id"]] = f["properties"].get("mean")
    print(f"  water share: {min(i + B, len(todo))} / {len(todo)}")
cells["water_share"] = cells["gitter_id_100m"].map(shares)
cells["rule3"] = cells["rule2"] & (cells["water_share"] < 0.5)
missing_w = int(cells.loc[cells.rule2, "water_share"].isna().sum())
print("cells passing rule 2 without a water value:", missing_w)

# --- outputs
geom = [box(x, y, x + 100, y + 100) for x, y in zip(cells.x_ll, cells.y_ll)]
g = gpd.GeoDataFrame(cells[["gitter_id_100m", "x_ll", "y_ll", "x_mp", "y_mp", "AGS", "city", "einwohner_n",
                            "water_share", "rule1", "rule2", "rule3"]], geometry=geom, crs=3035)
g.to_file(OUT / "cells_step2.gpkg", layer="cells", driver="GPKG")
cities.to_file(OUT / "cells_step2.gpkg", layer="cities", driver="GPKG")
counts = g.groupby("city").agg(rule1=("rule1", "sum"), rule2=("rule2", "sum"), rule3=("rule3", "sum"),
                               population_rule3=("einwohner_n", lambda s: int(s[g.loc[s.index, "rule3"]].sum())))
counts.loc["TOTAL"] = counts.sum()
counts.to_csv(OUT / "step2_counts.csv")
print(counts.to_string())
