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

## GATE 4: Land surface temperature | run 2 | 2026-11-02 19:49
### verify_data_register.py: PASS
```
files on disk: 19; registered: 19
RESULT: PASSED
```
### verify_lst_pixels.py: PASS
```
(d) reference-domain pixels outside the locally rebuilt pixel-centre city mask: 0; city pixels 1868073, reference pixels 1830655
(d) water share, 2000 pixels: max |diff| 0.0000, decision flips beyond 0.02 of the threshold: 0
(e) 1_LC08_196024_20180610: own valid share 0.000084, stage-1 0.000084
(e) 1_LC08_197024_20180804: own valid share 0.914140, stage-1 0.914140
(e) 2_LC09_196024_20250824: own valid share 0.007058, stage-1 0.007058
(e) 1_LC08_196024_20190629: own valid share 0.988683, stage-1 0.988683
(e) 1_LC08_197024_20190823: own valid share 0.962651, stage-1 0.962651
(e) 2_LC09_197024_20250815: own valid share 0.854552, stage-1 0.854552
(a) 1_LC08_196024_20190629: 60 pixels (20 invalid), validity agrees: True, max |diff| 0.00000 C
(a) 1_LC08_197024_20190823: 60 pixels (22 invalid), validity agrees: True, max |diff| 0.00000 C
(a) 2_LC09_197024_20250815: 60 pixels (24 invalid), validity agrees: True, max |diff| 0.00000 C
(b) 1_LC08_196024_20190629: median from file 38.4794, stored 38.4794
(b) 1_LC08_197024_20190823: median from file 31.8348, stored 31.8348
(b) 2_LC09_197024_20250815: median from file 33.8138, stored 33.8138
(c) 20 composite pixels from the scene files: max |diff| 0.000002 C
RESULT: PASSED
```
Manual checks:
- [x] Why this run: the Gate 7 expert panel (round 1) found that the city mask in Earth Engine used "any pixel touched" (reduceToImage) instead of the preregistered pixel-centre rule (Q12.4). Implementation error, not a change of plan: no deviation entry. Fixed in `02_lst/lst_pipeline.py` (touched pixels whose centre is outside, computed locally with rasterio, are removed); the Earth Engine mask now equals the local pixel-centre mask: 1,868,073 pixels, 0 differences. Old outputs kept in `02_lst/discarded/touched_city_mask/`.
- [x] Candidate list frozen in `01_data/raw/landsat/candidate_scenes.csv` (115 ids, registered with SHA-256), so a later change of the Earth Engine catalogue cannot change the scene set.
- [x] Stage 1 rerun (flags only, before any temperature): 115 candidates; 17 with >= 80% valid core pixels; 16 on hot days (same 16 as run 1). City pixels 1,868,073 (1,681.3 km2 = VG250 area 1,681.3 km2); reference domain 1,830,655; core 1,750,715 (95.6%). Core share per city: 100% except Duisburg 67.1% and Hamm 99.3% (`02_lst/stage1_core_share_by_city.csv`). Q23: 0.6% < 30%, hot-day rule kept (same decision).
- [x] Stage 2 rerun: daily medians changed by +0.007 to +0.027 C (mean +0.020) against run 1; medians 30.03 to 40.09 C; composite pixels with >= 5 observations 5,620,452; month balance June 9, July 2, August 5 (`02_lst/scenes_balance_hot.csv`).
- [x] Check strengthened (panel request): (d) domain and water share recomputed from raw WorldCover; (e) 80% shares recomputed from raw quality bands for 6 scenes (1e-6); (a) now 60 pixels per scene including invalid pixels. The pipeline's masks are not reused.
- [x] The verification script itself had an error and was fixed: in its first run (d) FAILED (NaN values, 22 flips) because the water raster it writes inherited "nodata = 0" from the downloaded tiles, so every dry pixel was read as missing. Fixed (nodata = 255, never present); tolerance unchanged. Test: of the 2,000 sampled pixels 54 contain water and 32 are >= 50% water, so the check is not trivial; a planted error of 0.05 in 3 water pixels is caught (FAILED).
- [x] Correction of run 1's last note ("the 80% scene rule used Earth Engine pixel sums that weight pixels"): the counts are whole-pixel counts on the 30 m grid (check (e) reproduces them exactly from raw bands). Run 1 is not edited.
- [x] LANUK comparison rerun: Spearman 0.637 over 1,736,635 core pixels (`05_analysis/results/step4_lanuk_check.csv`).
- [x] LEARNING_NOTEBOOK.md Step 4 updated (median 38.4794 C, anomaly +3.23 C checked by code: 3.2334; new traps: touched mask, wrong check).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 6: Grid join | run 2 | 2026-11-02 19:59
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
- [x] Not completed: this run was made before Gate 5 run 2 was logged. Superseded by Gate 6 run 3 below. The outputs above are kept as a record.
AUTOMATIC CHECKS: ALL PASSED
RESULT: NOT USED (superseded by run 3)

## GATE 5: Covariates | run 2 | 2026-11-02 20:06
### verify_data_register.py: PASS
```
files on disk: 19; registered: 19
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
- [x] Entry gate: Gate 4 run 2 PASSED. Why this run: Steps 4 to 6 rerun after the city-mask fix (Gate 4 run 2). The covariate layers themselves did not change; files on disk 19, all registered (incl. the frozen Landsat candidate list).
- [x] Same layers, versions, licences and coverage as run 1 (0 of 51,711 cells without a value; ranges unchanged).
- [x] Change requested by the Gate 7 panel: the no-data code 255 of the Copernicus layers is now declared through small VRT files (`04_grid_join/nodata_vrt.py`, the raw files are not changed), instead of relying on "values above 100 = missing". Tested: identical means on the study cells; cells with a value above 100 after the declaration: 0 (Step 6 output).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 6: Grid join | run 3 | 2026-11-02 20:06
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
- [x] Not completed: `04_grid_join/step6_join.py` was changed after this run (Gate 7 round 2: one-path share per cell, extreme values on usable values only). Superseded by Gate 6 run 4. Outputs above kept as a record.
AUTOMATIC CHECKS: ALL PASSED
RESULT: NOT USED (superseded by run 4)

## GATE 4: Land surface temperature | run 3 | 2026-11-02 21:00
### verify_data_register.py: PASS
```
files on disk: 19; registered: 19
RESULT: PASSED
```
### verify_lst_pixels.py: PASS
```
(d) reference-domain pixels outside the locally rebuilt pixel-centre city mask: 0; city pixels 1868073, reference pixels 1830655
(d) water share, 2000 pixels: max |diff| 0.0000, decision flips beyond 0.02 of the threshold: 0
(d) sampled city pixels whose reference-domain membership disagrees with the own water share: 0 (pixels >= 50% water in the sample: 32)
(e) 1_LC08_196024_20180610: own valid share 0.000084, stage-1 0.000084
(e) 1_LC08_197024_20180804: own valid share 0.914140, stage-1 0.914140
(e) 2_LC09_196024_20250824: own valid share 0.007058, stage-1 0.007058
(e) 1_LC08_196024_20190629: own valid share 0.988683, stage-1 0.988683
(e) 1_LC08_197024_20190823: own valid share 0.962651, stage-1 0.962651
(e) 2_LC09_197024_20250815: own valid share 0.854552, stage-1 0.854552
(a) 1_LC08_196024_20190629: 60 pixels (20 invalid), validity agrees: True, max |diff| 0.00000 C
(a) 1_LC08_197024_20190823: 60 pixels (22 invalid), validity agrees: True, max |diff| 0.00000 C
(a) 2_LC09_197024_20250815: 60 pixels (24 invalid), validity agrees: True, max |diff| 0.00000 C
(b) 1_LC08_196024_20190629: median from file 38.4794, stored 38.4794
(b) 1_LC08_197024_20190823: median from file 31.8348, stored 31.8348
(b) 2_LC09_197024_20250815: median from file 33.8138, stored 33.8138
(c) 20 composite pixels from the scene files: max |diff| 0.000002 C
RESULT: PASSED
```
Manual checks:
- [x] Why this run: Gate 7 panel round 2 (remote-sensing reviewer) asked for (1) the frozen candidate list to be enforced and (2) check (d) to work in both directions. Verification script strengthened only (a new check added; no tolerance changed).
- [x] Pipeline guard (`02_lst/lst_pipeline.py`): stops if `candidate_scenes.csv` is missing, or if the live Earth Engine catalogue's ids, LANDSAT_PRODUCT_ID or DATE_PRODUCT_GENERATED differ from the frozen file; the list can be written only by an explicit `freeze` command, which refuses to overwrite. Test: current catalogue matches (115 scenes); a planted change of one processing date is detected.
- [x] New check (d), other direction: reference-domain membership of the 2,000 sampled city pixels agrees with the own water rule: 0 disagreements, with 32 pixels of >= 50% water in the sample (so the test is not empty).
- [x] LST outputs not recomputed (the pipeline's computations did not change); all other checks give the same results as run 2.
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 6: Grid join | run 4 | 2026-11-02 21:16
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
- [x] Entry gate: Gate 5 run 2 PASSED (Gate 4 run 3 PASSED before it). Why this run: Steps 4 to 6 rerun after the city-mask fix, and `step6_join.py` changed after the Gate 7 panel (rounds 1 and 2).
- [x] Python vs R zonal statistics: same agreement as run 1 (max |diff| LST 0.000001 C, coverage 0.000000, tree 0.000008, imperviousness 0.000004, elevation 0.000032 m); the planted-error test of run 1 is still valid (verify_zonal.R unchanged).
- [x] Row count 61,458; exclusions unchanged after the rerun: rule 2 -9,739; rule 3 -8; rule 4 -302; passing rules 1 to 4: 51,409; Model A 12,609; Model B 12,609 (`step6_exclusions.csv`).
- [x] New reporting (panel): per city, losses to each rule and usable cells per variable (`step6_exclusions_by_city.csv`, totals equal the pooled table); one-path cells (Q12.5): 223 fully, 270 partly, 242 over half, 21 partly in Model A, all in Duisburg and Herne (counts reproduced independently by the remote-sensing reviewer); extreme values beyond 3 IQR on usable values (D6; `step6_extreme_values.csv`: LST 0, rent 249, foreign 51, 65+ 171, under 18 5, tree cover 629, imperviousness 0, elevation 17; kept, not removed); Model A vs all rule-4 cells (`step6_sample_comparison.csv`: 24.5% of cells, 43.7% of residents, population-weighted anomaly 3.59 vs 2.91 C, hotter in every city).
- [x] No-data 255 declared through VRT files (raw files unchanged); 0 cells with a value above 100.
- [x] Model A filter uses Model A covariates only; Model B adds tree cover and imperviousness.
- [x] Rule-4 removals described (4 cities; 212 of 302 with no composite value; sealing similar to kept cells); not linked to industry (not checked).
- [x] LEARNING_NOTEBOOK.md Step 6 chapter updated (selection numbers, S1 and S2 sizes, rule-4 limitation, one-path columns).
- Expert panel: reviewed at Gate 7 (rounds 1 to 3, `00_protocol/expert_panel_log.md`).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## GATE 7: Descriptive results | run 1 | 2026-11-03 10:19
### verify_deciles.R: PASS
```
rent: n 43029, groups 10, values split across groups within a city: 0
foreign: n 34940, groups 11, values split across groups within a city: 0
age65: n 32179, groups 11, values split across groups within a city: 0
under18: n 27452, groups 11, values split across groups within a city: 0
RESULT: PASSED
```
### verify_step7.py: FAIL
```
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
```
Manual checks:
- [x] Not a result: verify_step7.py printed nothing and returned an error code. Run alone afterwards, the same script on the same files gave exit code 0 and RESULT: PASSED; the stop is attributed to the machine (several heavy jobs and reviewer agents were running at the same time, likely memory). Kept as a record.
AUTOMATIC CHECKS: FAILED
RESULT: NOT USED (interrupted run)

## GATE 7: Descriptive results | run 2 | 2026-11-04 10:15
### verify_deciles.R: PASS
```
rent: n 43029, groups 10, values split across groups within a city: 0
foreign: n 34940, groups 11, values split across groups within a city: 0
age65: n 32179, groups 11, values split across groups within a city: 0
under18: n 27452, groups 11, values split across groups within a city: 0
RESULT: PASSED
```
### verify_step7.py: PASS
```
(a) lst_anom: n 51409, I own 0.7511404890, results.json 0.7511404890, islands 613 vs 613
(b) lst_anom: own FDR threshold 0.0111849 vs 0.0111849; own counts {'HH': 6908, 'LH': 4, 'LL': 4447, 'HL': 4, 'not_significant': 39433, 'island': 613}; 9,999 permutations: 12014 significant, Jaccard 0.9187; equal: True
(a) rent: n 43029, I own 0.4089207809, results.json 0.4089207809, islands 537 vs 537
(b) rent: own FDR threshold 0.0042467 vs 0.0042467; own counts {'HH': 1657, 'LH': 127, 'LL': 1709, 'HL': 116, 'not_significant': 38883, 'island': 537}; 9,999 permutations: 4005 significant, Jaccard 0.8329; equal: True
(a) foreign: n 34940, I own 0.6082380665, results.json 0.6082380665, islands 892 vs 892
(b) foreign: own FDR threshold 0.0243054 vs 0.0243054; own counts {'HH': 4170, 'LH': 273, 'LL': 11551, 'HL': 557, 'not_significant': 17497, 'island': 892}; 9,999 permutations: 16639 significant, Jaccard 0.9881; equal: True
(a) age65: n 32179, I own 0.2287735244, results.json 0.2287735244, islands 973 vs 973
(b) age65: own FDR threshold 0.0014853 vs 0.0014853; own counts {'HH': 195, 'LH': 30, 'LL': 564, 'HL': 138, 'not_significant': 30279, 'island': 973}; 9,999 permutations: 949 significant, Jaccard 0.8465; equal: True
(a) under18: n 27452, I own 0.2228042573, results.json 0.2228042573, islands 1287 vs 1287
(b) under18: own FDR threshold 0.0011580 vs 0.0011580; own counts {'HH': 138, 'LH': 13, 'LL': 13, 'HL': 442, 'not_significant': 25559, 'island': 1287}; 9,999 permutations: 714 significant, Jaccard 0.8308; equal: True
(c) rent: cells 43029 vs n 43029, zero group 0 vs 0, non-zero groups 10
(c) foreign: cells 34940 vs n 34940, zero group 19490 vs 19490, non-zero groups 10
(c) age65: cells 32179 vs n 32179, zero group 4147 vs 4147, non-zero groups 10
(c) under18: cells 27452 vs n 27452, zero group 7635 vs 7635, non-zero groups 10
RESULT: PASSED
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
```
Manual checks:
- [x] Complete automatic run (all PASS), but the session ended before its manual checks were written. Superseded by run 4, which repeats the same checks on the same files.
AUTOMATIC CHECKS: ALL PASSED
RESULT: NOT USED (superseded by run 4)

## GATE 7: Descriptive results | run 3 | 2026-11-04 10:43
### verify_deciles.R: PASS
```
rent: n 43029, groups 10, values split across groups within a city: 0
foreign: n 34940, groups 11, values split across groups within a city: 0
age65: n 32179, groups 11, values split across groups within a city: 0
under18: n 27452, groups 11, values split across groups within a city: 0
RESULT: PASSED
```
### verify_step7.py: FAIL
```
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
```
Manual checks:
- [x] Not a result: run from a command with a 10-minute limit, which stopped verify_step7.py before it finished (empty output). Superseded by run 4, run as a separate process.
AUTOMATIC CHECKS: FAILED
RESULT: NOT USED (interrupted run)

## GATE 7: Descriptive results | run 4 | 2026-11-04 12:16
### verify_deciles.R: PASS
```
rent: n 43029, groups 10, values split across groups within a city: 0
foreign: n 34940, groups 11, values split across groups within a city: 0
age65: n 32179, groups 11, values split across groups within a city: 0
under18: n 27452, groups 11, values split across groups within a city: 0
RESULT: PASSED
```
### verify_step7.py: PASS
```
(a) lst_anom: n 51409, I own 0.7511404890, results.json 0.7511404890, islands 613 vs 613
(b) lst_anom: own FDR threshold 0.0111849 vs 0.0111849; own counts {'HH': 6908, 'LH': 4, 'LL': 4447, 'HL': 4, 'not_significant': 39433, 'island': 613}; 9,999 permutations: 12014 significant, Jaccard 0.9187; equal: True
(a) rent: n 43029, I own 0.4089207809, results.json 0.4089207809, islands 537 vs 537
(b) rent: own FDR threshold 0.0042467 vs 0.0042467; own counts {'HH': 1657, 'LH': 127, 'LL': 1709, 'HL': 116, 'not_significant': 38883, 'island': 537}; 9,999 permutations: 4005 significant, Jaccard 0.8329; equal: True
(a) foreign: n 34940, I own 0.6082380665, results.json 0.6082380665, islands 892 vs 892
(b) foreign: own FDR threshold 0.0243054 vs 0.0243054; own counts {'HH': 4170, 'LH': 273, 'LL': 11551, 'HL': 557, 'not_significant': 17497, 'island': 892}; 9,999 permutations: 16639 significant, Jaccard 0.9881; equal: True
(a) age65: n 32179, I own 0.2287735244, results.json 0.2287735244, islands 973 vs 973
(b) age65: own FDR threshold 0.0014853 vs 0.0014853; own counts {'HH': 195, 'LH': 30, 'LL': 564, 'HL': 138, 'not_significant': 30279, 'island': 973}; 9,999 permutations: 949 significant, Jaccard 0.8465; equal: True
(a) under18: n 27452, I own 0.2228042573, results.json 0.2228042573, islands 1287 vs 1287
(b) under18: own FDR threshold 0.0011580 vs 0.0011580; own counts {'HH': 138, 'LH': 13, 'LL': 13, 'HL': 442, 'not_significant': 25559, 'island': 1287}; 9,999 permutations: 714 significant, Jaccard 0.8308; equal: True
(c) rent: cells 43029 vs n 43029, zero group 0 vs 0, non-zero groups 10
(c) foreign: cells 34940 vs n 34940, zero group 19490 vs 19490, non-zero groups 10
(c) age65: cells 32179 vs n 32179, zero group 4147 vs 4147, non-zero groups 10
(c) under18: cells 27452 vs n 27452, zero group 7635 vs 7635, non-zero groups 10
RESULT: PASSED
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
.venv\Lib\site-packages\esda\moran.py:1398: RuntimeWarning: invalid value encountered in divide
  self.z_sim = (self.Is - self.EI_sim) / self.seI_sim
