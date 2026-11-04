r"""GATE 7: independent checks of the Step 7 numbers (05_analysis/step7_descriptive.py).
(a) Global Moran's I for the LST anomaly and each social variable recomputed without PySAL: neighbours from a k-d tree
    (centres <= 142 m apart), row-standardised weights, I = (n / S0) * (z' W z) / (z' z). Must equal results.json within
    1e-9, with the same number of islands (cells with no neighbour).
(b) LISA recomputed with our own weights (same k-d tree neighbours, given to esda as a plain neighbour list), the same
    seed and 999 permutations; the Benjamini-Hochberg threshold computed by hand on non-island cells (largest k with
    p_(k) <= k * 0.05 / m, threshold k * 0.05 / m; 0.05 / m if none); quadrants from our own z and spatial lag.
    The FDR threshold and the HH, LH, LL, HL, not-significant and island counts must equal results.json exactly.
    The exploratory 9,999-permutation run is rechecked the same way: number of significant cells and Jaccard overlap
    with the 999-permutation map must equal results.json.
(c) The decile table: cells per variable add up to n, the zero group has zero_cells cells, every non-zero group exists.
Usage: .venv\Scripts\python.exe verification/verify_step7.py
"""
import json, pathlib, sys

import esda
import libpysal
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.spatial import cKDTree

ROOT = pathlib.Path(__file__).resolve().parent.parent
res = json.loads((ROOT / "05_analysis/results/results.json").read_text(encoding="utf-8"))["step7"]
dec = pd.read_csv(ROOT / "05_analysis/results/step7_decile_table.csv", dtype={"group": str})
t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
t = t[t.rule4]
errors = []


def neighbours(xy):
    pairs = cKDTree(xy).query_pairs(142.0, output_type="ndarray")
    nb = {i: [] for i in range(len(xy))}
    for a, b in pairs:
        nb[int(a)].append(int(b)); nb[int(b)].append(int(a))
    return pairs, nb


def bh(p, keep):
    ps = np.sort(p[keep]); m = len(ps)
    ok = np.nonzero(ps <= np.arange(1, m + 1) * 0.05 / m)[0]
    thr = (ok[-1] + 1) * 0.05 / m if len(ok) else 0.05 / m
    return thr, keep & (p <= thr)


def own_lisa(y, nb):
    w = libpysal.weights.W({i: sorted(v) for i, v in nb.items()}, silence_warnings=True)
    w.transform = "r"
    keep = np.array([len(nb[i]) > 0 for i in range(len(y))])
    thr, sig = bh(esda.Moran_Local(y, w, permutations=999, seed=20261102).p_sim, keep)
    _, sig9 = bh(esda.Moran_Local(y, w, permutations=9999, seed=20261102).p_sim, keep)
    z = y - y.mean()
    lag = np.array([z[nb[i]].mean() if nb[i] else 0.0 for i in range(len(y))])
    quad = np.select([(z > 0) & (lag > 0), (z < 0) & (lag > 0), (z < 0) & (lag < 0), (z > 0) & (lag < 0)], [1, 2, 3, 4], 0)
    q = np.where(keep, np.where(sig, quad, 0), -1)
    cnt = {lab: int((q == k).sum()) for k, lab in [(1, "HH"), (2, "LH"), (3, "LL"), (4, "HL"), (0, "not_significant"), (-1, "island")]}
    return thr, cnt, int(sig9.sum()), float((sig & sig9).sum() / max((sig | sig9).sum(), 1))


def moran(xy, y):
    pairs, _ = neighbours(xy)
    n = len(y)
    i = np.concatenate([pairs[:, 0], pairs[:, 1]]); j = np.concatenate([pairs[:, 1], pairs[:, 0]])
    W = sparse.csr_matrix((np.ones(len(i)), (i, j)), shape=(n, n))
    deg = np.asarray(W.sum(axis=1)).ravel()
    W = sparse.diags(np.where(deg > 0, 1 / np.maximum(deg, 1), 0)) @ W
    z = y - y.mean()
    return n / W.sum() * (z @ (W @ z)) / (z @ z), int((deg == 0).sum())


for v in ["lst_anom", "rent", "foreign", "age65", "under18"]:
    d = t if v == "lst_anom" else t[t[f"{v}_in_file"].fillna(False).astype(bool) & ~t[f"{v}_br"].fillna(False).astype(bool)]
    I, isl = moran(d[["x_mp", "y_mp"]].values, d[v].values.astype(float))
    m = res["moran"][v]
    print(f"(a) {v}: n {len(d)}, I own {I:.10f}, results.json {m['I']:.10f}, islands {isl} vs {m['islands']}")
    if len(d) != m["n"] or abs(I - m["I"]) > 1e-9 or isl != m["islands"]:
        errors.append(f"(a) {v}")
    L = res["lisa"][v]
    thr, cnt, n9, jac = own_lisa(d[v].values.astype(float), neighbours(d[["x_mp", "y_mp"]].values)[1])
    e9 = L["exploratory_9999_permutations"]
    same = (all(cnt[k] == L[k] for k in cnt) and abs(thr - L["fdr_threshold"]) < 1e-12
            and n9 == e9["significant"] and abs(jac - e9["jaccard_with_999"]) < 1e-12)
    print(f"(b) {v}: own FDR threshold {thr:.7f} vs {L['fdr_threshold']:.7f}; own counts {cnt}; "
          f"9,999 permutations: {n9} significant, Jaccard {jac:.4f}; equal: {same}")
    if not same:
        errors.append(f"(b) {v}")

for v, r in res["deciles"].items():
    g = dec[dec.variable == v]
    z = g.loc[g.group == "zero", "cells"]
    zc = int(z.iloc[0]) if len(z) else 0
    groups = set(g.group) - {"zero"}
    print(f"(c) {v}: cells {int(g.cells.sum())} vs n {r['n']}, zero group {zc} vs {r['zero_cells']}, non-zero groups {len(groups)}")
    if int(g.cells.sum()) != r["n"] or zc != r["zero_cells"] or groups != {f"{k:02d}" for k in range(1, 11)}:
        errors.append(f"(c) {v}")

for e in errors:
    print("FAIL", e)
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
