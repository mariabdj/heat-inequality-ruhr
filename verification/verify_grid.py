r"""GATE 2: the self-built 100 m cells match the official BKG GeoGitter, cities are assigned consistently,
and the counts file agrees with the cell file.
Checks:
1. every included cell exists in the BKG 100 m grid with the same lower-left corner and centre (tolerance 0.01 m);
2. city assignment: our VG250 (2026) city vs the BKG municipality key (VG25, 2019); disagreements listed, must be < 1%;
3. study-area size: BKG cells whose centre lies in the 11 cities, times 1 ha, vs the VG250 area (must agree within 1%);
4. step2_counts.csv equals a recount from cells_step2.gpkg, and rule 3 <= rule 2 <= rule 1 in every city.
Usage: .venv\Scripts\python.exe verification/verify_grid.py
"""
import io, pathlib, re, sys, zipfile

import geopandas as gpd
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
errors = []

cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities")

zf = zipfile.ZipFile(ROOT / "01_data/raw/bkg_grid/DE_Grid_ETRS89-LAEA_100m.csv.zip")
names = [n for n in zf.namelist() if re.search(r"100kmN3[12]E4[01]_DE_Grid", n)]
cols = ["id", "x_sw", "y_sw", "x_mp", "y_mp", "f_staat", "f_land", "f_wasser", "p_staat", "p_land", "p_wasser", "ags"]
bkg = pd.concat([pd.read_csv(io.BytesIO(zf.read(n)), sep=";", header=None, names=cols, dtype={"ags": str}) for n in names])

# 1. geometry
cells["bkg_id"] = "100mN" + (cells.y_ll // 100).astype(str) + "E" + (cells.x_ll // 100).astype(str)
m = cells.merge(bkg, left_on="bkg_id", right_on="id", how="left")
not_found = int(m["id"].isna().sum())
dx = (m.x_ll - m.x_sw).abs().max(); dy = (m.y_ll - m.y_sw).abs().max()
dmx = (m.x_mp_x - m.x_mp_y).abs().max(); dmy = (m.y_mp_x - m.y_mp_y).abs().max()
print(f"1. cells checked: {len(m)}; not in BKG grid: {not_found}; max corner diff: {dx}, {dy} m; max centre diff: {dmx}, {dmy} m")
if not_found or max(dx, dy, dmx, dmy) > 0.01:
    errors.append("geometry differs from the BKG grid")

# 2. city assignment
mis = m[m["ags"] != m["AGS"]]
share = len(mis) / len(m)
print(f"2. city differs from BKG municipality key: {len(mis)} cells ({share:.2%}); by our city: {mis.city.value_counts().to_dict()}")
if share >= 0.01:
    errors.append(f"city assignment differs for {share:.2%} of cells")

# 3. study-area size
inside = gpd.sjoin(gpd.GeoDataFrame(bkg, geometry=gpd.points_from_xy(bkg.x_mp, bkg.y_mp), crs=3035),
                   cities[["geometry"]], predicate="within")
a_cells = len(inside) * 0.01
a_poly = cities.area.sum() / 1e6
print(f"3. BKG cells with centre in the 11 cities: {len(inside)} -> {a_cells:.1f} km2; VG250 area: {a_poly:.1f} km2; diff {abs(a_cells - a_poly) / a_poly:.3%}")
if abs(a_cells - a_poly) / a_poly > 0.01:
    errors.append("study-area size mismatch")

# 4. counts
c = pd.read_csv(ROOT / "01_data/processed/step2_counts.csv", index_col=0)
re_ = cells.groupby("city")[["rule1", "rule2", "rule3"]].sum()
for city, r in re_.iterrows():
    if list(c.loc[city, ["rule1", "rule2", "rule3"]]) != list(r):
        errors.append(f"counts differ for {city}")
    if not (r.rule3 <= r.rule2 <= r.rule1):
        errors.append(f"rule order broken for {city}")
print(f"4. counts recomputed for {len(re_)} cities; total rule 3 cells: {int(re_.rule3.sum())}")

for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