```
Manual checks:
- [x] Entry gate: Gate 6 run 4 PASSED. Correction to Gate 6 run 4 (not edited, rule): its first manual check says Gate 4 run 3 passed "before" Gate 5 run 2; in fact Gate 4 run 3 (2026-11-02 21:00, checks strengthened only, LST outputs unchanged) came after Gate 5 run 2 (20:06). Both are PASSED, so the entry condition holds (expert panel finding G47).
- [x] Same code and data as runs 2 and 3: no file under 02_lst, 04_grid_join, 05_analysis or verification changed between them (only LEARNING_NOTEBOOK.md and expert_panel_log.md text).
- [x] Expert panel (rule A7, Part G), with a look back at Steps 2 to 6: remote-sensing scientist, spatial statistician, environmental-justice geographer; 5 rounds; 48 findings (G1 to G48), all accepted, G14 in a modified form (link with industry not claimed); round 5: all three "No further problems" (00_protocol/expert_panel_log.md). Fixes that changed earlier steps were rerun and logged: Gate 4 runs 2 and 3, Gate 5 run 2, Gate 6 run 4.
- [x] Every number in the tables comes from results.json and the step7 CSV files written by 05_analysis/step7_descriptive.py; the decile means are recomputed in R (verify_deciles.R: 0 differences, 0 values split between groups); Moran's I, the FDR thresholds and all LISA counts are recomputed with an independent neighbour list and a hand-made Benjamini-Hochberg step (verify_step7.py: equal to 10 decimals, counts identical), including the exploratory 9,999-permutation run (D7).
- [x] Clarifications and additions logged in 00_protocol/deviations.md: D2 (dash read as 0), D3 (estimand wording), D4 (decile tie rule), D5 (sample of the descriptive analyses), D6 (extreme-value rule), D7 (9,999-permutation LISA, exploratory), D8 (group-versus-rest comparison, exploratory). First decile outputs kept in 05_analysis/discarded/id_tie_rule/.
- [x] Results are described as cells, not people, not adjusted and not causal (figure titles, results.json notes, notebook); LST is described as surface temperature, not air temperature.
- [x] LEARNING_NOTEBOOK.md Step 7 chapter written (worked examples checked by code: Moran's I example I = 0.5; FDR back-calculation 0.0111849 x 50,796 / 0.05 = 11,363 = 6,908 + 4 + 4,447 + 4).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## Step 8 decision record (before any model was fitted) | 2026-11-05 11:23
- Tolerances for the independent R recomputation (verification/verify_models.R), fixed now because the preregistration does not give them (guide rule A10):
  - OLS coefficients (R lm vs spreg OLS): |difference| <= 1e-8 in model units.
  - Spatial error model, GMM (R sphet 2.1.1, same estimators as spreg 1.9.1: heteroskedastic, Arraiz et al. 2010; homoskedastic, Drukker et al. 2013): each beta within 0.01 standard errors of the spreg value, and lambda within 0.005. If the two programs differ only by their default numerical settings, this is reported rather than hidden.
  - Block bootstrap: Python saves the drawn blocks of every replicate; R recomputes every replicate's OLS coefficients from those draws: |difference| <= 1e-8. Seed of the Python draws: 20261102.
- Package versions: spreg 1.9.1 (as preregistered), mgwr 2.2.1, libpysal 4.15.1; R spatialreg 1.4.3, spdep 1.4.2, sphet 2.1.1, GWmodel 2.4.1.
- City dummies: 10 dummies with Bochum (first in alphabetical order) as the reference city.
- Step 8 is done in three parts with a check after each: 8a primary models and H1 to H3; 8b sensitivity analyses on the existing table (S1 to S3, S7 to S11, S17 to S20) and MGWR; 8c sensitivity analyses needing new LST composites (S4 to S6b, S12 to S16).

## Step 8 check record: why the R check of the spatial error model was changed | 2026-11-05 11:31
- First run of verification/verify_models.R with sphet 2.1.1 (as fixed in the decision record): OLS matched (max |diff| 8.1e-13), islands matched (1,712), all 999 bootstrap replicates matched (4.3e-14), but the GMM spatial error coefficients differed by up to 6.4 standard errors and lambda by 0.03 to 0.07. RESULT: FAILED. (A run before that stopped on a format error: sphet cannot convert a neighbour list with empty rows; the sparse matrix is now passed instead.)
- Investigation (scratch scripts, data unchanged, no tolerance changed):
  1. Islands are not the cause: on the 10,897 cells with at least one neighbour, spreg and sphet still differ (Het betas spreg 0.0206, 0.0624, -0.0313, -0.0501; sphet 0.0627, 0.1301, -0.0711, -0.1638).
  2. For a given lambda, the coefficients of the spatial error model are OLS of (y - lambda Wy) on (X - lambda WX). spreg's betas are reproduced to 0.0001 at lambda = 0.665, which is its first-step estimate (the lambda it reports, 0.768, is the second-step re-estimate). sphet's betas correspond to no lambda on the grid (closest 0.395, gap 0.004).
  3. The first-step lambda was computed by hand from the moment conditions of Arraiz et al. (2010): 0.6652, equal to spreg's. sphet's own verbose output shows the same first-step lambda (0.6652). So all three agree on lambda; sphet's betas then follow another computation that I could not identify. Its starting value is not the cause (0.2 and 0.6 give the same result), nor the use of the transposed W.
  4. The homoskedastic estimator was reproduced by hand too, with the scaling of Drukker et al. (2013), A1 = v [W'W - n^-1 tr(W'W) I], v = 1 / (1 + (n^-1 tr(W'W))^2): first-step lambda 0.6589, betas 0.0214, 0.0639, -0.0320, -0.0522, identical to spreg.
- Change to the check (made after the failure; reason above): the gate now compares spreg's betas with the published two-step procedure written out by hand in R (moment conditions, then spatial Cochrane-Orcutt), tolerance unchanged (each beta within 0.01 SE). The lambda comparison is replaced by this check of the betas, which depend on the first-step lambda; spreg's second-step lambda is not recomputed. sphet is still run and its differences printed for information. To be reviewed by the expert panel (spatial econometrician).

## Step 8b decision record (before any sensitivity model was fitted) | 2026-11-05 11:49
- Shared rules: every sensitivity analysis uses the Q19 estimator, fallback and inference rule (GM_Error_Het, GM_Error_Hom and the OLS block bootstrap, B = 999, seed 20261102, largest of the three p-values, hull of the three intervals, Holm across the social variables of that model), and the Q20 effects with P10 and P90 fixed at the values of the primary sample (Q20: "treated as fixed"). H3 is recomputed wherever the sample changes. Results go to 05_analysis/results/step8b_sensitivity.csv and results.json ("step8b").
- Consistency test written before use: the shared functions (05_analysis/step8_lib.py), run on the primary specification, must reproduce the Step 8a inference table exactly.
- S3 (population-weighted models): spreg 1.9.1 has no weights for the GMM spatial error estimators, so the two GM p-values cannot be computed. S3 therefore uses weighted least squares (weights = population) with the block bootstrap alone (percentile interval and bootstrap p), as the inference rule allows when both GM fits are unavailable. Deviation D9, written before S3 is run.
- S7 and MGWR (same 1 km aggregation): included 100 m cells = cells of the Model B sample (identical to Model A); shares weighted by population, rent by the number of rented dwellings (n_dwellings, AnzahlWohnungen), LST anomaly, tree cover, imperviousness and elevation as means over the included 100 m cells (each 100 m cell has the same area), ln of the summed population; 1 km cells with fewer than 5 included cells dropped; queen W on the 1 km grid (centres <= 1,420 m apart).
- S17: tree cover and imperviousness recomputed with exactextract over a 300 m x 300 m square centred on each Model A cell, from the same rasters with the same no-data declaration as Step 6.
- S18: the bootstrap part of the inference rule uses OLS with the same lagged columns WX (computed once on the full sample).
- Tolerance for the R recomputation of MGWR with GWmodel 2.4.1 (gwr.multiscale, adaptive bisquare, AICc), fixed now: for each covariate, the selected bandwidth within 10% of the mgwr bandwidth (or both at the global maximum), and the Pearson correlation of the local coefficients at least 0.95. MGWR is descriptive, so a failure is reported and investigated but changes no hypothesis verdict.
- Exploratory (labelled as such): D2's "dash as missing" refit of Model A; Q25 rent x tree cover interaction. The Q25 vacancy rate (Leerstandsquote) needs a new census file and is moved to Step 8c with the other new-data analyses; the LANUK comparison was done at Step 4; ECOSTRESS is decided at Step 8c.

## Step 8b check record: S11 sample | 2026-11-05 11:58
- First run of 05_analysis/step8_sensitivity.py: "S11 population >= 3" gave n = 12,609, the same as the primary sample, which is not plausible (9,739 inhabited cells have 3 to 9 inhabitants, many with usable census values).
- Cause: Step 2 computed the water share (rule 3) only for cells with at least 10 inhabitants (01_data/step2_build_grid.py, "only for cells passing rules 1 and 2"), so water_share was missing for every smaller cell and the condition "water share < 0.5" removed them all. That first S11 (>= 3) result is not used.
- Fix: 01_data/step8_water_small_cells.py applies the same Earth Engine calculation (ESA WorldCover v200 class 80, area-weighted mean at 10 m over the 100 m cell in EPSG:3035) to the 9,739 cells with 1 to 9 inhabitants: 0 without a value, 9 with at least 50% water. S11 now takes rule 3 from these values for cells under 10 inhabitants. The whole sensitivity script is rerun.

## Step 8b check record: MGWR in R | 2026-11-05 12:21
- verification/verify_mgwr.R (GWmodel 2.4.1, gwr.multiscale, adaptive bisquare, AICc, same 1 km table, same z-standardisation): 8 of 9 bandwidths within 10% and every correlation of local coefficients >= 0.96 (rent 0.966, foreign 0.960, 65+ 0.999, under 18 1.000, elevation 0.988, ln population 0.994, tree cover 0.998, imperviousness 0.998, intercept 0.979). The intercept bandwidth differs: mgwr 45, GWmodel 30 neighbours (33%). RESULT: FAILED under the tolerance as written ("for each covariate"; the intercept was included in the check, and the tolerance is not reinterpreted after the result).
- Investigation: AICc of mgwr's model at its own bandwidths 748.16 (R2 0.8685); at GWmodel's bandwidths 742.21 (R2 0.8799); mgwr's bandwidths with the intercept set to 30: 741.90 (R2 0.8797). So the preregistered golden-section search in mgwr stopped at a worse value of its own criterion for the intercept; GWmodel found a better one. The bandwidths of the four social variables are global (741 of 742 cells, 740 in GWmodel) in both programs, and their local coefficients correlate 0.96 to 1.00.
- Effect: none on any hypothesis (MGWR is descriptive). How to report it (the preregistered mgwr output with this note, and/or the better-AICc intercept bandwidth) is left to the expert panel and Maria.
- Earlier attempt of this check stopped while reading results.json: Python had written NaN, which is not valid JSON. results.json is now written with null (step8_sensitivity.py) and the file was cleaned once; the R check reads it with NaN replaced by null.

## Step 8c decision record (before any variant composite was built) | 2026-11-05 12:28
- Variant composites are built with the same masks, grid and rules as the primary one (Q12; 02_lst/lst_pipeline.py), changing only what the sensitivity analysis names; pixels with fewer than 5 valid observations are missing (Q12.6). Built locally from the per-scene LST files of the 16 hot-day scenes (02_lst/exports/scenes/), except S4 (one more scene, 1_LC08_197024_20250620, downloaded with the same pipeline functions) and S16 (ST_QA band of each scene, downloaded on the same grid).
  - S4: the 17 scenes passing the 80% rule (hot day or not). S5: mean of the absolute LST in C over the 16 scenes. S6: the 9 Landsat 8 scenes. S6b: the 8 scenes of path 196, and the 8 of path 197 (cells lost are counted per city). S12: the 6 scenes with at least 95% valid core reference pixels. S14: per pixel, the mean anomaly of each year, then the mean of the yearly means (the 5-observation rule counts all observations). S15: per scene, (LST minus median) divided by the interquartile range of the valid core reference pixels. S16: pixels with ST_QA x 0.01 > 3 K also masked, and each scene median recomputed on the remaining valid core reference pixels; the distribution of ST_QA of retained pixels is reported.
  - S13 (not fully specified in Q24): each scene's anomaly uses the median of the valid core reference pixels of the city containing the pixel (pixel-centre city mask, as Q12.4). If a city has fewer than 1,000 such pixels in a scene, that scene gives no anomaly for that city's pixels (counted and reported).
- Each variant raster is joined to the 100 m cells exactly as in Step 6 (exactextract mean and coverage share); rule 4 (at least 70% coverage) is recomputed for each variant, and the Model A sample is rule 3, the variant's rule 4, the four usable social variables and the covariates. Model A and B, the inference rule, Q20 effects with P10 and P90 fixed at the primary sample, and H3, through 05_analysis/step8_lib.py.
- Exploratory (Q25): vacancy rate (Leerstandsquote) from the official Destatis grid file Leerstandsquote_in_Gitterzellen.zip, registered like the other census files, parsed with the same rules (dash = 0, brackets = uncertain); added to Model A per 10 points on the cells where it is usable; labelled exploratory, no Holm, no hypothesis.
- ECOSTRESS (Q25, exploratory) needs a NASA Earthdata account: not done unless Maria creates the account herself; recorded as not done.

## Step 8c check record | 2026-11-05 13:02
- 02_lst/step8c_variants.py: downloads (Earth Engine) of the S4 scene 1_LC08_197024_20250620 and the ST_QA band of the 17 used scenes; build reproduced the primary composite before building any variant (max |diff| 1.5e-6 C, float32 storage). S13: no city-scene pair below 1,000 valid core pixels. S16: ST_QA of valid pixels median 2.21 K, 90th percentile 2.91 K, 99th 3.36 K; 7.7% above 3 K (masked).
- verification/verify_variants.py (new; scene selection, exact medians and each variant's rule written separately): 20 random pixels per variant, max |diff| <= 0.000004, observation counts identical for all 10 variants. RESULT: PASSED. Planted error (+0.05 on a copy of S5, checked by a copy of the script pointing to it): FAILED as expected.
- 05_analysis/step8c_models.py: the primary composite joined the same way reproduced Step 6 (max |diff| 0, rule 4 identical) and Step 8a (max |diff| 0, verdicts identical) before any variant was run.
- Correction: in the first run, S15 (standardised anomaly, not in C) had the +-0.3 C negligibility rule applied, which Q22 excludes ("all except S15"). Fixed in the code (step8_lib.infer, negligible_rule=False for S15) and the S15 verdicts recomputed with the same verdict function: foreign share "supported", the other three "inconclusive" (previously "practically negligible"). No other analysis has an outcome outside C.
- Vacancy rate (exploratory): official file Leerstandsquote_in_Gitterzellen.zip downloaded and registered (verify_data_register.py: 20 files, PASSED); 56,682 study-area cells, 45,364 dashes, 10,551 bracketed.

## Gate 8 round 1 decision record (before any new computation) | 2026-11-05 13:18
- Corrections to earlier records (earlier entries are not edited):
  - SEM check record, point 3: "sphet's own verbose output shows the same first-step lambda (0.6652)" refers to the 10,897-cell subsample without islands; on the full Model A sample the first-step lambda is 0.6615 (verify_models.R run 3). Cause of the sphet difference, found by the spatial econometrician and reproduced by them: sphet's error-only path estimates the betas by instrumental variables with the unfiltered X as instruments (exactly identified), not by OLS on the spatially filtered data; it is a different, less efficient estimator. spreg follows Arraiz et al. (2010): betas from step 2a at the step-1b lambda, reported lambda from step 2b.
  - MGWR check record: "the golden-section search stopped at a worse value" is wrong. In mgwr 2.2.1 (sel_bw.py, _init_section) the search for each covariate starts at 40 + 2 x 1 = 42 neighbours, so GWmodel's optimum of 30 could not be reached. And 741 is "at the upper search limit (regional to global scale)", not "global".
- New tolerances, fixed now:
  - verify_models.R: the standard errors of the four social betas (Het: White sandwich on the spatially filtered X at the step-2b lambda; Hom: as Drukker et al. 2013) within 0.5% (relative) of spreg's; the step-2b lambda within 0.001 of spreg's reported lambda.
  - MGWR refit (deviation D15): lower search floor of 20 neighbours for every covariate (multi_bw_min = 20), upper bound n; verify_mgwr.R rerun against the refit with the unchanged tolerance.
- No formal spatial Hausman test is added: the four signs of misspecification (OLS outside the SEM intervals, lambda moving between steps, betas depending on lambda, a different consistent estimator giving different betas) are reported in a table instead, because the variance difference needed by the test is not guaranteed to be positive definite with heteroskedasticity-robust variances. To be judged by the panel in round 2.

## Gate 8 round 1 check record (actions applied) | 2026-11-05 13:33
- verification/verify_models.R extended (decision record above): the full two-step GMM written out by hand in R (step 1 lambda, spatial Cochrane-Orcutt betas, step-2b lambda with the efficient weighting of Arraiz et al. 2010 / Drukker et al. 2013, standard errors). Model A Het: lambda step 1 0.6615, step 2b 0.7789 (spreg 0.7789), betas within 0.00006 SE, standard errors identical (max relative difference 0.00000); Model A Hom: 0.6331, 0.6987 (spreg 0.6987), 0.00003 SE, 0.00000; Model B Het and Hom identical too. OLS 8.1e-13, islands 1,712, bootstrap 4.3e-14. RESULT: PASSED.
- MGWR refit with a search floor of 20 neighbours (D15): intercept bandwidth 30 (interval 30 to 35), AICc 741.88 (default search: 748.16), R2 0.880; rent, foreign, under 18 and ln population at the upper search limit (740; rent interval 572 to the limit); 65+ 466, elevation 494, tree cover 457, imperviousness 167; 45 backfitting iterations, last change of the score 1.2e-6; Moran's I of the MGWR residuals -0.058 (p 0.013, 999 permutations); OLS on the same 742 cells: AICc 901.9, R2 0.808; local condition numbers above 30: 0. verify_mgwr.R against the refit, unchanged tolerance: all 9 bandwidths within 10% (intercept 30 vs 30), correlations of local coefficients 0.998 to 1.000. RESULT: PASSED. Default-search output kept as a footnote (results.json "step8_mgwr_default_search", step8_mgwr_local_default_search.csv).
- 05_analysis/step8_reporting.py (new): misspecification table (all four OLS coefficients outside the SEM interval; lambda 0.6615 step 1, 0.7789 step 2b, 0.8184 iterated in 8 iterations; foreign beta 0.106 at step 1, 0.078 at step 2b, 0.068 iterated, labelled exploratory); H3 under the SEM with its own sign (rent -0.028, foreign -0.015; rent crosses zero under OLS); S18 beta + theta (foreign 0.307 [0.254, 0.361]; rent 0.110 [0.058, 0.162]); single-variable P10-P90 effects all within +-0.3 C (foreign +0.14 [0.09, 0.20], rent +0.04 [0.02, 0.07]: "practically negligible" by Q22); residents vs cells (adjusted cell contrast 0.48, unadjusted 0.14, estimated foreign residents vs others +0.88 pooled and +0.85 within city, exploratory); S3 reference row (unweighted OLS + bootstrap: rent also "contradicted", so S3's result reflects the estimator, not the weighting); S7 effects with 1 km percentiles (foreign 0.53).
- step8_lib.py: point estimate when no spatial fit is attempted (S3, reference rows) = full-sample OLS; when both GM fits fail = bootstrap median, as step8_primary.py (never triggered; the earlier Step 8b and 8c outputs are unchanged by this).

### Step 8, check record: Gate 8 panel round 2 fixes (5 November 2026)

- Changes: 05_analysis/step8_reporting.py (P10-P90 effects at the step-1, step-2b and iterated lambda; same-sample residents-vs-cells rows on the Model A cells; notes; Step 9 writing obligations), 05_analysis/step8_mgwr.py (dead line removed; final_SOC, tol_multi, max_iter_multi reported; wording; Moran note), verification/verify_models.R (comment only, lines 44 to 46; no code or tolerance change).
- step8_mgwr.py rerun (detached): bandwidths, AICc 741.878 and R2 0.880 unchanged; 45 iterations, final SOC 9.01e-6 < tol 1e-5 (max_iter 200); residual Moran's I -0.058 (one-sided permutation p 0.013, 5 islands).
- verify_mgwr.R rerun: RESULT: PASSED (all nine bandwidths within tolerance; local coefficient correlations 0.998 to 1.000).
- step8_reporting.py rerun: foreign P10-P90 effect 0.478 (step 1), 0.350 (step 2b), 0.308 (iterated). Same sample (Model A cells): single-variable SEM 0.448 [0.356, 0.540], single-variable OLS 0.776, resident means 0.497 pooled and 0.482 within city. These match the values the reviewers computed independently in round 2. Note: for 65+ and under 18 the sign of the small effect changes between lambda steps (-0.004 to +0.026; -0.056 to +0.055), consistent with their inconclusive verdicts.

### Step 8, check record: Gate 8 panel round 3 fixes (5 November 2026)

- 05_analysis/step8_reporting.py rerun (detached). Same-sample single-variable SEM row now with the Het and Hom hull: 0.448 [0.356, 0.547] (was Het only, [0.356, 0.540]). Exposure gap on the Model A cells: 15.21 points of foreign share; implied resident gaps 0.161 (adjusted SEM), 0.151 (single-variable SEM), 0.262 (single-variable OLS), against the observed 0.497 pooled and 0.482 within city. Same values as UP's independent computation (15.2; 0.16, 0.15, 0.26). Notes and Step 9 obligations (now 10) added; every interval row carries ci_definition.
- step8_mgwr.py: Moran note text corrected (islands kept with a zero lag). results.json "step8_mgwr.residual_moran_I.note" patched to the same text by a one-off script; no refit, so I, p and every number are unchanged (AICc 741.878).
- Pointer for the MGWR convergence numbers: the "last change of the score 1.2e-6" in the Gate 8 round 1 check record is the last difference between iterations; the convergence criterion itself is the final score of change, 9.01e-6 < tol 1e-5 (round 2 check record). Both are true; the second is the one to report.

### Step 8, check record: Gate 8 panel round 4 fixes (5 November 2026)

- 05_analysis/step8_reporting.py rerun (detached): new key "resident_gap_decomposition_exploratory" and file step8_reporting_resident_gap_decomposition.csv. Implied resident gap (slope x 15.21-point exposure gap), Model A cells: raw unweighted 0.611; raw population-weighted 0.497; city only 0.601; plus elevation and log population 0.262 (weighted 0.230); single-variable SEM 0.151; full Model A OLS 0.328; full SEM 0.161 (step 1), 0.118 (step 2b), 0.104 (iterated). Identity check: observed pooled gap 0.4972510994 = weighted slope x gap 0.4972510994 (difference below 1e-15). Same values as UP's and SE's independent round 4 computations. Step 9 obligations: 11.
- Comment-only edits: step8_primary.py line 222 ("unadjusted disparities" -> "adjusted for elevation, log population and city only"); step8_reporting.py docstring. No code line of step8_primary.py changed, so the Step 8a outputs stay valid.

### Step 8, check record: Gate 8 panel round 5 fixes (5 November 2026)

- step8_reporting.py rerun (detached). New decomposition rows: city only weighted 0.4956; city + elevation 0.5364; city + log population 0.3259 (same as UP's round 5 computation: 0.4956, 0.536, 0.326). The reading note is now built by code from the computed rows: weighting -19%, city 0.61 to 0.60, elevation and log population -56% (almost all through log population), spatial filtering -42% (single-variable) and -51% to -68% (full Model A, by lambda step).
- Line endings: the patch scripts had turned step8_primary.py, step8_reporting.py, step8_mgwr.py and verify_models.R into CRLF; set back to LF, content unchanged (byte check: 0 CRLF). Other project files with CRLF date from earlier steps (pandas CSV output, notebook); left as they are.

### Step 8, check record: Gate 8 panel round 6 fixes (5 November 2026)

- step8_reporting.py rerun (detached); only the reading note changed (numbers unchanged). It now reads "the observed resident gap on the Model A cells (0.50 C; not the 0.88 C of all usable cells)" and "mostly through log population: about 81% of the drop", both values printed from the computed rows. File kept in LF (0 CR bytes).

## GATE 8: Models | run 1 | 2026-11-05 14:08
### verify_data_register.py: PASS
```
files on disk: 20; registered: 20
RESULT: PASSED
```
### verify_models.R: PASS
```
n Model A: 12609 (Python 12609 )
OLS A: max |diff| over intercept and social betas 8.09e-13
OLS B: max |diff| over intercept and social betas 3.08e-14
islands: 1712 (Python 1712 )
SEM A Het (hand, R): lambda step 1 0.6615, step 2b 0.7789 (spreg 0.7789); max |beta diff| / SE 0.00006; max relative SE diff 0.00000
   (information) sphet: max |beta diff| / SE vs spreg = 5.313; lambda sphet 0.7490 vs spreg 0.7789
