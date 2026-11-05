r"""Step 8, reporting tables asked by the Gate 8 expert panel (round 1). None of these changes a preregistered
verdict; the ones that are not preregistered are labelled exploratory.
1. Misspecification table (Model A): OLS vs SEM (Het) betas and intervals; lambda at step 1, step 2b and iterated to
   convergence, and the betas at each (exploratory).
2. H3 under the SEM with the SEM's own sign: delta*_SEM = sign(beta_A,SEM) x (beta_A,SEM - beta_B,SEM); zero crossing of OLS.
3. S18: beta + theta (direct + neighbourhood term) with a delta-method SE (descriptive).
4. Single-variable models: P10-P90 effects with the Q22 +-0.3 C rule (hull of the Het and Hom 95% intervals).
5. Residents vs cells: adjusted cell effect, single-variable cell effect (elevation, log population and city only), group-weighted
   resident means pooled and within city, implied resident gaps and their decomposition (exploratory).
6. S3 reference row: unweighted OLS with the same block bootstrap (to separate weighting from the change of estimator).
7. S7 effects with the 1 km P10 and P90 (descriptive, D13).
Usage: .venv\Scripts\python.exe 05_analysis/step8_reporting.py  ->  results.json ("step8_reporting"), step8_reporting_*.csv
"""
import json, pathlib, sys, warnings

