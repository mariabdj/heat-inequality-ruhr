r"""Builds the journal submission (Urban Climate) and the EarthArXiv preprint (private folder 06_manuscript/submission/).
Inserts the required use-of-AI statement and acknowledgements from the private file, then renders Word and PDF with Quarto.
Also writes the highlights, the title page and the preprint cover page. Highlight numbers come from numbers_used.json.
Usage (from the project root, after build_manuscript.py): .venv\Scripts\python.exe 06_manuscript/build_submission.py
"""
import json, pathlib, re, shutil, subprocess

OSF_DATA_DOI = "10.17605/OSF.IO/FSV6C"   # fill in once the analysis table is deposited on OSF (journal rule: data deposited and cited)

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
ph = "[OSF DATA DOI: added when deposited]"
if OSF_DATA_DOI and ph in t:
    t = t.replace(ph, "https://doi.org/" + OSF_DATA_DOI)
(OUT / "figures").mkdir(exist_ok=True)
for fpath in (MS.parent / "05_analysis/results/figures").glob("fig[0-9]_*.png"):
    shutil.copy(fpath, OUT / "figures" / fpath.name)
t = t.replace("](../05_analysis/results/figures/", "](figures/")
title = re.match(r"# ([^\n]*)\n", t).group(1)
t = re.sub(r"^# [^\n]*\n", "", t, count=1)
hdr = ("---\ntitle: \"" + title.replace('"', '\\"') + "\"\nformat:\n  docx: default\n  typst:\n    margin: {x: 2.2cm, y: 2.2cm}\n"
       "    fontsize: 10.5pt\n    papersize: a4\n---\n\n")
name = "Boudjelal_heat_inequality_Ruhr"
(OUT / f"{name}.qmd").write_text(hdr + t, encoding="utf-8")
shutil.copy(MS / "supplementary_table_S1.md", OUT / "Supplementary_Table_S1.md")
shutil.copy(MS / "supplementary_table_S0.md", OUT / "Supplementary_Table_S0.md")

# contact details are kept in the private submission folder
C = json.loads((OUT / "contact.json").read_text(encoding="utf-8")) if (OUT / "contact.json").is_file() else {}
EMAIL, POSTAL = C.get("email", "[e-mail]"), C.get("postal", "[postal address], Algiers, Algeria")

# preprint: same text, with the cover page EarthArXiv asks for
cover = ("**This is a non-peer reviewed preprint submitted to EarthArXiv.** The manuscript is being submitted to "
         "*Urban Climate* for peer review. Later versions may differ; if it is accepted, a link to the published article "
         "will be added.\n\nAuthor: Maria Boudjelal, independent researcher, Algiers, Algeria. "
         "ORCID: https://orcid.org/0009-0002-6434-784X. Contact: " + EMAIL + "\n\n{{< pagebreak >}}\n\n")
pre_hdr = hdr.replace("  docx: default\n", "")
supp = "".join("\n\n{{< pagebreak >}}\n\n" + (MS / f).read_text(encoding="utf-8").replace("\n# ", "\n## ").replace("# ", "## ", 1)
               for f in ("supplementary_table_S0.md", "supplementary_table_S1.md"))   # one PDF only (EarthArXiv rule)
small = "\n\n```{=typst}\n#set text(size: 7.5pt)\n```\n"   # wide supplementary tables
(OUT / f"{name}_EarthArXiv.qmd").write_text(pre_hdr + cover + t + small + supp, encoding="utf-8")

# highlights: 3 to 5 bullets, at most 85 characters each (journal rule)
N = {k: v["printed"] for k, v in json.loads((MS / "numbers_used.json").read_text(encoding="utf-8")).items()}
hl = ["Ruhr 100 m cells with a higher foreign-citizen share had hotter daytime surfaces",
      f"Adjusted, 10th vs 90th percentile cells of foreign share: +{N['e_for_it']} to {N['e_for']} °C",
      "Rent and age: inconclusive, as the statistical models disagreed",
      f"Estimated foreign residents lived in cells {N['rc_all_pooled']} °C hotter at the surface",
      "Exploratory: modelled night air temperature showed a positive gap too"]
for h in hl:
    assert len(h) <= 85, (len(h), h)
(OUT / "Highlights.md").write_text("# Highlights\n\n" + "\n".join("- " + h for h in hl) + "\n", encoding="utf-8")

# title page (single anonymized review: the names also stay in the manuscript)
tp = (f"# {title}\n\n**Author:** Maria Boudjelal\n\n**Affiliation:** Independent researcher, " + POSTAL + "\n\n"
      "**Corresponding author:** Maria Boudjelal, " + POSTAL + ". E-mail: " + EMAIL + ". "
      "ORCID: https://orcid.org/0009-0002-6434-784X\n\n"
      "**CRediT author statement.** Maria Boudjelal: Conceptualization, Methodology, Software, Validation, Formal analysis, "
      "Investigation, Data curation, Writing - original draft, Writing - review and editing, Visualization, Project administration.\n\n"
      "**Funding.** This research did not receive any specific grant from funding agencies in the public, commercial, or "
      "not-for-profit sectors.\n\n"
      "**Declaration of competing interest.** The author declares that she has no known competing financial interests or "
      "personal relationships that could have appeared to influence the work reported in this paper.\n\n"
      "**Acknowledgements.** " + ack + "\n")
(OUT / "Title_page.md").write_text(tp, encoding="utf-8")

q = r"C:\Program Files\Quarto\bin\quarto.exe"
subprocess.run([q, "render", f"{name}.qmd"], cwd=OUT, check=True)
subprocess.run([q, "render", f"{name}_EarthArXiv.qmd", "--to", "typst"], cwd=OUT, check=True)
for f in ("Supplementary_Table_S1.md", "Supplementary_Table_S0.md", "Highlights.md", "Title_page.md"):
    subprocess.run([q, "render", f, "--to", "docx"], cwd=OUT, check=True)
print("written:", sorted(p.name for p in OUT.iterdir()))
for h in hl:
    print(len(h), h)
if not OSF_DATA_DOI:
    print("NOT READY TO SUBMIT: OSF data DOI missing (set OSF_DATA_DOI after the deposit)")
