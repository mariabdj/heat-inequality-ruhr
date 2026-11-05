r"""Builds the article from manuscript_template.md: every {{name}} is replaced by a number read from the result files.
No number in the results is typed by hand. Rounding (guide A3): temperatures and effects in degrees C to 2 decimals
when they are model effects, 1 decimal when they are mean temperatures; coefficients to 2 or 3 decimals; p to 3
decimals; counts as integers; shares to whole %.
Writes manuscript.md and numbers_used.json (each name, its full-precision value and the printed text).
Usage (from the project root): .venv\Scripts\python.exe 06_manuscript/build_manuscript.py
"""
import json, pathlib, re

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
MS = ROOT / "06_manuscript"
R = json.loads((RES / "results.json").read_text(encoding="utf-8"))
N = {}                                      # name -> (value, printed text)


def put(name, value, fmt):
    assert name not in N, name
    v = float(value) if not isinstance(value, str) else value
    if fmt == "year":
        txt = str(int(v))
    elif fmt == "int":
        txt = f"{int(round(v)):,}"
    elif fmt == "pct":
        txt = f"{v:.0f}"
    elif fmt == "p":
        txt = "< .001" if v < .001 else f"{v:.3f}".lstrip("0")
    elif fmt.startswith("f"):
        txt = f"{v:.{int(fmt[1:])}f}"
        txt = (txt[1:] if txt.startswith("-") and float(txt) == 0 else txt).replace("-", "−")
    else:
        raise ValueError(fmt)
    N[name] = (v, txt)


# ---- sample (Step 6) ----------------------------------------------------------------------------------------
ex = pd.read_csv(RES / "step6_exclusions.csv").set_index("step").cells
put("n_rule1", ex["inhabited cells in the 11 cities (rule 1)"], "int")
put("n_rm_pop", ex["removed: population < 10 (rule 2)"], "int")
put("n_rm_water", ex["removed: >= 50% permanent water (rule 3)"], "int")
put("n_rm_lst", ex["removed: < 70% of area with LST composite (rule 4)"], "int")
put("n_rule4", ex["cells passing rules 1 to 4"], "int")
for v in ("rent", "foreign", "age65", "under18"):
    put(f"n_use_{v}", ex[f"  of which {v} usable (present, not bracketed)"], "int")
put("n_A", ex["Model A sample (rule 5: all four social variables usable)"], "int")
sc = pd.read_csv(RES / "step6_sample_comparison.csv", header=[0, 1], index_col=0)
tot = sc.loc["TOTAL"]
put("pop_rule4", tot[("rule4_all", "population")], "int")
put("pop_A", tot[("model_A", "population")], "int")
put("share_cells_A", 100 * tot[("model_A", "cells")] / tot[("rule4_all", "cells")], "f1")
put("share_pop_A", 100 * tot[("model_A", "population")] / tot[("rule4_all", "population")], "pct")
put("lst_pw_rule4", tot[("rule4_all", "pw_mean_lst_anom")], "f1")
put("lst_pw_A", tot[("model_A", "pw_mean_lst_anom")], "f1")
put("imp_med_rule4", tot[("rule4_all", "median_imperviousness")], "pct")
put("imp_med_A", tot[("model_A", "median_imperviousness")], "pct")
put("tree_med_rule4", tot[("rule4_all", "median_tree_cover")], "f1")
put("tree_med_A", tot[("model_A", "median_tree_cover")], "f1")
put("medpop_rule4", tot[("rule4_all", "median_population")], "int")
put("medpop_A", tot[("model_A", "median_population")], "int")

