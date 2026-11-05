r"""Shared functions for the Step 8 sensitivity analyses (preregistration Q19, Q20, Q22, Q24).
They repeat the rules of 05_analysis/step8_primary.py; step8_sensitivity.py first checks that, run on the primary
specification, they reproduce the Step 8a inference table exactly.
"""
import numpy as np
import pandas as pd
import libpysal
import spreg

SEED, B = 20261102, 999
SOC = ["rent", "foreign10", "age65_10", "under18_10"]
EXP = {"rent": -1, "foreign10": 1, "age65_10": None, "under18_10": None}       # H1, H2, RQ2


def prep(t):
    t = t.sort_values("gitter_id_100m").reset_index(drop=True).copy()
    t["foreign10"], t["age65_10"], t["under18_10"] = t.foreign / 10, t.age65 / 10, t.under18 / 10
    t["ln_pop"] = np.log(t.einwohner_n)
    cities = sorted(t.city.unique())
    dum = [f"city_{c}" for c in cities[1:]]
    for c, d in zip(cities[1:], dum):
        t[d] = (t.city == c).astype(float)
    return t, dum


def usable(t, raw, bracketed_ok=False):
    ok = t[f"{raw}_in_file"].fillna(False).astype(bool)
    return ok if bracketed_ok else ok & ~t[f"{raw}_br"].fillna(False).astype(bool)


def queen(d, thr=142):
    w = libpysal.weights.DistanceBand(d[["x_mp", "y_mp"]].values, threshold=thr, binary=True, silence_warnings=True)
    w.transform = "r"
    return w


def knn(d, k=8):
    w = libpysal.weights.KNN.from_array(d[["x_mp", "y_mp"]].values, k=k)
    w.transform = "r"
    return w


def ols_np(y, X, wts=None):
    Xc = np.column_stack([np.ones(len(y)), X])
    if wts is not None:
        s = np.sqrt(wts)
        return np.linalg.lstsq(Xc * s[:, None], y * s, rcond=None)[0][1:]
    return np.linalg.lstsq(Xc, y, rcond=None)[0][1:]


