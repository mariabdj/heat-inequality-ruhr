r"""Step 8a: primary models and the tests of H1, H2, RQ2 and H3 (preregistration Q19 to Q23).
y = cell LST anomaly (C). Units: rent per 1 EUR/m2; foreign, 65+ and under-18 shares per 10 percentage points.
Model A: y ~ rent + foreign + age65 + under18 + elevation + ln(population) + 10 city dummies (reference: Bochum).
Model B: Model A + tree cover + imperviousness, same cells.
W: queen contiguity on the 100 m grid (centres <= 142 m apart), row-standardised, on each model's own sample;
islands kept with an empty row.
Primary estimator: spreg.GM_Error_Het(hard_bound=True); fallback GM_Error_Hom (only if Het raises an error).
Inference (Q19): for each social beta of Model A, the largest of three two-sided p-values (GM_Error_Het, GM_Error_Hom,
OLS block bootstrap) is used for Holm across the four; the reported interval is the hull of the three 95% intervals.
H3: delta* = sign(beta_A) x (beta_A - beta_B), OLS, block bootstrap (1 km INSPIRE cell x city), B = 999, one-sided.
Effects (Q20): beta x (P90 - P10) of the pooled Model A sample; rent oriented so that positive = hotter where rent is low;
"practically negligible" if the whole 95% interval lies within +-0.3 C.
Results describe cells, not people; associations, not causes; LST is surface, not air temperature.
Usage: .venv\Scripts\python.exe 05_analysis/step8_primary.py
"""
import json, pathlib, sys, warnings

import libpysal
import numpy as np
import pandas as pd
import spreg
from scipy import sparse
from scipy.spatial import cKDTree

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", category=UserWarning)
SEED, B = 20261102, 999
SOC = ["rent", "foreign10", "age65_10", "under18_10"]
LABEL = {"rent": "rent (EUR/m2)", "foreign10": "foreign share (per 10 points)", "age65_10": "share 65+ (per 10 points)",
         "under18_10": "share under 18 (per 10 points)"}

t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
t = t.sort_values("gitter_id_100m").reset_index(drop=True)
t["foreign10"], t["age65_10"], t["under18_10"] = t.foreign / 10, t.age65 / 10, t.under18 / 10
t["ln_pop"] = np.log(t.einwohner_n)
CITIES = sorted(t.city.unique())                       # Bochum first = reference
DUM = [f"city_{c}" for c in CITIES[1:]]
for c, d in zip(CITIES[1:], DUM):
    t[d] = (t.city == c).astype(float)
XA = SOC + ["elevation", "ln_pop"] + DUM
XB = XA[:6] + ["tree_cover", "imperviousness"] + DUM
A = t[t.sample_model_A].reset_index(drop=True)
assert t.sample_model_B.sum() == len(A) and A.sample_model_B.all(), "Model B must use the same cells as Model A"
out = {"n_model_A": len(A), "reference_city": CITIES[0], "notes": "cells, not people; associations, not causes"}


def queen(d):
    w = libpysal.weights.DistanceBand(d[["x_mp", "y_mp"]].values, threshold=142, binary=True, silence_warnings=True)
    w.transform = "r"
    return w


def ols_np(y, X):
    Xc = np.column_stack([np.ones(len(y)), X])
    return np.linalg.lstsq(Xc, y, rcond=None)[0][1:]


def fit_sem(y, X, w, names):
    """GM_Error_Het and GM_Error_Hom; returns dict per estimator (None if it raised an error)."""
    res = {}
    for est in ("Het", "Hom"):
        try:
            m = getattr(spreg, f"GM_Error_{est}")(y, X, w=w, hard_bound=True, name_x=names)
            b, se = m.betas.ravel(), m.std_err.ravel()
            res[est] = {"betas": dict(zip(["const"] + names + ["lambda"], b)), "se": dict(zip(["const"] + names + ["lambda"], se)),
                        "p": dict(zip(["const"] + names + ["lambda"], [z[1] for z in m.z_stat]))}
        except Exception as e:                                 # logged, as the preregistration asks
            res[est] = None
            res[f"{est}_error"] = repr(e)
    return res