# ---- heat (Step 4) ------------------------------------------------------------------------------------------
sc4 = pd.read_csv(ROOT / "02_lst/scenes_used_hot.csv")
put("n_scenes", len(sc4), "int")
put("n_scenes_l8", (sc4.spacecraft == "LANDSAT_8").sum(), "int")
put("n_scenes_l9", (sc4.spacecraft == "LANDSAT_9").sum(), "int")
put("n_p196", (sc4.path == 196).sum(), "int")
put("n_p197", (sc4.path == 197).sum(), "int")
put("scene_med_min", sc4.median_c.min(), "f1")
put("scene_med_max", sc4.median_c.max(), "f1")
put("valid_min", 100 * sc4.valid_share.min(), "pct")
put("first_year", pd.to_datetime(sc4.date).dt.year.min(), "year")
put("last_year", pd.to_datetime(sc4.date).dt.year.max(), "year")
lan = pd.read_csv(RES / "step4_lanuk_check.csv").iloc[0]
put("lanuk_rho", lan.spearman, "f2")
put("lanuk_px", lan.pixels, "int")

# ---- descriptive (Step 7) -----------------------------------------------------------------------------------
s7 = R["step7"]
mor = s7["moran"]
for k, nm in [("lst_anom", "lst"), ("rent", "rent"), ("foreign", "foreign"), ("age65", "age65"), ("under18", "under18")]:
    put(f"moran_{nm}", mor[k]["I"], "f2")
grp = s7["group_vs_rest_exploratory"]
put("grp_foreign_members", grp["foreign"]["group_mean_lst_anom"], "f1")
put("grp_foreign_rest", grp["foreign"]["rest_mean_lst_anom"], "f1")

# ---- Step 8a --------------------------------------------------------------------------------------------------
a = R["step8a"]
ols = a["ols"]["A"]
put("ols_r2", ols["r2"], "f2")
put("ols_moran", ols["moran_residuals"]["I"], "f2")
put("lm_err", ols["robust_LM_error"]["stat"], "f0")
put("lm_lag", ols["robust_LM_lag"]["stat"], "f0")
put("vif_max", max(a["vif"]["A"].values()), "f1")
put("islands", a["W_model_A"]["islands"], "int")
put("islands_pct", 100 * a["W_model_A"]["islands"] / a["n_model_A"], "f1")
put("n_blocks", sum(a["blocks_per_city"].values()), "int")
inf = pd.DataFrame(a["inference"]).set_index("variable")
for v, nm in [("rent", "rent"), ("foreign10", "for"), ("age65_10", "a65"), ("under18_10", "u18")]:
    r = inf.loc[v]
    put(f"b_{nm}", r.beta_sem_het, "f3")
    put(f"b_{nm}_lo", r.ci_lo_hull, "f3"); put(f"b_{nm}_hi", r.ci_hi_hull, "f3")
    put(f"bols_{nm}", r.beta_ols, "f3")
    put(f"p_{nm}", r.p_holm, "p")
    put(f"e_{nm}", r.effect_P10_P90, "f2")
    put(f"e_{nm}_lo", r.effect_ci_lo, "f2"); put(f"e_{nm}_hi", r.effect_ci_hi, "f2")
    put(f"p10_{nm}", r.P10 * (10 if nm != "rent" else 1), "f2" if nm == "rent" else "f1")
    put(f"p90_{nm}", r.P90 * (10 if nm != "rent" else 1), "f2" if nm == "rent" else "f1")
h3 = pd.DataFrame(a["h3"]).set_index("variable")
for v, nm in [("rent", "rent"), ("foreign10", "for")]:
    put(f"h3_{nm}", h3.loc[v, "delta_star"], "f3")
    put(f"h3_{nm}_lo", h3.loc[v, "ci_lo"], "f3"); put(f"h3_{nm}_hi", h3.loc[v, "ci_hi"], "f3")
    put(f"h3_{nm}_p", h3.loc[v, "p_holm"], "p")
    put(f"bB_ols_{nm}", h3.loc[v, "beta_B_ols"], "f3")
