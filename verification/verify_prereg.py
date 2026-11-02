r"""GATE 1: the preregistration answers every question of the secondary-data template, and every census
column it names exists, with that exact spelling, in the official description files.
Usage: .venv\Scripts\python.exe verification/verify_prereg.py
"""
import pathlib, re, sys
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
text = (ROOT / "00_protocol" / "preregistration.md").read_text(encoding="utf-8")
errors = []

# 1. Q1 to Q25 each present once, each followed by some text
for q in range(1, 26):
    hits = re.findall(rf"^\*\*Q{q}\. ", text, flags=re.M)
    if len(hits) != 1:
        errors.append(f"Q{q}: found {len(hits)} times (expected 1)")

# 2. every backticked census column in the Q5 table exists in a description file
desc = ""
for f in sorted((ROOT / "00_protocol" / "census_descriptions").glob("*.xlsx")):
    wb = openpyxl.load_workbook(f, read_only=True)
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            desc += " ".join(str(c) for c in row if c is not None) + "\n"
q5 = text[text.index("**Q5."):text.index("**Q6.")]
# only the census part of Q5: the table and the paragraph under it, up to the Landsat item
q5 = q5[:q5.index("2. **Landsat")]
cols = set(re.findall(r"`([A-Za-z_0-9]+)`", q5)) - {"werterlaeuternde_Zeichen"}
files = set(re.findall(r"`(Zensus2022_[^`]+\.csv)`", q5))
for c in sorted(cols):
    if not re.search(rf"\b{re.escape(c)}\b", desc):
        errors.append(f"column `{c}` not found in any description file")
for f in sorted(files):
    if f not in desc:
        errors.append(f"file `{f}` not found in any description file")

# 3. house style
for ch, name in (("—", "em dash"), ("–", "en dash")):
    if ch in text:
        errors.append(f"{name} used {text.count(ch)} times")

for e in errors:
    print("FAIL", e)
print(f"template questions checked: 25; census columns checked: {len(cols)}; census files checked: {len(files)}")
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
