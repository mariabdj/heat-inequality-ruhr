r"""Step 3: distribution of each census variable on its own (no link with heat), and who gets the 'uncertain' flag.
Usage: .venv\Scripts\python.exe 05_analysis/step3_distributions.py
Writes 05_analysis/results/figures/step3_distributions.png and 05_analysis/results/step3_summary.csv.
"""
import pathlib, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
d = pd.read_csv(ROOT / "01_data/processed/census_step3.csv")
d = d[d.rule3]
LAB = {"rent": "Average net cold rent (EUR per m²)", "foreign": "Share of foreign citizens (%)",
       "age65": "Share aged 65 and over (%)", "under18": "Share aged under 18 (%)"}
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
rows = []
for ax, (v, lab) in zip(axes.flat, LAB.items()):
    br = d[f"{v}_br"].fillna(False).astype(bool)
    ok = d[v].notna() & ~br
    ax.hist(d.loc[ok, v], bins=50, color="#3b6ea8", alpha=0.85, label="usable (not bracketed)")
    ax.hist(d.loc[d[v].notna() & br, v], bins=50, color="#d08c2c", alpha=0.6, label="bracketed (uncertain)")
    ax.set_xlabel(lab); ax.set_ylabel("cells"); ax.legend(fontsize=8)
    s = d.loc[ok, v]
    rows.append({"variable": v, "n_usable": int(ok.sum()), "mean": s.mean(), "p10": s.quantile(.1), "median": s.median(),
                 "p90": s.quantile(.9), "min": s.min(), "max": s.max(),
                 "median_pop_usable": d.loc[ok, "einwohner_n"].median(),
                 "median_pop_bracketed": d.loc[br, "einwohner_n"].median()})
fig.suptitle("Census variables, 100 m cells passing rules 1 to 3 (Zensus 2022)")
fig.tight_layout()
(ROOT / "05_analysis/results/figures").mkdir(parents=True, exist_ok=True)
fig.savefig(ROOT / "05_analysis/results/figures/step3_distributions.png", dpi=150)
s = pd.DataFrame(rows)
s.to_csv(ROOT / "05_analysis/results/step3_summary.csv", index=False)
print(s.round(2).to_string(index=False))
