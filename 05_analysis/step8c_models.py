r"""Step 8c: Model A, B and H3 for the LST-variant sensitivity analyses (S4, S5, S6, S6b, S12, S13, S14, S15, S16) and the
exploratory vacancy rate (Q25). Each variant raster (02_lst/exports/variants/) is joined to the 100 m cells as in
Step 6 (exactextract mean and coverage share; rule 4 recomputed), then the Q19 inference rule is applied through
05_analysis/step8_lib.py. The primary composite, joined the same way, must reproduce Step 8a exactly.
Usage: .venv\Scripts\python.exe 05_analysis/step8c_models.py
"""
import json, pathlib, sys, warnings

import geopandas as gpd
import numpy as np
import pandas as pd
from exactextract import exact_extract

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import step8_lib as L

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
VAR = ROOT / "02_lst/exports/variants"
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
t, DUM = L.prep(pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet"))
P = {v: (t[t.sample_model_A][v].quantile(.10), t[t.sample_model_A][v].quantile(.90)) for v in L.SOC}
cells = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cells")
cells = cells[cells.rule3][["gitter_id_100m", "geometry"]].to_crs(32632)
area = dict(zip(cells.gitter_id_100m, cells.area))
use4 = L.usable(t, "rent") & L.usable(t, "foreign") & L.usable(t, "age65") & L.usable(t, "under18")
covs = t[["elevation", "tree_cover", "imperviousness"]].notna().all(axis=1)
summary, extra = [], {}


def join(path):
    z = exact_extract(str(path), cells, ["mean", "count"], include_cols=["gitter_id_100m"], output="pandas")
    mcol = "band_1_mean" if "band_1_mean" in z else "mean"; ccol = "band_1_count" if "band_1_count" in z else "count"
    z["cover"] = z[ccol] * 900 / z.gitter_id_100m.map(area)
    return z.set_index("gitter_id_100m")[mcol], z.set_index("gitter_id_100m").cover


def run(name, y_col, d, soc=L.SOC):
    d = d.reset_index(drop=True); xa, xb = soc + ["elevation", "ln_pop"] + DUM, soc + ["elevation", "ln_pop", "tree_cover", "imperviousness"] + DUM
    w = L.queen(d); y = d[y_col].values; XA, XB = d[xa].values, d[xb].values
    bid, blocks = L.make_blocks(d)
    bA, bB = L.bootstrap(y, [XA, XB], bid, blocks)
    olsA, olsB = L.ols_np(y, XA), L.ols_np(y, XB)
    semA, semB = L.sem(y, XA, w, xa), L.sem(y, XB, w, xb)
    inf = L.infer(soc, semA, bA, olsA, P, negligible_rule=not name.startswith("S15")); hh = L.h3(bA, bB, olsA, olsB, xa, xb, semA.get("Het"), semB.get("Het"))
    inf.insert(0, "analysis", name); inf.insert(1, "n", len(d)); inf.insert(2, "islands", len(w.islands))
    summary.extend(inf.to_dict(orient="records"))
    for r in hh.itertuples():
        summary.append({"analysis": name, "n": len(d), "variable": "H3_" + r.variable, "beta": r.delta_star, "ci_lo_hull": r.ci_lo,
                        "ci_hi_hull": r.ci_hi, "p_holm": r.p_holm, "verdict": r.verdict})
    extra[name] = {"n": len(d), "islands": len(w.islands), "lambda_het": semA["Het"]["betas"]["lambda"] if semA["Het"] else None,
                   "errors": {k: v for k, v in semA.items() if k.endswith("_error")}, "inference": inf.to_dict(orient="records"),
                   "h3": hh.to_dict(orient="records")}
    print(f"{name}: n {len(d)}; " + "; ".join(f"{r.variable} {r.beta:.3f} {r.verdict}" for r in inf.itertuples()), flush=True)
    return inf


# check: the primary composite joined this way reproduces the Step 6 values and Step 8a
m, c = join(ROOT / "02_lst/exports/lst_anomaly_hot.tif")
t["v_lst"], t["v_cover"] = t.gitter_id_100m.map(m), t.gitter_id_100m.map(c)
dmax = np.nanmax(np.abs(t.v_lst - t.lst_anom)); same4 = ((t.rule3 & (t.v_cover >= 0.7)) == t.rule4).all()
print(f"check: primary join max |diff| {dmax:.2e}, rule 4 identical {same4}"); assert dmax < 1e-9 and same4
prim = run("primary (check)", "v_lst", t[t.rule3 & (t.v_cover >= 0.7) & use4 & covs])
ref = pd.read_csv(RES / "step8_inference.csv")
diff = float(max(abs(prim.beta.values - ref.beta_sem_het.values).max(), abs(prim.p_max.values - ref.p_max.values).max()))
print(f"check: Step 8a reproduced, max |diff| {diff:.2e}"); assert diff < 1e-10 and (prim.verdict.values == ref.verdict.values).all()
extra = {"check_primary_reproduced": diff}; summary = []

lost = {}
for f in sorted(VAR.glob("S*.tif")):
    name = f.stem
    m, c = join(f)
    t["v_lst"], t["v_cover"] = t.gitter_id_100m.map(m), t.gitter_id_100m.map(c)
    s = t.rule3 & (t.v_cover >= 0.7) & use4 & covs
    lost[name] = t[t.sample_model_A & ~s].groupby("city").size().to_dict()
    run(name, "v_lst", t[s])
extra["model_A_cells_lost_by_city"] = lost

# exploratory: vacancy rate as a fifth social variable (per 10 points), primary LST, no Holm with the others
vac = pd.read_csv(ROOT / "01_data/processed/census_vacancy.csv").set_index("gitter_id_100m")
t["vacancy10"] = t.gitter_id_100m.map(vac.vacancy) / 10
okv = t.gitter_id_100m.map(vac.vacancy).notna() & ~t.gitter_id_100m.map(vac.vacancy_br).fillna(False).astype(bool)
d = t[t.sample_model_A & okv].reset_index(drop=True)
xv = L.SOC + ["vacancy10", "elevation", "ln_pop"] + DUM
sv = L.sem(d.lst_anom.values, d[xv].values, L.queen(d), xv)
extra["Exploratory Q25 vacancy rate"] = {"n": len(d), "zero_share": float((d.vacancy10 == 0).mean()),
                                         **{est: (None if sv[est] is None else {k: sv[est][k]["vacancy10"] for k in ("betas", "se", "p")}) for est in ("Het", "Hom")}}
print("vacancy:", extra["Exploratory Q25 vacancy rate"])
info = json.loads((VAR / "variants_info.json").read_text(encoding="utf-8"))
extra["variants_info"] = info

pd.DataFrame(summary).to_csv(RES / "step8c_sensitivity.csv", index=False)


def clean(o):
    if isinstance(o, float) and o != o:
        return None
    return {k: clean(v) for k, v in o.items()} if isinstance(o, dict) else [clean(v) for v in o] if isinstance(o, list) else o


path = RES / "results.json"
res = json.loads(path.read_text(encoding="utf-8"))
res["step8c"] = clean(json.loads(json.dumps(extra, default=lambda o: o.item() if hasattr(o, "item") else str(o))))
path.write_text(json.dumps(clean(res), indent=2, allow_nan=False), encoding="utf-8")
print("done")