put("h3_rent_R", h3.loc["rent", "R_percent"], "pct")
put("h3_for_R", h3.loc["foreign10", "R_percent"], "pct")
sv = pd.DataFrame(R["step8_reporting"]["single_variable_effects"]).set_index("variable")
for v, nm in [("rent", "rent"), ("foreign10", "for"), ("age65_10", "a65"), ("under18_10", "u18")]:
    put(f"sv_{nm}", sv.loc[v, "effect_P10_P90"], "f2")
    put(f"sv_{nm}_lo", sv.loc[v, "effect_ci_lo"], "f2"); put(f"sv_{nm}_hi", sv.loc[v, "effect_ci_hi"], "f2")
    put(f"sv_{nm}_n", sv.loc[v, "n"], "int")

# ---- reporting tables (expert review) -------------------------------------------------------------------------
rp = R["step8_reporting"]
mis = rp["misspecification"]
put("lam_2b", mis["lambda_step2b"], "f2"); put("lam_it", mis["lambda_iterated"], "f2")
mrow = pd.DataFrame(mis["rows"]).set_index("variable")
put("e_for_2b", mrow.loc["foreign10", "effect_P10_P90_step2b_exploratory"], "f2")
put("e_for_it", mrow.loc["foreign10", "effect_P10_P90_iterated_exploratory"], "f2")
hs = pd.DataFrame(rp["h3_under_sem"]).set_index("variable")
put("h3sem_rent", hs.loc["rent", "delta_star_sem_own_sign"], "f3"); put("h3sem_for", hs.loc["foreign10", "delta_star_sem_own_sign"], "f3")
s18 = pd.DataFrame(rp["s18_beta_plus_theta_descriptive"]).set_index("variable")
put("s18_rent", s18.loc["rent", "beta_plus_theta"], "f2"); put("s18_rent_lo", s18.loc["rent", "ci_lo"], "f2"); put("s18_rent_hi", s18.loc["rent", "ci_hi"], "f2")
put("s18_for", s18.loc["foreign10", "beta_plus_theta"], "f2"); put("s18_for_lo", s18.loc["foreign10", "ci_lo"], "f2"); put("s18_for_hi", s18.loc["foreign10", "ci_hi"], "f2")
same = [d for d in rp["residents_vs_cells_foreign"] if d["quantity"].startswith("SAME SAMPLE")]
put("rc_all_pooled", rp["residents_vs_cells_foreign"][2]["value_C"], "f2")
put("rc_all_within", rp["residents_vs_cells_foreign"][3]["value_C"], "f2")
put("rc_A_sv_sem", same[0]["value_C"], "f2"); put("rc_A_sv_ols", same[1]["value_C"], "f2")
put("rc_A_pooled", same[2]["value_C"], "f2"); put("rc_A_within", same[3]["value_C"], "f2")
put("exp_gap", rp["exposure_gap_points_foreign_share"], "f1")
dc = pd.DataFrame(rp["resident_gap_decomposition_exploratory"]).set_index("step").implied_resident_gap_C
put("dg_raw", dc["raw slope, unweighted"], "f2"); put("dg_city", dc["city dummies only, unweighted"], "f2")
put("dg_city_lp", dc["city + log population only, unweighted"], "f2"); put("dg_city_el", dc["city + elevation only, unweighted"], "f2")
put("dg_sv", dc["plus elevation and log population (single-variable OLS)"], "f2")
put("dg_sem1", dc["full Model A SEM, step-1 lambda (reported)"], "f2"); put("dg_semit", dc["full Model A SEM, iterated lambda (exploratory)"], "f2")
put("dg_lp_share", 100 * (dc["city dummies only, unweighted"] - dc["city + log population only, unweighted"])
    / (dc["city dummies only, unweighted"] - dc["plus elevation and log population (single-variable OLS)"]), "pct")
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet"); A = t[t.sample_model_A]
m = A.foreign / 100 * A.einwohner_n
put("expo_for", np.average(A.foreign, weights=m), "f1"); put("expo_rest", np.average(A.foreign, weights=A.einwohner_n - m), "f1")

