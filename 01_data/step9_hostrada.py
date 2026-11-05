r"""Step 9, deviation D17 (exploratory): air temperature from DWD HOSTRADA v1.0 (hourly, 1 km, EPSG:3034).
1. Downloads the monthly 2 m air temperature files that hold the 16 hot-day scene dates and the following nights,
   and registers each file (01_data/data_register.csv).
2. Day value per date: mean of the 10:00 and 11:00 UTC fields; night value: mean of the 01:00 and 02:00 UTC fields of
   the next calendar day. Bands are chosen by their time value, not by position.
3. Anomaly: field minus the median of the HOSTRADA cells whose centre lies inside the 11 cities; composite = mean of
   the 16 anomalies (day and night separately).
4. Each 100 m census cell takes the value of the HOSTRADA cell containing its centre (EPSG:3035 -> EPSG:3034).
Usage: .venv\Scripts\python.exe 01_data/step9_hostrada.py  ->  01_data/processed/air_temperature_cells.csv
"""
import csv, datetime, hashlib, json, pathlib, ssl, sys, urllib.request

import certifi
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from rasterio.features import geometry_mask

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data/raw/dwd/hostrada"; RAW.mkdir(parents=True, exist_ok=True)
REG = ROOT / "01_data/data_register.csv"
BASE = "https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/hostrada/air_temperature_mean/"
EPOCH = datetime.datetime(1949, 12, 1)
sys.stdout.reconfigure(encoding="utf-8")

dates = pd.to_datetime(pd.read_csv(ROOT / "02_lst/scenes_used_hot.csv").date).dt.date.tolist()
months = sorted({(d.year, d.month) for d in dates} | {((d + datetime.timedelta(days=1)).year, (d + datetime.timedelta(days=1)).month) for d in dates})


def fname(y, m):
    last = (datetime.date(y + (m == 12), m % 12 + 1, 1) - datetime.timedelta(days=1)).day
    return f"tas_1hr_HOSTRADA-v1-0_BE_gn_{y}{m:02d}0100-{y}{m:02d}{last}23.nc"


rows = list(csv.DictReader(open(REG, encoding="utf-8")))
have = {r["file"] for r in rows}
for y, m in months:
    f = RAW / fname(y, m)
    if not f.is_file():
        req = urllib.request.Request(BASE + f.name, headers={"User-Agent": "research download"})
        with urllib.request.urlopen(req, timeout=1800, context=ssl.create_default_context(cafile=certifi.where())) as r, open(f, "wb") as o:
            while chunk := r.read(1 << 20):
                o.write(chunk)
        print("downloaded", f.name, f.stat().st_size, flush=True)
    rel = f"dwd/hostrada/{f.name}"
    if rel not in have:
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rows.append({"file": rel, "dataset": "DWD HOSTRADA v1.0 hourly 2 m air temperature (tas), 1 km, EPSG:3034", "provider": "Deutscher Wetterdienst (DWD)",
                     "url": BASE + f.name, "download_date": datetime.date.today().isoformat(), "version": "HOSTRADA v1.0 (dataset description 2024-03-15)",
                     "licence": "GeoNutzV", "attribution": "Deutscher Wetterdienst (DWD), HOSTRADA v1.0", "size_bytes": f.stat().st_size, "sha256": h,
                     "note": "exploratory, deviation D17"})
        have.add(rel)
desc = "dwd/hostrada/DESCRIPTION_gridsgermany_hourly_hostrada_en.pdf"
if desc not in have and (RAW.parent.parent / desc).is_file():
    p = RAW.parent.parent / desc
    rows.append({**rows[-1], "file": desc, "dataset": "HOSTRADA dataset description (English)", "url": BASE.replace("air_temperature_mean/", "") + p.name,
                 "size_bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "note": "documentation, deviation D17"})
with open(REG, "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# city mask on the HOSTRADA grid (cell centre inside the union of the 11 cities)
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(3034)
first = RAW / fname(*months[0])
with rasterio.open(f'netCDF:"{first}":tas') as s:
    transform, shape = s.transform, s.shape
inside = ~geometry_mask(cities.geometry, out_shape=shape, transform=transform, all_touched=False)
print("HOSTRADA cells with centre inside the 11 cities:", int(inside.sum()))


def field(f, when):
    with rasterio.open(f'netCDF:"{f}":tas') as s:
        tv = np.array([float(x) for x in s.tags()["NETCDF_DIM_time_VALUES"].strip("{}").split(",")])
        target = (when - EPOCH).total_seconds() / 86400
        k = int(np.argmin(np.abs(tv - target)))
        assert abs(tv[k] - target) < 1e-6, (f.name, when)
        a = s.read(k + 1).astype(float)
        a[a == s.nodata] = np.nan
        return a * 0.1


day, night, log = [], [], []
for d in dates:
    dd = datetime.datetime(d.year, d.month, d.day); nx = dd + datetime.timedelta(days=1)
    fd = np.mean([field(RAW / fname(d.year, d.month), dd + datetime.timedelta(hours=h)) for h in (10, 11)], axis=0)
    fn = np.mean([field(RAW / fname(nx.year, nx.month), nx + datetime.timedelta(hours=h)) for h in (1, 2)], axis=0)
    md, mn = np.nanmedian(fd[inside]), np.nanmedian(fn[inside])
    day.append(fd - md); night.append(fn - mn)
    log.append({"date": str(d), "median_day_C": md, "median_night_C": mn})
    print(f"{d}: city median air temperature day {md:.1f} C, night {mn:.1f} C", flush=True)
day, night = np.nanmean(day, axis=0), np.nanmean(night, axis=0)

cells = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet", columns=["gitter_id_100m", "x_mp", "y_mp"])
x, y = Transformer.from_crs(3035, 3034, always_xy=True).transform(cells.x_mp.values, cells.y_mp.values)
rr, cc = rasterio.transform.rowcol(transform, x, y)
rr, cc = np.asarray(rr), np.asarray(cc)
okk = (rr >= 0) & (rr < shape[0]) & (cc >= 0) & (cc < shape[1])
cells["air_day"] = np.where(okk, day[rr.clip(0, shape[0] - 1), cc.clip(0, shape[1] - 1)], np.nan)
cells["air_night"] = np.where(okk, night[rr.clip(0, shape[0] - 1), cc.clip(0, shape[1] - 1)], np.nan)
cells[["gitter_id_100m", "air_day", "air_night"]].to_csv(ROOT / "01_data/processed/air_temperature_cells.csv", index=False)
pd.DataFrame(log).to_csv(ROOT / "01_data/processed/air_temperature_days.csv", index=False)
print("cells with a value:", int(cells.air_day.notna().sum()), "of", len(cells),
      "| day anomaly range", np.nanmin(cells.air_day).round(2), np.nanmax(cells.air_day).round(2),
      "| night anomaly range", np.nanmin(cells.air_night).round(2), np.nanmax(cells.air_night).round(2))
