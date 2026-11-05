r"""Step 9: exploratory checks asked by the Gate 9 expert panel (deviations D17 and D18). Not preregistered; no
hypothesis verdict depends on them. Same estimator and Q19 inference rule as the primary model (step8_lib.py).
D18a  Model A with the six continuous regressors smoothed over a 3 x 3 window (thermal resolution check)
D18b  number of valid observations per cell: correlations, and Model A on cells with >= 12 of 16 observations
D17   air temperature (DWD HOSTRADA, day and night): resident gap, and Model A on the 1 km grid (S7 set-up)
Usage: .venv\Scripts\python.exe 05_analysis/step9_checks.py  ->  results.json ("step9_checks"), step9_checks.csv
"""
import json, pathlib, sys, warnings

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import step8_lib as L

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
t, DUM = L.prep(pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet"))
XC = L.SOC + ["elevation", "ln_pop"]
out, rows = {}, []


def fit(name, d, ycol="lst_anom", dummies=DUM, thr=142, block=1000, P=None):
    """Q19 rule on one design; P = fixed P10/P90 per social variable (default: this sample)."""
    d = d.reset_index(drop=True)
    P = P or {v: (d[v].quantile(.10), d[v].quantile(.90)) for v in L.SOC}
    x = XC + dummies
    w = L.queen(d, thr=thr); y = d[ycol].values; X = d[x].values
    bid, blocks = L.make_blocks(d, block)
    boots = L.bootstrap(y, [X], bid, blocks)[0]
    sem = L.sem(y, X, w, x)
    inf = L.infer(L.SOC, sem, boots, L.ols_np(y, X), P)
    inf.insert(0, "analysis", name); inf.insert(1, "n", len(d))
    rows.extend(inf.to_dict(orient="records"))
    lam = sem["Het"]["betas"]["lambda"] if sem["Het"] else None
    print(f"{name}: n {len(d)}, islands {len(w.islands)}, lambda {lam}; "
          + "; ".join(f"{r.variable} effect {r.effect_P10_P90:.3f} [{r.effect_ci_lo:.3f}, {r.effect_ci_hi:.3f}] {r.verdict}" for r in inf.itertuples()), flush=True)
    return {"n": len(d), "islands": len(w.islands), "lambda_het": lam, "P10_P90": {k: list(v) for k, v in P.items()},
            "inference": inf.drop(columns="analysis").to_dict(orient="records")}


A = t[t.sample_model_A].reset_index(drop=True)
r4 = t[t.rule4].reset_index(drop=True)

# ---- D18a: 3 x 3 window values of the six continuous regressors -------------------------------------------------
tree = cKDTree(r4[["x_mp", "y_mp"]].values)
nb = tree.query_ball_point(A[["x_mp", "y_mp"]].values, r=142)         # the cell itself and its up to 8 neighbours
pop = r4.einwohner_n.values.astype(float); dw = r4.n_dwellings.fillna(0).values.astype(float)
S = A.copy()
for raw, scaled in [("foreign", "foreign10"), ("age65", "age65_10"), ("under18", "under18_10"), ("rent", "rent")]:
    ok = L.usable(r4, raw).values; v = r4[raw].values
    wts = dw if raw == "rent" else pop
    vals = []
    for idx in nb:
        i = [j for j in idx if ok[j] and wts[j] > 0]
        vals.append(np.average(v[i], weights=wts[i]))
    S[scaled] = np.array(vals) / (10 if scaled.endswith("10") else 1)
S["elevation"] = [np.nanmean(r4.elevation.values[idx]) for idx in nb]
S["ln_pop"] = [np.log(pop[idx].sum()) for idx in nb]
out["D18a_smoothed_3x3"] = fit("D18a 3x3 smoothed regressors", S)
memA = A.foreign / 100 * A.einwohner_n
gap_s = float(np.average(S.foreign10, weights=memA) - np.average(S.foreign10, weights=A.einwohner_n - memA))   # per 10 points
b_s = next(r for r in out["D18a_smoothed_3x3"]["inference"] if r["variable"] == "foreign10")["beta"]
out["D18a_smoothed_3x3"]["exposure_gap_points_smoothed"] = 10 * gap_s
out["D18a_smoothed_3x3"]["implied_resident_gap_C"] = b_s * gap_s
print(f"D18a exposure gap of the smoothed share {10 * gap_s:.2f} points; implied resident gap {b_s * gap_s:.3f} C")
out["D18a_smoothed_3x3"]["note"] ="P10/P90 of the smoothed variables on the Model A cells; compare effects with Table 1 (Q20 percentiles of the unsmoothed variables)"

# ---- D18b: observations per cell ---------------------------------------------------------------------------------
cor = {v: float(spearmanr(A.lst_nobs_mean, A[c], nan_policy="omit")[0]) for v, c in [("foreign", "foreign"), ("rent", "rent"), ("imperviousness", "imperviousness")]}
out["D18b_nobs"] = {"spearman_with_nobs": cor, "nobs_quantiles": A.lst_nobs_mean.quantile([0, .1, .5, .9, 1]).round(2).to_dict(),
                    "share_cells_nobs_ge_12": float((A.lst_nobs_mean >= 12).mean())}
P_A = {v: (A[v].quantile(.10), A[v].quantile(.90)) for v in L.SOC}
out["D18b_nobs"]["model_nobs_ge_12"] = fit("D18b cells with >= 12 observations", A[A.lst_nobs_mean >= 12], P=P_A)
print("D18b correlations with the number of observations:", {k: round(v, 3) for k, v in cor.items()})

# ---- D17: air temperature (only if the processed file exists) ------------------------------------------------------
air_f = ROOT / "01_data/processed/air_temperature_cells.csv"
if air_f.is_file():
    air = pd.read_csv(air_f)
    t2 = t.merge(air, on="gitter_id_100m", how="left")
    res = {}
    for ycol in ("air_day", "air_night"):
        g = {}
        for lab, d in [("model_A_cells", t2[t2.sample_model_A]), ("all_usable_foreign_cells", t2[t2.rule4 & L.usable(t2, "foreign")])]:
            d = d[d[ycol].notna()]; m = d.foreign / 100 * d.einwohner_n
            g[lab] = float(np.average(d[ycol], weights=m) - np.average(d[ycol], weights=d.einwohner_n - m))
        A2 = t2[t2.sample_model_A].reset_index(drop=True)
        agg = L.aggregate_1km(A2)
        A2["kx"], A2["ky"] = (A2.x_mp // 1000).astype(int), (A2.y_mp // 1000).astype(int)
        agg = agg.merge(A2.groupby(["kx", "ky"])[ycol].mean().reset_index(), on=["kx", "ky"])
        cities = sorted(t.city.unique()); dum7 = []
        for c in cities[1:]:
            col = f"city_{c}"; agg[col] = (agg.city == c).astype(float); dum7.append(col)
        dum7 = [c for c in dum7 if agg[c].sum() > 0]
        a = agg.dropna(subset=["rent", ycol])
        res[ycol] = {"resident_gap_foreign": g, "model_1km": fit(f"D17 {ycol} 1 km", a, ycol=ycol, dummies=dum7, thr=1420, block=2000)}
        lst = fit(f"D17 LST same 1 km cells ({ycol})", a, ycol="lst_anom", dummies=dum7, thr=1420, block=2000) if ycol == "air_day" else None
        if lst:
            res["lst_same_1km_cells"] = lst
        print(f"{ycol}: resident gap (foreign minus others) {g}")
    out["D17_air_temperature"] = res
else:
    print("D17 skipped: 01_data/processed/air_temperature_cells.csv not found")

pd.DataFrame(rows).to_csv(RES / "step9_checks.csv", index=False)


def clean(o):
    if isinstance(o, float) and o != o:
        return None
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return {str(k): clean(v) for k, v in o.items()} if isinstance(o, dict) else [clean(v) for v in o] if isinstance(o, (list, tuple)) else o


R = json.loads((RES / "results.json").read_text(encoding="utf-8"))
R["step9_checks"] = clean(out)
(RES / "results.json").write_text(json.dumps(clean(R), indent=2, allow_nan=False), encoding="utf-8")
print("written: results.json step9_checks, step9_checks.csv")
