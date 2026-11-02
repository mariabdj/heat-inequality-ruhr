# Verification log: Project 4 heat inequality

Rules: see HEAT-INEQUALITY_WORKFLOW_GUIDE.md, Part A. Every gate run is appended below (never deleted).
A gate is PASSED only when all automatic AND manual checks pass. Run automatic checks with:
`.venv\Scripts\python.exe verification/run_gate.py <gate number>`

## Setup (before Gate 0) | 2026-11-02
- Python environment `.venv` created; all 19 packages import (output saved in the session, versions in SETUP_GUIDE.md).
- R packages z22 1.1.4, sf 1.1.3, terra 1.9.50, spdep 1.4.2, spatialreg 1.4.3, GWmodel 2.4.1, exactextractr 0.10.1, tmap 4.4.1 installed.
- `00_setup/z22_features_list.csv` written by z22::z22_features(): 55 features, 36 for 2022.
- Dataset inventory written (`00_setup/dataset_inventory.md`). OpenGeodata.NRW folder `umwelt_klima/klima/klimaanalyse/` checked by direct request on 2026-11-02: contains "Klimaatlas NRW - Planung und Bau: Klimaanalyse - Betroffenheitsanalyse" (timestamp 2026-10-09).

## Accounts | 2026-11-02
- Earth Engine: Cloud project `peppy-apparatus-452923-g2` (owner account checked in the console: Maria Boudjelal). Registered for noncommercial use (organisation type "Other", use case "individual research or noncommercial use", Community tier, no billing). Console message: project registered for noncommercial use, eligibility expires 2 May 2028. Earth Engine API enabled.
- Python login: `earthengine set_project` + `earthengine authenticate` (Maria accepted in her browser): "Successfully saved authorization token".
- Connection test (not an analysis, scene count only): Landsat 8 + 9 C2 T1 L2, point 7.2162 E 51.4818 N (Bochum centre), June to August, 2018-01-01 to 2026-01-01: 115 scenes; 28 with CLOUD_COVER < 20.
- Copernicus CLMS profile completed and saved (page reloaded: required-data warning gone).

## GATE 0: Set-up and novelty | run 1 | 2026-11-02 13:18
### verify_structure.py: PASS
```
RESULT: PASSED (11 folders, 7 files present)
verification\verify_structure.py:1: SyntaxWarning: invalid escape sequence '\S'
  """GATE 0: the project folder structure exists. Usage: .venv\Scripts\python.exe verification/verify_structure.py"""
```
### verify_novelty_log.py: PASS
```
queries in script: 15; searches logged: 30; records saved: 5142; unique: 4508; candidates: 139
RESULT: PASSED
```
Manual checks:
- [x] Folders of guide A8 exist (verify_structure.py above). Note: the SyntaxWarning comes from a backslash in the script's docstring, not from the check; fixed after this run.
- [x] Novelty search logged: 15 queries x OpenAlex + Crossref = 30 rows in `00_setup/novelty_search_log.csv`, raw answers in `00_setup/novelty_search/raw/`, numbers checked by verify_novelty_log.py. The check was also tested with a planted error (records_saved of row 1 changed from 200 to 199): it printed `report says 5,142, files give 5141` and `RESULT: FAILED`; file restored, check PASSED again.
- [x] All 139 candidate titles read; abstracts of 8 closest read; full text pages of the 5 closest read: Klopfer & Pfeiffer 2023 (p. 1, 5), Chawla et al. 2026 (p. 3), Anderson & Hasler 2026 (methods: LST from about 60 Landsat images 2013 to 2023, 154 tracts; limitations: suggestion to use 100 m census grids), Kühnl et al. 2026 (abstract), LANUK Fachbericht 171 (p. 16 method, p. 29 to 30 results). Each listed with DOI or report name and the difference in `00_setup/NOVELTY_REPORT.md` section 2.
- [x] LANUK Fachbericht 171 read on the relevant pages: deciles per municipality of density of people 80+, children under 6 and average net cold rent (Zensus 2022), combined and overlaid with heat zones (p. 16); area shares (p. 29). No statistical test of a heat gap by social group.
- [x] LEARNING_NOTEBOOK.md chapter for Step 0 written; its arithmetic computed by code from the log (5,142 saved; 5,142 - 4,508 = 634 duplicates; 139 / 4,508 = 0.0308).
- [ ] PENDING [MARIA]: confirms the question and the angle (NOVELTY_REPORT.md section 3).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PENDING (waiting for Maria's confirmation of the angle)
