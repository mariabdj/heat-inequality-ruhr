r"""Gate 9: numbers in the article.
1. Recomputes key numbers from the result files with its own code (not build_manuscript.py) and compares them with
   06_manuscript/numbers_used.json (relative difference below 1e-9).
2. Checks that every number recorded in numbers_used.json appears, as printed, in manuscript.md.
3. Lists every number typed directly in manuscript_template.md (outside {{...}} and the reference list), for the
   manual check of the gate.
Usage: .venv\Scripts\python.exe verification/verify_manuscript_numbers.py [numbers_used.json]
"""
import json, pathlib, re, sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
used = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "06_manuscript/numbers_used.json").read_text(encoding="utf-8"))
ms = (ROOT / "06_manuscript/manuscript.md").read_text(encoding="utf-8")
ok = True

# 1. independent recomputation
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
r4 = t[t.rule4]; A = t[t.sample_model_A]
inf = pd.read_csv(RES / "step8_inference.csv").set_index("variable")
h3 = pd.read_csv(RES / "step8_h3.csv").set_index("variable")
b8 = pd.read_csv(RES / "step8b_sensitivity.csv"); c8 = pd.read_csv(RES / "step8c_sensitivity.csv")
J = json.loads((RES / "results.json").read_text(encoding="utf-8"))
dec = pd.read_csv(RES / "step8_reporting_resident_gap_decomposition.csv").set_index("step").implied_resident_gap_C
scenes = pd.read_csv(ROOT / "02_lst/scenes_used_hot.csv")
mem = A.foreign / 100 * A.einwohner_n; oth = A.einwohner_n - mem
SRC = {"foreign10": ("foreign", 10), "rent": ("rent", 1)}   # unit of the coefficient: 10 points of share, 1 EUR/m2
span = lambda v: (A[SRC[v][0]].quantile(.9) - A[SRC[v][0]].quantile(.1)) / SRC[v][1]
own = {
    "n_rule1": len(t), "n_rule4": int(t.rule4.sum()), "n_A": int(t.sample_model_A.sum()),
    "pop_rule4": r4.einwohner_n.sum(), "pop_A": A.einwohner_n.sum(),
    "share_cells_A": 100 * len(A) / len(r4), "share_pop_A": 100 * A.einwohner_n.sum() / r4.einwohner_n.sum(),
    "lst_pw_A": np.average(A.lst_anom, weights=A.einwohner_n), "lst_pw_rule4": np.average(r4.lst_anom, weights=r4.einwohner_n),
    "n_scenes": len(scenes), "scene_med_min": scenes.median_c.min(), "scene_med_max": scenes.median_c.max(),
    "b_for": inf.loc["foreign10", "beta_sem_het"], "p_for": inf.loc["foreign10", "p_holm"], "p_rent": inf.loc["rent", "p_holm"],
    "e_for": inf.loc["foreign10", "beta_sem_het"] * span("foreign10"),
    "e_rent": -inf.loc["rent", "beta_sem_het"] * span("rent"),
    "e_for_lo": inf.loc["foreign10", "ci_lo_hull"] * span("foreign10"), "e_for_hi": inf.loc["foreign10", "ci_hi_hull"] * span("foreign10"),
    "p90_for": A.foreign.quantile(.9), "p10_rent": A.rent.quantile(.1), "p90_rent": A.rent.quantile(.9),
    "eols_for": inf.loc["foreign10", "beta_ols"] * span("foreign10"),
    "ratio_for": inf.loc["foreign10", "beta_ols"] / inf.loc["foreign10", "beta_sem_het"],
    "h3_rent": inf.loc["rent", "beta_ols"] - h3.loc["rent", "beta_B_ols"], "h3_for": inf.loc["foreign10", "beta_ols"] - h3.loc["foreign10", "beta_B_ols"],
    "expo_for": np.average(A.foreign, weights=mem), "expo_rest": np.average(A.foreign, weights=oth),
    "exp_gap": np.average(A.foreign, weights=mem) - np.average(A.foreign, weights=oth),
    "rc_A_pooled": np.average(A.lst_anom, weights=mem) - np.average(A.lst_anom, weights=oth),
    "dg_sem1": dec["full Model A SEM, step-1 lambda (reported)"],
    "s10_sup": int(((b8.analysis.str.startswith("S10")) & (b8.variable == "foreign10") & (b8.verdict == "supported")).sum()),
    "s10_pos": int(((b8.analysis.str.startswith("S10")) & (b8.variable == "foreign10") & (b8.beta > 0)).sum()),
    "s3_for": b8[(b8.analysis.str.startswith("S3")) & (b8.variable == "foreign10")].effect_P10_P90.iloc[0],
    "mg_r2": J["step8_mgwr"]["r2"], "mg_aicc": J["step8_mgwr"]["aicc"], "bw_intercept": J["step8_mgwr"]["bandwidths"]["intercept"],
    "moran_lst": J["step7"]["moran"]["lst_anom"]["I"], "islands": J["step8a"]["W_model_A"]["islands"],
}
fs = pd.concat([b8, c8]); fs = fs[(fs.variable == "foreign10") & fs.verdict.notna() & ~fs.analysis.str.startswith(("S10", "S8"))]
own["n_sens_for"] = len(fs); own["n_sens_for_sup"] = int((fs.verdict == "supported").sum())
for k, v in own.items():
    if k not in used:
        print(f"note    {k}: not used in the article"); continue
    u = used[k]["value"]
    good = abs(u - float(v)) <= 1e-9 * max(1, abs(float(v)))
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}    {k}: article {u!r}, recomputed {float(v)!r}")

# 2. every printed value is in the text
for k, d in used.items():
    if d["printed"] not in ms:
        print(f"FAIL    {k}: printed text {d['printed']!r} not found in manuscript.md"); ok = False
print(f"checked: {len(own)} recomputed, {len(used)} names present in the text")

# 3. numbers typed in the template
tpl = (ROOT / "06_manuscript/manuscript_template.md").read_text(encoding="utf-8").split("\n## References")[0]
tpl = re.sub(r"\{\{\w+\}\}", "", tpl)
tpl = re.sub(r"https?://\S+|\]\([^)]*\)|`[^`]*`", "", tpl)
typed = sorted(set(re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", tpl)), key=lambda s: float(s.replace(",", "")))
print("typed numbers in the template (manual check):", ", ".join(typed))
print("RESULT:", "PASSED" if ok else "FAILED")
sys.exit(0 if ok else 1)
