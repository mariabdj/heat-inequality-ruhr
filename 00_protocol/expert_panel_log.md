# Expert panel log (Gate 1, preregistration)

Rule: guide A7. Three independent reviewers per round; every finding is listed with what was done. A finding judged wrong is not dropped silently: the reason is written here and shown to Maria.

## Round 1 (2 November 2026, on draft 1)

Reviewers: environmental epidemiologist (EPI), remote-sensing scientist (RS), spatial econometrician (SE).

| # | From | Severity | Finding (short) | Action in draft 2 |
|---|---|---|---|---|
| 1 | EPI | BLOCKER | Copernicus DEM is a surface model (buildings, trees): elevation control leaks surface information | Accepted. Elevation from Geobasis NRW bare-earth terrain model (WCS NW DGM, service checked: GetCapabilities answers "WCS NW DGM, Höhenmodell des Landes NRW") |
| 2 | EPI, SE | BLOCKER | Model B added ln(population) too, so the A to B change was not only trees and sealing | Accepted. ln(population) moved into Model A; Model B = A + tree cover + imperviousness |
| 3 | SE | BLOCKER | Ratio R undefined near 0 and wrong with sign flips | Accepted. H3 decided by Δ* = sign(β_A)(β_A − β_B) with bootstrap interval; R descriptive only when β_A CI excludes 0; sign-flip replicates counted |
| 4 | EPI | MAJOR | Estimand not stated | Accepted. "Primary estimand" paragraph added under Q3 |
| 5 | EPI | MAJOR | H3 reads as mediation | Accepted. Stated as descriptive change in estimate, not mediation |
| 6 | RS | MAJOR | Mask missed ST fill, ST valid range, medium cloud confidence, -9999 fills | Accepted (valid range 293 to 61,440 checked in USGS guide Table 6-1, p. 18). The ST_QA > 3 K rule moved to sensitivity S16 instead of primary: no published threshold found, so the primary mask avoids an arbitrary cut |
| 7 | RS, EPI | MAJOR | Scene, reference domain and median not defined; 50% valid rule lets partial scenes bias the median | Accepted. Scene = one product (path/row/date); reference domain defined on the native grid without water; threshold raised to 80% (RS) rather than kept at 50% (EPI), because a higher share protects the median; S12 (95%) and S13 (city-specific median) added |
| 8 | RS | MAJOR | Composite unbalanced across years, paths, satellites | Accepted. Counts per year/month/path/satellite reported; S14 (equal-year weights), S15 (standardised anomaly) |
| 9 | RS | MAJOR | Fallback rule order undefined | Accepted. Rule rewritten: counts first, no LST values, decision logged before any LST is opened |
| 10 | EPI | MAJOR | No category "significant but negligible" | Accepted (Q22) |
| 11 | EPI, SE | MAJOR | Bootstrap pool, strata, block membership, justification | Accepted. 1 km INSPIRE blocks, centre rule, stratified by city, correct justification (W undefined after resampling), 2 km sensitivity (S19) |
| 12 | EPI, RS | MAJOR/MINOR | "Data error" decided after seeing values | Accepted in a stricter form: no value removed by judgement at all (Q15). The RS proposal (inspect true-colour images) was not used because it is still a judgement after seeing data |
| 13 | EPI, RS | MAJOR/MINOR | 100 m thermal footprint blends neighbours; covariates measured only in-cell | Accepted. Vector reprojection to the Landsat grid (no raster resampling); limitation stated; S17 (3 × 3 cell window) |
| 14 | SE | MAJOR | Fallback estimator open-ended | Accepted. Exact calls; fallback only on error or non-convergence, logged |
| 15 | SE | MAJOR | ML standard errors may be too narrow | Accepted. Most conservative of SEM, GM_Error_Het and block bootstrap. The spatial Hausman test suggested by SE was not added: SE was not sure of the reference, and we cite nothing unverified |
| 16 | SE | MAJOR | Islands, W per sample, border crossing | Accepted (Q19 W paragraph) |
| 17 | SE | MAJOR | Lag-model impacts infeasible with 'full'; SDEM missing | Accepted. spat_impacts='simple'; S18 SDEM (slx_lags exists in installed spreg 1.9.1, signature checked) |
| 18 | SE | MAJOR | H3 multiplicity | Accepted. Family 2 with Holm |
| 19 | SE | MAJOR | MGWR specification incomplete | Accepted (kernel, AICc, bandwidth intervals, filter_tvals, condition numbers, minimum 5 cells, no fixed effects; both functions checked to exist in mgwr 2.2.1) |
| 20 | RS | MINOR | Overpass time wrong for path 197 | Accepted |
| 21 | RS | MINOR | L2SP filter not stated | Accepted |
| 22 | RS | MINOR | Emissivity artefacts | Partly: stated as limitation with the USGS quote. The proposed exclusion rule (ST_EMIS vs class median beyond ST_EMSD) was not added: it is not a published method and would add an untested rule |
| 23 | RS | MINOR | Hot-day data element and missing days | Accepted (KL, TXK, missing or unchecked = not hot) |
| 24 | RS | MINOR | Path-specific sensitivity | Accepted (S6b) |
| 25 | EPI | MINOR | Cell-Key noise attenuates coefficients | Accepted (Q14) |
| 26 | EPI | MINOR | Order of inclusion steps | Accepted (Q13 numbered order) |
| 27 | EPI | MINOR | GM_Error_Het as check | Accepted (part of #15) |
| 28 | EPI, SE | MINOR | P10 to P90 wording and computation | Accepted (Q20) |
| 29 | EPI | MINOR | S7 comparison with Chawla only approximate | Accepted |
| 30 | EPI, SE | MINOR | S10 estimator, MGWR fixed effects | Accepted |
| 31 | EPI | MINOR | Person-level title | Accepted (new title) |
| 32 | EPI | MINOR | Prior reading may have shaped H1/H2 | Accepted (Q18) |
| 33 | EPI | MINOR | Time mismatch of layers; ID check | Accepted (Q12, Q5) |
| 34 | SE | MINOR | LM lag dominance | Accepted |
| 35 | SE | MINOR | LISA settings | Accepted (999 permutations, FDR 5%) |
| 36 | SE | MINOR | Same 1 km aggregation for S7 and MGWR | Accepted |
| 37 | SE | MINOR | VIF on continuous predictors only | Accepted |

Self-checks after the fixes: `verify_prereg.py` (see below); all reference metadata re-read from Crossref on 2 November 2026 (authors, journal, volume, pages).

## Round 2 (2 November 2026, on draft 2)

Round-1 fixes: all three reviewers confirmed them as applied (EPI: items 1-37 correct, #3 and #15 left gaps, fixed below; RS: QA bits, ST fill and range, L2SP, overpass times, grid alignment all checked against USGS Table 6-1/6-2 and Earth Engine metadata; SE: ln(population) move, Δ* definition, Holm families, W per sample, MGWR chain run on simulated data).

| # | From | Severity | Finding (short) | Action in draft 3 |
|---|---|---|---|---|
| 38 | SE | BLOCKER | `ML_Error`/`ML_Lag` invert a dense n × n matrix in their variance step: infeasible at tens of thousands of cells (timed on simulated lattices: n = 8,100 took 157 s, growing about n³) | Accepted after checking the spreg 1.9.1 source myself (`spinv(I − λW)` in ml_error.py). Primary = `GM_Error_Het`, fallback `GM_Error_Hom`; S8 = `GM_Lag`; S10 same estimator |
| 39 | EPI, SE | MAJOR | "Widest interval" rule gave no p-value for Holm; bootstrap p not defined | Accepted. Three p-values (GM Het, GM Hom, bootstrap), largest one used for Holm; reported interval = hull of the three; bootstrap p formula written |
| 40 | EPI, SE | MAJOR | "Holm-adjusted interval" undefined for H3; sign(β_A) per replicate unclear | Accepted. sign fixed from full sample; one-sided bootstrap p; Holm on p |
| 41 | SE | MAJOR | Blocks crossing city borders have no stratum | Accepted. Block = 1 km cell ∩ city; same number of blocks drawn per city |
| 42 | EPI, SE | MAJOR | S18 call would lag all columns (default `slx_vars='All'`) | Accepted. Boolean `slx_vars` list (SE tested it runs) |
| 43 | RS | MAJOR | Path 196 misses west Duisburg; scene edges move about 6 km; the reference median changed between scenes | Accepted. Core reference domain (inside every candidate footprint, from footprints and fill bit only); cells observed by one path only reported; S6b losses reported |
| 44 | EPI | MINOR | Islands-dropped sensitivity unnumbered | Accepted (S20) |
| 45 | EPI | MINOR | Δ* > 0 also when the sign overshoots | Accepted ("sign reversal") |
| 46 | EPI | MINOR | "Dominates" and "large gap" undefined | Accepted (p rules; OLS outside SEM CI) |
| 47 | EPI, RS | MINOR | DWD quality rule not operational | Accepted in RS form: column and codes read from the DWD description file and recorded before download (EPI named a column, `QN_4`, that we have not yet read in the DWD file, so it is not named) |
| 48 | EPI | MINOR | Partial scene coverage | Covered by #43 |
| 49 | EPI | MINOR | S2 wording | Accepted |
| 50 | EPI, RS | MINOR | "No LST values" inexact: masks read ST_B10 numbers | Accepted (flags only; no temperature converted, summarised or shown) |
| 51 | EPI | MINOR | ±0.3 °C rule meaningless for S15 | Accepted (rule lists the °C analyses; S15 excluded) |
| 52 | RS | MINOR | Water rule undefined at 30 m | Accepted (exact 10 m overlap, < 50%) |
| 53 | RS | MINOR | Units of the ST valid range | Accepted (DN, about 150.0 to 359.0 K: 293 × 0.00341802 + 149 = 150.0; 61,440 × 0.00341802 + 149 = 359.0) |
| 54 | RS | MINOR | Bit 3 redundant with bits 8-9 | Accepted (note added, no change in behaviour) |
| 55 | SE | MINOR | Which CI for R rule | Accepted (OLS block-bootstrap interval) |
| 56 | SE | MINOR | LISA islands | Accepted |
| 57 | SE | MINOR | Correlogram not tied to a decision | Accepted (1 km stays primary; S19 only alternative) |

Self-check after the fixes: `verify_prereg.py` PASSED; no remaining mention of ML estimators as primary, of "widest" or of "Holm-adjusted interval".

## Round 3 (2 November 2026, on draft 3)

Round-2 fixes confirmed by all three reviewers, with the gaps below. Correction to the round-1 table, item 6: USGS Table 6-1 is on printed page 12 (PDF page 18); the preregistration cites the printed page.

| # | From | Severity | Finding (short) | Action in draft 4 |
|---|---|---|---|---|
| 58 | RS | MAJOR | "Candidate scene" undefined; Earth Engine trap: masked pixels outside a footprint are skipped by a minimum, giving a union instead of an intersection | Accepted. Candidate scenes = all scenes of Q12.1 whatever cloud or hot-day status; exact Earth Engine expression `unmask(0, False)`; same core for every analysis. RS measured from metadata only: core about 95.5% of the 11-city area (Duisburg about 66%, Hamm about 99%, others 100%) |
| 59 | EPI, RS | MAJOR | Fallback count used fill flags only, not the full mask and the 80% rule | Accepted |
| 60 | SE | MAJOR | "λ outside (−1, 1)" can never happen: spreg bounds λ to (−0.99, 0.99) | Accepted after checking spreg utils.py (bounds and `hard_bound`). `hard_bound=True` in primary, fallback and S18 |
| 61 | SE | MAJOR | Inference rule undefined if a GM fit fails; spreg gives no CIs; bootstrap interval type | Accepted (β ± 1.96 SE; percentile; rules when one or both GM fits fail) |
| 62 | SE | MAJOR | S8 'simple' gives no impact SEs and a trivial direct effect | Accepted (`robust='white'`, `spat_impacts='power'` checked as an option in spreg; total-impact interval by simulation) |
| 63 | SE | MAJOR | S10: city dummies constant within a city | Accepted (no dummies in S10) |
| 64 | EPI | MINOR | Intervals on both sides of 0 while all p < .05 | Accepted (inconclusive) |
| 65 | EPI | MINOR | "SEM 95% CI" ambiguous after the hull rule | Accepted (`GM_Error_Het` CI) |
| 66 | EPI | MINOR | Inference of sensitivity analyses unstated; S7 estimator | Accepted (Q24 header; S7 estimator and W) |
| 67 | EPI | MINOR | °C list incomplete | Accepted (all except S15) |
| 68 | EPI, SE | MINOR | Sign reversal verdict ambiguous | Accepted (Q22) |
| 69 | EPI, RS | MINOR | S12 still referred to the old domain | Accepted |
| 70 | EPI | MINOR | Q8 mentions the unused DEM | Accepted; Q8 also discloses the reviewer's footprint-only coverage figure |
| 71 | EPI, SE | MINOR | S19/S20 order | Accepted |
| 72 | SE | MINOR | X must not contain a constant | Accepted |

Self-check: `verify_prereg.py` PASSED.

## Round 4 (2 November 2026, on draft 4)

Round-3 fixes confirmed by all three (EPI: #58 to #72 consistent; RS: core expression tested on QA_PIXEL and footprints only, 115 candidate scenes on one aligned EPSG:32632 grid; SE: all calls run on a simulated lattice with islands, n = 10,778).

| # | From | Severity | Finding (short) | Action in draft 5 |
|---|---|---|---|---|
| 73 | EPI | MAJOR | Q22 did not carry the Q19 rule that all intervals must lie on one side of 0 | Accepted (Q22 rewritten with the interval condition) |
| 74 | SE, EPI | MAJOR/MINOR | S7: 1 km cells crossing city borders had no city; 1 km blocks = single units, not spatial | Accepted (city with most included 100 m cells, ties by population; 2 km blocks) |
| 75 | EPI | MINOR | Rule when Het succeeds but Hom fails | Accepted (Hom always fitted; any single failure rule) |
| 76 | EPI | MINOR | Total impact formula exact only with full row sums | Accepted (stated; S20 exact case) |
| 77 | SE | MINOR | S8: rho not bounded, no inference rule | Accepted (hard_bound=True, checked to exist in GM_Lag; draws with abs(rho) >= 1 discarded and counted; interval-only judgement) |
| 78 | RS | MINOR | Collection minimum has no native projection | Accepted (crs EPSG:32632 and crsTransform of QA_PIXEL fixed) |
| 79 | RS | MINOR | Q8 wording: reviewers of rounds 3 and 4 | Accepted |

Self-check: verify_prereg.py PASSED.

## Round 5 (2 November 2026, on draft 5)

RS: "No further problems". EPI and SE: round-4 fixes #73 to #79 confirmed (SE ran GM_Lag with hard_bound on simulated data; total multiplier 1.895 = 1/(1 - 0.472)).

| # | From | Severity | Finding (short) | Action in draft 6 |
|---|---|---|---|---|
| 80 | EPI | MINOR | Q22 negligibility sentence missed the case 'p < .05 but intervals on both sides of 0' | Accepted |
| 81 | EPI | MINOR | Negligibility rule could not apply to Delta* (H3) | Accepted (applies to P10 to P90 effects only) |
| 82 | SE | MINOR | S7: a 1 km cell could belong to one city by majority and to another by centre | Accepted (blocks split by assigned city) |

Self-check: verify_prereg.py PASSED.

## Round 6 (2 November 2026, on draft 6)

EPI: "No further problems". RS: "No further problems". SE: "No further problems" (fixes #80 to #82 checked; Holm families, H3 rules, Q24 header and the S8, S10, S18 calls consistent).

**Panel result: all three reviewers report no remaining problem in the same round (rule A7).** 82 findings over 6 rounds; every one accepted, accepted in a modified form, or not used with a written reason (#6 ST_QA cut, #12 image inspection, #15 Hausman test, #22 emissivity rule, #47 column name).

# Gate 7 panel (Steps 2 to 7: grid, census, LST, covariates, join, descriptive results)

## Gate 7, round 1 (2 November 2026)

Reviewers: remote-sensing scientist (RS), spatial statistician (SS), environmental-justice geographer (EJ). Each worked read-only on the project files and reproduced numbers with their own scratch code.

| # | From | Severity | Finding (short) | Action |
|---|---|---|---|---|
| G1 | SS, EJ | BLOCKER | Decile ties broken by cell ID (south to north): cells with the same value (above all 0) fell in different deciles, so part of the curve was geography; `top_minus_bottom_C` compared zero cells with the top decile; R check copied the same rule | Accepted. Separate zero group + city deciles of non-zero values with ties sharing a class (rank "min"); cells, population, median population per group; `top_minus_bottom_C` removed; R check rewritten with the new rule and a test that no value is split; D4 |
| G2 | RS | MAJOR | City mask built with "any pixel touched", not the registered pixel-centre rule (Q12.4) | Accepted. Touched pixels with centre outside removed; EE mask = local mask (0 differences); Steps 4 to 7 rerun (Gate 4 run 2) |
| G3 | RS | MAJOR | LST check reused the pipeline's own masks; no independent check of domain, 80% rule or selection; few invalid pixels tested | Accepted. Checks (d) and (e) added from raw bands; (a) includes invalid pixels and compares with the exported scene files |
| G4 | RS | MAJOR | Candidate scene list not recorded (Q12.4), live query | Accepted. 115 ids frozen in `01_data/raw/landsat/candidate_scenes.csv`, registered with SHA-256, read by the pipeline |
| G5 | EJ | MAJOR | Dash = 0 not in the registered text; zeros are 56% of usable foreign values | Accepted. D2; exploratory sensitivity "dash as missing" planned for Step 8; limitation |
| G6 | EJ | MAJOR | Estimand says "non-bracketed rent value" but rule 5 needs all four variables; size of selection not disclosed; S2 adds only 1,006 cells | Accepted. D3; `step6_sample_comparison.csv` (Model A vs all rule-4 cells, overall and per city); notebook says S1 is the key check |
| G7 | EJ, SS | MAJOR | Per-city losses (Q14) and extreme-value counts (Q15) missing | Accepted. `step6_exclusions_by_city.csv`, `step6_extreme_values.csv` |
| G8 | SS | MAJOR | Foreign LISA dominated by zero cells | Accepted. Zero share per variable and number of LL cells with value 0 in results.json (foreign: 11,516 of 11,551 LL cells) |
| G9 | SS | MAJOR | Folded one-sided pseudo p-values not stated; esda.fdr returns k·alpha/n | Accepted. Stated in the script header, results.json and caption |
| G10 | RS | MINOR | Core share per city (Q12.4), one-path cells per city (Q12.5), scenes per month (Q12.6) not reported | Accepted. `stage1_core_share_by_city.csv`, `one_path_only` per city (223 cells, 222 in Duisburg), `scenes_balance_hot.csv` |
| G11 | RS | MINOR | Log line on "weighted" 80% sums inaccurate | Accepted. Corrected in Gate 4 run 2 (run 1 not edited) |
| G12 | RS | MINOR | Model A filter used Model B covariates | Accepted. Per-model covariate lists in `step6_join.py` |
| G13 | RS | MINOR | No-data 255 handled by "any pixel > 100 -> cell missing" | Accepted. No-data declared through VRT files; raw files unchanged |
| G14 | RS | MINOR | Cells removed by rule 4 clustered (cloud-distance discs, maybe industry) | Accepted in modified form: described (4 cities, 212 with no composite value, sealing similar to kept cells); the link with industry was not checked (no registered land-use layer) and is not claimed |
| G15 | EJ | MINOR | Notebook: bracketed values remove the low non-zero range, not "the middle"; no-bias claim needs linearity and homogeneity | Accepted. Corrected with numbers (median 9.4%) |
| G16 | EJ | MINOR | Notebook: missing rent "mostly owner-occupied" unverified | Accepted. Reworded (no rented dwelling or secrecy) |
| G17 | EJ | MINOR | Population-weighted deciles are not group exposure; captions must not say "foreign residents are exposed" | Accepted. Exploratory group-weighted mean (share x population) added and labelled; captions say "cells, not people" |
| G18 | EJ | MINOR | p_sim = 0.001 is the floor | Accepted. Reported as p <= .001 |
| G19 | SS, EJ | MINOR | LISA map: legend, outlines, scale bar, plain titles, n/I/islands; holes from missing data; rent HH = advantaged | Accepted |
| G20 | SS | MINOR | Global Moran without seed | Accepted. numpy seed 20261102 set before each call (esda.Moran has no seed argument) |
| G21 | SS | MINOR | Decile figure: n per variable, pooling note | Accepted |
| G22 | SS | MINOR | Global I keeps islands in n | Accepted. I without islands also reported |
| G23 | EJ | MINOR | Sample of the descriptive analyses not registered | Accepted. D5 |

Found while fixing: the new water-share check (d) itself declared 0 as no-data; fixed and tested with a planted error (Gate 4 run 2).

## Gate 7, round 2 (2 November 2026)

All round 1 actions checked by the reviewer who raised them, each with own code: RS rebuilt the pixel-centre mask (0 reference pixels outside), rechecked the water rule in both directions on 10,000 pixels (0 wrong decisions) and rebuilt the whole composite from the 16 scene files (n_obs identical everywhere, max |diff| 4.5e-6 C); SS reproduced every decile group (100% membership match), every LISA count and FDR threshold for the four census variables; EJ reproduced the decile table and the Model A selection numbers.

| # | From | Severity | Finding (short) | Action |
|---|---|---|---|---|
| G24 | EJ, SS | MAJOR | Zero group mostly measures cell size (97% of usable cells under 30 residents have foreign = 0; median 17 to 29 residents vs 86 to 144 in deciles); its city mix differs; figure placed it as the low end | Accepted. Zero point shown apart, labelled "dash (0 or changed to 0), median N inhabitants, not comparable"; median population printed at every point; caption; zero share by city in results.json; notebook warning |
| G25 | SS | MAJOR | With 999 permutations, LISA significance for rent, 65+, under 18 sits at the p floor and changes with the seed (Jaccard 0.76 to 0.88) | Accepted. 999 kept (registered); caption and results.json say so; exploratory rerun with 9,999 permutations, counts and Jaccard reported (D7) |
| G26 | EJ | MINOR | Per-decile group-weighted column adds nothing; "Hsu style" wording | Accepted. Replaced by overall group vs rest means, exploratory, with caveats; header reworded |
| G27 | EJ, SS | MINOR | 55.7% should be 55.8% (19,490 / 34,940) | Accepted |
| G28 | EJ | MINOR | D3 wording on the sample number misleading | Accepted. Reworded (12,609 unchanged by the rerun) |
| G29 | EJ | MINOR | Extreme-value rule not stated; counted bracketed values | Accepted. D6; usable values only |
| G30 | EJ | MINOR | Notebook Step 1 "owner-occupied areas", Step 5 "> 100 as missing" out of date; Step 6 selection without numbers | Accepted. Reworded; Model A 24.5% of cells, 43.7% of residents, +0.68 C (hotter in every city) |
| G31 | SS, EJ | MINOR | LL cells with value 0 not shown on the map panels | Accepted. In the panel titles |
| G32 | SS | MINOR | Islands drawn as "not significant" | Accepted. Own colour and legend entry |
| G33 | SS | MINOR | verify_step7 (b) did not recompute the LISA | Accepted. Own neighbour list, hand-made BH threshold, own quadrants, exact match required |
| G34 | RS | MINOR | Frozen candidate list not enforced (live query filtered; re-freezes if file missing) | Accepted. Pipeline stops if the file is missing or if the live catalogue's ids, product ids or processing dates differ; freezing only by an explicit "freeze" command that refuses to overwrite. Planted change of a processing date detected |
| G35 | RS | MINOR | One-path count only for cells fully one-path | Accepted. Pixel-level one-path raster; per city: fully, partly (> 0%), over half, and partly in Model A |
| G36 | RS | MINOR | Check (d) one-directional | Accepted. Added: reference-domain membership of the 2,000 sampled city pixels must match the own water rule (outside 0.02 of the threshold) |

## Gate 7, round 3 (2 November 2026)

No BLOCKER or MAJOR finding from any reviewer. All round 2 actions confirmed with own code: RS reproduced the one-path raster exactly and the per-city counts; SS ran verify_step7.py (PASSED) and rechecked every worked example of the Step 7 notebook chapter; EJ reproduced every number of the Step 7 chapter and the Step 6 selection numbers.

| # | From | Severity | Finding (short) | Action |
|---|---|---|---|---|
| G37 | EJ | MINOR | Notebook lines on missing rent still say "owner-occupied areas" (Step 1 and Step 7) | Accepted. "No rented dwelling (only owner-occupied or empty dwellings) or withheld for confidentiality; we cannot tell which" |
| G38 | EJ | MINOR | D6 said no relationship had been seen, untrue for the round 2 correction | Accepted. Corrected |
| G39 | EJ | MINOR | Group-vs-rest comparison has no deviation entry | Accepted. D8 |
| G40 | EJ | MINOR | Caveat should say pooled and not adjusted | Accepted (results.json and notebook) |
| G41 | EJ | MINOR | Median-population label clipped at the top of one panel | Accepted. Margin added |
| G42 | EJ | MINOR | "Nothing yet." at the top of deviations.md stale | Accepted |
| G43 | RS | MINOR | Notebook silent on the frozen candidate list, reverse water check and one-path columns | Accepted. Step 4 and Step 6 chapters extended |
| G44 | SS | MINOR | "not_significant" included the islands, unlike the map | Accepted. Islands counted under their own key |
| G45 | SS | MINOR | Folded pseudo p definition missing the + 1 | Accepted |
| G46 | SS | MINOR | 9,999-permutation numbers not rechecked | Accepted. verify_step7.py (b) now also checks the exploratory count and Jaccard |

## Gate 7, round 4 (3 November 2026)

SS: "No further problems" (islands key, +1 in the folded pseudo p, 9,999-permutation recheck all confirmed; verify_step7.py PASSED). EJ: "No further problems" (G37 to G42 confirmed). RS: G43 confirmed; two MINOR points:

| # | From | Severity | Finding (short) | Action |
|---|---|---|---|---|
| G47 | RS | MINOR | Gate 6 run 4 manual check says Gate 4 run 3 passed "before" Gate 5 run 2, but Gate 4 run 3 (21:00) came after Gate 5 run 2 (20:06) | Accepted. Run 4 is not edited (rule); correction recorded in the Gate 7 entry of VERIFICATION_LOG.md |
| G48 | RS | MINOR | Notebook Step 6: "223 fully and 270 partly" reads as separate groups; duplicate bullet | Accepted. "270 at least partly one-path, including 223 fully one-path"; duplicate removed |

## Gate 7, round 5 (3 November 2026)

RS: "No further problems" (G48 fixed; G47 to be recorded in the Gate 7 entry). SS: "No further problems" (Step 7 outputs unchanged since the round 4 check). EJ: "No further problems".

**Panel result: all three reviewers report no remaining problem in the same round (rule A7).** 48 findings over 5 rounds at Gate 7; all accepted (G14 in a modified form: the link with industry was not claimed).