# --- weights, OLS diagnostics, VIF (Q19 "Before the SEM", Q23) ---
wA = queen(A)
out["W_model_A"] = {"islands": len(wA.islands), "components": int(wA.n_components)}
yA = A[["lst_anom"]].values
diag = {}
for name, cols in (("A", XA), ("B", XB)):
    o = spreg.OLS(yA, A[cols].values, w=wA, spat_diag=True, moran=True, robust="white", name_x=cols)
    diag[name] = {"betas": dict(zip(["const"] + cols, o.betas.ravel())), "r2": float(o.r2),
                  "moran_residuals": {"I": float(o.moran_res[0]), "z": float(o.moran_res[1]), "p": float(o.moran_res[2])},
                  "robust_LM_error": {"stat": float(o.rlm_error[0]), "p": float(o.rlm_error[1])},
                  "robust_LM_lag": {"stat": float(o.rlm_lag[0]), "p": float(o.rlm_lag[1])}}
    if name == "A":
        resid_ols = o.u.ravel()
out["ols"] = diag
out["lag_model_equal_weight"] = bool(diag["A"]["robust_LM_lag"]["p"] < .05 and diag["A"]["robust_LM_error"]["p"] >= .05)
vif = {}
for name, cols in (("A", SOC + ["elevation", "ln_pop"]), ("B", SOC + ["elevation", "ln_pop", "tree_cover", "imperviousness"])):
    Xc = A[cols].values
    for j, c in enumerate(cols):
        others = np.delete(Xc, j, axis=1)
        fit = np.column_stack([np.ones(len(Xc)), others]) @ np.linalg.lstsq(np.column_stack([np.ones(len(Xc)), others]), Xc[:, j], rcond=None)[0]
        r2 = 1 - ((Xc[:, j] - fit) ** 2).sum() / ((Xc[:, j] - Xc[:, j].mean()) ** 2).sum()
        vif.setdefault(name, {})[c] = float(1 / (1 - r2))
out["vif"] = vif
out["vif_above_10"] = any(v > 10 for d in vif.values() for v in d.values())

# --- SEM, Models A and B ---
sem = {name: fit_sem(yA, A[cols].values, wA, cols) for name, cols in (("A", XA), ("B", XB))}
out["sem"] = sem
if sem["A"]["Het"] is None:
    print("GM_Error_Het failed for Model A:", sem["A"].get("Het_error"))