import numpy as np
import pandas as pd
import spreg

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import step8_lib as L

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
t, DUM = L.prep(pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet"))
A = t[t.sample_model_A].reset_index(drop=True)
P = {v: (A[v].quantile(.10), A[v].quantile(.90)) for v in L.SOC}
SGN = {"rent": -1, "foreign10": 1, "age65_10": 1, "under18_10": 1}
res = json.loads((RES / "results.json").read_text(encoding="utf-8"))
s8a = res["step8a"]
XA = L.SOC + ["elevation", "ln_pop"] + DUM
XB = L.SOC + ["elevation", "ln_pop", "tree_cover", "imperviousness"] + DUM
y = A[["lst_anom"]].values
wA = L.queen(A)
out = {}

# 1. misspecification table
het = s8a["sem"]["A"]["Het"]; inf = pd.DataFrame(s8a["inference"]).set_index("variable")
boot = pd.read_csv(RES / "step8_boot_betas_A.csv")
it = spreg.GM_Error_Het(y, A[XA].values, w=wA, hard_bound=True, max_iter=100, name_x=XA)
lam_iter, it_n = float(it.betas[-1, 0]), int(it.iteration)
Xc, ys = np.column_stack([np.ones(len(A)), A[XA].values]), y.ravel()
co = lambda l: np.linalg.lstsq(Xc - l * (wA.sparse @ Xc), ys - l * (wA.sparse @ ys), rcond=None)[0][1:5]
lam3 = het["betas"]["lambda"]
rows = []
for j, v in enumerate(L.SOC):
    rows.append({"variable": v, "beta_ols": inf.loc[v, "beta_ols"], "boot_ci_lo": float(np.percentile(boot[v], 2.5)), "boot_ci_hi": float(np.percentile(boot[v], 97.5)),
                 "beta_sem_het": het["betas"][v], "sem_ci_lo": het["betas"][v] - 1.96 * het["se"][v], "sem_ci_hi": het["betas"][v] + 1.96 * het["se"][v],
                 "ols_outside_sem_ci": bool(abs(inf.loc[v, "beta_ols"] - het["betas"][v]) > 1.96 * het["se"][v]),
                 "beta_at_lambda_step2b_exploratory": float(co(lam3)[j]), "beta_at_lambda_iterated_exploratory": float(it.betas[1 + j, 0])})
    span, s = P[v][1] - P[v][0], SGN[v]
    rows[-1].update({"effect_P10_P90_step1": s * het["betas"][v] * span, "effect_P10_P90_step2b_exploratory": s * co(lam3)[j] * span,
                     "effect_P10_P90_iterated_exploratory": s * float(it.betas[1 + j, 0]) * span})
mis = pd.DataFrame(rows); mis.to_csv(RES / "step8_reporting_misspecification.csv", index=False)
out["misspecification"] = {"rows": mis.to_dict(orient="records"), "lambda_step2b": lam3, "lambda_iterated": lam_iter, "iterations": it_n,
                           "note": ("betas of GM_Error_Het are computed at the step-1 lambda; exploratory columns show them and the P10-P90 effects at the "
                                    "step-2b and iterated lambda. The adjusted foreign contrast ranges from about 0.31 to 0.48 C depending on the lambda step, "
                                    "partly outside the reported interval [0.38, 1.17]: the interval does not capture the uncertainty about lambda. "
                                    "OLS and SEM disagree, the pattern Pace and LeSage (2008) read as evidence against the joint specification (no formal test was run): the estimand is estimator-dependent and "
                                    "neither set of betas is 'correct'. Comparing OLS with the SEM interval ignores their covariance and is descriptive. "
                                    "'lambda moving between steps' and 'betas depending on lambda' are one phenomenon.")}

# 2. H3 under the SEM with its own sign
h3 = pd.DataFrame(s8a["h3"]).set_index("variable"); hetB = s8a["sem"]["B"]["Het"]
h3s = []
for v in ("rent", "foreign10"):
    bA, bB = het["betas"][v], hetB["betas"][v]
    h3s.append({"variable": v, "beta_A_sem": bA, "beta_B_sem": bB, "delta_star_sem_own_sign": float(np.sign(bA) * (bA - bB)),
                "beta_A_ols": h3.loc[v, "beta_A_ols"], "beta_B_ols": h3.loc[v, "beta_B_ols"],
                "ols_crosses_zero": bool(np.sign(h3.loc[v, "beta_A_ols"]) != np.sign(h3.loc[v, "beta_B_ols"])),
                "preregistered_verdict_ols": h3.loc[v, "verdict"]})
out["h3_under_sem"] = h3s; pd.DataFrame(h3s).to_csv(RES / "step8_reporting_h3_sem.csv", index=False)
out["h3_under_sem_notes"] = ["rent: beta_A under the SEM (-0.016) has a 95% interval that includes 0, so the sign used for its delta*_SEM is arbitrary: no clear direction",
                             "step8_h3.csv column delta_star_sem uses the sign of the OLS beta_A (as Q19 fixes it); this table's delta_star_sem_own_sign uses the SEM's own sign"]

# 3. S18 beta + theta with delta-method SE
xs = L.SOC + ["elevation", "ln_pop"] + DUM
m18 = spreg.GM_Error_Het(y, A[xs].values, w=wA, hard_bound=True, slx_lags=1, slx_vars=[True] * 4 + [False] * (len(xs) - 4), name_x=xs)
nm = list(m18.name_x); nm = nm + ["lambda"] if len(nm) == len(m18.betas) - 1 else nm
b18, V = m18.betas.ravel(), m18.vm
s18 = []
for v in L.SOC:
    i, j = nm.index(v), nm.index(f"W_{v}")
    tot = b18[i] + b18[j]; se = float(np.sqrt(V[i, i] + V[j, j] + 2 * V[i, j]))
    s18.append({"variable": v, "beta": b18[i], "theta": b18[j], "beta_plus_theta": tot, "se": se, "ci_lo": tot - 1.96 * se, "ci_hi": tot + 1.96 * se})
out["s18_beta_plus_theta_descriptive"] = s18

# 4. single-variable models: effects and the +-0.3 C rule
sv = []
for r in s8a["single_variable"]:
    v = r["variable"]; span = P[v][1] - P[v][0]; s = SGN[v]
    ivs = [(r[f"beta_{e}"] - 1.96 * r[f"se_{e}"], r[f"beta_{e}"] + 1.96 * r[f"se_{e}"]) for e in ("Het", "Hom") if r.get(f"beta_{e}") is not None]
    lo, hi = min(i[0] for i in ivs), max(i[1] for i in ivs); e = sorted([s * lo * span, s * hi * span])
    sv.append({"variable": v, "n": r["n"], "beta_het": r["beta_Het"], "effect_P10_P90": s * r["beta_Het"] * span, "effect_ci_lo": e[0], "effect_ci_hi": e[1],
               "within_0_3": bool(e[0] >= -0.3 and e[1] <= 0.3)})
out["single_variable_effects"] = sv; pd.DataFrame(sv).to_csv(RES / "step8_reporting_single_variable.csv", index=False)

# 5. residents vs cells (foreign share): pooled and within-city group-vs-rest (exploratory, cells not people)
d = t[t.rule4 & L.usable(t, "foreign")]
mem = d.foreign / 100 * d.einwohner_n; rest = d.einwohner_n - mem
within = []
for c, g in d.groupby("city"):
    m_, r_ = g.foreign / 100 * g.einwohner_n, g.einwohner_n - g.foreign / 100 * g.einwohner_n
    within.append((np.average(g.lst_anom, weights=m_) - np.average(g.lst_anom, weights=r_), m_.sum()))
w_diff = float(np.average([x[0] for x in within], weights=[x[1] for x in within]))
inf_f = inf.loc["foreign10"]; svf = next(x for x in sv if x["variable"] == "foreign10")
rc = [{"quantity": "adjusted cell contrast P10->P90 (Model A, within city)", "unit": "cells", "value_C": inf_f.effect_P10_P90, "ci": [inf_f.effect_ci_lo, inf_f.effect_ci_hi],
       "ci_definition": "Q19 hull: bootstrap OLS, SEM Het and SEM Hom"},
      {"quantity": "single-variable cell contrast P10->P90 (SEM, adjusted for elevation, log population and city only), all usable cells", "unit": "cells",
       "value_C": svf["effect_P10_P90"], "ci": [svf["effect_ci_lo"], svf["effect_ci_hi"]], "ci_definition": "hull of SEM Het and SEM Hom"},
      {"quantity": "estimated foreign residents minus other residents, pooled across cities (D8, exploratory)", "unit": "residents (estimated)", "value_C": float(np.average(d.lst_anom, weights=mem) - np.average(d.lst_anom, weights=rest)), "ci": None},
      {"quantity": "same, within city (weighted mean of city differences, exploratory)", "unit": "residents (estimated)", "value_C": w_diff, "ci": None}]
# same sample (Model A cells), so that adjustment is not mixed with a change of sample
dA = A.copy(); memA = dA.foreign / 100 * dA.einwohner_n; restA = dA.einwohner_n - memA
xs1 = ["foreign10", "elevation", "ln_pop"] + DUM
s1all = L.sem(dA.lst_anom.values, dA[xs1].values, wA, xs1); s1 = s1all["Het"]
o1 = L.ols_np(dA.lst_anom.values, dA[xs1].values)[0]
spanf = P["foreign10"][1] - P["foreign10"][0]
withinA = [(np.average(g.lst_anom, weights=g.foreign / 100 * g.einwohner_n) - np.average(g.lst_anom, weights=g.einwohner_n - g.foreign / 100 * g.einwohner_n),
            (g.foreign / 100 * g.einwohner_n).sum()) for _, g in dA.groupby("city")]
ivs1 = [(m["betas"]["foreign10"] - 1.96 * m["se"]["foreign10"], m["betas"]["foreign10"] + 1.96 * m["se"]["foreign10"]) for m in (s1all["Het"], s1all["Hom"]) if m]
rc += [{"quantity": "SAME SAMPLE (Model A cells): single-variable cell contrast, SEM (adjusted for elevation, log population and city only)", "unit": "cells",
        "value_C": s1["betas"]["foreign10"] * spanf, "ci": [min(i[0] for i in ivs1) * spanf, max(i[1] for i in ivs1) * spanf], "ci_definition": "hull of SEM Het and SEM Hom"},
       {"quantity": "SAME SAMPLE (Model A cells): single-variable cell contrast, OLS (adjusted for elevation, log population and city only)", "unit": "cells", "value_C": float(o1 * spanf), "ci": None},
       {"quantity": "SAME SAMPLE (Model A cells): estimated foreign residents minus others, pooled (exploratory)", "unit": "residents (estimated)",
        "value_C": float(np.average(dA.lst_anom, weights=memA) - np.average(dA.lst_anom, weights=restA)), "ci": None},
       {"quantity": "SAME SAMPLE (Model A cells): same, within city (exploratory)", "unit": "residents (estimated)",
        "value_C": float(np.average([x[0] for x in withinA], weights=[x[1] for x in withinA])), "ci": None}]
# exposure gap: share of foreign residents in the average cell of foreign residents vs of other residents (Model A cells)
gap10 = float(np.average(dA.foreign10, weights=memA) - np.average(dA.foreign10, weights=restA))
for lab, b in [("adjusted Model A SEM slope", het["betas"]["foreign10"]), ("single-variable SEM slope", s1["betas"]["foreign10"]), ("single-variable OLS slope", float(o1))]:
    rc.append({"quantity": f"SAME SAMPLE (Model A cells): implied resident gap = {lab} x exposure gap ({10 * gap10:.1f} points of foreign share), exploratory",
               "unit": "residents (implied)", "value_C": float(b * gap10), "ci": None})
out["residents_vs_cells_foreign"] = rc
out["exposure_gap_points_foreign_share"] = 10 * gap10

# decomposition of the resident gap, all on the Model A cells: slope for foreign share x exposure gap, adding one step at a time.
# With population weights and no other covariate, slope x gap equals the observed pooled resident gap exactly (identity).
yA, popA = dA.lst_anom.values, dA.einwohner_n.values
steps = [("raw slope, unweighted", float(L.ols_np(yA, dA[["foreign10"]].values)[0])),
         ("raw slope, population-weighted (identity: equals the observed pooled gap)", float(L.ols_np(yA, dA[["foreign10"]].values, popA)[0])),
         ("city dummies only, unweighted", float(L.ols_np(yA, dA[["foreign10"] + DUM].values)[0])),
         ("city dummies only, population-weighted", float(L.ols_np(yA, dA[["foreign10"] + DUM].values, popA)[0])),
         ("city + elevation only, unweighted", float(L.ols_np(yA, dA[["foreign10", "elevation"] + DUM].values)[0])),
         ("city + log population only, unweighted", float(L.ols_np(yA, dA[["foreign10", "ln_pop"] + DUM].values)[0])),
         ("plus elevation and log population (single-variable OLS)", float(o1)),
         ("same, population-weighted", float(L.ols_np(yA, dA[xs1].values, popA)[0])),
         ("single-variable SEM (step-1 lambda)", float(s1["betas"]["foreign10"])),
         ("full Model A OLS (adds rent, 65+, under 18)", float(inf.loc["foreign10", "beta_ols"])),
         ("full Model A SEM, step-1 lambda (reported)", float(het["betas"]["foreign10"])),
         ("full Model A SEM, step-2b lambda (exploratory)", float(co(lam3)[1])),
         ("full Model A SEM, iterated lambda (exploratory)", float(it.betas[2, 0]))]
dec = [{"step": k, "slope_per_10_points": b, "implied_resident_gap_C": b * gap10} for k, b in steps]
out["resident_gap_decomposition_exploratory"] = dec
out["resident_gap_identity_check"] = {"observed_pooled_gap": float(np.average(yA, weights=memA) - np.average(yA, weights=restA)),
                                      "weighted_slope_x_gap": dec[1]["implied_resident_gap_C"]}
pd.DataFrame(dec).to_csv(RES / "step8_reporting_resident_gap_decomposition.csv", index=False)
g = {d["step"]: d["implied_resident_gap_C"] for d in dec}
pc = lambda x, y: 100 * (g[y] - g[x]) / g[x]
gap_reading = (
    "reading of the implied gaps (resident_gap_decomposition_exploratory): the observed resident gap on the Model A cells ({obs:.2f} C; not the {allc:.2f} C of all usable cells) is exactly the population-weighted raw slope "
    "times the exposure gap; only that row equals the observed gap. Population weighting lowers the raw implied gap by {w:.0f}% ({r:.2f} to {obs:.2f}); city dummies change it "
    "little ({r:.2f} to {c:.2f}). Adding elevation and log population lowers it by {el:.0f}% ({c:.2f} to {sv:.2f}), mostly through log population: about {lpsh:.0f}% of the drop whichever is added first (city + log population "
    "{lp:.2f}; city + elevation {ev:.2f}). Spatial filtering removes {f1:.0f}% in the single-variable model ({sv:.2f} to {svs:.2f}) and {f2:.0f}% to {f3:.0f}% in the full Model A "
    "depending on the lambda step ({fo:.2f} to {s1:.2f}, {s2:.2f}, {s3:.2f}). Log population (density) may be a pathway (foreign residents live in dense, sealed, hot cells), "
    "not only a confounder: the implied gaps are conditional on density and elevation and are not 'the' disparity").format(
    obs=g["raw slope, population-weighted (identity: equals the observed pooled gap)"], r=g["raw slope, unweighted"], c=g["city dummies only, unweighted"],
    w=-pc("raw slope, unweighted", "raw slope, population-weighted (identity: equals the observed pooled gap)"),
    el=-pc("city dummies only, unweighted", "plus elevation and log population (single-variable OLS)"),
    allc=rc[2]["value_C"], lpsh=100 * (g["city dummies only, unweighted"] - g["city + log population only, unweighted"]) / (g["city dummies only, unweighted"] - g["plus elevation and log population (single-variable OLS)"]),
    sv=g["plus elevation and log population (single-variable OLS)"], lp=g["city + log population only, unweighted"], ev=g["city + elevation only, unweighted"],
    svs=g["single-variable SEM (step-1 lambda)"], f1=-pc("plus elevation and log population (single-variable OLS)", "single-variable SEM (step-1 lambda)"),
    fo=g["full Model A OLS (adds rent, 65+, under 18)"], s1=g["full Model A SEM, step-1 lambda (reported)"],
    s2=g["full Model A SEM, step-2b lambda (exploratory)"], s3=g["full Model A SEM, iterated lambda (exploratory)"],
    f2=-pc("full Model A OLS (adds rent, 65+, under 18)", "full Model A SEM, step-1 lambda (reported)"),
    f3=-pc("full Model A OLS (adds rent, 65+, under 18)", "full Model A SEM, iterated lambda (exploratory)"))
out["residents_vs_cells_notes"] = [
    "the first four rows use different samples (Model A 12,609 cells; single-variable 34,940 cells; residents: all rule-4 cells with a usable foreign share), so their differences mix adjustment with a change of sample; the SAME SAMPLE rows separate the two",
    "reading of the SAME SAMPLE rows: on the Model A cells the single-variable SEM contrast (about 0.45 C) is close to the adjusted one (0.48 C); the round 1 contrast 0.14 vs 0.48 came from the change of sample (the Model A cells have a steeper gradient), not from adjustment. The Q22 'practically negligible' reading of the single-variable foreign effect holds only on all usable cells",
    "P10 and P90 are those of the Model A sample in every row (Q20); the P10 to P90 span is about 45 points of foreign share, while the average cell of foreign residents and of other residents differ by only about 15 points: cell contrasts and resident differences are different quantities and not directly comparable (see the implied resident gap rows)",
    "SEM betas are computed at the step-1 lambda (0.66 for Model A, 0.68 for the same-sample single-variable model; the reported lambda is the step-2b value 0.78): they are partly within-neighbourhood contrasts, and neither OLS nor SEM betas are 'correct'",
    "'single-variable' models still adjust for elevation, log population and city (preregistered); they are not raw associations",
    "interval definitions differ by row: see ci_definition",
    gap_reading]

# 6. S3 reference row: unweighted OLS with the primary block bootstrap
ref = L.infer(L.SOC, None, boot[L.SOC].values, inf.loc[L.SOC, "beta_ols"].values, P)
ref.insert(0, "analysis", "S3 reference: unweighted OLS + bootstrap"); out["s3_reference_row"] = ref.to_dict(orient="records")

# 7. S7 with 1 km P10 and P90 (descriptive)
agg = pd.read_csv(RES / "step8_1km_aggregate.csv")
s7 = pd.DataFrame(res["step8b"]["S7 1 km grid"]["inference"]).set_index("variable")
out["s7_effects_1km_percentiles"] = [{"variable": v, "P10_1km": float(agg[v].quantile(.1)), "P90_1km": float(agg[v].quantile(.9)),
                                      "effect_1km": float(SGN[v] * s7.loc[v, "beta"] * (agg[v].quantile(.9) - agg[v].quantile(.1)))} for v in L.SOC]
out["step9_writing_obligations"] = [
    "never quote +0.48 C for the foreign share without the lambda range (about 0.31 to 0.48 C) and the note that the interval does not capture it",
    "say 'the estimand is estimator-dependent', not 'the data reject OLS'; H1 and RQ2 'inconclusive because SEM and non-SEM specifications disagree', with the table of which analyses disagree",
    "H3 holds for the OLS estimand only; give delta*_SEM next to it (negative for both; rent without clear direction) and the rent zero crossing",
    "Model A sample: 24.5% of cells, 44% of residents, hotter and more sealed: in the abstract and every policy sentence",
    "S18 beta + theta for rent is +0.11 [0.06, 0.16] (hotter where rent is high) and the S7 1 km effects for rent, 65+ and under 18 run against expectations: not support for H1",
    "surface temperature around midday on clear hot days, daytime only; cells, not people; the vacancy result is fragile (94% zeros); S10: positive in all 11 cities, supported in 3",
    "Q25 rent x tree cover: report the heteroskedastic p (0.148)",
    "single-variable foreign effect: 0.14 C on all usable cells but about 0.45 C on the Model A cells. Under the SEM, adding rent, 65+ and under 18 barely changes it (0.45 to 0.48); under OLS it moves from 0.78 to 0.97. Elevation and log population, present in both, already remove about half of the raw gradient. Never write 'the disparity appears only after adjustment', 'unadjusted, negligible' or 'robust to adjustment' without the sample and the estimator",
    "report the observed (estimated) resident exposure gap as the descriptive disparity; present the implied gaps as conditional on density and elevation; name density as a possible mediator in the limitations",
    "never set the +0.48 C cell contrast beside the 0.48 C resident difference as if they were the same quantity (45-point vs about 15-point span)",
    "call the single-variable models 'adjusted for elevation, log population and city only', not 'unadjusted'"]
out["residual_correlogram_note"] = "Moran's I of OLS residuals still positive at 2 to 3 km (0.024): range beyond 3 km; 1 and 2 km blocks are shorter, so bootstrap intervals may be too narrow (limitation, mainly for H3)"
out["islands_note"] = "1,712 of 12,609 Model A cells (13.6%) have no neighbour (3,029 components); S20 drops them"


def clean(o):
    if isinstance(o, float) and o != o:
        return None
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return {k: clean(v) for k, v in o.items()} if isinstance(o, dict) else [clean(v) for v in o] if isinstance(o, list) else o


res = json.loads((RES / "results.json").read_text(encoding="utf-8"))
res["step8_reporting"] = clean(out)
(RES / "results.json").write_text(json.dumps(clean(res), indent=2, allow_nan=False), encoding="utf-8")
pd.set_option("display.width", 220)
print(mis.round(4).to_string(index=False)); print("lambda step 2b", round(lam3, 4), "iterated", round(lam_iter, 4), "in", it_n, "iterations")
print(pd.DataFrame(h3s).round(4).to_string(index=False)); print(pd.DataFrame(s18).round(4).to_string(index=False))
print(pd.DataFrame(sv).round(4).to_string(index=False)); print(pd.DataFrame(rc).to_string(index=False))
print(ref[["variable", "beta", "ci_lo_hull", "ci_hi_hull", "p_holm", "verdict"]].round(4).to_string(index=False))
print(pd.DataFrame(out["s7_effects_1km_percentiles"]).round(3).to_string(index=False))