# ---- sensitivity (8b, 8c) ---------------------------------------------------------------------------------------
b8 = pd.read_csv(RES / "step8b_sensitivity.csv"); c8 = pd.read_csv(RES / "step8c_sensitivity.csv")
allsens = pd.concat([b8, c8])
fr = allsens[(allsens.variable == "foreign10") & allsens.verdict.notna() & ~allsens.analysis.str.startswith(("S10", "S8"))]
put("n_sens_for", len(fr), "int"); put("n_sens_for_sup", (fr.verdict == "supported").sum(), "int")
pre = fr[~fr.analysis.str.startswith("Exploratory")]
assert (pre.verdict == "supported").all() and (fr.verdict == "supported").all()
put("n_sens_prereg", len(pre), "int")
fe = fr[~fr.analysis.str.startswith(("S15", "S7"))]
put("sens_for_min", fe.effect_P10_P90.min(), "f2"); put("sens_for_max", fe.effect_P10_P90.max(), "f2")
cit = b8[b8.analysis.str.startswith("S10") & (b8.variable == "foreign10")]
put("s10_pos", (cit.beta > 0).sum(), "int"); put("s10_sup", (cit.verdict == "supported").sum(), "int")
put("s10_nmin", cit.n.min(), "int"); put("s10_nmax", cit.n.max(), "int")
put("eols_for", inf.loc["foreign10", "beta_ols"] * (inf.loc["foreign10", "P90"] - inf.loc["foreign10", "P10"]), "f2")
put("ratio_for", inf.loc["foreign10", "beta_ols"] / inf.loc["foreign10", "beta_sem_het"], "f1")
s3 = b8[b8.analysis.str.startswith("S3")].set_index("variable")
put("s3_rent", s3.loc["rent", "effect_P10_P90"], "f2"); put("s3_for", s3.loc["foreign10", "effect_P10_P90"], "f2")
s7 = b8[b8.analysis.str.startswith("S7")].set_index("variable")
put("s7_for_n", s7.loc["foreign10", "n"], "int")
s71 = pd.DataFrame(rp["s7_effects_1km_percentiles"]).set_index("variable")
put("s7_for_1km", s71.loc["foreign10", "effect_1km"], "f2"); put("s7_rent_1km", s71.loc["rent", "effect_1km"], "f2")
s8 = b8[b8.analysis.str.startswith("S8")].set_index("variable")
put("s8_for", s8.loc["foreign10", "effect_P10_P90"], "f2")
s20 = b8[b8.analysis.str.startswith("S20")].set_index("variable")
put("s20_for", s20.loc["foreign10", "effect_P10_P90"], "f2")
vac = R["step8c"]["Exploratory Q25 vacancy rate"]
put("vac_b", vac["Het"]["betas"], "f2"); put("vac_n", vac["n"], "int"); put("vac_zero", 100 * vac["zero_share"], "pct")

# ---- MGWR ---------------------------------------------------------------------------------------------------------
mg = R["step8_mgwr"]
put("mg_n", mg["n_1km"], "int"); put("mg_r2", mg["r2"], "f2"); put("mg_aicc", mg["aicc"], "f1")
put("mg_ols_aicc", mg["ols_same_cells"]["aicc"], "f1"); put("mg_ols_r2", mg["ols_same_cells"]["r2"], "f2")
for k in ("intercept", "rent", "foreign10", "age65_10", "under18_10", "tree_cover", "imperviousness", "elevation", "ln_pop"):
    put(f"bw_{k}", mg["bandwidths"][k], "int")
put("mg_for_sig", 100 * mg["local_share_significant"]["foreign10"], "pct")
put("mg_moran", mg["residual_moran_I"]["I"], "f2")

