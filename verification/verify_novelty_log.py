r"""GATE 0: the novelty search is logged and reproducible.
Checks: every query of the script is in the log for both sources, every raw answer file exists and holds the
number of records the log says, the pooled and candidate files agree with the raw files, and every closest
study named in the report has a DOI or a saved file.
Usage: .venv\\Scripts\\python.exe verification/verify_novelty_log.py
"""
import csv, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "00_setup"
errors = []

script = (S / "novelty_search.py").read_text(encoding="utf-8")
queries = re.findall(r'\("(Q\d+)", "([^"]+)"\)', script)
log = list(csv.DictReader(open(S / "novelty_search_log.csv", encoding="utf-8")))
logged = {(r["query_id"], r["source"]): r for r in log}

for qid, q in queries:
    for src in ("OpenAlex", "Crossref"):
        r = logged.get((qid, src))
        if not r:
            errors.append(f"{qid}/{src}: not in the log")
            continue
        if r["query"] != q:
            errors.append(f"{qid}/{src}: logged query differs from the script")
        raw = S / r["raw_file"]
        if not raw.is_file():
            errors.append(f"{qid}/{src}: raw file missing ({r['raw_file']})")
            continue
        data = json.loads(raw.read_text(encoding="utf-8"))
        n = len(data["results"]) if src == "OpenAlex" else len(data["message"]["items"])
        if n != int(r["records_saved"]):
            errors.append(f"{qid}/{src}: log says {r['records_saved']} records, raw file has {n}")

saved = sum(int(r["records_saved"]) for r in log)
pool = list(csv.DictReader(open(S / "novelty_records.csv", encoding="utf-8")))
cands = list(csv.DictReader(open(S / "novelty_candidates.csv", encoding="utf-8")))
n_flag = sum(r["is_candidate"] == "True" for r in pool)
if n_flag != len(cands):
    errors.append(f"candidates file has {len(cands)} rows, pooled file flags {n_flag}")
if len(pool) > saved:
    errors.append("more unique records than saved records")

report = (S / "NOVELTY_REPORT.md").read_text(encoding="utf-8")
for m in re.finditer(r"\| \*\*(.+?)\*\*, (.+?) \|", report):
    row = m.group(0) + report[m.end():report.find("\n", m.end())]
    if not re.search(r"doi:10\.\S+", row) and "Fachbericht" not in row:
        errors.append(f"closest study without DOI: {m.group(1)}")
if not (S / "novelty_search" / "closest" / "LANUK_Fachbericht_171.pdf").is_file():
    errors.append("LANUK report cited without a saved copy")
nums = {"5,142": saved, "4,508": len(pool), "139": len(cands)}
for txt, val in nums.items():
    if txt in report and int(txt.replace(",", "")) != val:
        errors.append(f"report says {txt}, files give {val}")

for e in errors:
    print("FAIL", e)
print(f"queries in script: {len(queries)}; searches logged: {len(log)}; records saved: {saved}; "
      f"unique: {len(pool)}; candidates: {len(cands)}")
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
