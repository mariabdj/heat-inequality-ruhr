r"""Step 8b, local and descriptive (preregistration Q19): MGWR of Model B on the 1 km grid.
Aggregation as S7 (step8_lib.aggregate_1km); no city dummies (the local intercept replaces them); all variables
z-standardised; adaptive bisquare kernel; golden-section search with AICc; bandwidth confidence intervals; local
t-values corrected for multiple testing (filter_tvals); local condition numbers above 30 flagged.
Usage: .venv\Scripts\python.exe 05_analysis/step8_mgwr.py
"""
import json, pathlib, sys, warnings

import numpy as np
import pandas as pd
from mgwr.gwr import MGWR
from mgwr.sel_bw import Sel_BW

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import step8_lib as L

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
t, _ = L.prep(pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet"))
agg = L.aggregate_1km(t[t.sample_model_B]).dropna(subset=["rent"]).reset_index(drop=True)
XV = ["rent", "foreign10", "age65_10", "under18_10", "elevation", "ln_pop", "tree_cover", "imperviousness"]
z = lambda a: (a - a.mean(0)) / a.std(0)
coords = agg[["x_mp", "y_mp"]].values.astype(float)
y = z(agg[["lst_anom"]].values)
X = z(agg[XV].values)
sel = Sel_BW(coords, y, X, multi=True, kernel="bisquare", fixed=False)
# D15: search floor of 20 neighbours (mgwr's default floor of 40 + 2 = 42 left the AICc optimum of the intercept out of reach)
bws = sel.search(criterion="AICc", search_method="golden_section", multi_bw_min=[20])
res = MGWR(coords, y, X, sel, kernel="bisquare", fixed=False).fit()
names = ["intercept"] + XV
intervals = res.get_bws_intervals(sel)
filt = res.filter_tvals()
cn = res.local_collinearity()[0]
local = pd.DataFrame(res.params, columns=names)
local.insert(0, "kx", agg.kx); local.insert(1, "ky", agg.ky)
for j, nme in enumerate(names):
    local[f"sig_{nme}"] = filt[:, j] != 0
local["local_cn"] = cn
local.to_csv(RES / "step8_mgwr_local.csv", index=False)
agg.to_csv(RES / "step8_1km_aggregate.csv", index=False)
import esda, libpysal
Xc = np.column_stack([np.ones(len(y)), X]); bo = np.linalg.lstsq(Xc, y, rcond=None)[0]; ro = (y - Xc @ bo).ravel()
n, k = len(ro), Xc.shape[1]
aicc_ols = 2 * n * np.log(np.sqrt((ro @ ro) / n)) + n * np.log(2 * np.pi) + n * (n + k) / (n - 2 - k)   # mgwr's Gaussian AICc with tr(S) = k
wq = libpysal.weights.DistanceBand(coords, threshold=1420, binary=True, silence_warnings=True); wq.transform = "r"
np.random.seed(20261102)
mi = esda.Moran(res.resid_response.ravel(), wq, permutations=999)
hist = sel.bw[1] if isinstance(sel.bw, tuple) and len(sel.bw) > 1 else []
scores = sel.bw[2] if isinstance(sel.bw, tuple) and len(sel.bw) > 2 else []
out = {"n_1km": len(agg), "aicc": float(res.aicc), "r2": float(res.R2), "search_floor_neighbours": 20,
       "enp_by_covariate": dict(zip(names, map(float, np.ravel(res.ENP_j)))),
       "critical_t_by_covariate": dict(zip(names, map(float, np.ravel(res.critical_tval())))),
       "ols_same_cells": {"aicc": float(aicc_ols), "r2": float(1 - (ro @ ro) / ((y - y.mean()) ** 2).sum()),
                          "betas_z": dict(zip(names, map(float, bo.ravel())))},
       "backfitting_iterations": len(hist), "final_SOC": float(scores[-1]) if len(scores) else None, "tol_multi": float(sel.tol_multi), "max_iter_multi": int(sel.max_iter_multi),
       "residual_moran_I": {"I": float(mi.I), "p_sim": float(mi.p_sim), "islands": len(wq.islands),
                            "note": "queen W on the 1 km grid (centres <= 1,420 m); the 5 islands are kept in n with a zero spatial lag (negligible: 5 of 742 cells); p_sim is the one-sided permutation p-value (999); a significant negative value with a very local intercept (30 neighbours) suggests the local intercept slightly overfits: read the intercept surface as descriptive only"},
       "reading": "a bandwidth at the upper search bound n = 742 (the largest reached here: 740) means regional to global scale, not strictly global; units are 1 km cells, not people",
       "bandwidths": dict(zip(names, map(float, bws))), "bandwidth_intervals": dict(zip(names, [list(map(float, i)) for i in intervals])),
       "local_share_significant": {nme: float((filt[:, j] != 0).mean()) for j, nme in enumerate(names)},
       "local_coef_quantiles": {nme: [float(q) for q in np.percentile(res.params[:, j], [5, 25, 50, 75, 95])] for j, nme in enumerate(names)},
       "cells_local_cn_above_30": int((cn > 30).sum()), "notes": "descriptive; z-standardised; cells, not people"}
path = RES / "results.json"
r = json.loads(path.read_text(encoding="utf-8")); r["step8_mgwr"] = out
path.write_text(json.dumps(r, indent=2), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("n_1km", "aicc", "r2", "bandwidths", "local_share_significant", "cells_local_cn_above_30")}, indent=1))
