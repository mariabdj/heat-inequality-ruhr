r"""Step 7: descriptive results (preregistration Q19, "Descriptive"). Descriptions only, not tests of H1 to H3.
Sample per variable: cells passing rules 1 to 4 with that variable usable (present, not bracketed). Results describe
cells, not people (ecological fallacy); no causal reading.
1. Population-weighted mean LST anomaly by city-specific decile of each social variable (cells, not people).
   Clarified rule (deviation D4): cells with the value 0 (dash: zero or changed to zero) form a separate "zero" group;
   the non-zero values are cut, within each city, into 10 classes by rank with ties sharing the lowest rank
   (decile = ceil(rank_min / n * 10)), so equal values always fall in the same class. Cell counts, population and median
   population are reported per class. Groups are pooled across cities after the assignment within each city.
   The zero group is mostly small cells (secrecy turns their small non-zero shares into brackets), and the share of zeros
   differs by city, so it is not a low-share contrast and is shown apart in the figure.
   Exploratory (not preregistered): for foreign, 65+ and under-18, mean LST anomaly of the estimated group members
   (weight share / 100 x population) against the rest of the residents (weight (1 - share / 100) x population), over
   each variable's usable cells. Bracketed cells are left out and dash cells count as 0 members.
2. Global Moran's I and LISA: queen contiguity on the 100 m grid (centres <= 142 m apart: edge 100 m, corner 141.4 m),
   row-standardised, 999 conditional permutations (seed 20261102); LISA p-values are folded pseudo p-values (one-sided,
   in the direction of the observed statistic), Benjamini-Hochberg false discovery rate 5% on non-island cells
   (esda.fdr returns the threshold k * alpha / n); islands are left out of LISA and of the FDR count. esda's global I
   keeps islands in n (their spatial lag is 0); I without islands is also reported. With 999 permutations the smallest
   pseudo p is 0.001, close to the FDR thresholds, so the exact footprint of significant cells depends partly on the
   random draw. Exploratory (not preregistered): LISA rerun with 9,999 permutations; counts and the overlap (Jaccard index
   of the significant cells) with the primary map are reported.
Usage: .venv\Scripts\python.exe 05_analysis/step7_descriptive.py  ->  results/results.json ("step7"), tables, figures
"""
import json, pathlib, sys

import esda
import geopandas as gpd
import libpysal
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
sys.stdout.reconfigure(encoding="utf-8")
SEED = 20261102
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
t = t[t.rule4].sort_values("gitter_id_100m").reset_index(drop=True)
VARS = {"rent": "average net cold rent (EUR/m²)", "foreign": "share of foreign citizens (%)",
        "age65": "share aged 65+ (%)", "under18": "share aged under 18 (%)"}
out = {"n_rule4": int(len(t)), "notes": "descriptive; cells not people; p_sim = 0.001 means p <= .001 with 999 permutations",
       "deciles": {}, "moran": {}, "lisa": {}}


def usable(d, v):
    return d[f"{v}_in_file"].fillna(False).astype(bool) & ~d[f"{v}_br"].fillna(False).astype(bool)


# 1. zero group + city-specific deciles of non-zero values
rows = []
for v in VARS:
    d = t[usable(t, v)].copy()
    d["group"] = "zero"
    nz = d[v] > 0
    rk = d[nz].groupby("city")[v].rank(method="min")
    n = d[nz].groupby("city")[v].transform("size")
    d.loc[nz, "group"] = np.ceil(rk / n * 10).clip(1, 10).astype(int).astype(str).str.zfill(2)
    def summ(x):
        s = {"cells": len(x), "population": int(x.einwohner_n.sum()), "median_population": float(x.einwohner_n.median()),
             "mean_value_pw": float(np.average(x[v], weights=x.einwohner_n)),
             "pw_mean_lst_anom": float(np.average(x.lst_anom, weights=x.einwohner_n))}
        return pd.Series(s)
    g = d.groupby("group").apply(summ, include_groups=False).reset_index()
    g["variable"] = v
    rows.append(g)
    out["deciles"][v] = {"n": int(len(d)), "zero_cells": int((~nz).sum()), "zero_share": float((~nz).mean()),
                         "zero_share_by_city": d.assign(z=~nz).groupby("city").z.mean().round(4).to_dict(),
                         "groups": g.drop(columns="variable").to_dict(orient="records")}
    if v != "rent":
        members = d[v] / 100 * d.einwohner_n
        out.setdefault("group_vs_rest_exploratory", {})[v] = {
            "group_members_est": float(members.sum()),
            "group_mean_lst_anom": float(np.average(d.lst_anom, weights=members)),
            "rest_mean_lst_anom": float(np.average(d.lst_anom, weights=d.einwohner_n - members)),
            "caveats": "usable cells only (bracketed left out); dash cells count as 0 members; pooled across cities; not adjusted; cells, not people"}
    d[["gitter_id_100m", "city", "group"]].to_csv(RES / f"step7_deciles_{v}.csv", index=False)