# ---- round 1 additions: scene funnel, data quality, rent and age disagreement, Q25 ----------------------------------
st1 = pd.read_csv(ROOT / "02_lst/scenes_stage1.csv")
put("n_cand", len(st1), "int"); put("n_hotday", st1.hot_day.sum(), "int"); put("n_ok80", (st1.valid_share >= .8).sum(), "int")
put("n_june", (pd.to_datetime(sc4.date).dt.month == 6).sum(), "int")
vi = json.loads((ROOT / "02_lst/exports/variants/variants_info.json").read_text(encoding="utf-8"))["S16_stqa_K_valid_pixels"]
put("stqa_med", vi["p50"], "f2"); put("stqa_gt3", 100 * vi["share_above_3K"], "f1")
r4t = t[t.rule4]
put("onepath_only", r4t.one_path_only.sum(), "int"); put("onepath_partly", r4t.one_path_partly.sum(), "int")
put("onepath_A", A.one_path_partly.sum(), "int")
q25 = R["step8b"]["Exploratory Q25 rent x tree cover"]
put("q25_p_het", q25["Het"]["p"], "p")
def b8row(name, v):
    return b8[(b8.analysis.str.startswith(name)) & (b8.variable == v)].iloc[0]
for v, nm in [("rent", "rent"), ("age65_10", "a65"), ("under18_10", "u18")]:
    r7 = b8row("S7", v); r8 = b8row("S8", v)
    put(f"s7_{nm}", r7.effect_P10_P90, "f2"); put(f"s7_{nm}_lo", r7.effect_ci_lo, "f2"); put(f"s7_{nm}_hi", r7.effect_ci_hi, "f2")
    put(f"s8_{nm}", r8.effect_P10_P90, "f2"); put(f"s8_{nm}_lo", r8.effect_ci_lo, "f2"); put(f"s8_{nm}_hi", r8.effect_ci_hi, "f2")
mu = b8row("S10 M", "rent"); do = b8row("S10 Dortmund", "rent")
put("mul_rent", mu.effect_P10_P90, "f2"); put("mul_rent_lo", mu.effect_ci_lo, "f2"); put("mul_rent_hi", mu.effect_ci_hi, "f2")
put("dor_rent", do.effect_P10_P90, "f2"); put("dor_rent_lo", do.effect_ci_lo, "f2"); put("dor_rent_hi", do.effect_ci_hi, "f2")
put("sv_A_sem", rp["residents_vs_cells_foreign"][4]["value_C"], "f2")
put("eols_rent", -inf.loc["rent", "beta_ols"] * (inf.loc["rent", "P90"] - inf.loc["rent", "P10"]), "f2")

# table: which analyses disagree (effects P10 to P90 in C, rent sign reversed)
def eff(v, b):
    lo, hi = inf.loc[v, "P10"], inf.loc[v, "P90"]
    return (-1 if v == "rent" else 1) * b * (hi - lo)
boot = pd.read_csv(RES / "step8_boot_betas_A.csv")
s18v = s18
lines = ["| Analysis | Rent (sign reversed) | Aged 65+ | Under 18 | Foreign citizens |", "|---|---|---|---|---|"]
def cellfmt(e, lo, hi):
    lo, hi = sorted([lo, hi]); fx = lambda x: (f"{x:.2f}"[1:] if f"{x:.2f}".startswith("-") and float(f"{x:.2f}") == 0 else f"{x:.2f}").replace("-", "−")
    return f"{fx(e)} ({fx(lo)} to {fx(hi)})"
V = [("rent", "rent"), ("age65_10", "a65"), ("under18_10", "u18"), ("foreign10", "for")]
lines.append("| Primary: spatial error model (reported hull) | " + " | ".join(cellfmt(inf.loc[v, "effect_P10_P90"], inf.loc[v, "effect_ci_lo"], inf.loc[v, "effect_ci_hi"]) for v, _ in V) + " |")
lines.append("| OLS, block bootstrap 95% interval | " + " | ".join(cellfmt(eff(v, inf.loc[v, "beta_ols"]), eff(v, np.percentile(boot[v], 2.5)), eff(v, np.percentile(boot[v], 97.5))) for v, _ in V) + " |")
for nm, lab in [("S3", "S3 population-weighted OLS"), ("S7", "S7 1 km grid (100 m percentiles)"), ("S8", "S8 spatial lag model, total effect")]:
    lines.append(f"| {lab} | " + " | ".join(cellfmt(b8row(nm, v).effect_P10_P90, b8row(nm, v).effect_ci_lo, b8row(nm, v).effect_ci_hi) for v, _ in V) + " |")
