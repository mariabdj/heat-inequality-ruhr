# GATE 8: independent R re-estimation of the Step 8a models (05_analysis/step8_primary.py).
# Tolerances fixed in VERIFICATION_LOG.md before the comparisons (Step 8 decision record; SE and step-2b lambda added in the Gate 8 round 1 decision record):
#   OLS |diff| <= 1e-8; spatial error GMM (by hand) each beta within 0.01 SE of spreg, SE within 0.5% (relative), step-2b lambda within 0.001;
#   bootstrap replicates recomputed from the saved block draws |diff| <= 1e-8.
# The sample, variables, city dummies and neighbours are rebuilt here, not read from the Python script.
# Usage: Rscript verification/verify_models.R
suppressMessages({library(arrow); library(spdep); library(spatialreg); library(Matrix); library(sphet); library(jsonlite)})
t <- as.data.frame(read_parquet("04_grid_join/analysis_table.parquet"))
t <- t[order(t$gitter_id_100m), ]
res <- fromJSON("05_analysis/results/results.json", simplifyVector = FALSE)$step8a
A <- t[t$sample_model_A, ]
A$foreign10 <- A$foreign / 10; A$age65_10 <- A$age65 / 10; A$under18_10 <- A$under18 / 10; A$ln_pop <- log(A$einwohner_n)
A$city <- factor(A$city, levels = sort(unique(t$city)))          # first level (Bochum) = reference
fail <- FALSE
cat("n Model A:", nrow(A), "(Python", res$n_model_A, ")\n")
if (nrow(A) != res$n_model_A) fail <- TRUE

fA <- lst_anom ~ rent + foreign10 + age65_10 + under18_10 + elevation + ln_pop + city
fB <- lst_anom ~ rent + foreign10 + age65_10 + under18_10 + elevation + ln_pop + tree_cover + imperviousness + city
soc <- c("rent", "foreign10", "age65_10", "under18_10")

# OLS
for (m in c("A", "B")) {
  b <- coef(lm(if (m == "A") fA else fB, data = A))
  py <- unlist(res$ols[[m]]$betas)
  d <- max(abs(b[c("(Intercept)", soc)] - py[c("const", soc)]))
  cat(sprintf("OLS %s: max |diff| over intercept and social betas %.2e\n", m, d))
  if (d > 1e-8) fail <- TRUE
}

# neighbours: queen on the 100 m grid = centres <= 142 m apart
nb <- dnearneigh(as.matrix(A[, c("x_mp", "y_mp")]), 0, 142)
lw <- nb2listw(nb, style = "W", zero.policy = TRUE)
Wm <- as(lw, "CsparseMatrix")       # sphet cannot convert a listw with empty rows (islands); the sparse matrix works
isl <- sum(card(nb) == 0)
cat("islands:", isl, "(Python", res$W_model_A$islands, ")\n")
if (isl != res$W_model_A$islands) fail <- TRUE