def make_blocks(d, size=1000, city="city"):
    """Block = INSPIRE cell of `size` m (EPSG:3035, from the cell centre) intersected with the city."""
    key = d[city].astype(str) + "_" + (d.x_mp // size).astype(int).astype(str) + "_" + (d.y_mp // size).astype(int).astype(str)
    blocks = pd.DataFrame({"block": key, "city": d[city].values}).drop_duplicates("block").sort_values(["city", "block"]).reset_index(drop=True)
    blocks["bid"] = np.arange(len(blocks))
    bid = key.map(dict(zip(blocks.block, blocks.bid))).values
    return bid, blocks


def bootstrap(y, designs, bid, blocks, wts=None, b=B, seed=SEED):
    """One shared set of block draws for all designs (list of X arrays); returns list of (b x k) arrays."""
    rows_of = [np.flatnonzero(bid == k) for k in range(len(blocks))]
    rng = np.random.default_rng(seed)
    out = [np.empty((b, X.shape[1])) for X in designs]
    for r in range(b):
        pick = np.concatenate([rng.choice(g.bid.values, size=len(g), replace=True) for _, g in blocks.groupby("city", sort=True)])
        idx = np.concatenate([rows_of[k] for k in pick])
        for o, X in zip(out, designs):
            o[r] = ols_np(y[idx], X[idx], None if wts is None else wts[idx])
    return out


def sem(y, X, w, names, slx_vars=None):
    res = {}
    for est in ("Het", "Hom"):
        try:
            kw = {} if slx_vars is None else {"slx_lags": 1, "slx_vars": slx_vars}
            m = getattr(spreg, f"GM_Error_{est}")(y.reshape(-1, 1), X, w=w, hard_bound=True, name_x=names, **kw)
            b, se = m.betas.ravel(), m.std_err.ravel()
            nm = list(m.name_x)
            if len(nm) == len(b) - 1:
                nm.append("lambda")
            assert len(nm) == len(b), (nm, len(b))
            res[est] = {"betas": dict(zip(nm, b)), "se": dict(zip(nm, se)), "p": dict(zip(nm, [z[1] for z in m.z_stat]))}
        except Exception as e:
            res[est] = None
            res[f"{est}_error"] = repr(e)
    return res


def holm(p):
    p = np.asarray(p, float); k = len(p); order = np.argsort(p); adj = np.empty(k); run = 0
    for i, j in enumerate(order):
        run = max(run, min(1, (k - i) * p[j])); adj[j] = run
    return adj


def verdict(beta, p_holm, same_side, negligible, expected):
    sig = p_holm < .05 and same_side
    if expected is None:
        base = ("positive" if beta > 0 else "negative") if sig else "inconclusive"
    elif sig and np.sign(beta) == expected:
        base = "supported"
    elif sig:
        base = "contradicted"
    else:
        base = "not supported (inconclusive)"
    if negligible:
        base = base + " but practically negligible" if sig else "practically negligible"
    return base


def infer(soc, sem_fit, boots, ols_full, P, negligible_rule=True):
    """Q19 inference rule and Q20/Q22 for the social variables `soc` (in the first columns of the design).
    negligible_rule=False for outcomes not in C (S15, standardised anomaly; Q22)."""
    rows = []
    for j, v in enumerate(soc):
        bs = boots[:, j]
        p_boot = min(1.0, 2 * min(1 + (bs <= 0).sum(), 1 + (bs >= 0).sum()) / (len(bs) + 1))
        ivs, ps = [(np.percentile(bs, 2.5), np.percentile(bs, 97.5))], [p_boot]
        for est in ("Het", "Hom"):
            m = sem_fit.get(est) if sem_fit else None
            if m is not None:
                ivs.append((m["betas"][v] - 1.96 * m["se"][v], m["betas"][v] + 1.96 * m["se"][v])); ps.append(m["p"][v])
        het, hom = (sem_fit or {}).get("Het"), (sem_fit or {}).get("Hom")
        if sem_fit is None:                       # no spatial fit by design (S3, reference rows): full-sample OLS
            point = float(ols_full[j])
        else:                                     # spatial fits attempted; both failing -> bootstrap median, as step8_primary.py
            point = het["betas"][v] if het else (hom["betas"][v] if hom else float(np.median(bs)))
        lo, hi = min(i[0] for i in ivs), max(i[1] for i in ivs)
        rows.append({"variable": v, "beta": point, "beta_ols": float(ols_full[j]), "p_het": het["p"][v] if het else np.nan,
                     "p_hom": hom["p"][v] if hom else np.nan, "p_boot": p_boot, "p_max": max(ps), "ci_lo_hull": lo, "ci_hi_hull": hi,
                     "same_side": bool(lo > 0 or hi < 0)})
    df = pd.DataFrame(rows)
    df["p_holm"] = holm(df.p_max.values)
    sgn = np.where(df.variable == "rent", -1, 1)
    span = np.array([P[v][1] - P[v][0] for v in df.variable])
    df["effect_P10_P90"] = sgn * df.beta * span
    e1, e2 = sgn * df.ci_lo_hull * span, sgn * df.ci_hi_hull * span
    df["effect_ci_lo"], df["effect_ci_hi"] = np.minimum(e1, e2), np.maximum(e1, e2)
    df["negligible_region"] = ((df.effect_ci_lo >= -0.3) & (df.effect_ci_hi <= 0.3)) if negligible_rule else False
    df["verdict"] = [verdict(r.beta, r.p_holm, r.same_side, r.negligible_region, EXP[r.variable]) for r in df.itertuples()]
    return df


def h3(bA, bB, olsA, olsB, xa, xb, semA=None, semB=None):
    rows = []
    for v in ("rent", "foreign10"):
        if v not in xa or v not in xb:
            continue
        ja, jb = xa.index(v), xb.index(v)
        s = np.sign(olsA[ja]); d_full = s * (olsA[ja] - olsB[jb]); d_b = s * (bA[:, ja] - bB[:, jb])
        ci_bA = (np.percentile(bA[:, ja], 2.5), np.percentile(bA[:, ja], 97.5))
        rows.append({"variable": v, "beta_A_ols": olsA[ja], "beta_B_ols": olsB[jb], "delta_star": d_full,
                     "p_one_sided": (1 + (d_b <= 0).sum()) / (len(d_b) + 1), "ci_lo": np.percentile(d_b, 2.5), "ci_hi": np.percentile(d_b, 97.5),
                     "replicates_beta_B_opposite_sign": int((np.sign(bB[:, jb]) != np.sign(bA[:, ja])).sum()),
                     "R_percent": 100 * d_full / abs(olsA[ja]) if (ci_bA[0] > 0 or ci_bA[1] < 0) else None,
                     "delta_star_sem": s * (semA["betas"][v] - semB["betas"][v]) if semA and semB else None,
                     "sign_reversal": bool(np.sign(olsB[jb]) != s and abs(olsB[jb]) > abs(olsA[ja]))})
    df = pd.DataFrame(rows)
    if len(df):
        df["p_holm"] = holm(df.p_one_sided.values)
        df["verdict"] = ["sign reversal" if r.sign_reversal else ("supported" if r.delta_star > 0 and r.p_holm < .05 else "not supported")
                         for r in df.itertuples()]
    return df


def aggregate_1km(d):
    """Q19 MGWR / S7 aggregation of the included 100 m cells to 1 km INSPIRE cells."""
    d = d.copy()
    d["kx"], d["ky"] = (d.x_mp // 1000).astype(int), (d.y_mp // 1000).astype(int)
    rows = []
    for (kx, ky), g in d.groupby(["kx", "ky"]):
        if len(g) < 5:
            continue
        pop = g.einwohner_n.values
        cnt = g.groupby("city").agg(n=("city", "size"), p=("einwohner_n", "sum")).sort_values(["n", "p"], ascending=False)
        dw = g.n_dwellings.fillna(0).values
        rows.append({"kx": kx, "ky": ky, "x_mp": kx * 1000 + 500, "y_mp": ky * 1000 + 500, "n_cells": len(g), "city": cnt.index[0],
                     "lst_anom": g.lst_anom.mean(), "tree_cover": g.tree_cover.mean(), "imperviousness": g.imperviousness.mean(),
                     "elevation": g.elevation.mean(), "ln_pop": np.log(pop.sum()), "pop": pop.sum(),
                     "rent": np.average(g.rent, weights=dw) if dw.sum() > 0 else np.nan,
                     "foreign10": np.average(g.foreign10, weights=pop), "age65_10": np.average(g.age65_10, weights=pop),
                     "under18_10": np.average(g.under18_10, weights=pop)})
    return pd.DataFrame(rows)