lines.append("| S18 own cell plus neighbours (β + θ), descriptive | " + " | ".join(cellfmt(eff(v, s18v.loc[v, "beta_plus_theta"]), eff(v, s18v.loc[v, "ci_lo"]), eff(v, s18v.loc[v, "ci_hi"])) for v, _ in V) + " |")
N["tab_disagree"] = (0.0, "\n".join(lines))

# ---- exploratory checks D17 (air temperature) and D18 (resolution, observations) ----------------------------------
ck = R["step9_checks"]
def inf_of(m, v):
    return next(r for r in m["inference"] if r["variable"] == v)
a18 = ck["D18a_smoothed_3x3"]
for v, nm in [("foreign10", "for"), ("age65_10", "a65"), ("under18_10", "u18"), ("rent", "rent")]:
    r = inf_of(a18, v); put(f"d18a_{nm}", r["effect_P10_P90"], "f2"); put(f"d18a_{nm}_lo", r["effect_ci_lo"], "f2"); put(f"d18a_{nm}_hi", r["effect_ci_hi"], "f2")
put("d18a_lam", a18["lambda_het"], "f2")
b18 = ck["D18b_nobs"]
put("d18b_cor_max", max(abs(v) for v in b18["spearman_with_nobs"].values()), "f2")
put("d18b_n", b18["model_nobs_ge_12"]["n"], "int"); put("d18b_for", inf_of(b18["model_nobs_ge_12"], "foreign10")["effect_P10_P90"], "f2")
air = ck["D17_air_temperature"]
for tod in ("day", "night"):
    m = air[f"air_{tod}"]
    for v, nm in [("foreign10", "for"), ("age65_10", "a65"), ("under18_10", "u18"), ("rent", "rent")]:
        r = inf_of(m["model_1km"], v)
        put(f"air_{tod}_{nm}", r["effect_P10_P90"], "f2"); put(f"air_{tod}_{nm}_lo", r["effect_ci_lo"], "f2"); put(f"air_{tod}_{nm}_hi", r["effect_ci_hi"], "f2")
    put(f"air_{tod}_gapA", m["resident_gap_foreign"]["model_A_cells"], "f2"); put(f"air_{tod}_gapAll", m["resident_gap_foreign"]["all_usable_foreign_cells"], "f2")
put("air_n1km", air["air_day"]["model_1km"]["n"], "int")
put("lst1km_for", inf_of(air["lst_same_1km_cells"], "foreign10")["effect_P10_P90"], "f2")
ac = pd.read_csv(ROOT / "01_data/processed/air_temperature_cells.csv")
ac = ac[ac.gitter_id_100m.isin(r4t.gitter_id_100m)]   # same cells as the LST standard deviation
put("air_day_sd", ac.air_day.std(), "f2"); put("air_night_sd", ac.air_night.std(), "f2"); put("lst_sd", r4t.lst_anom.std(), "f1")

put("d18a_b_for", next(r for r in a18["inference"] if r["variable"] == "foreign10")["beta"], "f3")
put("s18_rent_eff", eff("rent", s18v.loc["rent", "beta_plus_theta"]), "f2")
_lo, _hi = sorted([eff("rent", s18v.loc["rent", "ci_lo"]), eff("rent", s18v.loc["rent", "ci_hi"])])
put("s18_rent_eff_lo", _lo, "f2"); put("s18_rent_eff_hi", _hi, "f2")
put("s18_for_beta_eff", b8row("S18", "foreign10").effect_P10_P90, "f2")
_tc = r4t.groupby("city").tree_cover.median()
put("tree_med_hamm", _tc["Hamm"], "f1"); put("tree_med_others_lo", _tc.drop("Hamm").min(), "f1"); put("tree_med_others_hi", _tc.drop("Hamm").max(), "f1")