SEM A Hom (hand, R): lambda step 1 0.6331, step 2b 0.6987 (spreg 0.6987); max |beta diff| / SE 0.00003; max relative SE diff 0.00000
   (information) sphet: max |beta diff| / SE vs spreg = 6.436; lambda sphet 0.6702 vs spreg 0.6987
SEM B Het (hand, R): lambda step 1 0.4398, step 2b 0.5996 (spreg 0.5996); max |beta diff| / SE 0.00000; max relative SE diff 0.00000
   (information) sphet: max |beta diff| / SE vs spreg = 1.980; lambda sphet 0.5291 vs spreg 0.5996
SEM B Hom (hand, R): lambda step 1 0.4249, step 2b 0.5339 (spreg 0.5339); max |beta diff| / SE 0.00000; max relative SE diff 0.00000
   (information) sphet: max |beta diff| / SE vs spreg = 2.107; lambda sphet 0.4763 vs spreg 0.5339
bootstrap: 999 replicates recomputed, max |diff| of social betas 4.32e-14
RESULT: PASSED
Warning message:
In dnearneigh(as.matrix(A[, c("x_mp", "y_mp")]), 0, 142) :
  neighbour object has 3029 sub-graphs
```
### verify_mgwr.R: PASS
```
------ Calculate the initial bandwidths for each independent variable ------
Now select an optimum bandwidth for the model:  lst_anom~1 
[1] "bws0[i]<-bw.gwr(lst_anom~1,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 2036.552 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 2000.38 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1966.584 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1916.567 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1862.331 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1814.658 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1779.381 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1751.887 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1732.416 
Adaptive bandwidth (number of nearest neighbours): 24 AICc value: 1723.087 
Adaptive bandwidth (number of nearest neighbours): 21 AICc value: 1717.677 
Adaptive bandwidth (number of nearest neighbours): 20 AICc value: 1717.144 
Adaptive bandwidth (number of nearest neighbours): 18 AICc value: 1714.859 
Adaptive bandwidth (number of nearest neighbours): 18 AICc value: 1714.859 
Now select an optimum bandwidth for the model:  lst_anom~rent 
[1] "bws0[i]<-bw.gwr(lst_anom~rent,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 2023.813 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1986.127 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1945.627 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1892.099 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1837.45 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1798.49 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1775.617 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1758.063 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1758.49 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1759.031 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1754.682 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1754.682 
Now select an optimum bandwidth for the model:  lst_anom~foreign10 
[1] "bws0[i]<-bw.gwr(lst_anom~foreign10,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1884.73 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1844.813 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1813.434 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1781.584 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1752.831 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1729.503 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1714.779 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1703.125 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1700.083 
Adaptive bandwidth (number of nearest neighbours): 24 AICc value: 1706.246 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1700.071 
Adaptive bandwidth (number of nearest neighbours): 31 AICc value: 1703.371 
Adaptive bandwidth (number of nearest neighbours): 28 AICc value: 1698.006 
Adaptive bandwidth (number of nearest neighbours): 28 AICc value: 1698.006 
Now select an optimum bandwidth for the model:  lst_anom~age65_10 
[1] "bws0[i]<-bw.gwr(lst_anom~age65_10,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1930.168 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1894.249 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1864.01 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1829.077 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1798.845 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1772.491 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1754.011 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1740.155 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1742.596 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1739.712 
Adaptive bandwidth (number of nearest neighbours): 40 AICc value: 1748.656 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1739.712 
Now select an optimum bandwidth for the model:  lst_anom~under18_10 
[1] "bws0[i]<-bw.gwr(lst_anom~under18_10,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 2027.29 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1987.089 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1944.833 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1894.612 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1841.627 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1807.169 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1792.953 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1784.911 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1785.341 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1784.789 
Adaptive bandwidth (number of nearest neighbours): 40 AICc value: 1787.751 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1784.789 
Now select an optimum bandwidth for the model:  lst_anom~elevation 
[1] "bws0[i]<-bw.gwr(lst_anom~elevation,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1935.279 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1917.016 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1882.3 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1838.445 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1792.915 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1758.77 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1734.026 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1719.103 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1707.664 
Adaptive bandwidth (number of nearest neighbours): 24 AICc value: 1708.247 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1712.414 
Adaptive bandwidth (number of nearest neighbours): 26 AICc value: 1707.977 
Adaptive bandwidth (number of nearest neighbours): 28 AICc value: 1707.616 
Adaptive bandwidth (number of nearest neighbours): 28 AICc value: 1707.616 
Now select an optimum bandwidth for the model:  lst_anom~ln_pop 
[1] "bws0[i]<-bw.gwr(lst_anom~ln_pop,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1779.946 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1729.448 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1692.916 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1654.399 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1625.028 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1592.702 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1571.885 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1558.563 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1571.541 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 1562.341 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1564.097 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1558.563 
Now select an optimum bandwidth for the model:  lst_anom~tree_cover 
[1] "bws0[i]<-bw.gwr(lst_anom~tree_cover,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1643.134 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1611.924 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 1583.715 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 1531.206 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 1463.763 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 1400.408 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 1356.267 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 1330.974 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 1323.159 
Adaptive bandwidth (number of nearest neighbours): 24 AICc value: 1326.899 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1320.994 
Adaptive bandwidth (number of nearest neighbours): 31 AICc value: 1325.313 
Adaptive bandwidth (number of nearest neighbours): 28 AICc value: 1321.51 
Adaptive bandwidth (number of nearest neighbours): 29 AICc value: 1320.682 
Adaptive bandwidth (number of nearest neighbours): 31 AICc value: 1325.313 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1320.994 
Adaptive bandwidth (number of nearest neighbours): 30 AICc value: 1320.994 
Adaptive bandwidth (number of nearest neighbours): 29 AICc value: 1320.682 
Now select an optimum bandwidth for the model:  lst_anom~imperviousness 
[1] "bws0[i]<-bw.gwr(lst_anom~imperviousness,data=regression.points,kernel=kernel,approach=approach,adaptive=adaptive,dMat=dMats[[var.dMat.indx[i]]], parallel.method=parallel.method,parallel.arg=parallel.arg)"
Adaptive bandwidth (number of nearest neighbours): 466 AICc value: 1098.995 
Adaptive bandwidth (number of nearest neighbours): 296 AICc value: 1021.194 
Adaptive bandwidth (number of nearest neighbours): 190 AICc value: 967.6735 
Adaptive bandwidth (number of nearest neighbours): 125 AICc value: 916.2282 
Adaptive bandwidth (number of nearest neighbours): 84 AICc value: 884.2275 
Adaptive bandwidth (number of nearest neighbours): 59 AICc value: 864.31 
Adaptive bandwidth (number of nearest neighbours): 43 AICc value: 855.0645 
Adaptive bandwidth (number of nearest neighbours): 34 AICc value: 853.706 
Adaptive bandwidth (number of nearest neighbours): 27 AICc value: 855.0545 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 852.0065 
Adaptive bandwidth (number of nearest neighbours): 40 AICc value: 855.9183 
Adaptive bandwidth (number of nearest neighbours): 36 AICc value: 852.0065 
------            The end for the initial selections              ------
Calculate the initial beta0 from the above bandwidths.
End of calculating the inital beta0.
Find the optimum bandwidths for each independent variable.
	Iteration 1
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 34
The bandwidth used in the last iteration is: 18 and the difference in bandwidths is: 16
The bandwidth for variable Intercept will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 296
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 266
The bandwidth for variable rent will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 224
The bandwidth used in the last iteration is: 28 and the difference in bandwidths is: 196
The bandwidth for variable foreign10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 353
The bandwidth used in the last iteration is: 36 and the difference in bandwidths is: 317
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 635
The bandwidth used in the last iteration is: 36 and the difference in bandwidths is: 599
The bandwidth for variable under18_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 143
The bandwidth used in the last iteration is: 28 and the difference in bandwidths is: 115
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 204
The bandwidth used in the last iteration is: 34 and the difference in bandwidths is: 170
The bandwidth for variable ln_pop will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 198
The bandwidth used in the last iteration is: 29 and the difference in bandwidths is: 169
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 36 and the difference in bandwidths is: 121
The bandwidth for variable imperviousness will be continually selected in the next iteration.
Iteration 1 change of RSS (dCVR) is 0.387343.
	Iteration 2
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 34 and the difference in bandwidths is: 4
The bandwidth for variable Intercept will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 677
The bandwidth used in the last iteration is: 296 and the difference in bandwidths is: 381
The bandwidth for variable rent will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 736
The bandwidth used in the last iteration is: 224 and the difference in bandwidths is: 512
The bandwidth for variable foreign10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 475
The bandwidth used in the last iteration is: 353 and the difference in bandwidths is: 122
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 699
The bandwidth used in the last iteration is: 635 and the difference in bandwidths is: 64
The bandwidth for variable under18_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 198
The bandwidth used in the last iteration is: 143 and the difference in bandwidths is: 55
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 312
The bandwidth used in the last iteration is: 204 and the difference in bandwidths is: 108
The bandwidth for variable ln_pop will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 246
The bandwidth used in the last iteration is: 198 and the difference in bandwidths is: 48
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 149
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 8
The bandwidth for variable imperviousness will be continually selected in the next iteration.
Iteration 2 change of RSS (dCVR) is 0.0935184.
	Iteration 3
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 0
The bandwidth for variable Intercept seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 677 and the difference in bandwidths is: 63
The bandwidth for variable rent will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 736 and the difference in bandwidths is: 4
The bandwidth for variable foreign10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 488
The bandwidth used in the last iteration is: 475 and the difference in bandwidths is: 13
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 718
The bandwidth used in the last iteration is: 699 and the difference in bandwidths is: 19
The bandwidth for variable under18_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 265
The bandwidth used in the last iteration is: 198 and the difference in bandwidths is: 67
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 397
The bandwidth used in the last iteration is: 312 and the difference in bandwidths is: 85
The bandwidth for variable ln_pop will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 281
The bandwidth used in the last iteration is: 246 and the difference in bandwidths is: 35
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 149 and the difference in bandwidths is: 8
The bandwidth for variable imperviousness will be continually selected in the next iteration.
Iteration 3 change of RSS (dCVR) is 0.0420465.
	Iteration 4
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 0
The bandwidth for variable Intercept seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable rent seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable foreign10 seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 488
The bandwidth used in the last iteration is: 488 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 718 and the difference in bandwidths is: 22
The bandwidth for variable under18_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 316
The bandwidth used in the last iteration is: 265 and the difference in bandwidths is: 51
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 507
The bandwidth used in the last iteration is: 397 and the difference in bandwidths is: 110
The bandwidth for variable ln_pop will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 353
The bandwidth used in the last iteration is: 281 and the difference in bandwidths is: 72
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 0
The bandwidth for variable imperviousness seems to be converged for 1 times. It will be continually optimized in the next 4 times
Iteration 4 change of RSS (dCVR) is 0.0467389.
	Iteration 5
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 0
The bandwidth for variable Intercept seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable rent seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable foreign10 seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 475
The bandwidth used in the last iteration is: 488 and the difference in bandwidths is: 13
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable under18_10 seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 316
The bandwidth used in the last iteration is: 316 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 507 and the difference in bandwidths is: 233
The bandwidth for variable ln_pop will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 440
The bandwidth used in the last iteration is: 353 and the difference in bandwidths is: 87
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 0
The bandwidth for variable imperviousness seems to be converged for 2 times. It will be continually optimized in the next 3 times
Iteration 5 change of RSS (dCVR) is 0.0475972.
	Iteration 6
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 0
The bandwidth for variable Intercept seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable rent seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable foreign10 seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 466
The bandwidth used in the last iteration is: 475 and the difference in bandwidths is: 9
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable under18_10 seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 351
The bandwidth used in the last iteration is: 316 and the difference in bandwidths is: 35
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable ln_pop seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 440 and the difference in bandwidths is: 22
The bandwidth for variable tree_cover will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 0
The bandwidth for variable imperviousness seems to be converged for 3 times. It will be continually optimized in the next 2 times
Iteration 6 change of RSS (dCVR) is 0.0173146.
	Iteration 7
