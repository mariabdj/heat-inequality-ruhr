# Independent second reader of the census values (R package z22, data from the z22data repository).
# Writes 01_data/processed/census_z22.csv for the study-area cells; compared with the Python reader by verify_census_parse.py.
# Usage: Rscript verification/z22_read.R
suppressMessages(library(z22))
ids <- read.csv("01_data/processed/census_step3.csv")$gitter_id_100m
feats <- c(rent = "rent_avg", foreign = "foreigners", age65 = "age_from_65", under18 = "age_under_18")
out <- data.frame(gitter_id_100m = ids)
for (v in names(feats)) {
  d <- z22_data(feats[[v]], year = 2022, res = "100m", as = "df")
  # z22 returns the value (cat_0) and the cell centre (x, y), no ID and no uncertainty flag: rebuild the ID from the centre
  d <- data.frame(gitter_id_100m = sprintf("CRS3035RES100mN%dE%d", d$y - 50L, d$x - 50L), value = d$cat_0)
  d <- d[d$gitter_id_100m %in% ids, ]
  names(d) <- c("gitter_id_100m", paste0(v, "_z22"))
  out <- merge(out, d, by = "gitter_id_100m", all.x = TRUE)
  cat(v, ": z22 rows in study area", nrow(d), "\n")
}
write.csv(out, "01_data/processed/census_z22.csv", row.names = FALSE)
