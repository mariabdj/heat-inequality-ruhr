r"""Step 8b: sensitivity analyses on the existing table (preregistration Q24: S1, S2, S3, S7, S8, S9, S10, S11, S17,
S18, S19, S20) and two exploratory analyses (D2 dash as missing; Q25 rent x tree cover). Every analysis uses the Q19
estimator, fallback and inference rule (05_analysis/step8_lib.py) unless the preregistration says otherwise; S3 follows
deviation D9. First, the shared functions must reproduce the Step 8a inference table exactly.
Usage: .venv\Scripts\python.exe 05_analysis/step8_sensitivity.py
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
CTRL_A, CTRL_B = ["elevation", "ln_pop"], ["elevation", "ln_pop", "tree_cover", "imperviousness"]
A = t[t.sample_model_A].reset_index(drop=True)
P = {v: (A[v].quantile(.10), A[v].quantile(.90)) for v in L.SOC}       # fixed at the primary sample (Q20)
covs = t[["elevation", "lst_anom", "tree_cover", "imperviousness"]].notna().all(axis=1)
summary, extra = [], {}


def run(name, d, soc=L.SOC, w=None, block_size=1000, wts=None, dummies=None, slx=False, sem_on=True, do_h3=True, ctrl_b=CTRL_B):
    d = d.reset_index(drop=True)
    dum = DUM if dummies is None else dummies
    xa, xb = soc + CTRL_A + dum, soc + ctrl_b + dum
    w = L.queen(d) if w is None else w
    y = d.lst_anom.values
    XA, XB = d[xa].values, d[xb].values
    if slx:                                                   # S18: W x social columns appended (bootstrap OLS design)
        WX = np.column_stack([w.sparse @ d[v].values for v in soc]); XA_b = np.column_stack([XA, WX])
    bid, blocks = L.make_blocks(d, block_size)
    bA, bB = L.bootstrap(y, [XA_b if slx else XA, XB], bid, blocks, wts=wts)
    olsA = L.ols_np(y, XA_b if slx else XA, wts); olsB = L.ols_np(y, XB, wts)
    semA = L.sem(y, XA, w, xa, slx_vars=[True] * len(soc) + [False] * (len(xa) - len(soc)) if slx else None) if sem_on else None
    inf = L.infer(soc, semA, bA, olsA, P)
    inf.insert(0, "analysis", name); inf.insert(1, "n", len(d)); inf.insert(2, "islands", len(w.islands))
    rec = {"n": len(d), "islands": len(w.islands), "blocks": len(blocks), "inference": inf.drop(columns="analysis").to_dict(orient="records")}
    if sem_on:
        rec["lambda_het"] = semA["Het"]["betas"]["lambda"] if semA["Het"] else None
        rec["errors"] = {k: v for k, v in semA.items() if k.endswith("_error")}
        if slx and semA["Het"]:
            rec["theta_het"] = {f"W_{v}": semA["Het"]["betas"].get(f"W_{v}") for v in soc}
    if do_h3:
        semB = L.sem(y, XB, w, xb) if sem_on else None
        hh = L.h3(bA, bB, olsA, olsB, xa, xb, (semA or {}).get("Het"), (semB or {}).get("Het"))
        rec["h3"] = hh.to_dict(orient="records")
        for r in hh.itertuples():
            summary.append({"analysis": name, "n": len(d), "variable": "H3_" + r.variable, "beta": r.delta_star, "ci_lo_hull": r.ci_lo,
                            "ci_hi_hull": r.ci_hi, "p_holm": r.p_holm, "verdict": r.verdict})
    summary.extend(inf.to_dict(orient="records"))
    extra[name] = rec
    print(f"{name}: n {len(d)}; " + "; ".join(f"{r.variable} {r.beta:.3f} {r.verdict}" for r in inf.itertuples()), flush=True)
    return inf


# 0. consistency test: the shared functions reproduce Step 8a
prim = run("primary (check)", A)
ref = pd.read_csv(RES / "step8_inference.csv")
diff = max(abs(prim.beta.values - ref.beta_sem_het.values).max(), abs(prim.p_max.values - ref.p_max.values).max(),
           abs(prim.ci_lo_hull.values - ref.ci_lo_hull.values).max(), abs(prim.ci_hi_hull.values - ref.ci_hi_hull.values).max())
same_v = (prim.verdict.values == ref.verdict.values).all()
print(f"consistency with Step 8a: max |diff| {diff:.2e}, verdicts identical {same_v}")
assert diff < 1e-10 and same_v, "shared functions do not reproduce Step 8a"
extra["consistency_with_step8a"] = {"max_abs_diff": diff, "verdicts_identical": bool(same_v)}
summary = [s for s in summary if s["analysis"] != "primary (check)"]
del extra["primary (check)"]

base = t.rule4 & covs
# S1: bracketed values included
run("S1 bracketed included", t[base & L.usable(t, "rent", True) & L.usable(t, "foreign", True) & L.usable(t, "age65", True) & L.usable(t, "under18", True)])
# S2: no rent term, three shares on their own common cells
run("S2 no rent restriction", t[base & L.usable(t, "foreign") & L.usable(t, "age65") & L.usable(t, "under18")], soc=L.SOC[1:])
# S3: population weights (D9: WLS with block bootstrap only)
run("S3 population-weighted (WLS, D9)", A, wts=A.einwohner_n.values.astype(float), sem_on=False)
# S7: 1 km grid
agg = L.aggregate_1km(A)
cities = sorted(t.city.unique())
dum7 = []
for c in cities[1:]:
    col = f"city_{c}"; agg[col] = (agg.city == c).astype(float); dum7.append(col)
dum7 = [c for c in dum7 if agg[c].sum() > 0]
agg["lst_anom"] = agg.lst_anom
run("S7 1 km grid", agg.dropna(subset=["rent"]), w=L.queen(agg.dropna(subset=["rent"]), thr=1420), block_size=2000, dummies=dum7)
extra["S7 1 km grid"]["n_1km_cells"] = int(agg.rent.notna().sum())
# S8: spatial lag model, judged by the interval of the total impact only
wA = L.queen(A); xa = L.SOC + CTRL_A + DUM
try:
    m = spreg.GM_Lag(A[["lst_anom"]].values, A[xa].values, w=wA, robust="white", spat_impacts="power", hard_bound=True, name_x=xa)
    b, vm = m.betas.ravel(), m.vm
    rho = b[-1]; dmul, imul, tmul = m.sp_multipliers["power"]
    rng = np.random.default_rng(L.SEED); draws = rng.multivariate_normal(b, vm, size=1000)
    keep = np.abs(draws[:, -1]) < 1
    s8 = []
    for j, v in enumerate(L.SOC):
        tot = draws[keep, 1 + j] / (1 - draws[keep, -1])
        lo, hi = np.percentile(tot, [2.5, 97.5]); sgn = -1 if v == "rent" else 1; span = P[v][1] - P[v][0]
        e = sorted([sgn * lo * span, sgn * hi * span])
        s8.append({"analysis": "S8 spatial lag (total impact)", "n": len(A), "variable": v, "beta": b[1 + j] * tmul,
                   "direct": b[1 + j] * dmul, "indirect": b[1 + j] * imul, "ci_lo_hull": lo, "ci_hi_hull": hi,
                   "same_side": bool(lo > 0 or hi < 0), "effect_P10_P90": sgn * b[1 + j] * tmul * span, "effect_ci_lo": e[0], "effect_ci_hi": e[1],
                   "negligible_region": bool(e[0] >= -0.3 and e[1] <= 0.3),
                   "verdict": ("interval on one side of 0" if (lo > 0 or hi < 0) else "interval includes 0") + ("; within +-0.3 C" if (e[0] >= -0.3 and e[1] <= 0.3) else "")})
    summary.extend(s8)
    extra["S8 spatial lag"] = {"rho": rho, "multipliers_power": [dmul, imul, tmul], "draws_discarded": int((~keep).sum()), "rows": s8}
    print("S8: rho", round(rho, 3), "; " + "; ".join(f"{r['variable']} total {r['beta']:.3f} [{r['ci_lo_hull']:.3f}, {r['ci_hi_hull']:.3f}]" for r in s8), flush=True)
except Exception as e:
    extra["S8 spatial lag"] = {"error": repr(e)}; print("S8 not estimable:", repr(e))
# S9: 8 nearest neighbours
run("S9 8 nearest neighbours", A, w=L.knn(A, 8))
# S10: each city separately (no city dummies)
s10 = {}
for c in sorted(A.city.unique()):
    s10[c] = run(f"S10 {c}", A[A.city == c], dummies=[], do_h3=False)
pooled = pd.read_csv(RES / "step8_inference.csv").set_index("variable").beta_sem_het
extra["S10 same sign as pooled"] = {v: int(sum(np.sign(s10[c].set_index("variable").beta[v]) == np.sign(pooled[v]) for c in s10)) for v in L.SOC}
# S11: other population thresholds (rule 3 for cells under 10 inhabitants from 01_data/step8_water_small_cells.py)
ws_small = pd.read_csv(ROOT / "01_data/processed/water_share_small_cells.csv").set_index("gitter_id_100m").water_share
water = t.water_share.fillna(t.gitter_id_100m.map(ws_small))
extra["S11 water share missing"] = int((t.rule1 & (t.einwohner_n >= 3) & water.isna()).sum())
for thr in (3, 30):
    s = (t.rule1 & (t.einwohner_n >= thr) & (water < 0.5) & (t.lst_cover_share >= 0.70) & covs
         & L.usable(t, "rent") & L.usable(t, "foreign") & L.usable(t, "age65") & L.usable(t, "under18"))
    run(f"S11 population >= {thr}", t[s])
# S17: tree cover and imperviousness in a 300 m window (Model B and H3)
w300 = pd.read_csv(ROOT / "04_grid_join/window300_covariates.csv")
A17 = A.merge(w300, on="gitter_id_100m", how="left")
run("S17 300 m window covariates", A17, ctrl_b=["elevation", "ln_pop", "tree_cover_300", "imperviousness_300"])
# S18: spatial Durbin error model
run("S18 spatial Durbin error", A, slx=True, do_h3=False)
# S19: H3 with 2 km blocks
run("S19 2 km blocks", A, block_size=2000)
# S20: islands dropped, W rebuilt
isl = set(wA.islands)
run("S20 islands dropped", A[[i not in isl for i in range(len(A))]])
# exploratory: D2 dashes as missing; Q25 rent x tree cover
dash = A[["foreign_dash", "age65_dash", "under18_dash"]].fillna(False).astype(bool).any(axis=1)
run("Exploratory D2 dashes as missing", A[~dash])
A["rent_x_tree"] = (A.rent - A.rent.mean()) * (A.tree_cover - A.tree_cover.mean())
xi = L.SOC + CTRL_B + ["rent_x_tree"] + DUM
mi = L.sem(A.lst_anom.values, A[xi].values, wA, xi)
extra["Exploratory Q25 rent x tree cover"] = {est: (None if mi[est] is None else {"beta": mi[est]["betas"]["rent_x_tree"], "se": mi[est]["se"]["rent_x_tree"],
                                                   "p": mi[est]["p"]["rent_x_tree"]}) for est in ("Het", "Hom")}
print("Q25 rent x tree:", extra["Exploratory Q25 rent x tree cover"])

pd.DataFrame(summary).to_csv(RES / "step8b_sensitivity.csv", index=False)
path = RES / "results.json"
res = json.loads(path.read_text(encoding="utf-8"))
res["step8b"] = json.loads(json.dumps(extra, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


def clean(o):                                      # NaN is not valid JSON: written as null
    if isinstance(o, float) and o != o:
        return None
    return {k: clean(v) for k, v in o.items()} if isinstance(o, dict) else [clean(v) for v in o] if isinstance(o, list) else o


path.write_text(json.dumps(clean(res), indent=2, allow_nan=False), encoding="utf-8")
print("done")
