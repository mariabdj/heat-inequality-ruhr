# GATE 7: independent recomputation (R) of the population-weighted mean LST anomaly by group (zero group + city-specific
# deciles of non-zero values, ties sharing the lowest rank: decile = ceiling(rank_min / n * 10)).
# Same rule as 05_analysis/step7_descriptive.py, written separately. Also checks that no value appears in two groups
# within a city. Compares with 05_analysis/results/step7_decile_table.csv; tolerance 0.0001 C and exact cell counts.
# Usage: Rscript verification/verify_deciles.R
suppressMessages(library(arrow))
t <- as.data.frame(read_parquet("04_grid_join/analysis_table.parquet"))
t <- t[t$rule4, ]
py <- read.csv("05_analysis/results/step7_decile_table.csv", colClasses = c(group = "character"))
fail <- FALSE
for (v in c("rent", "foreign", "age65", "under18")) {
  ok <- !is.na(t[[v]]) & !(t[[paste0(v, "_br")]] %in% TRUE)
  d <- t[ok, c("gitter_id_100m", "city", v, "einwohner_n", "lst_anom")]
  d$group <- "zero"
  nz <- d[[v]] > 0
  for (cty in unique(d$city)) {
    i <- which(nz & d$city == cty)
    r <- rank(d[[v]][i], ties.method = "min")
    d$group[i] <- sprintf("%02d", pmin(pmax(ceiling(r / length(i) * 10), 1), 10))
  }
  split_ties <- sum(tapply(d$group, paste(d$city, d[[v]]), function(g) length(unique(g)) > 1))
  for (g in sort(unique(d$group))) {
    x <- d[d$group == g, ]
    r_mean <- sum(x$lst_anom * x$einwohner_n) / sum(x$einwohner_n)
    p <- py[py$variable == v & py$group == g, ]
    diff <- abs(r_mean - p$pw_mean_lst_anom)
    if (nrow(p) != 1 || diff > 1e-4 || p$cells != nrow(x)) { fail <- TRUE; cat("  mismatch", v, g, "\n") }
  }
  cat(sprintf("%s: n %d, groups %d, values split across groups within a city: %d\n", v, nrow(d), length(unique(d$group)), split_ties))
  if (split_ties > 0) fail <- TRUE
}
cat(if (fail) "RESULT: FAILED\n" else "RESULT: PASSED\n")
if (fail) quit(status = 1)