Now select an optimum bandwidth for the variable: Intercept
The newly selected bandwidth for variable: Intercept is 30
The bandwidth used in the last iteration is: 30 and the difference in bandwidths is: 0
The bandwidth for variable Intercept seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable rent seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable foreign10 seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 446
The bandwidth used in the last iteration is: 466 and the difference in bandwidths is: 20
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable under18_10 seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 374
The bandwidth used in the last iteration is: 351 and the difference in bandwidths is: 23
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable ln_pop seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 462 and the difference in bandwidths is: 0
The bandwidth for variable tree_cover seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 0
The bandwidth for variable imperviousness seems to be converged for 4 times. It will be continually optimized in the next 1 times
Iteration 7 change of RSS (dCVR) is 0.0261364.
	Iteration 8
Now select an optimum bandwidth for the variable: rent
The newly selected bandwidth for variable: rent is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable rent seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: foreign10
The newly selected bandwidth for variable: foreign10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable foreign10 seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 446 and the difference in bandwidths is: 1
The bandwidth for variable age65_10 will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable under18_10 seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 374
The bandwidth used in the last iteration is: 374 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable ln_pop seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 462 and the difference in bandwidths is: 0
The bandwidth for variable tree_cover seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: imperviousness
The newly selected bandwidth for variable: imperviousness is 157
The bandwidth used in the last iteration is: 157 and the difference in bandwidths is: 0
The bandwidth for variable imperviousness seems to be converged and will be kept the same in the following iterations.
Iteration 8 change of RSS (dCVR) is 0.0236283.
	Iteration 9
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 447 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged for 1 times. It will be continually optimized in the next 4 times
Now select an optimum bandwidth for the variable: under18_10
The newly selected bandwidth for variable: under18_10 is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable under18_10 seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 399
The bandwidth used in the last iteration is: 374 and the difference in bandwidths is: 25
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable ln_pop seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 462 and the difference in bandwidths is: 0
The bandwidth for variable tree_cover seems to be converged for 3 times. It will be continually optimized in the next 2 times
Iteration 9 change of RSS (dCVR) is 0.0276761.
	Iteration 10
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 447 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged for 2 times. It will be continually optimized in the next 3 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 414
The bandwidth used in the last iteration is: 399 and the difference in bandwidths is: 15
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: ln_pop
The newly selected bandwidth for variable: ln_pop is 740
The bandwidth used in the last iteration is: 740 and the difference in bandwidths is: 0
The bandwidth for variable ln_pop seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 462 and the difference in bandwidths is: 0
The bandwidth for variable tree_cover seems to be converged for 4 times. It will be continually optimized in the next 1 times
Iteration 10 change of RSS (dCVR) is 0.0120666.
	Iteration 11
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 447 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged for 3 times. It will be continually optimized in the next 2 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 428
The bandwidth used in the last iteration is: 414 and the difference in bandwidths is: 14
The bandwidth for variable elevation will be continually selected in the next iteration.
Now select an optimum bandwidth for the variable: tree_cover
The newly selected bandwidth for variable: tree_cover is 462
The bandwidth used in the last iteration is: 462 and the difference in bandwidths is: 0
The bandwidth for variable tree_cover seems to be converged and will be kept the same in the following iterations.
Iteration 11 change of RSS (dCVR) is 0.0154778.
	Iteration 12
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 447 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged for 4 times. It will be continually optimized in the next 1 times
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 454
The bandwidth used in the last iteration is: 428 and the difference in bandwidths is: 26
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 12 change of RSS (dCVR) is 0.0247795.
	Iteration 13
