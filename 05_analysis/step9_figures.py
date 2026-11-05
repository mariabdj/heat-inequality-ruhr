r"""Step 9a: figures for the article, all drawn from the result files (no number typed by hand).
Fig 1  maps of the LST anomaly and the foreign share (rule-4 cells, 100 m)
Fig 2  P10-P90 effects with their intervals: primary model and every sensitivity analysis in degrees C
Fig 3  effects city by city (S10)
Fig 4  resident heat gap, step by step (exploratory decomposition)
Colours: ColorBrewer RdBu (diverging, grey-white midpoint at 0) and Oranges (sequential); two series colours
(blue, orange) for foreign share and rent; filled marker = Holm p < .05 with the interval on one side of 0.
Usage: .venv\Scripts\python.exe 05_analysis/step9_figures.py  ->  05_analysis/results/figures/fig*.png and .pdf
"""
import json, pathlib

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "05_analysis/results"
FIG = RES / "figures"; FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                     "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.labelcolor": "#0b0b0b",
                     "savefig.dpi": 300, "figure.facecolor": "white"})
BLUE, ORANGE, INK, MUTED, GRID, NODATA = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#cfcdc8"
LABEL = {"Primary (Model A)": "Primary (Model A)", "S1 bracketed included": "S1  bracketed values included",
         "S2 no rent restriction": "S2  rent term left out (more cells)", "S3 population-weighted (WLS, D9)": "S3  population-weighted OLS",
         "S4_all_summer": "S4  hot-day rule relaxed (+1 scene)", "S5_absolute": "S5  absolute LST, not anomaly", "S6_landsat8": "S6  Landsat 8 only",
         "S6b_path196": "S6b  orbit path 196 only", "S6b_path197": "S6b  orbit path 197 only", "S9 8 nearest neighbours": "S9  8 nearest neighbours",
         "S11 population >= 3": "S11  minimum 3 residents (not 10)", "S11 population >= 30": "S11  minimum 30 residents (not 10)",
         "S12_valid95": "S12  scenes with 95%+ valid pixels", "S13_city_median": "S13  anomaly from city median", "S14_yearly_mean": "S14  mean of yearly composites",
         "S16_stqa3K": "S16  pixels with LST uncertainty > 3 K masked", "S17 300 m window covariates": "S17  covariates in a 300 m window",
         "S18 spatial Durbin error": "S18  spatial Durbin error model", "S19 2 km blocks": "S19  2 km bootstrap blocks",
         "S20 islands dropped": "S20  cells without neighbours dropped", "Exploratory D2 dashes as missing": "Exploratory: dashes as missing"}


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)


t = pd.read_parquet(ROOT / "04_grid_join/analysis_table.parquet")
cities = gpd.read_file(ROOT / "01_data/processed/cells_step2.gpkg", layer="cities").to_crs(3035)
r4 = t[t.rule4].copy()


# ---- Fig 1: maps -------------------------------------------------------------------------------------------
def grid(d, col):
    x0, y1 = t.x_mp.min() - 50, t.y_mp.max() + 50
    nx, ny = int(round((t.x_mp.max() + 50 - x0) / 100)), int(round((y1 - (t.y_mp.min() - 50)) / 100))
    a = np.full((ny, nx), np.nan)
    c = ((d.x_mp - 50 - x0) / 100).round().astype(int); r = ((y1 - d.y_mp - 50) / 100).round().astype(int)
    a[r.values, c.values] = d[col].values
    return a, (x0, x0 + nx * 100, y1 - ny * 100, y1)