dec = pd.concat(rows)
dec.to_csv(RES / "step7_decile_table.csv", index=False)
print(dec.pivot(index="group", columns="variable", values="pw_mean_lst_anom").round(2).to_string())

fig, ax = plt.subplots(1, 4, figsize=(18, 4), sharey=True)
for a, v in zip(ax, VARS):
    g = dec[(dec.variable == v)]
    gz, gd = g[g.group == "zero"], g[g.group != "zero"]
    a.plot(gd.group.astype(int), gd.pw_mean_lst_anom, "o-", color="#b2182b", label="deciles of non-zero values")
    for _, r in gd.iterrows():
        a.annotate(f"{r.median_population:.0f}", (int(r.group), r.pw_mean_lst_anom), textcoords="offset points", xytext=(0, 6),
                   ha="center", fontsize=6, color="#555555")
    if len(gz):
        z = gz.iloc[0]
        a.scatter([-1], [z.pw_mean_lst_anom], marker="s", color="k",
                  label=f"dash (0 or changed to 0): {int(z.cells)} cells,\nmedian {z.median_population:.0f} inhabitants, not comparable")
        a.axvline(-0.2, color="k", lw=0.8, ls=":")
    ticks = ([-1] if len(gz) else []) + list(range(1, 11))
    a.set_xticks(ticks); a.set_xticklabels(["dash" if k == -1 else str(k) for k in ticks])
    a.set_xlabel(f"city-specific decile of the {VARS[v]}\n(n = {int(g.cells.sum())} cells)", fontsize=9)
    a.axhline(0, color="grey", lw=0.5); a.legend(fontsize=7, loc="lower right"); a.margins(y=0.12)
ax[0].set_ylabel("population-weighted mean\nLST anomaly (°C)")
fig.suptitle("Descriptive only: surface heat anomaly of 100 m cells by decile of each census variable (cells, not people; not adjusted for density). "
             "Each variable uses its own usable cells; deciles set within each city, then pooled. Small grey numbers: median inhabitants per cell.\n"
             "The dash group is mostly small, sparsely populated cells (confidentiality removes their small non-zero values) and its city mix differs "
             "from the deciles: it is not the low end of the scale.", fontsize=9)
fig.tight_layout(); fig.savefig(RES / "figures/step7_deciles.png", dpi=150)


# 2. Moran's I and LISA
def queen_w(d):
    w = libpysal.weights.DistanceBand(d[["x_mp", "y_mp"]].values, threshold=142, binary=True, silence_warnings=True)
    w.transform = "r"
    return w


TITLES = {"lst_anom": "LST anomaly (°C)", "rent": "average net cold rent", "foreign": "share of foreign citizens",
          "age65": "share aged 65+", "under18": "share aged under 18"}
