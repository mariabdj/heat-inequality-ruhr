# GATE 8: independent R recomputation of the MGWR of Step 8b (05_analysis/step8_mgwr.py) with GWmodel.
# Tolerance fixed in VERIFICATION_LOG.md (Step 8b decision record) before the comparison: for each covariate, the
# bandwidth within 10% of the mgwr bandwidth (or both at the global maximum), and the Pearson correlation of the local
# coefficients at least 0.95. Same 1 km table (05_analysis/results/step8_1km_aggregate.csv), same z-standardisation.
# Usage: Rscript verification/verify_mgwr.R
suppressMessages({library(GWmodel); library(sp); library(jsonlite)})
a <- read.csv("05_analysis/results/step8_1km_aggregate.csv")
xv <- c("rent", "foreign10", "age65_10", "under18_10", "elevation", "ln_pop", "tree_cover", "imperviousness")
z <- function(v) (v - mean(v)) / sd(v) * sqrt(length(v) / (length(v) - 1))   # numpy std (divisor n), as in Python
d <- data.frame(lst_anom = z(a$lst_anom), sapply(a[, xv], z))
coordinates(d) <- as.matrix(a[, c("x_mp", "y_mp")])
f <- as.formula(paste("lst_anom ~", paste(xv, collapse = " + ")))
m <- gwr.multiscale(f, data = d, kernel = "bisquare", adaptive = TRUE, criterion = "dCVR", approach = "AIC",
                    predictor.centered = rep(FALSE, length(xv)), hatmatrix = FALSE, verbose = FALSE)
bwR <- m$GW.arguments$bws
py <- fromJSON(gsub("\\bNaN\\b", "null", paste(readLines("05_analysis/results/results.json", warn = FALSE), collapse = "\n")))$step8_mgwr
loc <- read.csv("05_analysis/results/step8_mgwr_local.csv")
nm <- c("intercept", xv); n <- nrow(a); fail <- FALSE
cf <- as.data.frame(m$SDF)[, c("Intercept", xv)]
for (j in seq_along(nm)) {
  bp <- py$bandwidths[[nm[j]]]; br <- bwR[j]
  ok_bw <- abs(br - bp) <= 0.1 * bp || (br >= n - 1 && bp >= n - 1)
  r <- suppressWarnings(cor(cf[[j]], loc[[nm[j]]]))
  if (is.na(r)) r <- if (sd(cf[[j]]) < 1e-8 && sd(loc[[nm[j]]]) < 1e-8) 1 else 0       # both constant (global)
  cat(sprintf("%-15s bandwidth mgwr %6.0f  GWmodel %6.0f  %s | correlation of local coefficients %.3f\n",
              nm[j], bp, br, if (ok_bw) "ok" else "DIFFERENT", r))
  if (!ok_bw || r < 0.95) fail <- TRUE
}
cat(if (fail) "RESULT: FAILED\n" else "RESULT: PASSED\n")
if (fail) quit(status = 1)