lim = float(np.ceil(np.nanpercentile(np.abs(r4.lst_anom), 98)))
fsh = r4[r4.foreign_in_file.fillna(False).astype(bool) & ~r4.foreign_br.fillna(False).astype(bool)]
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
for a_, d, col, cmap, vmin, vmax, lab, title in [
        (ax[0], r4, "lst_anom", "RdBu_r", -lim, lim, "LST anomaly (°C)", f"a  Summer daytime surface heat ({len(r4):,} cells)"),
        (ax[1], fsh, "foreign", "Oranges", 0, float(np.ceil(fsh.foreign.quantile(.98) / 10) * 10), "Foreign citizens (% of residents)",
         f"b  Share of foreign citizens ({len(fsh):,} cells)")]:
    arr, ext = grid(d, col)
    cities.plot(ax=a_, color=NODATA, linewidth=0)      # grey = no usable value in that cell
    im = a_.imshow(arr, extent=ext, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest", zorder=2)
    cities.boundary.plot(ax=a_, color=MUTED, linewidth=0.35, zorder=3)
    a_.set_title(title, loc="left"); a_.set_axis_off(); a_.set_aspect("equal")
    cb = fig.colorbar(im, ax=a_, orientation="horizontal", shrink=0.7, pad=0.02, extend="both" if cmap == "RdBu_r" else "max")
    cb.set_label(lab); cb.outline.set_visible(False)
    xb = ext[0] + 2000; a_.plot([xb, xb + 10000], [ext[2] + 2000] * 2, color=INK, lw=1.2); a_.text(xb + 5000, ext[2] + 2600, "10 km", ha="center", fontsize=7)
save(fig, "fig1_maps")

# ---- Fig 2: effects across analyses -------------------------------------------------------------------------
inf = pd.read_csv(RES / "step8_inference.csv").assign(analysis="Primary (Model A)")
b = pd.read_csv(RES / "step8b_sensitivity.csv"); c = pd.read_csv(RES / "step8c_sensitivity.csv")
keep = lambda d: d[~d.analysis.str.startswith(("S10", "S8", "S15", "S7"))]
rows = pd.concat([inf, keep(b), keep(c)], ignore_index=True)
rows = rows[rows.variable.isin(["foreign10", "rent"])]
order = ["Primary (Model A)"] + sorted(set(rows.analysis) - {"Primary (Model A)"}, key=lambda s: (int("".join(ch for ch in s.split()[0].split("_")[0][1:] if ch.isdigit()) or 99) if s.startswith("S") else 100, s))
sig = lambda d: (d.p_holm < .05) & ((d.effect_ci_lo > 0) | (d.effect_ci_hi < 0))
fig, ax = plt.subplots(1, 2, figsize=(7.2, 5.2), sharey=True, constrained_layout=True)
for a_, v, colr, title in [(ax[0], "foreign10", BLUE, "a  Foreign share (H2)"), (ax[1], "rent", ORANGE, "b  Rent, sign reversed (H1)")]:
    d = rows[rows.variable == v].set_index("analysis").reindex(order)
    y = np.arange(len(order))[::-1]
    a_.axvspan(-0.3, 0.3, color=GRID, zorder=0, lw=0); a_.axvline(0, color=MUTED, lw=0.6)
    a_.hlines(y, d.effect_ci_lo, d.effect_ci_hi, color=colr, lw=1.6)
    s = sig(d).values
    a_.scatter(d.effect_P10_P90[s], y[s], s=22, color=colr, zorder=3, edgecolor="white", linewidth=0.8)
    a_.scatter(d.effect_P10_P90[~s], y[~s], s=22, facecolor="white", edgecolor=colr, linewidth=1.2, zorder=3)
    a_.set_title(title, loc="left"); a_.set_xlabel("P10 → P90 difference (°C)")
    a_.set_yticks(y); a_.set_yticklabels([LABEL.get(o, o) for o in order]); a_.grid(axis="x", color=GRID, lw=0.5); a_.set_axisbelow(True)
save(fig, "fig2_effects")

# ---- Fig 3: city by city (S10) ------------------------------------------------------------------------------
cty = b[b.analysis.str.startswith("S10") & b.variable.isin(["foreign10", "rent"])].copy()
cty["city"] = cty.analysis.str.replace("S10 ", "", regex=False)
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True, constrained_layout=True)
names = sorted(cty.city.unique())[::-1]
for a_, v, colr, title in [(ax[0], "foreign10", BLUE, "a  Foreign share"), (ax[1], "rent", ORANGE, "b  Rent, sign reversed")]:
    d = cty[cty.variable == v].set_index("city").reindex(names); y = np.arange(len(names))
    a_.axvspan(-0.3, 0.3, color=GRID, zorder=0, lw=0); a_.axvline(0, color=MUTED, lw=0.6)
    a_.hlines(y, d.effect_ci_lo, d.effect_ci_hi, color=colr, lw=1.6)
    s = sig(d).values
    a_.scatter(d.effect_P10_P90[s], y[s], s=22, color=colr, zorder=3, edgecolor="white", linewidth=0.8)
    a_.scatter(d.effect_P10_P90[~s], y[~s], s=22, facecolor="white", edgecolor=colr, linewidth=1.2, zorder=3)
    a_.set_yticks(y); a_.set_yticklabels([f"{n} (n = {int(d.loc[n, 'n']):,})" for n in names])
    a_.set_title(title, loc="left"); a_.set_xlabel("P10 → P90 difference (°C)")
    a_.grid(axis="x", color=GRID, lw=0.5); a_.set_axisbelow(True)
