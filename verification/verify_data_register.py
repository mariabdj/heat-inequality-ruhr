r"""GATES 2 to 5: every raw file is registered, its SHA-256 and size match the register, and licence and URL are filled.
Usage: .venv\Scripts\python.exe verification/verify_data_register.py
"""
import csv, hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "01_data" / "raw"
rows = list(csv.DictReader(open(ROOT / "01_data" / "data_register.csv", encoding="utf-8")))
reg = {r["file"]: r for r in rows}
errors = []


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


on_disk = {p.relative_to(RAW).as_posix() for p in RAW.rglob("*") if p.is_file()}
for f in sorted(on_disk - reg.keys()):
    errors.append(f"not registered: {f}")
for f, r in reg.items():
    p = RAW / f
    if not p.is_file():
        if "deleted" not in r["note"]:
            errors.append(f"registered but missing (and not marked deleted): {f}")
        continue
    if str(p.stat().st_size) != r["size_bytes"]:
        errors.append(f"size differs: {f}")
    if sha256(p) != r["sha256"]:
        errors.append(f"SHA-256 differs: {f}")
    for k in ("url", "licence", "attribution", "download_date"):
        if not r[k].strip():
            errors.append(f"{k} empty: {f}")
for e in errors:
    print("FAIL", e)
print(f"files on disk: {len(on_disk)}; registered: {len(reg)}")
print("RESULT: FAILED" if errors else "RESULT: PASSED")
sys.exit(1 if errors else 0)
