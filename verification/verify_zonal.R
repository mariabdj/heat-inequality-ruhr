# Independent second implementation of the Step 6 zonal statistics (R: sf, terra, exactextractr).
# Builds the 100 m cells from their IDs (not from the Python file), reprojects them to each raster CRS,
# and computes coverage-weighted means. Writes 04_grid_join/zonal_R.csv.
# Usage: Rscript verification/verify_zonal.R
suppressMessages({library(sf); library(terra); library(exactextractr)})
ids <- read.csv("01_data/processed/census_step3.csv")$gitter_id_100m
ll <- regmatches(ids, regexec("N(\\d+)E(\\d+)$", ids))
y0 <- as.numeric(sapply(ll, `[`, 2)); x0 <- as.numeric(sapply(ll, `[`, 3))
polys <- st_sfc(lapply(seq_along(ids), function(i) st_polygon(list(matrix(
  c(x0[i], y0[i], x0[i] + 100, y0[i], x0[i] + 100, y0[i] + 100, x0[i], y0[i] + 100, x0[i], y0[i]), ncol = 2, byrow = TRUE)))), crs = 3035)
cells <- st_sf(gitter_id_100m = ids, geometry = polys)

lst <- rast("02_lst/exports/lst_anomaly_hot.tif")[[1]]
c32 <- st_transform(cells, 32632)
lst_mean <- exact_extract(lst, c32, "mean", progress = FALSE)
lst_cnt <- exact_extract(lst, c32, "count", progress = FALSE)
lst_cover <- lst_cnt * 900 / as.numeric(st_area(c32))

tcd <- rast("01_data/raw/copernicus/CLMS_HRLVLCC_TCD_R10m_2022_bbox.tif"); NAflag(tcd) <- 255
tree <- exact_extract(tcd, cells, "mean", progress = FALSE)

imd_files <- Sys.glob("01_data/raw/copernicus/*IMD*2021*.tif")
imd <- do.call(merge, lapply(imd_files, function(f) { r <- rast(f); NAflag(r) <- 255; r }))
imp <- exact_extract(imd, cells, "mean", progress = FALSE)

dgm <- rast("01_data/raw/geobasis_nrw/dgm_nrw_10m.tif")
elev <- exact_extract(dgm, st_transform(cells, 25832), "mean", progress = FALSE)

write.csv(data.frame(gitter_id_100m = ids, lst_anom_R = lst_mean, lst_cover_share_R = lst_cover,
                     tree_cover_R = tree, imperviousness_R = imp, elevation_R = elev),
          "04_grid_join/zonal_R.csv", row.names = FALSE)
cat("cells:", length(ids), "\n")