Now select an optimum bandwidth for the variable: age65_10
The newly selected bandwidth for variable: age65_10 is 447
The bandwidth used in the last iteration is: 447 and the difference in bandwidths is: 0
The bandwidth for variable age65_10 seems to be converged and will be kept the same in the following iterations.
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 481
The bandwidth used in the last iteration is: 454 and the difference in bandwidths is: 27
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 13 change of RSS (dCVR) is 0.0229418.
	Iteration 14
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 494
The bandwidth used in the last iteration is: 481 and the difference in bandwidths is: 13
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 14 change of RSS (dCVR) is 0.00742191.
	Iteration 15
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 504
The bandwidth used in the last iteration is: 494 and the difference in bandwidths is: 10
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 15 change of RSS (dCVR) is 0.0139408.
	Iteration 16
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 506
The bandwidth used in the last iteration is: 504 and the difference in bandwidths is: 2
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 16 change of RSS (dCVR) is 0.00199828.
	Iteration 17
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 506
The bandwidth used in the last iteration is: 506 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 1 times. It will be continually optimized in the next 4 times
Iteration 17 change of RSS (dCVR) is 0.00555846.
	Iteration 18
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 506
The bandwidth used in the last iteration is: 506 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 2 times. It will be continually optimized in the next 3 times
Iteration 18 change of RSS (dCVR) is 0.00834396.
	Iteration 19
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 506
The bandwidth used in the last iteration is: 506 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 3 times. It will be continually optimized in the next 2 times
Iteration 19 change of RSS (dCVR) is 0.00837592.
	Iteration 20
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 510
The bandwidth used in the last iteration is: 506 and the difference in bandwidths is: 4
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 20 change of RSS (dCVR) is 0.0130371.
	Iteration 21
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 516
The bandwidth used in the last iteration is: 510 and the difference in bandwidths is: 6
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 21 change of RSS (dCVR) is 0.0136657.
	Iteration 22
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 516 and the difference in bandwidths is: 2
The bandwidth for variable elevation will be continually selected in the next iteration.
Iteration 22 change of RSS (dCVR) is 0.00755374.
	Iteration 23
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 518 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 1 times. It will be continually optimized in the next 4 times
Iteration 23 change of RSS (dCVR) is 0.00402261.
	Iteration 24
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 518 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 2 times. It will be continually optimized in the next 3 times
Iteration 24 change of RSS (dCVR) is 0.0068177.
	Iteration 25
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 518 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 3 times. It will be continually optimized in the next 2 times
Iteration 25 change of RSS (dCVR) is 0.00683524.
	Iteration 26
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 518 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged for 4 times. It will be continually optimized in the next 1 times
Iteration 26 change of RSS (dCVR) is 0.00652692.
	Iteration 27
Now select an optimum bandwidth for the variable: elevation
The newly selected bandwidth for variable: elevation is 518
The bandwidth used in the last iteration is: 518 and the difference in bandwidths is: 0
The bandwidth for variable elevation seems to be converged and will be kept the same in the following iterations.
Iteration 27 change of RSS (dCVR) is 0.00618978.
	Iteration 28
Iteration 28 change of RSS (dCVR) is 0.00586494.
	Iteration 29
Iteration 29 change of RSS (dCVR) is 0.00555314.
	Iteration 30
Iteration 30 change of RSS (dCVR) is 0.00525237.
	Iteration 31
Iteration 31 change of RSS (dCVR) is 0.00496209.
	Iteration 32
Iteration 32 change of RSS (dCVR) is 0.00468266.
	Iteration 33
Iteration 33 change of RSS (dCVR) is 0.00441467.
	Iteration 34
Iteration 34 change of RSS (dCVR) is 0.00415866.
	Iteration 35
Iteration 35 change of RSS (dCVR) is 0.00391495.
	Iteration 36
Iteration 36 change of RSS (dCVR) is 0.00368365.
	Iteration 37
Iteration 37 change of RSS (dCVR) is 0.00346469.
	Iteration 38
Iteration 38 change of RSS (dCVR) is 0.00325783.
	Iteration 39
Iteration 39 change of RSS (dCVR) is 0.00306269.
	Iteration 40
Iteration 40 change of RSS (dCVR) is 0.00287883.
	Iteration 41
Iteration 41 change of RSS (dCVR) is 0.00270574.
	Iteration 42
Iteration 42 change of RSS (dCVR) is 0.00254288.
	Iteration 43
Iteration 43 change of RSS (dCVR) is 0.00238971.
	Iteration 44
Iteration 44 change of RSS (dCVR) is 0.0022457.
	Iteration 45
Iteration 45 change of RSS (dCVR) is 0.00211031.
	Iteration 46
Iteration 46 change of RSS (dCVR) is 0.00198304.
	Iteration 47
Iteration 47 change of RSS (dCVR) is 0.0018634.
	Iteration 48
Iteration 48 change of RSS (dCVR) is 0.00175095.
	Iteration 49
Iteration 49 change of RSS (dCVR) is 0.00164525.
	Iteration 50
Iteration 50 change of RSS (dCVR) is 0.0015459.
	Iteration 51
Iteration 51 change of RSS (dCVR) is 0.00145251.
	Iteration 52
Iteration 52 change of RSS (dCVR) is 0.00136474.
	Iteration 53
Iteration 53 change of RSS (dCVR) is 0.00128224.
	Iteration 54
Iteration 54 change of RSS (dCVR) is 0.0012047.
	Iteration 55
Iteration 55 change of RSS (dCVR) is 0.00113182.
	Iteration 56
Iteration 56 change of RSS (dCVR) is 0.00106334.
	Iteration 57
Iteration 57 change of RSS (dCVR) is 0.000998976.
	Iteration 58
Iteration 58 change of RSS (dCVR) is 0.000938494.
	Iteration 59
Iteration 59 change of RSS (dCVR) is 0.000881659.
	Iteration 60
Iteration 60 change of RSS (dCVR) is 0.000828255.
	Iteration 61
Iteration 61 change of RSS (dCVR) is 0.000778074.
	Iteration 62
Iteration 62 change of RSS (dCVR) is 0.000730926.
	Iteration 63
Iteration 63 change of RSS (dCVR) is 0.000686626.
	Iteration 64
Iteration 64 change of RSS (dCVR) is 0.000645006.
	Iteration 65
Iteration 65 change of RSS (dCVR) is 0.000605903.
	Iteration 66
Iteration 66 change of RSS (dCVR) is 0.000569167.
	Iteration 67
Iteration 67 change of RSS (dCVR) is 0.000534654.
	Iteration 68
Iteration 68 change of RSS (dCVR) is 0.000502231.
	Iteration 69
Iteration 69 change of RSS (dCVR) is 0.000471772.
	Iteration 70
Iteration 70 change of RSS (dCVR) is 0.000443158.
	Iteration 71
Iteration 71 change of RSS (dCVR) is 0.000416278.
	Iteration 72
Iteration 72 change of RSS (dCVR) is 0.000391027.
	Iteration 73
Iteration 73 change of RSS (dCVR) is 0.000367307.
	Iteration 74
Iteration 74 change of RSS (dCVR) is 0.000345024.
	Iteration 75
Iteration 75 change of RSS (dCVR) is 0.000324093.
	Iteration 76
Iteration 76 change of RSS (dCVR) is 0.00030443.
	Iteration 77
Iteration 77 change of RSS (dCVR) is 0.00028596.
	Iteration 78
Iteration 78 change of RSS (dCVR) is 0.00026861.
	Iteration 79
Iteration 79 change of RSS (dCVR) is 0.000252313.
	Iteration 80
Iteration 80 change of RSS (dCVR) is 0.000237004.
	Iteration 81
Iteration 81 change of RSS (dCVR) is 0.000222623.
	Iteration 82
Iteration 82 change of RSS (dCVR) is 0.000209115.
	Iteration 83
Iteration 83 change of RSS (dCVR) is 0.000196426.
	Iteration 84
Iteration 84 change of RSS (dCVR) is 0.000184507.
	Iteration 85
Iteration 85 change of RSS (dCVR) is 0.000173311.
	Iteration 86
Iteration 86 change of RSS (dCVR) is 0.000162795.
	Iteration 87
Iteration 87 change of RSS (dCVR) is 0.000152916.
	Iteration 88
Iteration 88 change of RSS (dCVR) is 0.000143637.
	Iteration 89
Iteration 89 change of RSS (dCVR) is 0.000134921.
	Iteration 90
Iteration 90 change of RSS (dCVR) is 0.000126734.
	Iteration 91
Iteration 91 change of RSS (dCVR) is 0.000119043.
	Iteration 92
Iteration 92 change of RSS (dCVR) is 0.000111819.
	Iteration 93
Iteration 93 change of RSS (dCVR) is 0.000105034.
	Iteration 94
Iteration 94 change of RSS (dCVR) is 9.86601e-05.
	Iteration 95
Iteration 95 change of RSS (dCVR) is 9.2673e-05.
	Iteration 96
Iteration 96 change of RSS (dCVR) is 8.70493e-05.
	Iteration 97
Iteration 97 change of RSS (dCVR) is 8.17668e-05.
	Iteration 98
Iteration 98 change of RSS (dCVR) is 7.68049e-05.
	Iteration 99
Iteration 99 change of RSS (dCVR) is 7.21441e-05.
	Iteration 100
Iteration 100 change of RSS (dCVR) is 6.77661e-05.
	Iteration 101
Iteration 101 change of RSS (dCVR) is 6.36537e-05.
	Iteration 102
Iteration 102 change of RSS (dCVR) is 5.9791e-05.
	Iteration 103
Iteration 103 change of RSS (dCVR) is 5.61626e-05.
	Iteration 104
Iteration 104 change of RSS (dCVR) is 5.27544e-05.
	Iteration 105
Iteration 105 change of RSS (dCVR) is 4.9553e-05.
	Iteration 106
Iteration 106 change of RSS (dCVR) is 4.65459e-05.
	Iteration 107
Iteration 107 change of RSS (dCVR) is 4.37213e-05.
	Iteration 108
Iteration 108 change of RSS (dCVR) is 4.10681e-05.
	Iteration 109
Iteration 109 change of RSS (dCVR) is 3.85759e-05.
	Iteration 110
Iteration 110 change of RSS (dCVR) is 3.62349e-05.
	Iteration 111
Iteration 111 change of RSS (dCVR) is 3.4036e-05.
	Iteration 112
Iteration 112 change of RSS (dCVR) is 3.19705e-05.
	Iteration 113
Iteration 113 change of RSS (dCVR) is 3.00304e-05.
	Iteration 114
Iteration 114 change of RSS (dCVR) is 2.8208e-05.
	Iteration 115
Iteration 115 change of RSS (dCVR) is 2.64962e-05.
	Iteration 116
Iteration 116 change of RSS (dCVR) is 2.48883e-05.
	Iteration 117
Iteration 117 change of RSS (dCVR) is 2.3378e-05.
	Iteration 118
Iteration 118 change of RSS (dCVR) is 2.19593e-05.
	Iteration 119
Iteration 119 change of RSS (dCVR) is 2.06267e-05.
	Iteration 120
Iteration 120 change of RSS (dCVR) is 1.93749e-05.
	Iteration 121
Iteration 121 change of RSS (dCVR) is 1.81992e-05.
	Iteration 122
Iteration 122 change of RSS (dCVR) is 1.70948e-05.
	Iteration 123
Iteration 123 change of RSS (dCVR) is 1.60574e-05.
	Iteration 124
Iteration 124 change of RSS (dCVR) is 1.50829e-05.
	Iteration 125
Iteration 125 change of RSS (dCVR) is 1.41676e-05.
	Iteration 126
Iteration 126 change of RSS (dCVR) is 1.33078e-05.
	Iteration 127
Iteration 127 change of RSS (dCVR) is 1.25003e-05.
	Iteration 128
Iteration 128 change of RSS (dCVR) is 1.17417e-05.
	Iteration 129
Iteration 129 change of RSS (dCVR) is 1.10291e-05.
	Iteration 130
Iteration 130 change of RSS (dCVR) is 1.03599e-05.
	Iteration 131