# --- block bootstrap (1 km INSPIRE cell x city), shared by the inference rule and H3 ---
A["block"] = (A.city + "_" + (A.x_mp // 1000).astype(int).astype(str) + "_" + (A.y_mp // 1000).astype(int).astype(str))
blocks = A.groupby("block").city.first().reset_index()
blocks = blocks.sort_values(["city", "block"]).reset_index(drop=True)
blocks["bid"] = np.arange(len(blocks))
A = A.merge(blocks[["block", "bid"]], on="block", how="left")
rows_of = [np.flatnonzero(A.bid.values == b) for b in range(len(blocks))]
out["blocks_per_city"] = blocks.groupby("city").size().to_dict()
rng = np.random.default_rng(SEED)
XAv, XBv, y1 = A[XA].values, A[XB].values, A.lst_anom.values
draws = np.empty((B, len(blocks)), dtype=np.int32)
bA = np.empty((B, len(XA))); bB = np.empty((B, len(XB)))
for r in range(B):
    pick = np.concatenate([rng.choice(g.bid.values, size=len(g), replace=True) for _, g in blocks.groupby("city", sort=True)])
    draws[r] = pick
    idx = np.concatenate([rows_of[b] for b in pick])
    bA[r], bB[r] = ols_np(y1[idx], XAv[idx]), ols_np(y1[idx], XBv[idx])
pd.DataFrame(draws).to_csv(RES / "step8_boot_draws.csv.gz", index=False, header=False)
A[["gitter_id_100m", "block", "bid"]].to_csv(RES / "step8_cell_blocks.csv", index=False)
pd.DataFrame(bA, columns=XA).to_csv(RES / "step8_boot_betas_A.csv", index=False)
pd.DataFrame(bB, columns=XB).to_csv(RES / "step8_boot_betas_B.csv", index=False)

# --- inference rule, Holm, verdicts, effects (Q19, Q20, Q22) ---
olsA = ols_np(y1, XAv); olsB = ols_np(y1, XBv)
rows = []
for j, v in enumerate(SOC):
    bs = bA[:, j]
    p_boot = min(1.0, 2 * min(1 + (bs <= 0).sum(), 1 + (bs >= 0).sum()) / (B + 1))
    ivs, ps = [(np.percentile(bs, 2.5), np.percentile(bs, 97.5))], [p_boot]
    for est in ("Het", "Hom"):
        m = sem["A"][est]
        if m is not None:
            ivs.append((m["betas"][v] - 1.96 * m["se"][v], m["betas"][v] + 1.96 * m["se"][v])); ps.append(m["p"][v])
    point = (sem["A"]["Het"] or sem["A"]["Hom"])["betas"][v] if (sem["A"]["Het"] or sem["A"]["Hom"]) else float(np.median(bs))
    lo, hi = min(i[0] for i in ivs), max(i[1] for i in ivs)
    het = sem["A"]["Het"]
    rows.append({"variable": v, "beta_sem_het": point, "beta_ols": olsA[j], "p_het": het["p"][v] if het else np.nan,
                 "p_hom": sem["A"]["Hom"]["p"][v] if sem["A"]["Hom"] else np.nan, "p_boot": p_boot, "p_max": max(ps),
                 "ci_lo_hull": lo, "ci_hi_hull": hi, "same_side": bool(lo > 0 or hi < 0),
                 "ols_outside_het_ci": bool(het and not (het["betas"][v] - 1.96 * het["se"][v] <= olsA[j] <= het["betas"][v] + 1.96 * het["se"][v]))})
inf = pd.DataFrame(rows)
order = np.argsort(inf.p_max.values)                      # Holm, 4 tests
adj = np.empty(4); run = 0
for k, i in enumerate(order):
    run = max(run, min(1, (4 - k) * inf.p_max.values[i])); adj[i] = run
inf["p_holm"] = adj
P = {v: (A[v].quantile(.10), A[v].quantile(.90)) for v in SOC}
inf["P10"], inf["P90"] = [P[v][0] for v in SOC], [P[v][1] for v in SOC]
sgn = np.where(inf.variable == "rent", -1, 1)              # rent: positive = hotter where rent is low
span = inf.P90 - inf.P10
inf["effect_P10_P90"] = sgn * inf.beta_sem_het * span
e1, e2 = sgn * inf.ci_lo_hull * span, sgn * inf.ci_hi_hull * span
inf["effect_ci_lo"], inf["effect_ci_hi"] = np.minimum(e1, e2), np.maximum(e1, e2)
inf["negligible_region"] = (inf.effect_ci_lo >= -0.3) & (inf.effect_ci_hi <= 0.3)


def verdict(r, expected):
    sig = r.p_holm < .05 and r.same_side
    if expected is None:
        base = ("positive" if r.beta_sem_het > 0 else "negative") if sig else "inconclusive"
    elif sig and np.sign(r.beta_sem_het) == expected:
        base = "supported"
    elif sig:
        base = "contradicted"
    else:
        base = "not supported (inconclusive)"
    if r.negligible_region:
        base = base + " but practically negligible" if sig else "practically negligible"
    return base


EXP = {"rent": -1, "foreign10": 1, "age65_10": None, "under18_10": None}   # H1, H2, RQ2
inf["verdict"] = [verdict(r, EXP[r.variable]) for r in inf.itertuples()]
inf.to_csv(RES / "step8_inference.csv", index=False)
out["inference"] = inf.to_dict(orient="records")

# --- H3 ---
h3 = []
for v in ("rent", "foreign10"):
    ja, jb = XA.index(v), XB.index(v)
    s = np.sign(olsA[ja])
    d_full = s * (olsA[ja] - olsB[jb])
    d_b = s * (bA[:, ja] - bB[:, jb])
    p1 = (1 + (d_b <= 0).sum()) / (B + 1)
    ci_bA = (np.percentile(bA[:, ja], 2.5), np.percentile(bA[:, ja], 97.5))
    semA, semB = sem["A"]["Het"], sem["B"]["Het"]
    h3.append({"variable": v, "sign_beta_A": int(s), "beta_A_ols": olsA[ja], "beta_B_ols": olsB[jb], "delta_star": d_full, "p_one_sided": p1,
               "ci_lo": np.percentile(d_b, 2.5), "ci_hi": np.percentile(d_b, 97.5),
               "replicates_beta_B_opposite_sign": int((np.sign(bB[:, jb]) != np.sign(bA[:, ja])).sum()),
               "R_percent": 100 * d_full / abs(olsA[ja]) if (ci_bA[0] > 0 or ci_bA[1] < 0) else None,
               "delta_star_sem": s * (semA["betas"][v] - semB["betas"][v]) if semA and semB else None,
               "sign_reversal": bool(np.sign(olsB[jb]) != s and abs(olsB[jb]) > abs(olsA[ja]))})
h3 = pd.DataFrame(h3)
h3["p_holm"] = np.minimum(1, np.maximum.accumulate((2 - np.arange(2)) * np.sort(h3.p_one_sided.values)))[np.argsort(np.argsort(h3.p_one_sided.values))]
h3["verdict"] = ["sign reversal" if r.sign_reversal else ("supported" if r.delta_star > 0 and r.p_holm < .05 else "not supported")
                 for r in h3.itertuples()]
h3.to_csv(RES / "step8_h3.csv", index=False)
out["h3"] = h3.to_dict(orient="records")

# --- residual correlogram of OLS Model A (range reported; 1 km blocks stay primary) ---
xy = A[["x_mp", "y_mp"]].values
tree = cKDTree(xy)
z = resid_ols - resid_ols.mean()
corr = []
for d0, d1 in [(0, 142), (142, 300), (300, 600), (600, 1000), (1000, 1500), (1500, 2000), (2000, 3000)]:
    pairs = tree.query_pairs(d1, output_type="ndarray")
    dist = np.hypot(*(xy[pairs[:, 0]] - xy[pairs[:, 1]]).T)
    pairs = pairs[dist > d0]
    i = np.concatenate([pairs[:, 0], pairs[:, 1]]); j = np.concatenate([pairs[:, 1], pairs[:, 0]])
    W = sparse.csr_matrix((np.ones(len(i)), (i, j)), shape=(len(z), len(z)))
    deg = np.asarray(W.sum(1)).ravel(); W = sparse.diags(np.where(deg > 0, 1 / np.maximum(deg, 1), 0)) @ W
    corr.append({"from_m": d0, "to_m": d1, "pairs": int(len(pairs)), "moran_I": float(len(z) / W.sum() * (z @ (W @ z)) / (z @ z))})
out["residual_correlogram"] = corr
pd.DataFrame(corr).to_csv(RES / "step8_residual_correlogram.csv", index=False)

# --- single-variable models (adjusted for elevation, log population and city only), each on its own available cells ---
single = []
for v, raw in (("rent", "rent"), ("foreign10", "foreign"), ("age65_10", "age65"), ("under18_10", "under18")):
    ok = t.rule4 & t[f"{raw}_in_file"].fillna(False).astype(bool) & ~t[f"{raw}_br"].fillna(False).astype(bool) & t[["elevation", "lst_anom"]].notna().all(axis=1)
    d = t[ok].reset_index(drop=True)
    w = queen(d); cols = [v, "elevation", "ln_pop"] + DUM
    s = fit_sem(d[["lst_anom"]].values, d[cols].values, w, cols)
    rec = {"variable": v, "n": len(d), "islands": len(w.islands)}
    for est in ("Het", "Hom"):
        m = s[est]
        rec[f"beta_{est}"] = m["betas"][v] if m else None; rec[f"se_{est}"] = m["se"][v] if m else None; rec[f"p_{est}"] = m["p"][v] if m else None
    single.append(rec)
out["single_variable"] = single
pd.DataFrame(single).to_csv(RES / "step8_single_variable.csv", index=False)

# --- residuals saved for diagnostics ---
semres = spreg.GM_Error_Het(yA, A[XA].values, w=wA, hard_bound=True)
pd.DataFrame({"gitter_id_100m": A.gitter_id_100m, "resid_ols_A": resid_ols, "resid_sem_het_A": semres.e_filtered.ravel()}).to_csv(RES / "step8_residuals_A.csv", index=False)

path = RES / "results.json"
res = json.loads(path.read_text(encoding="utf-8"))
res["step8a"] = json.loads(json.dumps(out, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
path.write_text(json.dumps(res, indent=2), encoding="utf-8")
pd.set_option("display.width", 200)
print(inf[["variable", "beta_sem_het", "p_het", "p_hom", "p_boot", "p_holm", "ci_lo_hull", "ci_hi_hull", "effect_P10_P90", "effect_ci_lo", "effect_ci_hi", "verdict"]].round(4).to_string(index=False))
print(h3[["variable", "delta_star", "p_one_sided", "p_holm", "ci_lo", "ci_hi", "verdict"]].round(4).to_string(index=False))
print("lambda (Het, A):", sem["A"]["Het"]["betas"]["lambda"] if sem["A"]["Het"] else None, "| islands", len(wA.islands), "| VIF>10:", out["vif_above_10"])