save(fig, "fig3_cities")

# ---- Fig 4: resident gap decomposition ----------------------------------------------------------------------
dec = pd.read_csv(RES / "step8_reporting_resident_gap_decomposition.csv")
obs = json.loads((RES / "results.json").read_text(encoding="utf-8"))["step8_reporting"]["resident_gap_identity_check"]["observed_pooled_gap"]
fig, ax = plt.subplots(figsize=(7.2, 3.6), constrained_layout=True)
y = np.arange(len(dec))[::-1]
ax.axvline(obs, color=MUTED, lw=0.8, ls="--")
ax.text(obs, len(dec) - 0.4, f"observed gap {obs:.2f} °C", ha="center", va="bottom", fontsize=6.5, color=MUTED)
ax.hlines(y, 0, dec.implied_resident_gap_C, color=BLUE, lw=1.6)
ax.scatter(dec.implied_resident_gap_C, y, s=22, color=BLUE, zorder=3, edgecolor="white", linewidth=0.8)
for yi, v in zip(y, dec.implied_resident_gap_C):
    ax.text(v + 0.012, yi, f"{v:.2f}", va="center", fontsize=6.5, color=INK)
short = {"raw slope, population-weighted (identity: equals the observed pooled gap)": "raw slope, population-weighted (= observed gap)",
         "plus elevation and log population (single-variable OLS)": "city + elevation + log population (OLS)",
         "same, population-weighted": "same, population-weighted",
         "single-variable SEM (step-1 lambda)": "same, spatial error model (first λ)",
         "full Model A OLS (adds rent, 65+, under 18)": "full model, OLS (adds rent, 65+, under 18)",
         "full Model A SEM, step-1 lambda (reported)": "full model, spatial error model, first λ (Table 1)",
         "full Model A SEM, step-2b lambda (exploratory)": "full model, spatial error model, λ reported by software",
         "full Model A SEM, iterated lambda (exploratory)": "full model, spatial error model, iterated λ"}
ax.set_yticks(y); ax.set_yticklabels([short.get(x, x) for x in dec.step]); ax.set_xlim(0, max(dec.implied_resident_gap_C.max(), obs) * 1.15)
ax.set_xlabel("Implied heat gap between foreign and other residents (°C)")
ax.grid(axis="x", color=GRID, lw=0.5); ax.set_axisbelow(True)
save(fig, "fig4_resident_gap")
print("figures written:", sorted(p.name for p in FIG.glob("fig*")))
print("map colour limit +-", lim, "C; foreign share map cells", len(fsh), "; effect plot analyses", len(order))
