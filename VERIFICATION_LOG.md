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

## GATE 0: Set-up and novelty | run 2 | 2026-11-02 13:27
### verify_structure.py: PASS
```
RESULT: PASSED (11 folders, 7 files present)
```
### verify_novelty_log.py: PASS
```
queries in script: 15; searches logged: 30; records saved: 5142; unique: 4508; candidates: 139
RESULT: PASSED
```
Manual checks:
- [x] Run 2 made after fixing the docstring warning of run 1 (no warning now); same numbers as run 1.
- [x] All manual checks of run 1 still hold (no file of the novelty search changed since; first commit `Set up project structure and novelty check` by Maria Boudjelal, no-reply email; verify_public_release.py PASSED).
- [x] [MARIA] confirmed the question and the angle in the chat on 2026-11-02: "Oui, je confirme".
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 1: Preregistration | run 1 | 2026-11-02 14:05
### verify_prereg.py: PASS
```
template questions checked: 25; census columns checked: 11; census files checked: 5
RESULT: PASSED
```
Manual checks:
- [x] Expert panel (guide A7, Part G roles for Gate 1: environmental epidemiologist, remote-sensing scientist, spatial econometrician): 6 rounds; 82 findings, each with its action in `00_protocol/expert_panel_log.md`; round 6: all three "No further problems".
- [x] Every template item answered: Q1 to Q25 each present once (verify_prereg.py) and each matched to the van den Akker et al. (2021) question wording read from the template PDF.
- [x] Every census variable exists with its exact column name: 11 backticked names checked against the 6 official description files; planted typo test (`AnteilUnter_18`) gave FAILED, file restored.
- [x] Facts used in the plan checked by code in this session: ST scale/offset and valid range (USGS guide Table 6-1, printed p. 12); scene centre times and paths (Earth Engine metadata); DWD "Sommertag" >= 25 C (DWD glossary); dense inverse in spreg ML variance step (source ml_error.py); hard_bound and lambda bounds (spreg utils.py); GM_Lag options; WCS NW DGM service answers; all 11 DOIs re-read on Crossref.
- [x] Knowledge disclosure (Q8, Q18): no census value and no temperature value has been opened; only description files, metadata, footprints and fill bits.
- [x] LEARNING_NOTEBOOK.md chapter for Step 1 written; arithmetic checked by code (44,947 -> 302.63 K -> 29.48 C; range 150.0 to 359.0 K; Holm example; bootstrap p example 0.013).
- [x] [MARIA] approved `00_protocol/preregistration.md` (draft 6, with the 11 cities) in the chat on 2026-11-02: "J'approuve".
- [x] OSF project https://osf.io/b3t8d/ (created 2026-11-02, private). Files uploaded: preregistration.md (OSF SHA-256 equals local 5819827ab3b654631fd492e1b83e5215b62b30786b799a70d771feaf9f9be2cb) and 00_setup/NOVELTY_REPORT.md.
- [x] Registration form "Secondary Data Preregistration" filled from the approved file by script; read back from the OSF API: 24 of 24 fields identical (after undoing OSF's HTML escaping of <, > and &). Subjects (5), tags (9), licence CC BY 4.0.
- [x] [MARIA] clicked Register: registration https://osf.io/cmxs2/, date_registered 2026-11-02T13:14:19 UTC; read back from the API after registration: 24 of 24 fields identical, archiving finished.
- [x] [MARIA] approved the registration from the OSF email ("C'est approuvé", 2026-11-02). Checked from the OSF API: public = true, pending approval = false, anonymous (logged-out) request returns 200, identifier doi:10.17605/OSF.IO/CMXS2.
- OSF registration: https://osf.io/cmxs2/ , DOI https://doi.org/10.17605/OSF.IO/CMXS2 , registered 2026-11-02 13:14 UTC.
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 2: Study area and grid | run 1 | 2026-11-02 14:34
### verify_data_register.py: PASS
```
files on disk: 3; registered: 3
RESULT: PASSED
```
### verify_grid.py: PASS
```
1. cells checked: 61458; not in BKG grid: 0; max corner diff: 0, 0 m; max centre diff: 0, 0 m
2. city differs from BKG municipality key: 269 cells (0.44%); by our city: {'Oberhausen': 50, 'Duisburg': 45, 'Dortmund': 37, 'Gelsenkirchen': 31, 'Bochum': 28, 'Essen': 23, 'Mülheim an der Ruhr': 16, 'Herne': 15, 'Hamm': 15, 'Hagen': 7, 'Bottrop': 2}
3. BKG cells with centre in the 11 cities: 168177 -> 1681.8 km2; VG250 area: 1682.0 km2; diff 0.013%
4. counts recomputed for 11 cities; total rule 3 cells: 51711
RESULT: PASSED
```
Manual checks:
- [x] Entry gate: Gate 1 PASSED (OSF https://osf.io/cmxs2/, 2026-11-02).
- [x] Self-built cells vs BKG GeoGitter: all 61,458 inhabited cells of the 11 cities checked (guide asks for at least 1,000): 0 not found, corner and centre differences 0 m. Cell ID vs centre columns of the census file: 0 mismatches in 3,088,037 cells.
- [x] Cells per city logged (`01_data/processed/step2_counts.csv`): rule 1 61,458; rule 2 51,719; rule 3 51,711 (3,261,441 inhabitants). Counted before any other census value or any heat value was opened (Q13).
- [x] Study-area check: 168,177 BKG cells x 0.01 km2 = 1,681.8 km2 vs VG250 1,682.0 km2 (0.013%).
- [x] City assignment differs from the BKG municipality key (VG25, 2019) for 269 cells (0.44%), all on city borders; the preregistered rule (centre in VG250 2026) is applied as written. (In the output above, "Mülheim" is shown with a broken character by the log encoding; the data are correct.)
- [x] Every raw file registered with SHA-256 (verify_data_register.py). Planted-error test of verify_grid.py (one count changed): FAILED as expected, restored, PASSED.
- [x] Deviation D1 logged before use (population column `Einwohner` instead of `Bevoelkerungszahl`, naming only).
- [x] Rule 3 water share: Earth Engine ESA/WorldCover/v200, Map == 80, area-weighted mean at 10 m over each cell rectangle in EPSG:3035; values for all 51,719 cells passing rule 2 (0 missing).
- [x] LEARNING_NOTEBOOK.md chapter for Step 2 written; its numbers recomputed by code (61,458 - 51,719 = 9,739; 51,719 - 51,711 = 8; 3,312,842 - 3,261,441 = 51,401).
- Expert panel: not required at this gate (guide A7: internal step, reviewed at Gate 7).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 3: Census data | run 1 | 2026-11-02 16:17
### verify_data_register.py: PASS
```
files on disk: 8; registered: 8
RESULT: PASSED
```
### verify_census_parse.py: PASS
```
official rent versions (2025 file we use vs 2024 file): cells differing 683, max |diff| 0.0100 EUR
rent: both 45613, max |diff| 0.0000, values > 0.005 apart 0; official dash with no z22 value 0; other presence differences 0
foreign: both 32742, max |diff| 0.0000, values > 0.005 apart 0; official dash with no z22 value 28716; other presence differences 0
age65: both 50642, max |diff| 0.0000, values > 0.005 apart 0; official dash with no z22 value 10816; other presence differences 0
under18: both 45499, max |diff| 0.0000, values > 0.005 apart 0; official dash with no z22 value 15959; other presence differences 0
RESULT: PASSED
```
Manual checks:
- [x] Entry gate: Gate 2 PASSED (2026-11-02).
- [x] Python reader vs R z22: identical for every study-area cell (0 differences above 0.005) once both read the same file. Explained differences: (a) official dash ('–') = z22 no value (28,716 / 10,816 / 15,959 cells for foreign / 65+ / under 18); (b) z22 reads the rent-only file (Version 2, 30.09.2024), we read the preregistered rent + dwellings file (Version 2, 08.07.2025): the two official versions differ by exactly 0.01 EUR in 683 cells. Found by investigation (rent-only file downloaded and registered as "check only"); the comparison was changed to the same source, the tolerance (0.005) was not changed.
- [x] Missingness table per variable and city (`05_analysis/results/step3_missingness.csv`): usable (present and not bracketed) among 51,711 cells: rent 43,283 (83.7%; 7,890 absent, 538 bracketed), foreign 35,152 (68.0%), 65+ 32,371 (62.6%), under 18 27,614 (53.4%); all four usable: 12,692.
- [x] Distributions plotted per variable (`05_analysis/results/figures/step3_distributions.png`); no relationship with heat computed or looked at (no heat data exist yet).
- [x] Observation (no change to the plan): bracketed shares are mostly small non-zero shares from small cells (median population 31 vs 66 for usable 65+ shares). Primary analysis stays as registered (brackets = missing); S1 (brackets included) will be reported with the same prominence in the discussion.
- [x] Flags: only "" and "KLAMMERN" occur (script asserts no other flag); rent file has one flag column for rent and number of dwellings, applied to rent.
- [x] LEARNING_NOTEBOOK.md chapter for Step 3 written.
- Expert panel: not required at this gate (guide A7).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## Step 4 decision record (before any temperature was converted) | 2026-11-02
- Hot-day rule fixed in `01_data/data_register.csv` before the station data were downloaded: TXK >= 25.0 C, QN_4 in {2, 3, 5, 7, 8, 9, 10}. Station 01303: 736 June-August days 2018-2025, 0 missing, all QN_4 = 9, 268 hot days.
- Stage 1 (flags only) first run discarded: the city outlines had been sent to Earth Engine in UTM coordinates, which Earth Engine reads as longitude/latitude, so the city mask was wrong (4.75 million core pixels). Files kept in `02_lst/discarded/`. No temperature was involved.
- Stage 1 rerun: city pixels 1,878,332 (1,690.5 km2 vs VG250 1,681.3 km2); reference domain 1,840,185 pixels; core reference domain 1,759,285 (95.6%). 115 candidate scenes, 17 used (>= 80% valid core pixels), 16 hot-day and used.
- Q23 check: 0.6% of the 51,711 cells have < 70% of their area covered by pixels with >= 5 valid hot-day observations (threshold 30%): hot-day rule kept, no fallback.

## GATE 4: Land surface temperature | run 1 | 2026-11-02 17:29
### verify_data_register.py: PASS
```
files on disk: 13; registered: 13
RESULT: PASSED
```
### verify_lst_pixels.py: PASS
```
(a) scene 1_LC08_196024_20190629: 20 pixels, valid 20, validity agrees: True, max |diff| 0.00000 C (example DN 48526 -> 41.713 C)
(a) scene 1_LC08_197024_20190823: 20 pixels, valid 19, validity agrees: True, max |diff| 0.00000 C (example DN 44400 -> 27.610 C)
(a) scene 2_LC09_197024_20250815: 20 pixels, valid 19, validity agrees: True, max |diff| 0.00000 C (example DN 45856 -> 32.587 C)
(b) scene 1_LC08_196024_20190629: 1739364 valid core pixels, numpy median 38.4555 C, pipeline median 38.4555 C, |diff| 0.0000
(b) scene 1_LC08_197024_20190823: 1693538 valid core pixels, numpy median 31.8279 C, pipeline median 31.8279 C, |diff| 0.0000
(b) scene 2_LC09_197024_20250815: 1503645 valid core pixels, numpy median 33.8070 C, pipeline median 33.8070 C, |diff| 0.0000
(c) 20 composite pixels recomputed from 16 scenes: max |diff| 0.00000 C
RESULT: PASSED
```
Manual checks:
- [x] Entry gate: Gate 3 PASSED. Q23 decision logged above before any temperature was converted (hot-day rule kept, 0.6% < 30%).
- [x] Independent check (guide: at least 3 scenes x 20 pixels from raw DN, within 0.01 C): 3 scenes x 20 pixels, max |diff| 0.00000 C, validity identical. Also exact medians (3 scenes, |diff| 0.0000 C) and 20 composite pixels recomputed from all 16 scenes (|diff| 0.00000 C, same observation counts).
- [x] Two pipeline errors found by this check and fixed before any use, failed runs kept in `02_lst/discarded/`: (1) Earth Engine median is histogram-based (0.045 to 0.114 C off): medians now exact, computed locally with numpy on the downloaded scenes; (2) download outside a scene footprint returned 0 (unmask without sameFootprint=False), counted as observations at 0 C at the edges: fixed, composite recomputed. Same definitions as the preregistration (Q12.5, Q12.6); no deviation.
- [x] Valid observations per pixel mapped (`05_analysis/results/figures/step4_lst_and_obs.png`); composite pixels with >= 5 observations: 5,620,452 (whole download rectangle).
- [x] Scene balance reported (Q12.6): 16 hot-day scenes; Landsat 8: 9, Landsat 9: 7; path 196: 8, path 197: 8; years 2018: 2, 2019: 2, 2021: 1, 2023: 4, 2024: 3, 2025: 3 (none from 2020 and 2022). S14 covers the year imbalance.
- [x] Visual check against the LANUK day map (typical summer day, averaged to our grid): same broad hot and cool areas (`05_analysis/results/figures/step4_lanuk_comparison.png`); Spearman correlation over 1,745,112 core pixels: 0.637.
- [x] Note: the 80% scene rule used Earth Engine pixel sums that weight pixels cut by the region rectangle; the same weights enter numerator and denominator.
- [x] LEARNING_NOTEBOOK.md chapter for Step 4 written; its arithmetic checked by code (48,526 -> 41.7128 C; anomaly +3.257 C; 45,750 -> 32.2244 C).
- Expert panel: not required at this gate (guide A7: reviewed at Gate 7).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 5: Covariates | run 1 | 2026-11-02 18:16
### verify_data_register.py: PASS
```
files on disk: 18; registered: 18
RESULT: PASSED
```
### verify_covariates.py: PASS
```
tree_cover_2022: files 1; cells 51711; missing or out of range 0; range 0.0 to 99.0
imperviousness_2021: files 2; cells 51711; missing or out of range 0; range 0.0 to 100.0
elevation_dgm: files 1; cells 51711; missing or out of range 0; range 14.8 to 406.3
RESULT: PASSED
```
Manual checks:
- [x] Entry gate: Gate 4 PASSED.
- [x] Each layer registered with version, licence and SHA-256 (18 files, verify_data_register.py): Copernicus tree cover density 10 m reference year 2022 (preregistered year; 2018 to 2024 offered), imperviousness density 10 m 2021 (V01 R02, tiles E40N31 and E41N31), CLMS job 7188 archive; NRW terrain model (WCS NW DGM, 77 tiles, 10 m, dl-de/zero-2-0).
- [x] Reprojection logged: tree cover and imperviousness delivered in EPSG:3035 (same as the cells): no reprojection. Terrain model in EPSG:25832: the raster is not resampled by us; cell polygons will be reprojected to EPSG:25832 for zonal statistics (Step 6). The 1 m to 10 m resampling of the terrain model was done by the NRW service (method not documented in the capabilities; elevation varies slowly at 100 m).
- [x] Coverage: 0 of 51,711 cells without a valid value in any layer (verify_covariates.py). Special value 255 (no data, from the legend file clms_hrlvlcc_tcd_r10m.clr): 0 pixels inside the 11 cities for both Copernicus layers (16.8 million pixels each); Step 6 will still treat values above 100 as missing.
- [x] Terrain model plausibility: 14.8 m (Rhine plain) to 406.3 m (Hagen hills) at cell centres.
- [x] LEARNING_NOTEBOOK.md chapter for Step 5 written.
- Expert panel: not required at this gate (guide A7).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 6: Grid join | run 1 | 2026-11-02 18:45
### verify_zonal.R: PASS
```
|---------|---------|---------|---------|
=========================================
                                          
cells: 61458 
Warning message:
In .local(x, y, ...) :
  Polygons transformed to raster CRS (EPSG: 3035) . To avoid on-the-fly coordinate transformation, ensure that st_crs() returns the same result for both raster and polygon inputs.
```
### verify_zonal.py: PASS
```
lst_anom: compared 61195, max |diff| 0.000001 (tolerance 0.01), cells above tolerance 0, presence differs 0
lst_cover_share: compared 61458, max |diff| 0.000000 (tolerance 0.001), cells above tolerance 0, presence differs 0
tree_cover: compared 61458, max |diff| 0.000008 (tolerance 0.1), cells above tolerance 0, presence differs 0
imperviousness: compared 61458, max |diff| 0.000004 (tolerance 0.1), cells above tolerance 0, presence differs 0
elevation: compared 61458, max |diff| 0.000032 (tolerance 0.01), cells above tolerance 0, presence differs 0
rasterstats (pixel centres) vs exactextract (exact shares), cells passing rule 4: mean |diff| 0.077 C, 90th percentile 0.176 C, max 0.881 C
rows: 61458; passing rules 1 to 4: 51409; Model A sample: 12609
RESULT: PASSED
```
Manual checks:
- [x] Entry gate: Gate 5 PASSED.
- [x] Python exactextract vs R exactextractr (cells rebuilt from IDs in R): within tolerance for every cell (max |diff| LST 0.000001 C, coverage share 0.000000, tree cover 0.000008, imperviousness 0.000004 percentage points, elevation 0.000032 m). rasterstats (pixel-centre method) differs by 0.077 C on average (max 0.881 C): reported. Planted error (+0.5 point in one R tree value): FAILED as expected, restored, PASSED.
- [x] Row count = inhabited cells of the 11 cities (61,458). Exclusions table by reason (`05_analysis/results/step6_exclusions.csv`): rule 2 -9,739; rule 3 -8; rule 4 -302; passing rules 1 to 4: 51,409; covariates missing 0; Model A sample 12,609.
- [x] No-data code 255 of the Copernicus layers: 0 cells touched (column max checked).
- [x] No relationship between heat and social variables was computed (only per-variable summaries of the Model A sample, logged in the notebook as a description of the sample).
- [x] LEARNING_NOTEBOOK.md chapter for Step 6 written (worked example: (2 x 1.0 + 4 x 0.5 + 6 x 0.25) / 1.75 = 3.14 C).
- Expert panel: not required at this gate (guide A7: Steps 2 to 6 are reviewed at Gate 7).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED
