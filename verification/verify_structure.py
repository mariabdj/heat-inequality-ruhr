r"""GATE 0: the project folder structure exists. Usage: .venv\Scripts\python.exe verification/verify_structure.py"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOLDERS = ["00_setup", "00_protocol", "01_data/raw", "01_data/processed", "02_lst", "03_covariates",
           "04_grid_join", "05_analysis/results", "06_manuscript", "verification", "Documentation"]
FILES = ["VERIFICATION_LOG.md", "README.md", "LEARNING_NOTEBOOK.md", "HEAT-INEQUALITY_WORKFLOW_GUIDE.md",
         "00_setup/dataset_inventory.md", "Documentation/README.md", ".gitignore"]

missing = [f for f in FOLDERS if not (ROOT / f).is_dir()] + [f for f in FILES if not (ROOT / f).is_file()]
for m in missing:
    print(f"FAIL missing: {m}")
print("RESULT: FAILED" if missing else f"RESULT: PASSED ({len(FOLDERS)} folders, {len(FILES)} files present)")
sys.exit(1 if missing else 0)
