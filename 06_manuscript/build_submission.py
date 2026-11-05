r"""Builds the submission and preprint version of the article (private folder 06_manuscript/submission/).
Inserts the required use-of-AI statement and acknowledgements from the private file, then renders Word and PDF with Quarto.
Usage (from the project root, after build_manuscript.py): .venv\Scripts\python.exe 06_manuscript/build_submission.py
"""
import pathlib, re, shutil, subprocess

MS = pathlib.Path(__file__).resolve().parent
OUT = MS / "submission"; OUT.mkdir(exist_ok=True)
t = (MS / "manuscript.md").read_text(encoding="utf-8")
ai = (MS / "ai_use_statement_PRIVATE.md").read_text(encoding="utf-8")
section = ai.split("## SECTION", 1)[1].split("## ACKNOWLEDGEMENTS", 1)[0].strip()
ack = ai.split("## ACKNOWLEDGEMENTS", 1)[1].split("## DECLARATION", 1)[0].strip()
decl = ai.split("## DECLARATION", 1)[1].strip()
for old, new in [("[USE OF AI TOOLS: written in the submitted version.]", section),
                 ("[ACKNOWLEDGEMENTS: written in the submitted version.]", ack),
                 ("\n## References\n", "\n" + decl + "\n\n## References\n")]:
    assert t.count(old) == 1, old
    t = t.replace(old, new)
assert "[" + "USE OF AI" not in t and "written in the submitted version" not in t
(OUT / "figures").mkdir(exist_ok=True)
for fpath in (MS.parent / "05_analysis/results/figures").glob("fig[0-9]_*.png"):
    shutil.copy(fpath, OUT / "figures" / fpath.name)
t = t.replace("](../05_analysis/results/figures/", "](figures/")
title = re.match(r"# ([^\n]*)\n", t).group(1).replace('"', '\\"')
t = re.sub(r"^# [^\n]*\n", "", t, count=1)
hdr = ("---\ntitle: \"" + title + "\"\nformat:\n  docx: default\n  typst:\n    margin: {x: 2.2cm, y: 2.2cm}\n    fontsize: 10.5pt\n"
       "    papersize: a4\n---\n\n")
name = "Boudjelal_heat_inequality_Ruhr"
(OUT / f"{name}.qmd").write_text(hdr + t, encoding="utf-8")
shutil.copy(MS / "supplementary_table_S1.md", OUT / "Supplementary_Table_S1.md")
shutil.copy(MS / "supplementary_table_S0.md", OUT / "Supplementary_Table_S0.md")
q = r"C:\Program Files\Quarto\bin\quarto.exe"
subprocess.run([q, "render", f"{name}.qmd"], cwd=OUT, check=True)
subprocess.run([q, "render", "Supplementary_Table_S1.md", "--to", "docx"], cwd=OUT, check=True)
subprocess.run([q, "render", "Supplementary_Table_S0.md", "--to", "docx"], cwd=OUT, check=True)
print("written:", sorted(p.name for p in OUT.iterdir()))