lisa_maps = {}
for v in ["lst_anom"] + list(VARS):
    d = t if v == "lst_anom" else t[usable(t, v)]
    d = d.reset_index(drop=True)
    w = queen_w(d)
    np.random.seed(SEED)                            # esda.Moran draws its permutations from numpy's global generator
    mi = esda.Moran(d[v].values, w, permutations=999)
    isl = set(w.islands)
    keep = np.array([i not in isl for i in range(len(d))])
    dk = d[keep].reset_index(drop=True)
    np.random.seed(SEED)
    mi_noisl = esda.Moran(dk[v].values, queen_w(dk), permutations=999)
    loc = esda.Moran_Local(d[v].values, w, permutations=999, seed=SEED)
    p = loc.p_sim.copy()
    thr = esda.fdr(p[keep], 0.05)
    sig = keep & (p <= thr)
    loc9 = esda.Moran_Local(d[v].values, w, permutations=9999, seed=SEED)      # exploratory
    sig9 = keep & (loc9.p_sim <= esda.fdr(loc9.p_sim[keep], 0.05))
    jac = float((sig & sig9).sum() / max((sig | sig9).sum(), 1))
    q = np.where(sig, loc.q, 0)                     # esda: 1 HH, 2 LH, 3 LL, 4 HL; 0 not significant
    qi = np.where(keep, q, -1)                      # islands counted apart (no local statistic)
    counts = {lab: int((qi == k).sum()) for k, lab in [(1, "HH"), (2, "LH"), (3, "LL"), (4, "HL"), (0, "not_significant"), (-1, "island")]}
    zero = d[v].values == 0
    out["moran"][v] = {"n": int(len(d)), "islands": len(isl), "components": int(w.n_components), "I": float(mi.I), "p_sim": float(mi.p_sim),
                       "I_without_islands": float(mi_noisl.I), "zero_share": float(zero.mean())}
    out["lisa"][v] = {"fdr_threshold": float(thr), **counts, "LL_cells_with_value_0": int(((q == 3) & zero).sum()),
                      "islands_excluded": len(isl),
                      "exploratory_9999_permutations": {"significant": int(sig9.sum()), "significant_999": int(sig.sum()),
                                                        "jaccard_with_999": jac,
                                                        **{lab: int((np.where(sig9, loc9.q, 0) == k).sum())
                                                           for k, lab in [(1, "HH"), (2, "LH"), (3, "LL"), (4, "HL")]}}}
    ll0, ll = int(((q == 3) & zero).sum()), int((q == 3).sum())
    q = np.where(keep, q, -1)                       # -1 island: no local statistic
    lisa_maps[v] = (d, q, mi.I, len(isl), ll0, ll)
    print(f"Moran's I {v}: {mi.I:.3f} (without islands {mi_noisl.I:.3f}; p <= .001; n {len(d)}, islands {len(isl)}, zero share {zero.mean():.1%}); LISA {counts}; "
          f"9,999 permutations: {int(sig9.sum())} significant vs {int(sig.sum())}, Jaccard {jac:.2f}")

cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(3035)
fig, axes = plt.subplots(2, 3, figsize=(20, 11))
colors = {-1: "#000000", 0: "#e0e0e0", 1: "#d7191c", 2: "#abd9e9", 3: "#2c7bb6", 4: "#fdae61"}
for a, (v, (d, q, I, ni, ll0, ll)) in zip(axes.flat, lisa_maps.items()):
    a.scatter(d.x_mp, d.y_mp, c=[colors[k] for k in q], s=1.2, marker="s", linewidths=0)
    cities.boundary.plot(ax=a, color="k", linewidth=0.4)
    x0, y0 = cities.total_bounds[0] + 2000, cities.total_bounds[1] + 2000
    a.plot([x0, x0 + 10000], [y0, y0], "k-", lw=2); a.text(x0, y0 + 800, "10 km", fontsize=8)
    note = " (high-high = high rent: the advantaged side)" if v == "rent" else ""
    zl = f"\nlow-low: {ll0:,} of {ll:,} cells have the value 0 (dash)" if v in ("foreign", "age65", "under18") else ""
    a.set_title(f"LISA clusters: {TITLES[v]}{note}\nn = {len(d)} cells, Moran's I = {I:.2f}, {ni} islands (black){zl}", fontsize=10)
    a.set_aspect("equal"); a.set_axis_off()
axes.flat[-1].set_axis_off()
axes.flat[-1].legend(handles=[mpatches.Patch(color=colors[k], label=l) for k, l in
                              [(1, "high-high cluster"), (3, "low-low cluster"), (2, "low-high outlier"), (4, "high-low outlier"),
                               (0, "not significant (FDR 5%)"), (-1, "island: no neighbour, no local statistic")]],
                     loc="center", fontsize=11)
fig.suptitle("Local Moran's I (LISA), queen contiguity, 999 permutations, folded pseudo p, FDR 5% on non-islands. "
             "Census panels use each variable's usable cells only: holes partly reflect missing or uncertain census values.\n"
             "With 999 permutations the smallest p is 0.001, near the FDR thresholds: the exact footprint of significant cells varies with the "
             "random draw (9,999-permutation check in results.json).", fontsize=11)
fig.tight_layout(); fig.savefig(RES / "figures/step7_lisa.png", dpi=130)

path = RES / "results.json"
res = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
res["step7"] = out
path.write_text(json.dumps(res, indent=2), encoding="utf-8")
