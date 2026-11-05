r"""Novelty check (Step 0): has someone already linked surface heat and social indicators in the Ruhr / Germany?
Runs fixed queries on OpenAlex and Crossref, saves every raw answer, logs each query with its hit count,
then pools the records, removes duplicates and applies a simple title/abstract rule to list candidates to read.
Usage (from the project folder): .venv\\Scripts\\python.exe 00_setup/novelty_search.py
"""
import csv, datetime, json, os, pathlib, re, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "novelty_search" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()
MAILTO = "129296788+mariabdj@users.noreply.github.com"
KEY = os.environ.get("OPENALEX_API_KEY", "")
PER_QUERY = 200

# English and German queries: heat x social x place; each one targets a different way the same study could be described
QUERIES = [
    ("Q01", "land surface temperature Ruhr"),
    ("Q02", "urban heat social inequality Ruhr"),
    ("Q03", "heat exposure environmental justice Germany"),
    ("Q04", "land surface temperature census grid Germany"),
    ("Q05", "land surface temperature Zensus 2022"),
    ("Q06", "heat vulnerability migration background Germany city"),
    ("Q07", "urban heat island socioeconomic Dortmund"),
    ("Q08", "urban heat island Bochum"),
    ("Q09", "urban heat Essen Duisburg Gelsenkirchen"),
    ("Q10", "heat inequality rent foreigners Germany"),
    ("Q11", "Hitze soziale Ungleichheit Ruhrgebiet"),
    ("Q12", "Umweltgerechtigkeit Hitze Stadt"),
    ("Q13", "Hitzebelastung Sozialstruktur Stadtteile"),
    ("Q14", "land surface temperature spatial regression neighbourhood deprivation Europe"),
    ("Q15", "multiscale geographically weighted regression land surface temperature social"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"novelty-check (mailto:{MAILTO})"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # network hiccup: wait and retry, then give up loudly
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))


def openalex(qid, q):
    params = {"search": q, "per-page": "200", "select": "id,doi,title,publication_year,authorships,abstract_inverted_index,primary_location", "mailto": MAILTO}
    if KEY:
        params["api_key"] = KEY
    data = get("https://api.openalex.org/works?" + urllib.parse.urlencode(params))
    (RAW / f"{qid}_openalex.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    recs = []
    for w in data.get("results", []):
        inv = w.get("abstract_inverted_index") or {}
        words = sorted(((p, word) for word, ps in inv.items() for p in ps))
        recs.append({
            "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
            "title": w.get("title") or "",
            "year": w.get("publication_year") or "",
            "first_author": ((w.get("authorships") or [{}])[0].get("author") or {}).get("display_name", "") if w.get("authorships") else "",
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "") if w.get("primary_location") else "",
            "abstract": " ".join(word for _, word in words),
            "id": w.get("id", ""),
        })
    return data.get("meta", {}).get("count", ""), recs


def crossref(qid, q):
    params = {"query.bibliographic": q, "rows": str(PER_QUERY), "mailto": MAILTO,
              "select": "DOI,title,issued,author,container-title,abstract"}
    data = get("https://api.crossref.org/works?" + urllib.parse.urlencode(params))
    (RAW / f"{qid}_crossref.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    recs = []
    for w in data.get("message", {}).get("items", []):
        recs.append({
            "doi": (w.get("DOI") or "").lower(),
            "title": (w.get("title") or [""])[0],
            "year": ((w.get("issued") or {}).get("date-parts") or [[""]])[0][0],
            "first_author": (w.get("author") or [{}])[0].get("family", "") if w.get("author") else "",
            "venue": (w.get("container-title") or [""])[0],
            "abstract": re.sub(r"<[^>]+>", " ", w.get("abstract") or ""),
            "id": "",
        })
    return data.get("message", {}).get("total-results", ""), recs


# candidate rule: about heat AND about social groups or justice AND set in Germany / Ruhr (or a method we must compare with)
HEAT = re.compile(r"\bheat|thermal|land surface temperature|\bLST\b|hitze|temperatur|urban heat island|\bUHI\b", re.I)
SOCIAL = re.compile(r"social|socio|inequal|justice|equity|vulnerab|income|poverty|deprivation|rent|migra|foreign|ethnic|elderly|older|ungleich|gerecht|sozial|armut|miete", re.I)
PLACE = re.compile(r"german|deutschland|ruhr|nrw|north rhine|nordrhein|bochum|dortmund|essen|duisburg|gelsenkirchen|oberhausen|bottrop|herne|hagen|hamm|m(ü|u)lheim|census grid|zensus", re.I)

log_rows, pool = [], {}
for qid, q in QUERIES:
    for source, fn in (("OpenAlex", openalex), ("Crossref", crossref)):
        total, recs = fn(qid, q)
        log_rows.append({"query_id": qid, "source": source, "query": q, "date": TODAY,
                         "total_hits_reported": total, "records_saved": len(recs),
                         "raw_file": f"novelty_search/raw/{qid}_{source.lower()}.json"})
        for r in recs:
            k = r["doi"] or re.sub(r"\W+", "", r["title"].lower())[:120]
            if not k:
                continue
            if k not in pool:
                pool[k] = dict(r, found_by=set())
            pool[k]["found_by"].add(f"{qid}/{source}")
            if not pool[k]["abstract"] and r["abstract"]:
                pool[k]["abstract"] = r["abstract"]
        time.sleep(1)

with open(HERE / "novelty_search_log.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(log_rows[0]))
    w.writeheader()
    w.writerows(log_rows)

cands = []
for k, r in pool.items():
    text = f"{r['title']} {r['abstract']}"
    r["is_candidate"] = bool(HEAT.search(text) and SOCIAL.search(text) and PLACE.search(text))
    r["found_by"] = ";".join(sorted(r["found_by"]))
    if r["is_candidate"]:
        cands.append(r)

fields = ["doi", "title", "year", "first_author", "venue", "found_by", "is_candidate"]
with open(HERE / "novelty_records.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(sorted(pool.values(), key=lambda r: (not r["is_candidate"], str(r["year"]))))
with open(HERE / "novelty_candidates.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields + ["abstract"], extrasaction="ignore")
    w.writeheader()
    w.writerows(sorted(cands, key=lambda r: str(r["year"]), reverse=True))

print(f"queries: {len(QUERIES)} x 2 sources = {len(log_rows)} searches")
print(f"records saved (with duplicates): {sum(r['records_saved'] for r in log_rows)}")
print(f"unique records: {len(pool)}")
print(f"candidates (heat AND social AND Germany/Ruhr rule): {len(cands)}")