put("n_sens_distinct", len(pre[~pre.analysis.str.startswith("S17")]), "int")
put("d18a_expgap", a18["exposure_gap_points_smoothed"], "f1"); put("d18a_implied", a18["implied_resident_gap_C"], "f2")

# ---- render ---------------------------------------------------------------------------------------------------------
tpl = (MS / "manuscript_template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", tpl)) - set(N))
assert not missing, f"unknown names in the template: {missing}"
out = re.sub(r"\{\{(\w+)\}\}", lambda mt: N[mt.group(1)][1], tpl)
(MS / "manuscript.md").write_text(out, encoding="utf-8")
used = sorted(set(re.findall(r"\{\{(\w+)\}\}", tpl)))
(MS / "numbers_used.json").write_text(json.dumps({k: {"value": N[k][0], "printed": N[k][1]} for k in used}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"manuscript.md written: {len(used)} names used, {len(N)} available, {len(out.split())} words")

# ---- Supplementary Table S1: every analysis with a P10-P90 effect -------------------------------------------------
cols = ["analysis", "variable", "n", "beta", "ci_lo_hull", "ci_hi_hull", "p_holm", "effect_P10_P90", "effect_ci_lo", "effect_ci_hi", "verdict"]
prim = pd.read_csv(RES / "step8_inference.csv").rename(columns={"beta_sem_het": "beta"}).assign(analysis="Primary (Model A)", n=R["step8a"]["n_model_A"])
s1 = pd.concat([prim[cols], b8[b8.variable.isin(["rent", "foreign10", "age65_10", "under18_10"])][cols],
                c8[c8.variable.isin(["rent", "foreign10", "age65_10", "under18_10"])][cols]], ignore_index=True)
ck9 = pd.read_csv(RES / "step9_checks.csv")
ck9["verdict"] = ck9.verdict + " (exploratory)"
s1 = pd.concat([s1, ck9[cols]], ignore_index=True)
s1.to_csv(MS / "supplementary_table_S1.csv", index=False)
f = lambda x, d: "" if pd.isna(x) else (lambda s: (s[1:] if s.startswith("-") and float(s) == 0 else s).replace("-", "−"))(f"{x:.{d}f}")
VARL = {"rent": "Rent (per EUR/m², sign reversed in the effect)", "foreign10": "Foreign citizens (per 10 points)",
        "age65_10": "Aged 65+ (per 10 points)", "under18_10": "Under 18 (per 10 points)"}
ANL = {"S1 bracketed included": "S1 uncertain (bracketed) values included", "S2 no rent restriction": "S2 rent term left out (more cells)",
       "S3 population-weighted (WLS, D9)": "S3 population-weighted OLS (deviation D9)", "S7 1 km grid": "S7 1 km grid (100 m percentiles, deviation D13)",
       "S8 spatial lag (total impact)": "S8 spatial lag model (total effect)", "S9 8 nearest neighbours": "S9 8 nearest neighbours",
       "S11 population >= 3": "S11 minimum 3 residents (not 10)", "S11 population >= 30": "S11 minimum 30 residents (not 10)",
       "S17 300 m window covariates": "S17 covariates in a 300 m window (Model B only)", "S18 spatial Durbin error": "S18 spatial Durbin error model",
       "S19 2 km blocks": "S19 2 km bootstrap blocks", "S20 islands dropped": "S20 cells without neighbours dropped",
       "Exploratory D2 dashes as missing": "Exploratory: census dashes as missing", "S4_all_summer": "S4 hot-day rule relaxed (+1 scene)",
       "S5_absolute": "S5 absolute LST, not anomaly", "S6_landsat8": "S6 Landsat 8 only", "S6b_path196": "S6b orbit path 196 only",
       "S6b_path197": "S6b orbit path 197 only", "S12_valid95": "S12 scenes with 95%+ valid pixels", "S13_city_median": "S13 anomaly from the city median",
       "S14_yearly_mean": "S14 mean of yearly composites", "S15_standardised": "S15 standardised anomaly (no °C)", "S16_stqa3K": "S16 pixels with LST uncertainty > 3 K masked", "D18a 3x3 smoothed regressors": "D18a regressors as 3 x 3 window means", "D18b cells with >= 12 observations": "D18b cells with 12+ of 16 observations",
       "D17 air_day 1 km": "D17 air temperature by day, 1 km (HOSTRADA, modelled)", "D17 air_night 1 km": "D17 air temperature at night, 1 km (HOSTRADA, modelled)",
       "D17 LST same 1 km cells (air_day)": "D17 LST on the same 1 km cells"}
VERD = {"not supported (inconclusive)": "inconclusive"}
lines = ["# Supplementary Table S1. All analyses with a P10 to P90 effect", "",
         "β per unit with the reported 95% interval (hull of the three intervals); Holm-adjusted p; P10 to P90 effect in °C (S15: standardised "
         "units; S8: total effect, judged by its interval only, no p); rent effect with its sign reversed (positive = hotter where rent is low). "
         "\"Practically negligible\" = whole interval within ±0.3 °C. Deviation codes refer to 00_protocol/deviations.md in the repository. "
         "Full-precision values: supplementary_table_S1.csv.", "",
         "| Analysis | Variable | n | β | 95% interval | Holm p | Effect | 95% interval | Verdict |", "|---|---|---|---|---|---|---|---|---|"]
for r in s1.itertuples():
    lines.append(f"| {ANL.get(r.analysis, r.analysis)} | {VARL[r.variable]} | {int(r.n):,} | {f(r.beta, 3)} | {f(r.ci_lo_hull, 3)} to {f(r.ci_hi_hull, 3)} | "
                 f"{'' if pd.isna(r.p_holm) else ('< .001' if r.p_holm < .001 else f'{r.p_holm:.3f}'.lstrip('0'))} | {f(r.effect_P10_P90, 2)} | "
                 f"{f(r.effect_ci_lo, 2)} to {f(r.effect_ci_hi, 2)} | {'' if pd.isna(r.verdict) else VERD.get(r.verdict, r.verdict).replace('+-0.3 C', '±0.3 °C')} |")
(MS / "supplementary_table_S1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"supplementary table S1: {len(s1)} rows")

# ---- Supplementary Table S0: the scenes ------------------------------------------------------------------------------
s0 = sc4.copy(); s0["date"] = pd.to_datetime(s0.date).dt.date
lines = ["# Supplementary Table S0. The 16 Landsat scenes used", "", f"Selection: {len(st1)} candidate scenes (paths 196 and 197, row 24, June to August "
         f"{N['first_year'][1]} to {N['last_year'][1]}); {int(st1.hot_day.sum())} on hot days (daily maximum at Essen-Bredeney at least 25 °C); "
         f"{len(sc4)} of these with at least 80% valid pixels in the core area. Time: scene centre (UTC). Median: median LST of the valid core pixels (°C), "
         "subtracted to form the anomaly.", "", "| Date | Satellite | Path | Time (UTC) | Valid core pixels (%) | Median LST (°C) |", "|---|---|---|---|---|---|"]
for r in s0.sort_values("date").itertuples():
    lines.append(f"| {r.date} | {r.spacecraft.replace('_', ' ').title()} | {r.path} | {r.time[:5]} | {100 * r.valid_share:.1f} | {r.median_c:.1f} |")
(MS / "supplementary_table_S0.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("supplementary table S0:", len(s0), "scenes")