# spatial error model, GMM: the published two-step procedure written out by hand (the gate check).
# Step 1: OLS residuals u; lambda minimises the squared moment conditions n^-1 e'A1 e and n^-1 e'W e, e = u - lambda Wu,
#   with A1 = W'W - diag(W'W) (heteroskedastic, Arraiz et al. 2010) or
#   A1 = v [W'W - n^-1 tr(W'W) I], v = 1 / (1 + (n^-1 tr(W'W))^2) (homoskedastic, Drukker et al. 2013).
# Step 2: betas by OLS of (y - lambda Wy) on (X - lambda WX) (spatial Cochrane-Orcutt).
# Step 2b (efficiently weighted lambda, the one spreg reports) and the standard errors are rebuilt too and checked.
# sphet is run too and printed for information: its error-only route estimates the betas by instrumental variables
# with the unfiltered X as instruments, a different estimator (VERIFICATION_LOG.md, Gate 8 round 1 decision record).
trp <- function(A, B) sum(A * t(B))          # trace(A %*% B) without forming the product
hand_sem <- function(f, het) {
  X <- model.matrix(f, A); y <- A$lst_anom; n <- length(y)
  WtW <- crossprod(Wm); A2 <- (Wm + t(Wm)) / 2
  A1 <- if (het) WtW - Diagonal(x = diag(WtW)) else {
    tr <- sum(diag(WtW)); (WtW - Diagonal(n, tr / n)) / (1 + (tr / n)^2) }
  # moment conditions n^-1 e'A1 e and n^-1 e'A2 e (e'A2e = e'We), e = u - l Wu, written as g - G (l, l^2)
  mom <- function(u) { wu <- as.vector(Wm %*% u)
    g <- c(sum(u * as.vector(A1 %*% u)), sum(u * as.vector(A2 %*% u))) / n
    G <- rbind(c(2 * sum(wu * as.vector(A1 %*% u)), -sum(wu * as.vector(A1 %*% wu))),
               c(2 * sum(wu * as.vector(A2 %*% u)), -sum(wu * as.vector(A2 %*% wu)))) / n
    list(g = g, G = G) }
  solve_l <- function(m, Ec = diag(2)) optimize(function(l) sum((Ec %*% (m$g - m$G %*% c(l, l^2)))^2), c(-0.99, 0.99), tol = 1e-12)$minimum
  # step 1: OLS residuals, identity weights
  u0 <- as.vector(y - X %*% lm.fit(X, y)$coefficients)
  l1 <- solve_l(mom(u0))
  # step 2a: spatial Cochrane-Orcutt at l1
  b <- lm.fit(as.matrix(X - l1 * (Wm %*% X)), y - l1 * as.vector(Wm %*% y))$coefficients
  u <- as.vector(y - X %*% b); wu <- as.vector(Wm %*% u)
  # step 2b: efficiently weighted moments; Psi from Arraiz et al. 2010 (het) or Drukker et al. 2013 (hom), at l1
  e1 <- u - l1 * wu
  Psi <- if (het) {
    S <- Diagonal(x = e1^2); a <- 2 * A1 %*% S; bb <- (Wm + t(Wm)) %*% S
    matrix(c(trp(a, a), trp(a, bb), trp(a, bb), trp(bb, bb)), 2) / (2 * n)
  } else {
    s2 <- sum(e1^2) / n; mu4 <- sum(e1^4) / n; d1 <- diag(A1)
    p11 <- 2 * s2^2 * trp(A1, A1) + (mu4 - 3 * s2^2) * sum(d1^2)
    p12 <- s2^2 * trp(A1, 2 * A2); p22 <- s2^2 * trp(A2, 2 * A2)
    matrix(c(p11, p12, p12, p22), 2) / n
  }
  l2 <- solve_l(mom(u), chol(solve(Psi)))
  # standard errors of the betas at the reported (step-2b) lambda
  Xs <- as.matrix(X - l2 * (Wm %*% X)); es <- u - l2 * wu; XtXi <- solve(crossprod(Xs))
  V <- if (het) XtXi %*% crossprod(Xs * es) %*% XtXi else (sum(es^2) / n) * XtXi
  list(lambda1 = l1, lambda2 = l2, betas = b, se = sqrt(diag(V)))
}
for (m in c("A", "B")) for (est in c("Het", "Hom")) {
  py <- res$sem[[m]][[est]]
  if (is.null(py)) { cat(m, est, ": Python fit failed; skipped\n"); next }
  h <- hand_sem(if (m == "A") fA else fB, het = (est == "Het"))
  bP <- unlist(py$betas)[soc]; seP <- unlist(py$se)[soc]
  worst <- max(abs(h$betas[soc] - bP) / seP)
  se_rel <- max(abs(h$se[soc] - seP) / seP); dl <- abs(h$lambda2 - py$betas$lambda)
  cat(sprintf("SEM %s %s (hand, R): lambda step 1 %.4f, step 2b %.4f (spreg %.4f); max |beta diff| / SE %.5f; max relative SE diff %.5f\n",
              m, est, h$lambda1, h$lambda2, py$betas$lambda, worst, se_rel))
  if (worst > 0.01 || se_rel > 0.005 || dl > 0.001) fail <- TRUE
  co <- coef(sphet::spreg(if (m == "A") fA else fB, data = A, listw = Wm, model = "error", het = (est == "Het")))
  cat(sprintf("   (information) sphet: max |beta diff| / SE vs spreg = %.3f; lambda sphet %.4f vs spreg %.4f\n",
              max(abs(co[soc, 1] - bP) / seP), co["rho", 1], py$betas$lambda))
}

# bootstrap replicates from the saved block draws
cb <- read.csv("05_analysis/results/step8_cell_blocks.csv")
stopifnot(all(cb$gitter_id_100m == A$gitter_id_100m))
dr <- as.matrix(read.csv(gzfile("05_analysis/results/step8_boot_draws.csv.gz"), header = FALSE))
bAp <- as.matrix(read.csv("05_analysis/results/step8_boot_betas_A.csv"))
rows_of <- split(seq_len(nrow(A)), factor(cb$bid, levels = 0:(max(cb$bid))))
XA <- model.matrix(fA, A); XB <- model.matrix(fB, A); y <- A$lst_anom
worst <- 0
for (r in seq_len(nrow(dr))) {
  idx <- unlist(rows_of[dr[r, ] + 1], use.names = FALSE)
  bA <- lm.fit(XA[idx, ], y[idx])$coefficients[soc]
  worst <- max(worst, max(abs(bA - bAp[r, soc])))
}
cat(sprintf("bootstrap: %d replicates recomputed, max |diff| of social betas %.2e\n", nrow(dr), worst))
if (worst > 1e-8) fail <- TRUE
cat(if (fail) "RESULT: FAILED\n" else "RESULT: PASSED\n")
if (fail) quit(status = 1)