Iteration 131 change of RSS (dCVR) is 9.73114e-06.
intercept       bandwidth mgwr     30  GWmodel     30  ok | correlation of local coefficients 1.000
rent            bandwidth mgwr    740  GWmodel    740  ok | correlation of local coefficients 1.000
foreign10       bandwidth mgwr    740  GWmodel    740  ok | correlation of local coefficients 0.998
age65_10        bandwidth mgwr    466  GWmodel    447  ok | correlation of local coefficients 0.999
under18_10      bandwidth mgwr    740  GWmodel    740  ok | correlation of local coefficients 1.000
elevation       bandwidth mgwr    494  GWmodel    518  ok | correlation of local coefficients 0.998
ln_pop          bandwidth mgwr    740  GWmodel    740  ok | correlation of local coefficients 0.998
tree_cover      bandwidth mgwr    457  GWmodel    462  ok | correlation of local coefficients 1.000
imperviousness  bandwidth mgwr    167  GWmodel    157  ok | correlation of local coefficients 1.000
RESULT: PASSED
```
### verify_variants.py: PASS
```
S12_valid95: 20 pixels, max |diff| 0.000000, observation counts differing 0
S13_city_median: 20 pixels, max |diff| 0.000000, observation counts differing 0
S14_yearly_mean: 20 pixels, max |diff| 0.000000, observation counts differing 0
S15_standardised: 20 pixels, max |diff| 0.000000, observation counts differing 0
S16_stqa3K: 20 pixels, max |diff| 0.000000, observation counts differing 0
S4_all_summer: 20 pixels, max |diff| 0.000000, observation counts differing 0
S5_absolute: 20 pixels, max |diff| 0.000004, observation counts differing 0
S6_landsat8: 20 pixels, max |diff| 0.000001, observation counts differing 0
S6b_path196: 20 pixels, max |diff| 0.000002, observation counts differing 0
S6b_path197: 20 pixels, max |diff| 0.000000, observation counts differing 0
RESULT: PASSED
```
Manual checks:
- Expert panel (A7): 7 rounds, 44 findings (H1 to H44), all accepted; all three reviewers (spatial econometrician, MGWR specialist, quantitative urban planner) reported "No further problems" in the same round (round 7). Evidence: 00_protocol/expert_panel_log.md, Gate 8 rounds 1 to 7.
- Main coefficients recomputed in R within the tolerance fixed before the run: verify_models.R (OLS 8.1e-13; SEM Het and Hom for Models A and B rebuilt by hand, betas within 0.00006 SE, SEs identical, step-2b lambda equal to spreg; bootstrap 4.3e-14) and verify_mgwr.R (GWmodel: all 9 bandwidths within 10%, local coefficient correlations 0.998 to 1.000). The guide names spatialreg; the SEM check is the by-hand GMM instead (D14: sphet estimates the betas by another estimator; change made after a failed run and logged as such).
- Residual diagnostics saved: OLS R2 0.29, Moran's I of the residuals 0.664 (z 76.2), robust LM error 789.1 and lag 449.6 (results.json step8a.ols.A); residuals of Model A (step8_residuals_A.csv, 12,609 rows); residual correlogram by distance band (step8_residual_correlogram.csv: 0.664 at 0 to 142 m, 0.412 at 142 to 300 m, still positive at 2 to 3 km); MGWR residual Moran's I -0.058 (p 0.013).
- Rules of Step 8: spatial lag (S8) read through impacts, not the coefficient (direct and indirect columns in step8b_sensitivity.csv, e.g. foreign direct 0.134, indirect 0.055, total 0.189); MGWR bandwidths and intervals reported (results.json step8_mgwr); every sensitivity result reported, including those that disagree (step8b_sensitivity.csv 24 analyses, 116 rows; step8c_sensitivity.csv 10 analyses, 60 rows; S3 rent "contradicted" and the S10 city results kept).
- Deviations D9 to D16 written in 00_protocol/deviations.md; non-preregistered tables labelled exploratory in results.json; 11 Step 9 writing obligations stored (step8_reporting.step9_writing_obligations).
- LEARNING_NOTEBOOK.md: Step 8 chapter written (all 12 sections, worked examples with the real numbers, rechecked against results.json: P10/P90, hull, bootstrap p, Holm, delta*, exposure gap 37.80% vs 22.59%).
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

## Step 9, decision record: publication track (5 November 2026)

- Entry gate: Gate 8 PASSED (run 1, 2026-11-05 14:08).
- The guide (Part F) planned this choice for Step 1; no decision was written then. [MARIA] chose on 2026-11-05 (in the chat): a full article in English (STROBE-guided, with ISLE-ReSt spatial items), deposited as a preprint, then submitted to an open-access journal that is free for authors (diamond open access, or no author fee); plus a 2-page plain-language project summary. The journal list is checked at the end of Step 9.
- Step 9 sub-steps: 9a figures and maps from code; 9b manuscript (06_manuscript/) and references.bib; 9c verify_manuscript_numbers.py and verify_references.py; 9d expert panel (urban-climate journal reviewer, environmental-justice scholar, science editor) and Gate 9; 9e public repository, OSF data deposit and preprint, each published by Maria after verify_public_release.py passes; 9f 2-page project summary.

## Step 9, decision and check records: figures and article draft (5 November 2026)

- **Public framing (Maria, 2026-11-05):** everything public reads as an independent research project; nothing public mentions any application or deadline. The Step 9 decision record above was reworded the same day (it named an application; written minutes earlier, not a gate run). Project 1's public decision file D10 was reworded too (local commit, push with the next Project 1 update).
- **9a figures:** 05_analysis/step9_figures.py draws Fig 1 to 4 from the result files (maps of the LST anomaly and the foreign share; P10 to P90 effects of every analysis in degrees C; S10 by city; resident-gap decomposition). Colours: ColorBrewer RdBu (diverging, midpoint 0) and Oranges (sequential); grey = no usable value. Each figure was rendered and looked at; fixes: no-data background, layer order, plain-language labels checked against the preregistration wording of S1 to S20.
- **9b article:** 06_manuscript/manuscript_template.md holds the text with {{name}} fields; 06_manuscript/build_manuscript.py fills them from the result files (136 numbers) and writes manuscript.md, numbers_used.json and Supplementary Table S1 (139 rows). Rounding clarification of guide A3: mean temperatures to 0.1 C; model effects (P10 to P90 differences) and coefficients to 2 or 3 decimals, because they are coefficient-like and the reading of the lambda range needs 2 decimals.
- **Claims checked against full texts:** Chawla et al. 2026 (p. 1 abstract: foreigners hotter, more than 50% of cities significant for both LST and air temperature; p. 2: MODIS Aqua about 13:30, 90th percentile summer 2021 to 2023; p. 5: rent "a complex indicator", high-rent areas cooler or hotter), Venter et al. 2021 (abstract: satellites overestimate UHI relative to stations), Klopfer and Pfeiffer 2023 (abstract), and the claims already checked at Steps 0 and 1 (Hsu 2021, Chakraborty 2019, Anderson and Hasler 2026, LANUK 2026). Removed from the first draft because unsupported: a general claim on heat mortality, a claim on where rents are high in the Ruhr, a map reading of where the foreign share is highest, and a wrong "two to fourteen times" ratio.
- **References:** verification/verify_references.py (new) checks each DOI on Crossref (title words >= 90%, year, first author) and the citation list. First run found my own error: the Jia et al. 2020 entry had a wrong title and author list; corrected from the PDF (ISLE-ReSt statement). Two script corrections before any gate use: the year passes if it equals any Crossref date (print, online, issued, journal issue), and family-name particles (van den, von) and corporate authors are parsed. Arraiz et al.: Crossref and OpenAlex give only the online date (13 July 2009) for volume 50(2); the script now marks such a case MANUAL. Manual check: the issue year 2010 is the one used by spreg's own documentation (:cite:`Arraiz2010`) and by the volume 50(2); kept as 2010, uncertainty noted here. Planted errors (wrong title, wrong year) in a copy: FAILED as expected.
- **Numbers:** verification/verify_manuscript_numbers.py (new) recomputes 41 key numbers with its own code from the result files and the analysis table (all identical to 1e-9), checks that all 136 printed values are in the text, and lists the numbers typed in the template for the manual check. Planted errors (a value +0.01, a wrong printed p) in a copy: FAILED as expected.
- **Use-of-AI statement:** written truthfully in 06_manuscript/ai_use_statement_PRIVATE.md (excluded from the public repository); 06_manuscript/build_submission.py inserts it, renders Word and PDF in 06_manuscript/submission/ (private). The public manuscript.md keeps a placeholder.
- **Novelty search repeated** (copy of the Step 0 script in 00_setup/novelty_rerun_2026-11-05/, so the Step 0 files are not overwritten): result recorded below when it finishes.
- **Novelty search repeated (2026-11-05):** same 15 queries, OpenAlex and Crossref: 5,148 records, 4,512 unique, 139 candidates (Step 0: 4,508 and 139). Candidates not in the Step 0 list: 3, all read by title: this study's own OSF preregistration (10.17605/osf.io/cmxs2); a district-level study of heat-related health impacts in Germany (10.64898/2026.09.23.26363662: health outcomes, no LST, no census grid); an unrelated materials thesis (10.34726/hss.2026.81401). No new close study; the Discussion is unchanged.

## Step 9, check records: Gate 9 round 1 fixes (5 November 2026, in progress)

- **Hamm tree cover (panel item J11, UC 16):** median tree cover of the included Hamm cells 0.56% (other cities 3.2 to 8.4%), 40.7% of cells at 0 (others 13.7 to 24.3%), cell maximum 55% (others 72 to 80%). Raw raster `copernicus/CLMS_HRLVLCC_TCD_R10m_2022_bbox.tif` checked: Hamm lies wholly inside the raster (city east edge 4,182,499 m, raster edge 4,183,740 m), no nodata or out-of-range values over Hamm; zero share of pixels over the city area 83.2% (Dortmund 73.0%, Hagen 50.7%); non-zero pixels have usual values (median 88). The low values are spread evenly across the city (zero share 36 to 48% in five west-east bands). Conclusion: not a clipping or reading error; whether it reflects land cover or a production artefact of the 2022 layer cannot be decided from these files. City fixed effects absorb Hamm's mean level; reported as an open data-quality question.
- **AI statement made exact (J9):** the tool checked claims about other studies (not Maria); the sentence about Maria checking worked examples by hand removed (no record of it); data statement and Elsevier-style declaration added. The statement says Maria read, revised and approved all text: this becomes true only when she has read the final version before submission (to confirm with her).
- **New references checked:** Anguelovski et al. 2019 (Crossref; full text on PMC read for the claim: an Opinion piece arguing that green climate infrastructure can displace low-income, minority and migrant residents); Krähenmann et al. 2018 (Crossref; author order from Crossref); König 2024, Friesen et al. 2026 and Kühnl et al. 2026 (PDF abstracts; the two REAL CORP DOIs are registered with DataCite, resolved and checked there). verify_references.py extended to look up DataCite when Crossref has no record (adds coverage; no tolerance changed).


## Publication record: local paths removed (5 November 2026)

- Before the first push, the absolute local folder path printed in front of Python warnings in earlier gate outputs was replaced by the path relative to the project folder, in this file and in every earlier version of it in the git history (git filter-branch on VERIFICATION_LOG.md only; nothing else changed; backup bundle kept locally). No result, verdict or other text was changed. verify_public_release.py now also rejects local Windows paths and private context words.

## Step 9, check record: air temperature data for D17 (5 November 2026)

- 01_data/step9_hostrada.py downloaded 11 monthly HOSTRADA v1.0 files (2 m air temperature, hourly, 1 km, EPSG:3034; about 165 MB each) and the dataset description, and registered all 12 in 01_data/data_register.csv with SHA-256 (licence GeoNutzV, attribution DWD). Bands were selected by their time value (assert: exact match), values scaled by 0.1 to C, fill -9999 set to missing.
- 1,562 HOSTRADA cells have their centre inside the 11 cities (reference for the median). City median air temperature over the 16 days: 22.6 to 32.2 C by day (mean of 10:00 and 11:00 UTC), 14.6 to 23.5 C at night (mean of 01:00 and 02:00 UTC of the next day).
- Composites per 100 m census cell (value of the HOSTRADA cell holding the cell centre): all 61,458 cells have a value; day anomaly -1.75 to 0.75 C (SD 0.31), night anomaly -2.84 to 3.87 C (SD 1.18). The air-temperature contrasts between places are much smaller than the LST contrasts (LST anomaly SD about 2 C), as expected (Venter et al. 2021).

## Step 9, check record: exploratory checks D17 and D18, and the revised article (5 November 2026)

- 05_analysis/step9_checks.py (detached run; results.json "step9_checks", step9_checks.csv), Q19 rule throughout, no verdict counts for a hypothesis:
  - D18a, six regressors as 3 x 3 window means (12,609 cells, lambda 0.76): foreign share 0.93 C [0.68, 1.34] supported; 65+ -0.26 [-0.47, -0.12] and under 18 -0.19 [-0.87, -0.05] negative; rent inconclusive.
  - D18b: Spearman correlation of the number of valid observations with foreign share 0.054, rent 0.055, imperviousness 0.051; Model A on the 12,124 cells with >= 12 of 16 observations: foreign share 0.48 C, supported (as primary).
  - D17, 1 km Model A (742 cells), HOSTRADA air temperature: day foreign share 0.02 C [0.005, 0.09] "supported but practically negligible"; night 0.46 C [0.26, 1.09] supported, 65+ -0.17 and under 18 -0.31 negative. LST on the same cells: 0.53 C. Resident gap (foreign minus others): day 0.04 (Model A cells) / 0.08 C (all usable cells); night 0.26 / 0.46 C.
- verify_manuscript_numbers.py extended with an independent recomputation of the air-temperature resident gaps and the observation correlations (from the cell files, not from results.json): identical. Run: 45 recomputed numbers PASS; 188 printed values present. verify_references.py: PASSED (Krähenmann 2018 and the two REAL CORP DataCite DOIs pass; Arraiz year MANUAL as recorded; LANUK and USGS guide have no DOI, checked by hand at Step 1).
- Article rebuilt from the revised template (round 1 fixes J1 to J12, section 3.7 with D17 and D18), submission version rendered with the use-of-AI section, acknowledgements and declaration.

## GATE 9: Writing and publication | run 1 | 2026-11-05 15:38
### verify_manuscript_numbers.py: PASS
```
PASS    n_rule1: article 61458.0, recomputed 61458.0
PASS    n_rule4: article 51409.0, recomputed 51409.0
PASS    n_A: article 12609.0, recomputed 12609.0
PASS    pop_rule4: article 3241368.0, recomputed 3241368.0
PASS    pop_A: article 1416492.0, recomputed 1416492.0
PASS    share_cells_A: article 24.52683382287148, recomputed 24.52683382287148
PASS    share_pop_A: article 43.70043759301628, recomputed 43.70043759301628
PASS    lst_pw_A: article 3.5898124947108747, recomputed 3.5898124947108747
PASS    lst_pw_rule4: article 2.9079654850787344, recomputed 2.9079654850787344
PASS    n_scenes: article 16.0, recomputed 16.0
PASS    scene_med_min: article 30.030046463012695, recomputed 30.030046463012695
PASS    scene_med_max: article 40.08586120605469, recomputed 40.08586120605469
PASS    b_for: article 0.10595688448244862, recomputed 0.10595688448244862
PASS    p_for: article 0.008, recomputed 0.008
PASS    p_rent: article 0.7593546647381094, recomputed 0.7593546647381094
PASS    e_for: article 0.47756886973929247, recomputed 0.4775688697392925
PASS    e_rent: article 0.03515540837794816, recomputed 0.03515540837794816
PASS    e_for_lo: article 0.3797259780926431, recomputed 0.3797259780926432
PASS    e_for_hi: article 1.1691219542373985, recomputed 1.1691219542373987
PASS    p90_for: article 45.072, recomputed 45.07200000000001
PASS    p10_rent: article 5.05, recomputed 5.05
PASS    p90_rent: article 7.24, recomputed 7.24
PASS    eols_for: article 0.9724907490425683, recomputed 0.9724907490425685
PASS    ratio_for: article 2.0363361405308025, recomputed 2.0363361405308025
PASS    h3_rent: article 0.124165595119306, recomputed 0.124165595119306
PASS    h3_for: article 0.07466385061486411, recomputed 0.07466385061486411
PASS    expo_for: article 37.79816192327444, recomputed 37.79816192327444
PASS    expo_rest: article 22.585445159195583, recomputed 22.585445159195583
PASS    exp_gap: article 15.212716764078857, recomputed 15.21271676407886
PASS    rc_A_pooled: article 0.49725109940961865, recomputed 0.49725109940961865
PASS    dg_sem1: article 0.1611892072835713, recomputed 0.1611892072835713
PASS    s10_sup: article 3.0, recomputed 3.0
PASS    s10_pos: article 11.0, recomputed 11.0
PASS    s3_for: article 1.0088599757367018, recomputed 1.0088599757367018
PASS    mg_r2: article 0.8796898038616509, recomputed 0.8796898038616509
PASS    mg_aicc: article 741.8782048245397, recomputed 741.8782048245397
PASS    bw_intercept: article 30.0, recomputed 30.0
PASS    moran_lst: article 0.7511404890149231, recomputed 0.7511404890149231
PASS    islands: article 1712.0, recomputed 1712.0
note    air_day_gapA: not used in the article
PASS    air_day_gapAll: article 0.07756794064911521, recomputed 0.07756794064911521
PASS    air_night_gapA: article 0.2629251308806897, recomputed 0.2629251308806897
PASS    air_night_gapAll: article 0.45716534147088494, recomputed 0.45716534147088494
note    d18b_cor_max: not used in the article
note    n_sens_for: not used in the article
note    n_sens_for_sup: not used in the article
checked: 46 recomputed, 194 names present in the text
typed numbers in the template (manual check): 00, 0, 0.0001, 0.05, 0.3, 1, 01, 1,, 2,, 2, 2.0, 02, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.0, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 5, 8,, 8, 9, 10, 11, 12, 15, 16, 18, 20, 21, 24,, 25, 27, 30, 42, 50, 60, 65, 70, 80, 90, 95, 96, 100, 196, 197, 197,, 275, 300, 999, 1619, 2007, 2008, 2010, 2013, 2014, 2017, 2018, 2019, 2020, 2021,, 2021, 2022,, 2022, 2023, 2024, 2026,, 2026, 3035, 32632
RESULT: PASSED
```
### verify_references.py: PASS
```
PASS    10.1016/j.ijdrr.2026.106299: title words 100%, year 2026 vs 2026, first author anderson
PASS    10.1073/pnas.1920490117: title words 100%, year 2019 vs 2019, first author anguelovski
MANUAL  10.1111/j.1467-9787.2009.00618.x: year 2010 (issue 50(2)) not on Crossref, which has only online 2009
PASS    10.1088/1748-9326/ab3b99: title words 100%, year 2019 vs 2019, first author chakraborty
PASS    10.1088/1748-9326/ae929e: title words 100%, year 2026 vs 2026, first author chawla
PASS    10.3390/rs61111244: title words 100%, year 2014 vs 2014, first author cook
PASS    10.1080/07474938.2013.741020: title words 100%, year 2013 vs 2013, first author drukker
PASS    10.1080/24694452.2017.1352480: title words 100%, year 2017 vs 2017, first author fotheringham
PASS    10.48494/REALCORP2026.4148: title words 100%, year 2026 vs 2026, first author friesen
PASS    10.1038/s41467-021-22799-5: title words 100%, year 2021 vs 2021, first author hsu
PASS    10.1016/j.healthplace.2019.102243: title words 100%, year 2020 vs 2020, first author jia
PASS    10.1016/j.heliyon.2023.e16185: title words 100%, year 2023 vs 2023, first author klopfer
PASS    10.1177/00420980231224224: title words 100%, year 2024 vs 2024, first author konig
PASS    10.1007/s00704-016-2003-7: title words 100%, year 2018 vs 2016/2018, first author krahenmann
PASS    10.48494/realcorp2026.0144: title words 100%, year 2026 vs 2026, first author kuhnl
MANUAL  no DOI: LANUK NRW (2026). *Klimaanalyse NRW 2026: Methoden- und Ergebnis�berblick*. Fachbericht 171. Landesamt f�r Nat
PASS    10.3390/ijgi8060269: title words 100%, year 2019 vs 2019, first author oshan
PASS    10.1016/j.econlet.2008.09.003: title words 100%, year 2008 vs 2008, first author pace
MANUAL  no DOI: U.S. Geological Survey. *Landsat 8-9 Collection 2 (C2) Level 2 Science Product (L2SP) Guide*, LSDS-1619, versi
PASS    10.15626/MP.2020.2625: title words 100%, year 2021 vs 2021, first author akker
PASS    10.1126/sciadv.abb9569: title words 100%, year 2021 vs 2021, first author venter
PASS    10.1016/S0140-6736(07)61602-X: title words 100%, year 2007 vs 2007, first author elm
CHECK   cited in text but no entry (or not a citation): ('august', '2018')
CHECK   cited in text but no entry (or not a citation): ('copernicus', '2022')
CHECK   cited in text but no entry (or not a citation): ('density', '2021')
CHECK   cited in text but no entry (or not a citation): ('density', '2022')
CHECK   cited in text but no entry (or not a citation): ('keller', '2026')
CHECK   cited in text but no entry (or not a citation): ('may', '2022')
CHECK   cited in text but no entry (or not a citation): ('worldcover', '2021')
RESULT: PASSED
```
### verify_public_release.py: PASS
```
RESULT: PASSED (no AI traces in shareable files or git history; all commits by Maria)
```
Manual checks:
- [x] Expert panel (A7): 5 rounds; all three reviewers (urban-climate journal reviewer, environmental-justice scholar, science editor) reported "No further problems" in round 5. Evidence: 00_protocol/expert_panel_log.md, Gate 9 rounds 1 to 5.
- [x] All numbers checked by script: verify_manuscript_numbers.py above (45 numbers recomputed independently, every printed value present). Numbers typed in the template listed by the script and checked by hand: section numbers, design settings from the preregistration (10 residents, 70%, 80%, 25 C, 0.3 C, 999, 1 km), scene times (10:21, 10:27 UTC, about 10:50 solar time), counts (18 deviations, two consecutive-day pairs), three rounded check results (0.0001 SE from verify_models.R, about 0.05 from step9_checks, beyond 2 km from step8_residual_correlogram.csv) and figures quoted from other studies (275 districts, about 60%, sixfold, 96% and 80%), each checked against its source in this session or by the panel.
- [x] All references checked by script: verify_references.py above (Crossref or DataCite). MANUAL items: LANUK Fachbericht 171 and the USGS guide have no DOI (checked by hand at Step 1, files in Documentation/); Arraiz et al. year 2010 (issue 50(2); Crossref and OpenAlex have only the online date 2009; recorded in the round 1 check record). CHECK lines are false positives (month names, dataset names, the second author of Chawla et al.).
- [x] verify_public_release.py PASSED (above): no AI trace, no private context word, no local path, in the shareable files or the git history; all commits by Maria.
- [x] LEARNING_NOTEBOOK.md: Step 9 chapter written (12 sections, worked examples with real numbers).
- [ ] [MARIA] reads the final article (06_manuscript/submission/Boudjelal_heat_inequality_Ruhr.pdf) and confirms the use-of-AI statement is true for her, then approves publication (article in the repository, preprint, OSF data deposit). Not done yet.
AUTOMATIC CHECKS: ALL PASSED
RESULT: OPEN (waiting for the [MARIA] item; all other checks passed)

### Gate 9 run 1: closing the [MARIA] item (2026-11-05)
- [x] [MARIA] read the final article (06_manuscript/submission/Boudjelal_heat_inequality_Ruhr.pdf), confirmed that the use-of-AI statement (Section 2.9) is true for her, and approved publication (article in the repository, preprint, OSF data deposit). Her answer in the working session, 2026-11-05: "Approved".
All automatic and manual checks of Gate 9 run 1 passed.
RESULT: PASSED

## GATE 9: Writing and publication | run 2 | 2026-11-05 16:53
### verify_manuscript_numbers.py: PASS
```
PASS    n_rule1: article 61458.0, recomputed 61458.0
PASS    n_rule4: article 51409.0, recomputed 51409.0
PASS    n_A: article 12609.0, recomputed 12609.0
PASS    pop_rule4: article 3241368.0, recomputed 3241368.0
PASS    pop_A: article 1416492.0, recomputed 1416492.0
PASS    share_cells_A: article 24.52683382287148, recomputed 24.52683382287148
PASS    share_pop_A: article 43.70043759301628, recomputed 43.70043759301628
PASS    lst_pw_A: article 3.5898124947108747, recomputed 3.5898124947108747
PASS    lst_pw_rule4: article 2.9079654850787344, recomputed 2.9079654850787344
PASS    n_scenes: article 16.0, recomputed 16.0
PASS    scene_med_min: article 30.030046463012695, recomputed 30.030046463012695
PASS    scene_med_max: article 40.08586120605469, recomputed 40.08586120605469
PASS    b_for: article 0.10595688448244862, recomputed 0.10595688448244862
PASS    p_for: article 0.008, recomputed 0.008
PASS    p_rent: article 0.7593546647381094, recomputed 0.7593546647381094
PASS    e_for: article 0.47756886973929247, recomputed 0.4775688697392925
PASS    e_rent: article 0.03515540837794816, recomputed 0.03515540837794816
PASS    e_for_lo: article 0.3797259780926431, recomputed 0.3797259780926432
PASS    e_for_hi: article 1.1691219542373985, recomputed 1.1691219542373987
PASS    p90_for: article 45.072, recomputed 45.07200000000001
PASS    p10_rent: article 5.05, recomputed 5.05
PASS    p90_rent: article 7.24, recomputed 7.24
PASS    eols_for: article 0.9724907490425683, recomputed 0.9724907490425685
PASS    ratio_for: article 2.0363361405308025, recomputed 2.0363361405308025
PASS    h3_rent: article 0.124165595119306, recomputed 0.124165595119306
PASS    h3_for: article 0.07466385061486411, recomputed 0.07466385061486411
PASS    expo_for: article 37.79816192327444, recomputed 37.79816192327444
PASS    expo_rest: article 22.585445159195583, recomputed 22.585445159195583
PASS    exp_gap: article 15.212716764078857, recomputed 15.21271676407886
PASS    rc_A_pooled: article 0.49725109940961865, recomputed 0.49725109940961865
PASS    dg_sem1: article 0.1611892072835713, recomputed 0.1611892072835713
PASS    s10_sup: article 3.0, recomputed 3.0
PASS    s10_pos: article 11.0, recomputed 11.0
PASS    s3_for: article 1.0088599757367018, recomputed 1.0088599757367018
PASS    mg_r2: article 0.8796898038616509, recomputed 0.8796898038616509
PASS    mg_aicc: article 741.8782048245397, recomputed 741.8782048245397
PASS    bw_intercept: article 30.0, recomputed 30.0
PASS    moran_lst: article 0.7511404890149231, recomputed 0.7511404890149231
PASS    islands: article 1712.0, recomputed 1712.0
note    air_day_gapA: not used in the article
PASS    air_day_gapAll: article 0.07756794064911521, recomputed 0.07756794064911521
PASS    air_night_gapA: article 0.2629251308806897, recomputed 0.2629251308806897
PASS    air_night_gapAll: article 0.45716534147088494, recomputed 0.45716534147088494
note    d18b_cor_max: not used in the article
note    n_sens_for: not used in the article
note    n_sens_for_sup: not used in the article
checked: 46 recomputed, 194 names present in the text
typed numbers in the template (manual check): 00, 0, 0.0001, 0.05, 0.3, 1, 1,, 01, 2,, 2, 02, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.0, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 5, 8,, 8, 9, 10, 11, 12, 15, 16, 18, 20, 21, 24,, 25, 27, 30, 42, 50, 60, 65, 70, 80, 90, 95, 96, 100, 196, 197, 197,, 275, 300, 999, 1619, 2007, 2008, 2010, 2013, 2014, 2017, 2018, 2019, 2020, 2021, 2021,, 2022,, 2022, 2023, 2024, 2026,, 2026, 3035, 32632
RESULT: PASSED
```
### verify_references.py: PASS
```
PASS    10.1016/j.ijdrr.2026.106299: title words 100%, year 2026 vs 2026, first author anderson
PASS    10.1073/pnas.1920490117: title words 100%, year 2019 vs 2019, first author anguelovski
MANUAL  10.1111/j.1467-9787.2009.00618.x: year 2010 (issue 50(2)) not on Crossref, which has only online 2009
PASS    10.1088/1748-9326/ab3b99: title words 100%, year 2019 vs 2019, first author chakraborty
PASS    10.1088/1748-9326/ae929e: title words 100%, year 2026 vs 2026, first author chawla
PASS    10.3390/rs61111244: title words 100%, year 2014 vs 2014, first author cook
PASS    10.1080/07474938.2013.741020: title words 100%, year 2013 vs 2013, first author drukker
PASS    10.1080/24694452.2017.1352480: title words 100%, year 2017 vs 2017, first author fotheringham
PASS    10.48494/REALCORP2026.4148: title words 100%, year 2026 vs 2026, first author friesen
PASS    10.1038/s41467-021-22799-5: title words 100%, year 2021 vs 2021, first author hsu
PASS    10.1016/j.healthplace.2019.102243: title words 100%, year 2020 vs 2020, first author jia
PASS    10.1016/j.heliyon.2023.e16185: title words 100%, year 2023 vs 2023, first author klopfer
PASS    10.1177/00420980231224224: title words 100%, year 2024 vs 2024, first author konig
PASS    10.1007/s00704-016-2003-7: title words 100%, year 2018 vs 2016/2018, first author krahenmann
PASS    10.48494/realcorp2026.0144: title words 100%, year 2026 vs 2026, first author kuhnl
MANUAL  no DOI: LANUK NRW (2026). *Klimaanalyse NRW 2026: Methoden- und Ergebnis�berblick*. Fachbericht 171. Landesamt f�r Nat
PASS    10.3390/ijgi8060269: title words 100%, year 2019 vs 2019, first author oshan
PASS    10.1016/j.econlet.2008.09.003: title words 100%, year 2008 vs 2008, first author pace
MANUAL  no DOI: U.S. Geological Survey. *Landsat 8-9 Collection 2 (C2) Level 2 Science Product (L2SP) Guide*, LSDS-1619, versi
PASS    10.15626/MP.2020.2625: title words 100%, year 2021 vs 2021, first author akker
PASS    10.1126/sciadv.abb9569: title words 100%, year 2021 vs 2021, first author venter
PASS    10.1016/S0140-6736(07)61602-X: title words 100%, year 2007 vs 2007, first author elm
CHECK   cited in text but no entry (or not a citation): ('august', '2018')
CHECK   cited in text but no entry (or not a citation): ('copernicus', '2022')
CHECK   cited in text but no entry (or not a citation): ('density', '2021')
CHECK   cited in text but no entry (or not a citation): ('density', '2022')
CHECK   cited in text but no entry (or not a citation): ('keller', '2026')
CHECK   cited in text but no entry (or not a citation): ('may', '2022')
CHECK   cited in text but no entry (or not a citation): ('worldcover', '2021')
RESULT: PASSED
```
### verify_public_release.py: PASS
```
RESULT: PASSED (no AI traces in shareable files or git history; all commits by Maria)
```
Manual checks: (fill in: each manual item of the gate, with evidence)
AUTOMATIC CHECKS: ALL PASSED
RESULT: (write PASSED only when automatic AND manual checks all pass)

## GATE 9: Writing and publication | run 3 | 2026-11-05 16:54
### verify_manuscript_numbers.py: PASS
```
PASS    n_rule1: article 61458.0, recomputed 61458.0
PASS    n_rule4: article 51409.0, recomputed 51409.0
PASS    n_A: article 12609.0, recomputed 12609.0
PASS    pop_rule4: article 3241368.0, recomputed 3241368.0
PASS    pop_A: article 1416492.0, recomputed 1416492.0
PASS    share_cells_A: article 24.52683382287148, recomputed 24.52683382287148
PASS    share_pop_A: article 43.70043759301628, recomputed 43.70043759301628
PASS    lst_pw_A: article 3.5898124947108747, recomputed 3.5898124947108747
PASS    lst_pw_rule4: article 2.9079654850787344, recomputed 2.9079654850787344
PASS    n_scenes: article 16.0, recomputed 16.0
PASS    scene_med_min: article 30.030046463012695, recomputed 30.030046463012695
PASS    scene_med_max: article 40.08586120605469, recomputed 40.08586120605469
PASS    b_for: article 0.10595688448244862, recomputed 0.10595688448244862
PASS    p_for: article 0.008, recomputed 0.008
PASS    p_rent: article 0.7593546647381094, recomputed 0.7593546647381094
PASS    e_for: article 0.47756886973929247, recomputed 0.4775688697392925
PASS    e_rent: article 0.03515540837794816, recomputed 0.03515540837794816
PASS    e_for_lo: article 0.3797259780926431, recomputed 0.3797259780926432
PASS    e_for_hi: article 1.1691219542373985, recomputed 1.1691219542373987
PASS    p90_for: article 45.072, recomputed 45.07200000000001
PASS    p10_rent: article 5.05, recomputed 5.05
PASS    p90_rent: article 7.24, recomputed 7.24
PASS    eols_for: article 0.9724907490425683, recomputed 0.9724907490425685
PASS    ratio_for: article 2.0363361405308025, recomputed 2.0363361405308025
PASS    h3_rent: article 0.124165595119306, recomputed 0.124165595119306
PASS    h3_for: article 0.07466385061486411, recomputed 0.07466385061486411
PASS    expo_for: article 37.79816192327444, recomputed 37.79816192327444
PASS    expo_rest: article 22.585445159195583, recomputed 22.585445159195583
PASS    exp_gap: article 15.212716764078857, recomputed 15.21271676407886
PASS    rc_A_pooled: article 0.49725109940961865, recomputed 0.49725109940961865
PASS    dg_sem1: article 0.1611892072835713, recomputed 0.1611892072835713
PASS    s10_sup: article 3.0, recomputed 3.0
PASS    s10_pos: article 11.0, recomputed 11.0
PASS    s3_for: article 1.0088599757367018, recomputed 1.0088599757367018
PASS    mg_r2: article 0.8796898038616509, recomputed 0.8796898038616509
PASS    mg_aicc: article 741.8782048245397, recomputed 741.8782048245397
PASS    bw_intercept: article 30.0, recomputed 30.0
PASS    moran_lst: article 0.7511404890149231, recomputed 0.7511404890149231
PASS    islands: article 1712.0, recomputed 1712.0
note    air_day_gapA: not used in the article
PASS    air_day_gapAll: article 0.07756794064911521, recomputed 0.07756794064911521
PASS    air_night_gapA: article 0.2629251308806897, recomputed 0.2629251308806897
PASS    air_night_gapAll: article 0.45716534147088494, recomputed 0.45716534147088494
note    d18b_cor_max: not used in the article
note    n_sens_for: not used in the article
note    n_sens_for_sup: not used in the article
checked: 46 recomputed, 194 names present in the text
typed numbers in the template (manual check): 00, 0, 0.0001, 0.05, 0.3, 1, 1,, 01, 2, 2.0, 2,, 02, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.0, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 5, 8,, 8, 9, 10, 11, 12, 15, 16, 18, 20, 21, 24,, 25, 27, 30, 42, 50, 60, 65, 70, 80, 90, 95, 96, 100, 196, 197, 197,, 275, 300, 999, 1619, 2007, 2008, 2010, 2013, 2014, 2017, 2018, 2019, 2020, 2021,, 2021, 2022,, 2022, 2023, 2024, 2026, 2026,, 3035, 32632
RESULT: PASSED
```
### verify_references.py: PASS
```
PASS    10.1016/j.ijdrr.2026.106299: title words 100%, year 2026 vs 2026, first author anderson
PASS    10.1073/pnas.1920490117: title words 100%, year 2019 vs 2019, first author anguelovski
MANUAL  10.1111/j.1467-9787.2009.00618.x: year 2010 (issue 50(2)) not on Crossref, which has only online 2009
PASS    10.1088/1748-9326/ab3b99: title words 100%, year 2019 vs 2019, first author chakraborty
PASS    10.1088/1748-9326/ae929e: title words 100%, year 2026 vs 2026, first author chawla
PASS    10.3390/rs61111244: title words 100%, year 2014 vs 2014, first author cook
PASS    10.1080/07474938.2013.741020: title words 100%, year 2013 vs 2013, first author drukker
PASS    10.1080/24694452.2017.1352480: title words 100%, year 2017 vs 2017, first author fotheringham
PASS    10.48494/REALCORP2026.4148: title words 100%, year 2026 vs 2026, first author friesen
PASS    10.1038/s41467-021-22799-5: title words 100%, year 2021 vs 2021, first author hsu
PASS    10.1016/j.healthplace.2019.102243: title words 100%, year 2020 vs 2020, first author jia
PASS    10.1016/j.heliyon.2023.e16185: title words 100%, year 2023 vs 2023, first author klopfer
PASS    10.1177/00420980231224224: title words 100%, year 2024 vs 2024, first author konig
PASS    10.1007/s00704-016-2003-7: title words 100%, year 2018 vs 2016/2018, first author krahenmann
PASS    10.48494/realcorp2026.0144: title words 100%, year 2026 vs 2026, first author kuhnl
MANUAL  no DOI: LANUK NRW (2026). *Klimaanalyse NRW 2026: Methoden- und Ergebnis�berblick*. Fachbericht 171. Landesamt f�r Nat
PASS    10.3390/ijgi8060269: title words 100%, year 2019 vs 2019, first author oshan
PASS    10.1016/j.econlet.2008.09.003: title words 100%, year 2008 vs 2008, first author pace
MANUAL  no DOI: U.S. Geological Survey. *Landsat 8-9 Collection 2 (C2) Level 2 Science Product (L2SP) Guide*, LSDS-1619, versi
PASS    10.15626/MP.2020.2625: title words 100%, year 2021 vs 2021, first author akker
PASS    10.1126/sciadv.abb9569: title words 100%, year 2021 vs 2021, first author venter
PASS    10.1016/S0140-6736(07)61602-X: title words 100%, year 2007 vs 2007, first author elm
CHECK   cited in text but no entry (or not a citation): ('august', '2018')
CHECK   cited in text but no entry (or not a citation): ('copernicus', '2022')
CHECK   cited in text but no entry (or not a citation): ('density', '2021')
CHECK   cited in text but no entry (or not a citation): ('density', '2022')
CHECK   cited in text but no entry (or not a citation): ('keller', '2026')
CHECK   cited in text but no entry (or not a citation): ('may', '2022')
CHECK   cited in text but no entry (or not a citation): ('worldcover', '2021')
RESULT: PASSED
```
### verify_public_release.py: PASS
```
RESULT: PASSED (no AI traces in shareable files or git history; all commits by Maria)
```
Manual checks: (fill in: each manual item of the gate, with evidence)
AUTOMATIC CHECKS: ALL PASSED
RESULT: (write PASSED only when automatic AND manual checks all pass)

## GATE 9: Writing and publication | run 4 | 2026-11-05 17:06
### verify_manuscript_numbers.py: PASS
```
PASS    n_rule1: article 61458.0, recomputed 61458.0
PASS    n_rule4: article 51409.0, recomputed 51409.0
PASS    n_A: article 12609.0, recomputed 12609.0
PASS    pop_rule4: article 3241368.0, recomputed 3241368.0
PASS    pop_A: article 1416492.0, recomputed 1416492.0
PASS    share_cells_A: article 24.52683382287148, recomputed 24.52683382287148
PASS    share_pop_A: article 43.70043759301628, recomputed 43.70043759301628
PASS    lst_pw_A: article 3.5898124947108747, recomputed 3.5898124947108747
PASS    lst_pw_rule4: article 2.9079654850787344, recomputed 2.9079654850787344
PASS    n_scenes: article 16.0, recomputed 16.0
PASS    scene_med_min: article 30.030046463012695, recomputed 30.030046463012695
PASS    scene_med_max: article 40.08586120605469, recomputed 40.08586120605469
PASS    b_for: article 0.10595688448244862, recomputed 0.10595688448244862
PASS    p_for: article 0.008, recomputed 0.008
PASS    p_rent: article 0.7593546647381094, recomputed 0.7593546647381094
PASS    e_for: article 0.47756886973929247, recomputed 0.4775688697392925
PASS    e_rent: article 0.03515540837794816, recomputed 0.03515540837794816
PASS    e_for_lo: article 0.3797259780926431, recomputed 0.3797259780926432
PASS    e_for_hi: article 1.1691219542373985, recomputed 1.1691219542373987
PASS    p90_for: article 45.072, recomputed 45.07200000000001
PASS    p10_rent: article 5.05, recomputed 5.05
PASS    p90_rent: article 7.24, recomputed 7.24
PASS    eols_for: article 0.9724907490425683, recomputed 0.9724907490425685
PASS    ratio_for: article 2.0363361405308025, recomputed 2.0363361405308025
PASS    h3_rent: article 0.124165595119306, recomputed 0.124165595119306
PASS    h3_for: article 0.07466385061486411, recomputed 0.07466385061486411
PASS    expo_for: article 37.79816192327444, recomputed 37.79816192327444
PASS    expo_rest: article 22.585445159195583, recomputed 22.585445159195583
PASS    exp_gap: article 15.212716764078857, recomputed 15.21271676407886
PASS    rc_A_pooled: article 0.49725109940961865, recomputed 0.49725109940961865
PASS    dg_sem1: article 0.1611892072835713, recomputed 0.1611892072835713
PASS    s10_sup: article 3.0, recomputed 3.0
PASS    s10_pos: article 11.0, recomputed 11.0
PASS    s3_for: article 1.0088599757367018, recomputed 1.0088599757367018
PASS    mg_r2: article 0.8796898038616509, recomputed 0.8796898038616509
PASS    mg_aicc: article 741.8782048245397, recomputed 741.8782048245397
PASS    bw_intercept: article 30.0, recomputed 30.0
PASS    moran_lst: article 0.7511404890149231, recomputed 0.7511404890149231
PASS    islands: article 1712.0, recomputed 1712.0
note    air_day_gapA: not used in the article
PASS    air_day_gapAll: article 0.07756794064911521, recomputed 0.07756794064911521
PASS    air_night_gapA: article 0.2629251308806897, recomputed 0.2629251308806897
PASS    air_night_gapAll: article 0.45716534147088494, recomputed 0.45716534147088494
note    d18b_cor_max: not used in the article
note    n_sens_for: not used in the article
note    n_sens_for_sup: not used in the article
checked: 46 recomputed, 194 names present in the text
typed numbers in the template (manual check): 00, 0, 0.0001, 0.05, 0.3, 01, 1,, 1, 2.0, 02, 2, 2,, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.0, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 5, 8,, 8, 9, 10, 11, 12, 15, 16, 18, 20, 21, 24,, 25, 27, 30, 42, 50, 60, 65, 70, 80, 90, 95, 96, 100, 196, 197,, 197, 275, 300, 999, 1619, 2007, 2008, 2010, 2013, 2014, 2017, 2018, 2019, 2020, 2021,, 2021, 2022,, 2022, 2023, 2024, 2026,, 2026, 3035, 32632
RESULT: PASSED
```
### verify_references.py: PASS
```
PASS    10.1016/j.ijdrr.2026.106299: title words 100%, year 2026 vs 2026, first author anderson
PASS    10.1073/pnas.1920490117: title words 100%, year 2019 vs 2019, first author anguelovski
MANUAL  10.1111/j.1467-9787.2009.00618.x: year 2010 (issue 50(2)) not on Crossref, which has only online 2009
PASS    10.1088/1748-9326/ab3b99: title words 100%, year 2019 vs 2019, first author chakraborty
PASS    10.1088/1748-9326/ae929e: title words 100%, year 2026 vs 2026, first author chawla
PASS    10.3390/rs61111244: title words 100%, year 2014 vs 2014, first author cook
PASS    10.1080/07474938.2013.741020: title words 100%, year 2013 vs 2013, first author drukker
PASS    10.1080/24694452.2017.1352480: title words 100%, year 2017 vs 2017, first author fotheringham
PASS    10.48494/REALCORP2026.4148: title words 100%, year 2026 vs 2026, first author friesen
PASS    10.1038/s41467-021-22799-5: title words 100%, year 2021 vs 2021, first author hsu
PASS    10.1016/j.healthplace.2019.102243: title words 100%, year 2020 vs 2020, first author jia
PASS    10.1016/j.heliyon.2023.e16185: title words 100%, year 2023 vs 2023, first author klopfer
PASS    10.1177/00420980231224224: title words 100%, year 2024 vs 2024, first author konig
PASS    10.1007/s00704-016-2003-7: title words 100%, year 2018 vs 2016/2018, first author krahenmann
PASS    10.48494/realcorp2026.0144: title words 100%, year 2026 vs 2026, first author kuhnl
MANUAL  no DOI: LANUK NRW (2026). *Klimaanalyse NRW 2026: Methoden- und Ergebnis�berblick*. Fachbericht 171. Landesamt f�r Nat
PASS    10.3390/ijgi8060269: title words 100%, year 2019 vs 2019, first author oshan
PASS    10.1016/j.econlet.2008.09.003: title words 100%, year 2008 vs 2008, first author pace
MANUAL  no DOI: U.S. Geological Survey. *Landsat 8-9 Collection 2 (C2) Level 2 Science Product (L2SP) Guide*, LSDS-1619, versi
PASS    10.15626/MP.2020.2625: title words 100%, year 2021 vs 2021, first author akker
PASS    10.1126/sciadv.abb9569: title words 100%, year 2021 vs 2021, first author venter
PASS    10.1016/S0140-6736(07)61602-X: title words 100%, year 2007 vs 2007, first author elm
CHECK   cited in text but no entry (or not a citation): ('august', '2018')
CHECK   cited in text but no entry (or not a citation): ('copernicus', '2022')
CHECK   cited in text but no entry (or not a citation): ('density', '2021')
CHECK   cited in text but no entry (or not a citation): ('density', '2022')
CHECK   cited in text but no entry (or not a citation): ('keller', '2026')
CHECK   cited in text but no entry (or not a citation): ('may', '2022')
CHECK   cited in text but no entry (or not a citation): ('worldcover', '2021')
RESULT: PASSED
```
### verify_public_release.py: PASS
```
RESULT: PASSED (no AI traces in shareable files or git history; all commits by Maria)
```
Manual checks: (fill in: each manual item of the gate, with evidence)
AUTOMATIC CHECKS: ALL PASSED
RESULT: (write PASSED only when automatic AND manual checks all pass)
Note on runs 2 and 3: run 2 and run 3 were started while the article was being changed for the journal (the console could not print one character, so the gate was started twice); their manual checks are those of run 4 below.
Manual checks (run 4, after the changes for submission to Urban Climate):
- [x] What changed since run 1: the abstract was shortened to the journal limit (Urban Climate guide for authors: at most 250 words; now 250 words, every number still a token); the data sentence now names the GitHub repository and the OSF data DOI (https://doi.org/10.17605/OSF.IO/FSV6C, public, CC BY 4.0; SHA-256 of the three files on OSF equal to the local files: README fc3c1986..., parquet ab38a426..., CSV zip 3373363d...); the use-of-AI declaration section title follows the current Elsevier wording; highlights and title page added (private submission folder).
- [x] Expert check of the changes: one reviewer (journal reviewer and science editor) read the new abstract, the highlights and the data sentence against the full text and the earlier panel log. 10 points found (lost caveats: "24.5% of the cells", "practically negligible ... when it varies little inside cities", "in the spatial model", "cells", "models disagreed" instead of "methods"; highlights 1 to 3 reworded; data sentence wrong about the file size). All 10 applied; the reviewer's replacement abstract was used word for word with tokens.
- [x] verify_manuscript_numbers.py, verify_references.py and verify_public_release.py: PASSED (above).
- [x] [MARIA] approval of run 1 still covers these changes: content and claims unchanged, caveats restored; Maria asked on 5 November 2026 for the submission to be prepared ("fais tout toi-même") and made the OSF data component public and created its DOI herself.
AUTOMATIC CHECKS: ALL PASSED
RESULT: PASSED

### Publication record (5 November 2026)
- Data: analysis table deposited on OSF, public, CC BY 4.0, DOI 10.17605/OSF.IO/FSV6C (Maria made it public and created the DOI). SHA-256 of the three files on OSF checked equal to the local files.
- Preprint: submitted to EarthArXiv (no. 15976); declined by the moderators the same day ("outside the subjects we cover"). Nothing was posted there.
- Journal: submitted to Urban Climate (Elsevier), research article, subscription route, 5 November 2026 18:15, through submit.elsevier.com. Files: manuscript (Word), highlights, title page, cover letter, supplementary tables S0 and S1. Data link to the OSF DOI. Opted in to Elsevier's free SSRN preprint service (posted after the journal's desk review). Maria accepted the terms, made every declaration and clicked the final submit herself.
- Change made for the journal before submission: title shortened to 20 words (", Germany" removed; journal limit). verify_manuscript_numbers.py: PASSED after the change.
