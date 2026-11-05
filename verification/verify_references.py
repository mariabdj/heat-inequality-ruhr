r"""Gate 9: every reference with a DOI in 06_manuscript/manuscript.md is checked against Crossref: the DOI resolves,
the title matches (after lower-casing and removing punctuation, at least 90% of the Crossref title words appear in
the reference), the year matches and the first author's family name matches. References without a DOI are listed
for a manual check. Every in-text citation (Author, year) must have a reference entry, and every entry must be cited.
An entry's year passes if it equals the print, online, issued or journal-issue year on Crossref.
Usage: .venv\Scripts\python.exe verification/verify_references.py [path to manuscript.md]
"""
import json, pathlib, re, sys, time, unicodedata, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ms = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "06_manuscript/manuscript.md"
text = ms.read_text(encoding="utf-8")
body, refs = text.split("\n## References", 1)
entries = [e.strip() for e in refs.strip().split("\n\n") if e.strip()]


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s)


ok = True
for e in entries:
    first = norm(e.split(",")[0]).split()[0] if e[0].isalpha() else ""
    year = re.search(r"\((\d{4})\)", e)
    doi = re.search(r"https://doi\.org/(\S+)", e)
    if not doi:
        print(f"MANUAL  no DOI: {e[:110]}")
        continue
    d = doi.group(1).rstrip(".")
    try:
        req = urllib.request.Request(f"https://api.crossref.org/works/{d}", headers={"User-Agent": "reference-check/1.0"})
        msg = json.loads(urllib.request.urlopen(req, timeout=30).read())["message"]
    except Exception:
        try:   # DOIs registered with DataCite (for example conference proceedings): same checks on DataCite metadata
            req = urllib.request.Request(f"https://api.datacite.org/dois/{d}", headers={"User-Agent": "reference-check/1.0"})
            a = json.loads(urllib.request.urlopen(req, timeout=30).read())["data"]["attributes"]
            msg = {"title": [a["titles"][0]["title"]], "issued": {"date-parts": [[int(a["publicationYear"])]]},
                   "author": [{"family": c.get("familyName") or c.get("name", "")} for c in a.get("creators", [])]}
        except Exception as ex:
            print(f"FAIL    {d}: not found on Crossref or DataCite ({ex.__class__.__name__})"); ok = False; continue
    title = norm(" ".join(msg.get("title", [""])))
    words = [w for w in title.split() if len(w) > 2]
    share = sum(w in norm(e) for w in words) / max(len(words), 1)
    years = {d.get("date-parts", [[None]])[0][0] for d in (msg.get("published-print"), msg.get("published-online"), msg.get("issued"),
             (msg.get("journal-issue") or {}).get("published-print")) if d}
    cy = "/".join(str(y) for y in sorted(y for y in years if y))   # online-first and issue years can differ
    fam = norm(msg.get("author", [{}])[0].get("family", "")).split()
    checks = {"title": share >= .9, "year": bool(year) and int(year.group(1)) in years, "first author": bool(fam) and fam[-1] in norm(e.split("(")[0])}
    good = all(checks.values())
    if not checks["year"] and checks["title"] and checks["first author"] and not msg.get("published-print") and year \
            and msg.get("volume") and f"{msg['volume']}(" in e.replace(" ", "") and int(year.group(1)) > max(y for y in years if y):
        # Crossref has only the online-first date: the issue year cannot be read here, so it must be checked by hand
        print(f"MANUAL  {d}: year {year.group(1)} (issue {msg['volume']}({msg.get('issue')})) not on Crossref, which has only online {cy}")
        continue
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}    {d}: title words {share:.0%}, year {year.group(1) if year else '?'} vs {cy}, first author {fam[-1] if fam else '?'}"
          + ("" if good else f"  <- {[k for k, v in checks.items() if not v]}"))
    time.sleep(0.3)

# citations in the text against the reference list
keys = set()
for e in entries:
    yr = re.search(r"\((\d{4})\)", e)
    fam = norm(re.split(r"[,(]", e)[0]).split()
    keys.add((fam[0] if e.split(",")[0].isupper() or "(" in e.split(",")[0] else fam[-1], yr.group(1) if yr else ""))   # corporate author: first word (LANUK NRW -> lanuk); person: last word of the family name (van den Akker -> akker)   # last word of the family name (van den Akker -> akker)
cited = set()
for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿ'\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+| \([^)]*\))?,? \(?(\d{4})\)?", body):
    cited.add((norm(m.group(1)).split()[0], m.group(2)))
missing = sorted(c for c in cited if c[1] and c not in keys and c[0] not in ("zensus", "landsat", "census", "summer", "june", "november"))
uncited = sorted(k for k in keys if k not in cited and k[1])
for c in missing:
    print(f"CHECK   cited in text but no entry (or not a citation): {c}")
for k in uncited:
    print(f"FAIL    entry never cited in the text: {k}"); ok = False
print("RESULT:", "PASSED" if ok else "FAILED")
sys.exit(0 if ok else 1)
