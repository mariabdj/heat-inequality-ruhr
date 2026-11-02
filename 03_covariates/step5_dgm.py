r"""Step 5: bare-earth elevation (Geobasis NRW digital terrain model, WCS NW DGM), requested at 10 m (preregistration Q5.4).
Tiles of 10 km over the bounding box of the 11 cities (+500 m), native CRS EPSG:25832; resampling from 1 m to 10 m is
done by the service. Mosaic written to 01_data/raw/geobasis_nrw/dgm_nrw_10m.tif and registered in 01_data/data_register.csv.
Usage: .venv\Scripts\python.exe 03_covariates/step5_dgm.py
"""
import csv, datetime, hashlib, io, pathlib, ssl, urllib.request

import certifi
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.merge import merge

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "01_data/raw/geobasis_nrw"; OUT.mkdir(parents=True, exist_ok=True)
CTX = ssl.create_default_context(cafile=certifi.where())
URL = "https://www.wcs.nrw.de/geobasis/wcs_nw_dgm"

cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(25832)
x0, y0, x1, y1 = cities.total_bounds
x0, y0 = np.floor((x0 - 500) / 10000) * 10000, np.floor((y0 - 500) / 10000) * 10000
x1, y1 = np.ceil((x1 + 500) / 10000) * 10000, np.ceil((y1 + 500) / 10000) * 10000
tiles = []
for x in np.arange(x0, x1, 10000):
    for y in np.arange(y0, y1, 10000):
        q = (f"{URL}?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=nw_dgm&FORMAT=image/tiff"
             f"&SUBSET=x({int(x)},{int(x + 10000)})&SUBSET=y({int(y)},{int(y + 10000)})&SCALESIZE=x(1000),y(1000)")
        data = urllib.request.urlopen(urllib.request.Request(q, headers={"User-Agent": "research download"}), timeout=300, context=CTX).read()
        tiles.append(rasterio.open(io.BytesIO(data)))
print("tiles:", len(tiles), "| first tile:", tiles[0].crs, tiles[0].res, tiles[0].dtypes[0], "nodata", tiles[0].nodata)
mosaic, transform = merge(tiles)
prof = tiles[0].profile.copy()
prof.update(height=mosaic.shape[1], width=mosaic.shape[2], transform=transform, compress="deflate", driver="GTiff")
dest = OUT / "dgm_nrw_10m.tif"
with rasterio.open(dest, "w", **prof) as dst:
    dst.write(mosaic)
v = mosaic[0][np.isfinite(mosaic[0]) & (mosaic[0] > -100)]
print(f"mosaic {mosaic.shape}; elevation range {v.min():.1f} to {v.max():.1f} m")

reg = ROOT / "01_data/data_register.csv"
rows = list(csv.DictReader(open(reg, encoding="utf-8")))
rows = [r for r in rows if r["file"] != "geobasis_nrw/dgm_nrw_10m.tif"]
rows.append({"file": "geobasis_nrw/dgm_nrw_10m.tif", "dataset": "Geobasis NRW digital terrain model (DGM), WCS NW DGM, 10 m",
             "provider": "Bezirksregierung Köln, Geobasis NRW", "url": URL + " (GetCoverage nw_dgm, 10 km tiles, SCALESIZE 1000 x 1000)",
             "download_date": datetime.date.today().isoformat(), "version": "service state at download", "licence": "Datenlizenz Deutschland Zero 2.0",
             "attribution": "Geobasis NRW (dl-de/zero-2-0)", "size_bytes": dest.stat().st_size,
             "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(), "note": "mosaic written by 03_covariates/step5_dgm.py; 1 m to 10 m resampling by the service"})
w = csv.DictWriter(open(reg, "w", newline="", encoding="utf-8"), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
